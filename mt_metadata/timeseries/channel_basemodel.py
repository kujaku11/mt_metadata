# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from mt_metadata.common import (
    Comment,
    Rating,
    DataQuality,
    Filtered,
    TimePeriod,
    Instrument,
    Fdsn,
)
from pydantic import Field, field_validator, ValidationInfo

# dq_dict.add_dict(get_schema("rating", SCHEMA_FN_PATHS), "rating")
# attr_dict.add_dict(dq_dict, "data_quality")
# attr_dict.add_dict(get_schema("filtered", SCHEMA_FN_PATHS), "filter")
# attr_dict.add_dict(get_schema("time_period", SCHEMA_FN_PATHS), "time_period")
# attr_dict.add_dict(get_schema("instrument", SCHEMA_FN_PATHS), "sensor")
# attr_dict.add_dict(get_schema("fdsn", SCHEMA_FN_PATHS), "fdsn")
# attr_dict.add_dict(
#     get_schema("location", SCHEMA_FN_PATHS),
#     "location",
#     keys=["latitude", "longitude", "elevation"],
# )


# =====================================================
class ComponentEnum(str, Enum):
    Ex = "Ex"
    Ey = "Ey"
    Hx = "Hx"
    Hy = "Hy"
    Hz = "Hz"
    Bx = "Bx"
    By = "By"
    Bz = "Bz"
    T = "T"
    Battery = "Battery"
    other = "other"
    none = ""


class UnitsEnum(str, Enum):
    metric = "metric"
    celsius = "celsius"
    meters = "meters"
    degrees = "degrees"
    kilograms = "kilograms"
    volts = "volts"
    amps = "amps"
    ohms = "ohms"
    hertz = "hertz"
    pascals = "pascals"
    tesla = "tesla"
    gauss = "gauss"
    microvolts = "microvolts"
    millivolts = "millivolts"
    nanotesla = "nanotesla"
    microtesla = "microtesla"
    millitesla = "millitesla"
    microamps = "microamps"
    milliamps = "milliamps"
    microohms = "microohms"
    milliohms = "milliohms"
    counts = "counts"
    counts_per_second = "counts per second"
    other = "other"
    none = ""


class Channel(MetadataBase):
    channel_number: Annotated[
        int,
        Field(
            default=None,
            description="Channel number on the data logger.",
            examples="1",
            type="integer",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channel_id: Annotated[
        str | None,
        Field(
            default=None,
            description="channel id given by the user or data logger",
            examples="1001.11",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=Comment,
            description="Any comments about the channel.",
            examples="ambient air temperature was chilly, ice on cables",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    component: Annotated[
        ComponentEnum,
        Field(
            default="",
            description="Name of the component measured, can be uppercase and/or lowercase.  For now electric channels should start with an 'e' and magnetic channels start with an 'h', followed by the component. If there are multiples of the same channel the name could include an integer.  {type}{component}{number} --> Ex01.",
            examples="T",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    measurement_azimuth: Annotated[
        float,
        Field(
            default=0.0,
            description="Horizontal azimuth of the channel in measurement coordinate system spcified in station.orientation.reference_frame.  Default reference frame is a geographic right-handed coordinate system with north=0, east=90, vertical=+ downward.",
            examples="0",
            type="number",
            alias=["azimuth"],
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    measurement_tilt: Annotated[
        float,
        Field(
            default=0.0,
            description="Vertical tilt of the channel in measurement coordinate system specified in station.orientation.reference_frame.  Default reference frame is a geographic right-handed coordinate system with north=0, east=90, vertical=+ downward.",
            examples="0",
            type="number",
            alias=["dip"],
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    sample_rate: Annotated[
        float,
        Field(
            default=0.0,
            description="Digital sample rate",
            examples="8",
            type="number",
            alias=["sampling_rate"],
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    translated_azimuth: Annotated[
        float | None,
        Field(
            default=None,
            description="Horizontal azimuth of the channel in translated coordinate system, this should only be used for derived product.  For instance if you collected your data in geomagnetic coordinates and then translated them to geographic coordinates you would set measurement_azimuth=0, translated_azimuth=-12.5 for a declination angle of N12.5E.",
            examples="0",
            type="number",
            alias=["azimuth"],
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    translated_tilt: Annotated[
        float | None,
        Field(
            default=None,
            description="Tilt of channel in translated coordinate system, this should only be used for derived product.  For instance if you collected your data using a tripod you would set measurement_tilt=45, translated_tilt=0 for a vertical component.",
            examples="0",
            type="number",
            alias=["dip"],
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    type: Annotated[
        str,
        Field(
            default="",
            description="Data type for the channel, should be a descriptive word that a user can understand.",
            examples="temperature",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    units: Annotated[
        UnitsEnum,
        Field(
            default="",
            description="Units of the data, should be in SI units and represented as the full name of the unit all lowercase.  If a complex unit use 'per' and '-'.",
            examples="celsius",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        """
        Validate that the value is a valid comment.
        """
        if isinstance(value, str):
            return Comment(value=value)
        return value
