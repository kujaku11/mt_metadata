# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 12:09:13 2021

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================

from mt_metadata.base import get_schema
from .standards import SCHEMA_FN_PATHS
from mt_metadata.transfer_functions.tf import Location
from mt_metadata.utils.mttime import MTime, get_now_utc
from mt_metadata.utils.exceptions import MTTimeError
from mt_metadata import __version__

# =============================================================================
attr_dict = get_schema("header", SCHEMA_FN_PATHS)
attr_dict.add_dict(Location()._attr_dict.copy())
# =============================================================================


class Header(Location):
    def __init__(self, **kwargs):
        

        self._acqdate = MTime()
        self._enddate = MTime()
        self._filedate = MTime()
        self._progdate = MTime("2020-11-10")

        self.phoenix_edi = False

        super().__init__()
        super(Location, self).__init__(attr_dict=attr_dict)
        
        self.units = "millivolts_per_kilometer_per_nanotesla"
        self.empty = 1e32
        self.progvers = __version__
        self.progname = "mt_metadata"
        self.datum = "WGS84"

        for k, v in kwargs.items():
            self.set_attr_from_name(k, v)
        

    def __str__(self):
        return "".join(self.write_header())

    def __repr__(self):
        return self.__str__()

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
    def long(self):
        return self.longitude

    @long.setter
    def long(self, value):
        self.longitude = value

    @property
    def elev(self):
        return self.elevation

    @elev.setter
    def elev(self, value):
        self.elevation = value

    @property
    def acqdate(self):
        return self._acqdate.isoformat()

    @acqdate.setter
    def acqdate(self, value):
        try:
            self._acqdate.from_str(value)
        except MTTimeError as error:
            msg = f"Cannot set Header.acqdata with {value}. {error}"
            self.logger.debug(msg)

    @property
    def enddate(self):
        if self._enddate is not None:
            return self._enddate.isoformat()

    @enddate.setter
    def enddate(self, value):
        try:
            self._enddate.from_str(value)
        except MTTimeError as error:
            msg = f"Cannot set Header.enddata with {value}. {error}"
            self.logger.debug(msg)

    @property
    def filedate(self):
        return self._filedate.date

    @filedate.setter
    def filedate(self, value):
        try:
            self._filedate.from_str(value)
        except MTTimeError as error:
            msg = f"Cannot set Header.filedata with {value}. {error}"
            self.logger.debug(msg)

    @property
    def progdate(self):
        return self._progdate.date

    @progdate.setter
    def progdate(self, value):
        try:
            self._progdate.from_str(value)
        except MTTimeError as error:
            msg = f"Cannot set Header.progdata with {value}. {error}"
            self.logger.debug(msg)

    def get_header_list(self, edi_lines):
        """
        Get the header information from the .edi file in the form of a list,
        where each item is a line in the header section.

        :param edi_lines: DESCRIPTION
        :type edi_lines: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        header_list = []
        head_find = False

        # read in list line by line and then truncate
        for line in edi_lines:
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

    def read_header(self, edi_lines):
        """
        read a header information from a list of lines
        containing header information.

        :param edi_lines: DESCRIPTION
        :type edi_lines: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        for h_line in self.get_header_list(edi_lines):
            h_list = h_line.split("=")
            key = h_list[0].lower()
            value = h_list[1]
            # test if its a phoenix formated .edi file
            if key in ["progvers"]:
                if value.lower().find("mt-editor") != -1:
                    self.phoenix_edi = True

            setattr(self, key, value)

    def write_header(
        self,
        longitude_format="LON",
        latlon_format="dms",
        required=True,
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
        
        self.filedate = get_now_utc()
        self.progvers = __version__
        self.progname = "mt_metadata"
        self.progdate = "2021-12-01"
        
        header_lines = [">HEAD\n"]
        for key, value in self.to_dict(single=True, required=required).items():
            if key in ["x", "x2", "y", "y2", "z", "z2"]:
                continue

            if key in ["latitude"]:
                key = "lat"
            elif key in ["longitude"]:
                key = longitude_format.lower()
            elif key in ["elevation"]:
                key = "elev"
            if "declination" in key:
                if self.declination.value == 0.0:
                    continue

            if key in ["lat", "lon", "long"] and value is not None:
                if latlon_format.lower() == "dd":
                    value = f"{value:.6f}"
                else:
                    value = self._convert_position_float2str(value)
            if key in ["elev"] and value is not None:
                value = "{0:.3f}".format(value)
            

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
