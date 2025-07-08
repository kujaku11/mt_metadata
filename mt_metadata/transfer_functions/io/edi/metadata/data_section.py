# =====================================================
# Imports
# =====================================================
from typing import Annotated

from loguru import logger
from pydantic import Field, PrivateAttr

from mt_metadata.base import MetadataBase
from mt_metadata.base.helpers import validate_name


# =====================================================
class DataSection(MetadataBase):
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

    nfreq: Annotated[
        int,
        Field(
            default=0,
            description="Number of frequencies",
            examples=[16, 1],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),  # type: ignore
    ]

    sectid: Annotated[
        str,
        Field(
            default="",
            description="ID of the station that the data is from. This is important if you have more than one station per file.",
            examples=["mt001"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    nchan: Annotated[
        int,
        Field(
            default=0,
            description="Number of channels in the transfer function",
            examples=[7],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    maxblocks: Annotated[
        int,
        Field(
            default=999,
            description="Maximum number of data blocks",
            examples=[999],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    ex: Annotated[
        str | None,
        Field(
            default=None,
            description="Measurement ID for EX",
            examples=["1"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    ey: Annotated[
        str | None,
        Field(
            default=None,
            description="Measurement ID for EY",
            examples=["2"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    hx: Annotated[
        str | None,
        Field(
            default=None,
            description="Measurement ID for HX",
            examples=["3"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    hy: Annotated[
        str | None,
        Field(
            default=None,
            description="Measurement ID for HY",
            examples=["4"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    hz: Annotated[
        str | None,
        Field(
            default=None,
            description="Measurement ID for HZ",
            examples=["5"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    rrhx: Annotated[
        str | None,
        Field(
            default=None,
            description="Measurement ID for RRHX",
            examples=["6"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    rrhy: Annotated[
        str | None,
        Field(
            default=None,
            description="Measurement ID for RRHY",
            examples=["7"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    # List of keywords for the data section, used for writing metadata.
    # This list can be modified to change what is written to the EDI file.
    _kw_list: list[str] = PrivateAttr(
        default_factory=lambda: [
            "nfreq",
            "sectid",
            "nchan",
            "maxblocks",
            "ex",
            "ey",
            "hx",
            "hy",
            "hz",
            "rrhx",
            "rrhy",
        ]
    )

    # Private attributes
    # Line number in the EDI file where the data section starts.
    _line_num: int = PrivateAttr(default=0)

    # Data type for output, typically 'z' for complex impedance data.
    _data_type_out: str = PrivateAttr(default="z")

    # Data type for input, typically 'z' for complex impedance data.
    _data_type_in: str = PrivateAttr(default="z")

    # List of channel IDs associated with the data section.
    _channel_ids: list[str] = PrivateAttr(default_factory=list)

    def __str__(self) -> str:
        return "".join(self.write_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_data(self, edi_lines: list[str]) -> list[str]:
        """
        Read in the data of the file, will detect if reading spectra or
        impedance.
        """
        data_list = []
        data_find = False

        for ii, line in enumerate(edi_lines):
            if ">=" in line and "sect" in line.lower():
                data_find = True
                self._line_num = ii
                if "spect" in line.lower():
                    self._data_type_in = "spectra"
                elif "mt" in line.lower():
                    self._data_type_in = "z"
            elif ">" in line and data_find is True:
                self._line_num = ii
                break

            elif data_find:
                if len(line.strip()) > 2:
                    data_list.append(line.strip())
        return data_list

    def read_data(self, edi_lines: list[str]) -> None:
        """
        Read data section
        """
        data_list = self.get_data(edi_lines)

        channels = False
        self._channel_ids = []
        for d_line in data_list:
            d_list = d_line.split("=")
            if len(d_list) > 1:
                key = d_list[0].lower()
                value = d_list[1].strip().replace('"', "")
                if key not in ["sectid"]:
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                elif key in ["sectid"]:
                    value = validate_name(value)
                setattr(self, key, value)
            else:
                if "//" in d_line:
                    channels = True
                    continue
                if channels:
                    if len(d_line) > 10:
                        self._channel_ids += d_line.strip().split()
                    else:
                        self._channel_ids.append(d_line)
        if self._channel_ids == []:
            for comp in self._kw_list[4:]:
                ch_id = getattr(self, comp)
                if ch_id is not None:
                    self._channel_ids.append(ch_id)

    def write_data(
        self, data_list: list[str] | None = None, over_dict: dict | None = None
    ) -> list[str]:
        """
        Write the data section to a list of strings.
        """
        # FZ: need to modify the nfreq (number of freqs),
        # when re-writing effective EDI files)
        if over_dict is not None:
            for akey in list(over_dict.keys()):
                self.__setattr__(akey, over_dict[akey])

        if data_list is not None:
            self.read_data(data_list)

        logger.debug("Writing out data a impedances")

        if self._data_type_out == "z":
            data_lines = ["\n>=mtsect\n".upper()]
        elif self._data_type_out == "spectra":
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
            if ch[1] not in [0, "0"]:
                data_lines.append(f"{' '*4}{ch[0]}={ch[1]}\n")

        data_lines.append("\n")

        return data_lines

    def match_channels(self, ch_ids: dict[str, str]) -> None:
        """
        Match the channels in the data section with the provided channel IDs.
        This method updates the channel IDs based on the provided list.
        """

        for ch_id in self._channel_ids:
            for key, value in ch_ids.items():
                if isinstance(ch_id, (str)):
                    ch_id = ch_id.lower().split("ch")[-1]
                try:
                    if float(ch_id) == value:
                        setattr(self, key.lower(), value)
                except ValueError:
                    logger.warning(f"Could not match channel {ch_id}")
