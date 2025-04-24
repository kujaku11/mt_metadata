# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from mt_metadata.common import (
    Comment,
    DataQuality,
    TimePeriod,
    Instrument,
    Fdsn,
    Location,
)
from mt_metadata.timeseries.filtered_basemodel import Filtered
from pydantic import Field, field_validator, ValidationInfo, AliasChoices

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


class PartialLocation(Location):
    """
    A partial location class that only includes the latitude, longitude, and elevation.
    This is used to avoid circular imports.
    """

    latitude: Annotated[
        float | None,
        Field(
            default=None,
            description="Latitude of the location.",
            examples="12.324",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    longitude: Annotated[
        float | None,
        Field(
            default=None,
            description="Longitude of the location.",
            examples="12.324",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    elevation: Annotated[
        float | None,
        Field(
            default=None,
            description="Elevation of the location.",
            examples="1234.0",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]


class Channel(MetadataBase):
    channel_number: Annotated[
        int,
        Field(
            default=None,
            description="Channel number on the data logger.",
            examples="1",
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
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    component: Annotated[
        str,
        Field(
            default="",
            description="Name of the component measured, can be uppercase and/or lowercase.  For now electric channels should start with an 'e' and magnetic channels start with an 'h', followed by the component. If there are multiples of the same channel the name could include an integer.  {type}{component}{number} --> Ex01.",
            examples="ex",
            alias=None,
            pattern=r"\w+",
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
            validation_alias=AliasChoices("measurement_azimuth", "azimuth"),
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
            validation_alias=AliasChoices("measurement_tilt", "dip"),
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
            validation_alias=AliasChoices("sample_rate", "sampling_rate"),
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
            alias=None,
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
            alias=None,
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
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    data_quality: Annotated[
        DataQuality,
        Field(
            default_factory=DataQuality,
            description="Data quality for the channel.",
            examples="",
            type="object",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    filter: Annotated[
        Filtered,
        Field(
            default_factory=Filtered,
            description="Filtered data for the channel.",
            examples="Filtered()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    time_period: Annotated[
        TimePeriod,
        Field(
            default_factory=TimePeriod,
            description="Time period for the channel.",
            examples="TimePeriod(start='2020-01-01', end='2020-12-31')",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    sensor: Annotated[
        Instrument,
        Field(
            default_factory=Instrument,
            description="Sensor for the channel.",
            examples="Instrument()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    fdsn: Annotated[
        Fdsn,
        Field(
            default_factory=Fdsn,
            description="FDSN information for the channel.",
            examples="Fdsn()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    location: Annotated[
        PartialLocation,
        Field(
            default_factory=PartialLocation,
            description="Location information for the channel.",
            examples="PartialLocation(latitude=0.0, longitude=0.0, elevation=0.0)",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
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
