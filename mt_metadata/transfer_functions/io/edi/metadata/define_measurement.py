# =====================================================
# Imports
# =====================================================
from typing import Annotated

from loguru import logger
from pydantic import computed_field, Field, field_validator, PrivateAttr, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.timeseries import Auxiliary, Electric, Magnetic  # noqa: F401
from mt_metadata.transfer_functions.io.tools import _validate_str_with_equals
from mt_metadata.utils.location_helpers import (
    convert_position_float2str,
    validate_position,
)
from mt_metadata.utils.units import get_unit_object

from . import EMeasurement, HMeasurement


# =====================================================
class DefineMeasurement(MetadataBase):
    """
    DefineMeasurement class holds information about the measurement.  This
    includes how each channel was setup.  The main block contains information
    on the reference location for the station.  This is a bit of an archaic
    part and was meant for a multiple station .edi file.  This section is also
    important if you did any forward modeling with Winglink cause it only gives
    the station location in this section.  The other parts are how each channel
    was collected.  An example define measurement section looks like::

        >=DEFINEMEAS

            MAXCHAN=7
            MAXRUN=999
            MAXMEAS=9999
            UNITS=M
            REFTYPE=CART
            REFLAT=-30:12:49.4693
            REFLONG=139:47:50.87
            REFELEV=0

        >HMEAS ID=1001.001 CHTYPE=HX X=0.0 Y=0.0 Z=0.0 AZM=0.0
        >HMEAS ID=1002.001 CHTYPE=HY X=0.0 Y=0.0 Z=0.0 AZM=90.0
        >HMEAS ID=1003.001 CHTYPE=HZ X=0.0 Y=0.0 Z=0.0 AZM=0.0
        >EMEAS ID=1004.001 CHTYPE=EX X=0.0 Y=0.0 Z=0.0 X2=0.0 Y2=0.0
        >EMEAS ID=1005.001 CHTYPE=EY X=0.0 Y=0.0 Z=0.0 X2=0.0 Y2=0.0
        >HMEAS ID=1006.001 CHTYPE=HX X=0.0 Y=0.0 Z=0.0 AZM=0.0
        >HMEAS ID=1007.001 CHTYPE=HY X=0.0 Y=0.0 Z=0.0 AZM=90.0

    :param fn: full path to .edi file to read in.
    :type fn: string

    ================= ==================================== ======== ===========
    Attributes        Description                          Default  In .edi
    ================= ==================================== ======== ===========
    fn                Full path to edi file read in        None     no
    maxchan           Maximum number of channels measured  None     yes
    maxmeas           Maximum number of measurements       9999     yes
    maxrun            Maximum number of measurement runs   999      yes
    meas_####         HMeasurement or EMEasurment object   None     yes
                      defining the measurement made [1]__
    refelev           Reference elevation (m)              None     yes
    reflat            Reference latitude [2]_              None     yes
    refloc            Reference location                   None     yes
    reflon            Reference longituted [2]__           None     yes
    reftype           Reference coordinate system          'cart'   yes
    units             Units of length                      m        yes
    _define_meas_keys Keys to include in define_measurment [3]__     no
                      section.
    ================= ==================================== ======== ===========

    .. [1] Each channel with have its own define measurement and depending on
           whether it is an E or H channel the metadata will be different.
           the #### correspond to the channel number.
    .. [2] Internally everything is converted to decimal degrees.  Output is
          written as HH:MM:SS.ss so Winglink can read them in.
    .. [3] If you want to change what metadata is written into the .edi file
           change the items in _header_keys.  Default attributes are:
               * maxchan
               * maxrun
               * maxmeas
               * reflat
               * reflon
               * refelev
               * reftype
               * units

    """

    maxchan: Annotated[
        int,
        Field(
            default=999,
            description="maximum number of channels",
            examples=["16"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    maxrun: Annotated[
        int,
        Field(
            default=999,
            description="maximum number of runs",
            examples=["999"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    maxmeas: Annotated[
        int,
        Field(
            default=7,
            description="maximum number of measurements",
            examples=["999"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    reftype: Annotated[
        str | None,
        Field(
            default="cartesian",
            description="Type of offset from reference center point.",
            examples=["cartesian", "cart"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    refloc: Annotated[
        str | None,
        Field(
            default=None,
            description="Description of location reference center point.",
            examples=["here"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    reflat: Annotated[
        float,
        Field(
            default=0,
            description="Latitude of reference center point.",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    reflon: Annotated[
        float,
        Field(
            default=0,
            description="Longitude reference center point.",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    refelev: Annotated[
        float,
        Field(
            default=0,
            description="Elevation reference center point.",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    units: Annotated[
        str | None,
        Field(
            default="m",
            description="In the EDI standards this is the elevation units.",
            examples=["m"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    measurements: Annotated[
        dict[str, EMeasurement | HMeasurement],
        Field(
            default_factory=dict,
            description="Dictionary of measurements with keys as channel types "
            "(e.g., 'hx', 'hy', 'ex', 'ey', etc.) and values as "
            "EMeasurement or HMeasurement objects.",
            examples=["{'hx': EMeasurement(...), 'hy': HMeasurement(...)}"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    _define_meas_keys: list[str] = PrivateAttr(
        default=[
            "maxchan",
            "maxrun",
            "maxmeas",
            "reflat",
            "reflon",
            "refelev",
            "reftype",
            "units",
        ]
    )

    @field_validator("units", mode="before")
    @classmethod
    def validate_units(cls, value: str) -> str:
        if value in [None, ""]:
            return ""
        if value.lower() in ["m", "meters"]:
            value = "m"
        try:
            unit_object = get_unit_object(value)
            return unit_object.name
        except ValueError as error:
            raise KeyError(error)
        except KeyError as error:
            raise KeyError(error)

    @field_validator("reflat", "reflon", mode="before")
    @classmethod
    def validate_position(cls, value, info: ValidationInfo):
        if "lat" in info.field_name:
            position_type = "latitude"
        elif "lon" in info.field_name:
            position_type = "longitude"
        return validate_position(value, position_type)

    def __str__(self):
        return "".join(self.write_measurement())

    def __repr__(self):
        return self.__str__()

    @computed_field
    @property
    def channel_ids(self) -> dict[str, str]:
        ch_ids = {}
        for comp in ["ex", "ey", "hx", "hy", "hz", "rrhx", "rrhy"]:
            try:
                m = self.measurements[comp]
                # if there are remote references that are the same as the
                # h channels skip them.
                ch_ids[m.chtype] = m.id
            except KeyError:
                continue

        return ch_ids

    def get_measurement_lists(self, edi_lines: str) -> None:
        """
        get measurement list including measurement setup

        Attributes
        ----------
        edi_lines : str
            lines from the edi file to parse
        """

        self._measurement_list = []
        meas_find = False
        count = 0

        for line in edi_lines:
            if ">=" in line and "definemeas" in line.lower():
                meas_find = True
            elif ">=" in line:
                if meas_find is True:
                    return
            elif meas_find is True and ">" not in line:
                line = line.strip()
                if len(line) > 2:
                    if count > 0:
                        line_list = _validate_str_with_equals(line)
                        for ll in line_list:
                            ll_list = ll.split("=")
                            key = ll_list[0].lower()
                            value = ll_list[1]
                            self._measurement_list[-1][key] = value
                    else:
                        self._measurement_list.append(line.strip())

            # look for the >XMEAS parts
            elif ">" in line and meas_find:
                if line.find("!") > 0:
                    pass
                elif "meas" in line.lower():
                    count += 1
                    line_list = _validate_str_with_equals(line)
                    m_dict = {}
                    for ll in line_list:
                        ll_list = ll.split("=")
                        key = ll_list[0].lower()
                        value = ll_list[1]
                        m_dict[key] = value
                    self._measurement_list.append(m_dict)
                else:
                    return

    def read_measurement(self, edi_lines: str) -> None:
        """
        read the define measurment section of the edi file

        should be a list with lines for:

            - maxchan
            - maxmeas
            - maxrun
            - refelev
            - reflat
            - reflon
            - reftype
            - units
            - dictionaries for >XMEAS with keys:

                - id
                - chtype
                - x
                - y
                - axm
                - acqchn

        """
        self.get_measurement_lists(edi_lines)

        for line in self._measurement_list:
            if isinstance(line, str):
                line_list = line.split("=")
                key = line_list[0].lower()
                value = line_list[1].strip()
                if key in "reflatitude":
                    key = "reflat"
                    value = value
                elif key in "reflongitude":
                    key = "reflon"
                    value = value
                elif key in "refelevation":
                    key = "refelev"
                    value = value
                elif key in "maxchannels":
                    key = "maxchan"
                    try:
                        value = int(value)
                    except ValueError:
                        value = 0
                elif key in "maxmeasurements":
                    key = "maxmeas"
                    try:
                        value = int(value)
                    except ValueError:
                        value = 0
                elif key in "maxruns":
                    key = "maxrun"
                    try:
                        value = int(value)
                    except ValueError:
                        value = 0
                setattr(self, key, value)

            elif isinstance(line, dict):
                ch_type = line["chtype"].lower()
                key = f"{ch_type}"
                if ch_type.find("h") >= 0:
                    value = HMeasurement(**line)
                elif ch_type.find("e") >= 0:
                    value = EMeasurement(**line)
                    if value.azm == 0:
                        value.azm = value.azimuth
                if key in self.measurements.keys():
                    existing_ch = self.measurements[key]
                    existing_line = existing_ch.write_meas_line()
                    value_line = value.write_meas_line()
                    if existing_line != value_line:
                        value.chtype = f"rr{ch_type}".upper()
                        key = f"rr{ch_type}"
                    else:
                        continue
                self.measurements[key] = value

    def _sort_measurements(self) -> list[str]:
        """
        Sort the measurements by channel type and return a list of sorted keys.
        This is used to ensure that the measurements are written in a consistent order.
        """
        # need to write the >XMEAS type, but sort by channel number
        m_key_list = []
        count = 1.0
        for key, meas in self.measurements.items():
            value = meas.id
            if value == 0.0:
                value = count
                count += 1
            m_key_list.append((key, value))

        return sorted(m_key_list, key=lambda x: x[1])

    def write_measurement(
        self,
        longitude_format: str = "LON",
        latlon_format: str = "dd",
    ) -> list[str]:
        """
        write_measurement writes the define measurement section of the edi file.

        Parameters
        ----------
        longitude_format : str, optional
            longitude format [ "LONG" | "LON" ] , by default "LON"
        latlon_format : str, optional
            position format [ "dd" | " degrees" ], by default "dd" for decimal degrees
            If you want to write the position in degrees, use " degrees" for the
            latlon_format.  This will write the position in the format of
            HH:MM:SS.ss for the latitude and longitude.  If you want to write
            the position in decimal degrees, use "dd" for the latlon_format.

        Returns
        -------
        list[str]
            list of lines for the define measurement section or an empty list if no
            measurements are defined.

        Raises
        ------
        ValueError
            If a value cannot be converted to a float or if the longitude format is not
            recognized.
        """

        measurement_lines = ["\n>=DEFINEMEAS\n"]
        for key in self._define_meas_keys:
            value = getattr(self, key)
            if key in ["reflat", "reflon", "reflong"]:
                if latlon_format.lower() == "dd":
                    value = f"{float(value):.6f}"
                else:
                    value = convert_position_float2str(value)
            elif key == "refelev":
                value = value
            if key.upper() == "REFLON":
                if longitude_format == "LONG":
                    key += "G"
            if value is not None:
                measurement_lines.append(f"{' '*4}{key.upper()}={value}\n")
        measurement_lines.append("\n")

        # need to write the >XMEAS type, but sort by channel number
        m_key_list = self._sort_measurements()

        if len(m_key_list) == 0:
            logger.warning("No XMEAS information.")
        else:
            # need to sort the dictionary by chanel id
            for meas in sorted(m_key_list, key=lambda x: x[1]):
                x_key = meas[0]
                m_obj = self.measurements[x_key]
                if m_obj.id == 0.0:
                    m_obj.id = meas[1]
                if m_obj.acqchan == "0":
                    m_obj.acqchan = meas[1]

                measurement_lines.append(m_obj.write_meas_line())

        return measurement_lines

    def from_metadata(self, channel: Electric | Magnetic | Auxiliary) -> None:
        """

        from_metadata converts a channel object into a measurement object
        and sets the attributes for the measurement object.

        Parameters
        ----------
        channel : Electric | Magnetic | Auxiliary
            The channel object to convert into a measurement object.
        """

        if channel.component is None:
            return

        azm = channel.measurement_azimuth
        if azm != channel.translated_azimuth:
            azm = channel.translated_azimuth
        if azm is None:
            azm = 0.0
        if "e" in channel.component:
            for attr in [
                "negative.x",
                "negative.y",
                "positive.x2",
                "positive.y2",
                "measurement_azimuth",
                "translated_azimuth",
            ]:
                if channel.get_attr_from_name(attr) is None:
                    channel.update_attribute(attr, 0)
            meas = EMeasurement(
                **{
                    "x": channel.negative.x,
                    "x2": channel.positive.x2,
                    "y": channel.negative.y,
                    "y2": channel.positive.y2,
                    "chtype": channel.component,
                    "id": channel.channel_id,
                    "azm": azm,
                    "acqchan": channel.channel_number,
                }
            )
            self.measurements[channel.component.lower()] = meas

        elif "h" in channel.component:
            for attr in ["location.x", "location.y", "location.z"]:
                if channel.get_attr_from_name(attr) is None:
                    channel.update_attribute(attr, 0)
            meas = HMeasurement(
                **{
                    "x": channel.location.x,
                    "y": channel.location.y,
                    "azm": azm,
                    "chtype": channel.component,
                    "id": channel.channel_id,
                    "acqchan": channel.channel_number,
                    "dip": channel.measurement_tilt,
                }
            )
            self.measurements[channel.component.lower()] = meas

    @computed_field(return_type=list[str])
    @property
    def channels_recorded(self) -> list[str]:
        """Get the channels recorded"""

        return [cc.lower() for cc in self.measurements.keys()]
