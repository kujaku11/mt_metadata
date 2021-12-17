# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 18:52:52 2021

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================

from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("data_section", SCHEMA_FN_PATHS)

# ==============================================================================
# data section
# ==============================================================================
class DataSection(Base):
    """
    DataSection contains the small metadata block that describes which channel
    is which.  A typical block looks like::

        >=MTSECT

            ex=1004.001
            ey=1005.001
            hx=1001.001
            hy=1002.001
            hz=1003.001
            nfreq=14
            sectid=par28ew
            nchan=None
            maxblks=None


    :param fn: full path to .edi file to read in.
    :type fn: string


    ================= ==================================== ======== ===========
    Attributes        Description                          Default  In .edi
    ================= ==================================== ======== ===========
    ex                ex channel id number                 None     yes
    ey                ey channel id number                 None     yes
    hx                hx channel id number                 None     yes
    hy                hy channel id number                 None     yes
    hz                hz channel id number                 None     yes
    nfreq             number of frequencies                None     yes
    sectid            section id, should be the same
                      as the station name -> Header.dataid None     yes
    maxblks           maximum number of data blocks        None     yes
    nchan             number of channels                   None     yes
    _kw_list          list of key words to put in metadata [1]_     no
    ================= ==================================== ======== ===========

    .. [1] Changes these values to change what is written to edi file
    """

    def __init__(self, **kwargs):
        """
        writing the EDI files MTSECT
        :param fn:
        :param edi_lines:
        """

        self.data_type_out = "z"
        self.data_type_in = "z"
        self._line_num = 0
        self.data_list = None

        self.nfreq = 0
        self.sectid = None
        self.nchan = 0
        self.maxblks = 999
        self.ex = None
        self.ey = None
        self.hx = None
        self.hy = None
        self.hz = None
        self.rrhx = None
        self.rrhy = None
        self.channel_ids = []

        super().__init__(attr_dict=attr_dict, **kwargs)

        self._kw_list = [
            "nfreq",
            "sectid",
            "nchan",
            "maxblks",
            "ex",
            "ey",
            "hx",
            "hy",
            "hz",
            "rrhx",
            "rrhy",
        ]

    def __str__(self):
        return "".join(self.write_data())

    def __repr__(self):
        return self.__str__()

    def get_data(self, edi_lines):
        """
        read in the data of the file, will detect if reading spectra or
        impedance.
        """

        self.data_list = []
        data_find = False

        for ii, line in enumerate(edi_lines):
            if ">=" in line and "sect" in line.lower():
                data_find = True
                self._line_num = ii
                if "spect" in line.lower():
                    self.data_type_in = "spectra"
                elif "mt" in line.lower():
                    self.data_type_in = "z"
            elif ">" in line and data_find is True:
                self._line_num = ii
                break

            elif data_find:
                if len(line.strip()) > 2:
                    self.data_list.append(line.strip())

    def read_data(self, edi_lines):
        """
        read data section
        """

        self.get_data(edi_lines)

        channels = False
        self.channel_ids = []
        for d_line in self.data_list:
            d_list = d_line.split("=")
            if len(d_list) > 1:
                key = d_list[0].lower()
                value = d_list[1].strip().replace('"', "")
                if key not in ["sectid"]:
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                setattr(self, key, value)
            else:
                if "//" in d_line:
                    channels = True
                    continue
                if channels:
                    if len(d_line) > 10:
                        self.channel_ids += d_line.strip().split()
                    else:
                        self.channel_ids.append(d_line)
        if self.channel_ids == []:
            for comp in self._kw_list[4:]:
                ch_id = getattr(self, comp)
                if ch_id is not None:
                    self.channel_ids.append(ch_id)

    def write_data(self, data_list=None, over_dict=None):
        """
        write a data section
        """

        # FZ: need to modify the nfreq (number of freqs),
        # when re-writing effective EDI files)
        if over_dict is not None:
            for akey in list(over_dict.keys()):
                self.__setattr__(akey, over_dict[akey])

        if data_list is not None:
            self.read_data(data_list)

        self.logger.debug("Writing out data a impedances")

        if self.data_type_out == "z":
            data_lines = ["\n>=mtsect\n".upper()]
        elif self.data_type_out == "spectra":
            data_lines = ["\n>spectrasect\n".upper()]

        for key in self._kw_list[0:4]:
            data_lines.append(f"{' '*4}{key.upper()}={getattr(self, key)}\n")

        # need to sort the list so it is descending order by channel number
        ch_list = [
            (key.upper(), getattr(self, key))
            for key in self._kw_list[4:-2]
            if getattr(self, key) is not None
        ]
        rr_ch_list = [
            (key.upper(), getattr(self, key))
            for key in self._kw_list[-2:]
            if getattr(self, key) is not None
        ]
        ch_list2 = sorted(ch_list, key=lambda x: x[1]) + sorted(
            rr_ch_list, key=lambda x: x[1]
        )

        for ch in ch_list2:
            data_lines.append(f"{' '*4}{ch[0]}={ch[1]}\n")

        data_lines.append("\n")

        return data_lines

    def match_channels(self, ch_ids):
        """


        Parameters
        ----------
        ch_ids : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        for ch_id in self.channel_ids:
            for key, value in ch_ids.items():
                if float(ch_id) == value:
                    setattr(self, key.lower(), value)
