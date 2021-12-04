# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 12:09:13 2021

@author: jpeacock
"""

from mt_metadata.transfer_functions.io.edi.metadata import 


# ==============================================================================
#  Header object
# ==============================================================================
class Header(metadata.Location):
    """
    Header class contains all the information in the header section of the .edi
    file. A typical header block looks like::

        >HEAD

            ACQBY=None
            ACQDATE=None
            DATAID=par28ew
            ELEV=0.000
            EMPTY=1e+32
            FILEBY=WG3DForward
            FILEDATE=2016/04/11 19:37:37 UTC
            LAT=-30:12:49
            LOC=None
            LON=139:47:50
            PROGDATE=2002-04-22
            PROGVERS=WINGLINK EDI 1.0.22
            COORDINATE SYSTEM = GEOGRAPHIC NORTH
            DECLINATION = 10.0


    :param fn: full path to .edi file to be read in.
                   *default* is None. If an .edi file is input attributes
                   of Header are filled.
    :type fn: string

    Many of the attributes are needed in the .edi file.  They are marked with
    a yes for 'In .edi'

    ============== ======================================= ======== ===========
    Attributes     Description                             Default  In .edi
    ============== ======================================= ======== ===========
    acqby          Acquired by                             None     yes
    acqdate        Acquired date (YYYY-MM-DD)              None     yes
    coordinate     [ geographic | geomagnetic ]            None     yes
    dataid         Station name, should be a string        None     yes
    declination    geomagnetic declination                 None     yes
    fn         Full path to .edi file                  None     no
    elev           Elevation of station (m)                None     yes
    empty          Value for missing data                  1e32     yes
    fileby         File written by                         None     yes
    filedate       Date the file is written (YYYY-MM-DD)   None     yes
    header_list    List of header lines                    None     no
    lat            Latitude of station [1]_                None     yes
    loc            Location name where station was         None     yes
                   collected
    lon            Longitude of station [1]_               None     yes
    phoenix_edi    [ True | False ] if phoenix .edi format False    no
    progdate       Date of program version to write .edi   None     yes
    progvers       Version of program writing .edi         None     yes
    stdvers        Standard version                        None     yes
    units          Units of distance                       m        yes
    _header_keys   list of metadata input into .edi        [2]_
                   header block.                                    no
    ============== ======================================= ======== ===========

    .. [1] Internally everything is converted to decimal degrees.  Output is
          written as HH:MM:SS.ss so Winglink can read them in.
    .. [2] If you want to change what metadata is written into the .edi file
           change the items in _header_keys.  Default attributes are:
               * acqby
               * acqdate
               * coordinate_system
               * dataid
               * declination
               * elev
               * fileby
               * lat
               * loc
               * lon
               * filedate
               * empty
               * progdate
               * progvers


    ====================== ====================================================
    Methods                Description
    ====================== ====================================================
    get_header_list        get header lines from edi file
    read_header            read in header information from header_lines
    write_header           write header lines, returns a list of lines to write
    ====================== ====================================================

    :Read Header: ::

        >>> import mtpy.core.edi as mtedi
        >>> header_obj = mtedi.Header(fn=r"/home/mt/mt01.edi")

    """

    def __init__(self, fn=None, **kwargs):
        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")
        self._fn = None
        self.fn = fn
        self.edi_lines = None
        self.dataid = None
        self.acqby = None
        self.fileby = "mt_metadata"
        self._acqdate = MTime()
        self._enddate = None
        self._filedate = MTime()
        self.units = "[mV/km]/[nT]"
        self.empty = 1e32
        self.progvers = "0.1.6"
        self._progdate = MTime("2020-11-10")
        self.progname = "mt_metadata"
        self.project = None
        self.survey = None
        self.coordinate_system = "Geographic North"
        self.declination = None
        self.datum = "WGS84"
        self.phoenix_edi = False
        self.stdvers = "SEG 1.0"
        self.state = None
        self.country = None

        self.header_list = None

        self._header_keys = [
            "acqby",
            "acqdate",
            "dataid",
            "elev",
            "fileby",
            "lat",
            "loc",
            "lon",
            "filedate",
            "empty",
            "progname",
            "progdate",
            "progvers",
            "coordinate_system",
            "declination",
            "datum",
            "project",
            "survey",
            "units",
            "stdvers",
        ]

        self._optional_keys = ["enddate", "state", "country"]

        for key in list(kwargs.keys()):
            setattr(self, key, kwargs[key])

        if self.fn is not None or self.edi_lines is not None:
            self.read_header()

    def __str__(self):
        return "".join(self.write_header())

    def __repr__(self):
        return self.__str__()

    @property
    def fn(self):
        return self._fn

    @fn.setter
    def fn(self, value):
        if value is None:
            self._fn = None
            return
        self._fn = Path(value)
        if self._fn.exists():
            self.read_header()

    @property
    def lat(self):
        return self.latitude

    @lat.setter
    def lat(self, value):
        self.latitude = value

    @property
    def lon(self):
        return self.longitude

    @lon.setter
    def lon(self, value):
        self.longitude = value

    @property
    def elev(self):
        return self.elevation

    @elev.setter
    def elev(self, value):
        self.elevation = value

    @property
    def acqdate(self):
        return self._acqdate.date

    @acqdate.setter
    def acqdate(self, value):
        if value in [None, "NONE", "None", "none"]:
            self.logger.debug("Header.acqdate is None, cannot set value")
            return
        try:
            self._acqdate = MTime(value)
        except MTTimeError as error:
            msg = f"Cannot set Header.acqdata with {value}. {error}"
            self.logger.debug(msg)

    @property
    def enddate(self):
        if self._enddate is not None:
            return self._enddate.date

    @enddate.setter
    def enddate(self, value):
        if value in [None, "NONE", "None", "none"]:
            self.logger.debug("Header.enddate is None, cannot set value")
            return
        try:
            self._enddate = MTime(value)
        except MTTimeError as error:
            msg = f"Cannot set Header.enddate with {value}. {error}"
            self.logger.debug(msg)

    @property
    def filedate(self):
        return self._filedate.date

    @filedate.setter
    def filedate(self, value):
        if value in [None, "NONE", "None", "none"]:
            self.logger.debug("Header.filedate is None, cannot set value")
            return
        try:
            self._filedate = MTime(value)
        except MTTimeError as error:
            msg = f"Cannot set Header.filedate with {value}. {error}"
            self.logger.debug(msg)

    @property
    def progdate(self):
        return self._progdate.date

    @progdate.setter
    def progdate(self, value):
        if value in [None, "NONE", "None", "none"]:
            self.logger.debug("Header.progdate is None, cannot set value")
            return
        try:
            self._progdate = MTime(value)
        except MTTimeError as error:
            msg = f"Header.progdate must be a date not {value}. {error}"
            self.logger.debug(msg)

    def get_header_list(self):
        """
        Get the header information from the .edi file in the form of a list,
        where each item is a line in the header section.
        """

        if self.fn is None and self.edi_lines is None:
            self.logger.info("No edi file to read.")
            return

        header_list = []
        head_find = False

        # read in file line by line
        if self.fn is not None:
            if not self.fn.exists():
                msg = f"Could not find {self.fn}"
                self.logger.error(msg)
                raise IOError(msg)
            with open(self.fn, "r") as fid:
                self.edi_lines = _validate_edi_lines(fid.readlines())

        # read in list line by line and then truncate
        for line in self.edi_lines:
            # check for header label
            if ">" in line and "head" in line.lower():
                head_find = True
            # if the header line has been found then the next >
            # should be the next section so stop
            elif ">" in line:
                if head_find is True:
                    break
                else:
                    pass
            # get the header information into a list
            elif head_find:
                # skip any blank lines
                if len(line.strip()) > 2:
                    line = line.strip().replace('"', "")
                    h_list = line.split("=")
                    if len(h_list) == 2:
                        key = h_list[0].strip()
                        value = h_list[1].strip()
                        header_list.append("{0}={1}".format(key, value))

        return header_list

    def read_header(self, header_list=None):
        """
        read a header information from either edi file or a list of lines
        containing header information.

        :param header_list: should be read from an .edi file or input as
                            ['key_01=value_01', 'key_02=value_02']
        :type header_list: list

        :Input header_list: ::

            >>> h_list = ['lat=36.7898', 'lon=120.73532', 'elev=120.0', ...
            >>>           'dataid=mt01']
            >>> import mtpy.core.edi as mtedi
            >>> header = mtedi.Header()
            >>> header.read_header(h_list)

        """

        if header_list is not None:
            self.header_list = self._validate_header_list(header_list)

        if self.header_list is None and self.fn is None and self.edi_lines is None:
            self.logger.info("Nothing to read. header_list and fn are None")

        elif self.fn is not None or self.edi_lines is not None:
            self.header_list = self.get_header_list()

        for h_line in self.header_list:
            h_list = h_line.split("=")
            key = h_list[0].lower()
            value = h_list[1]
            # test if its a phoenix formated .edi file
            if key in ["progvers"]:
                if value.lower().find("mt-editor") != -1:
                    self.phoenix_edi = True
            if key in "latitude":
                key = "lat"
            elif key in "longitude":
                key = "lon"
            elif key in "elevation":
                key = "elev"
            elif key in "location":
                key = "loc"

            setattr(self, key, value)

            # be sure to pass any uncommon keys through to new file
            if key not in self._header_keys:
                self._optional_keys.append(key)

    def write_header(
        self, header_list=None, longitude_format="LON", latlon_format="dms"
    ):
        """
        Write header information to a list of lines.


        :param header_list: should be read from an .edi file or input as
                            ['key_01=value_01', 'key_02=value_02']
        :type header_list: list
        :param longitude_format:  whether to write longitude as LON or LONG.
                                  options are 'LON' or 'LONG', default 'LON'
        :type longitude_format:  string
        :param latlon_format:  format of latitude and longitude in output edi,
                               degrees minutes seconds ('dms') or decimal
                               degrees ('dd')
        :type latlon_format:  string

        :returns header_lines: list of lines containing header information
                               will be of the form::

                               ['>HEAD\n',
                                '    key_01=value_01\n']
                                if None is input then reads from input .edi
                                file or uses attribute information to write
                                metadata.

        """

        if header_list is not None:
            self.read_header(header_list)

        if self.header_list is None and self.fn is not None:
            self.header_list = self.get_header_list()

        header_lines = [">HEAD\n"]
        for key in sorted(self._header_keys + self._optional_keys):
            value = getattr(self, key)
            if key in self._optional_keys and value is None:
                continue
            if key in ["lat", "lon"] and value is not None:
                if latlon_format.upper() == "DD":
                    value = "%.6f" % value
                else:
                    # value = gis_tools.convert_position_float2str(value)
                    value = value
            if key in ["elev", "declination"] and value is not None:
                try:
                    value = "{0:.3f}".format(value)
                except ValueError:
                    # raise Exception("value error for key elev or declination")
                    value = "0.000"

            if key in ["filedate"]:
                value = get_now_utc()
            #
            if key == "lon":
                if longitude_format == "LONG":
                    key = "long"
            if isinstance(value, list):
                value = ",".join(value)

            header_lines.append(f"\t{key.upper()}={value}\n")

        header_lines.append("\n")
        return header_lines

    def _validate_header_list(self, header_list):
        """
        make sure the input header list is valid

        returns a validated header list
        """

        if header_list is None:
            self.logger.info("No header information to read")
            return None

        new_header_list = []
        for h_line in header_list:
            h_line = h_line.strip().replace('"', "")
            if len(h_line) > 1:
                h_list = h_line.split("=")
                if len(h_list) == 2:
                    key = h_list[0].strip().lower()
                    value = h_list[1].strip()
                    new_header_list.append("{0}={1}".format(key, value))

        return new_header_list