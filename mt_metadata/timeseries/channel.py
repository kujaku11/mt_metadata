# =====================================================
# Imports
# =====================================================

from typing import Annotated
from loguru import logger

from mt_metadata.base import MetadataBase
from mt_metadata.common import (
    Comment,
    DataQuality,
    TimePeriod,
    Instrument,
    Fdsn,
    BasicLocation,
)
from mt_metadata.timeseries import Filter
from pydantic import Field, field_validator, ValidationInfo, AliasChoices, PrivateAttr
from mt_metadata.utils.units import get_unit_object, Unit
from mt_metadata.timeseries.filters import ChannelResponse

# =====================================================


# this is a channel base for channels that have multiple sensors and locations like an
# electric dipole.
class ChannelBase(MetadataBase):
    _channel_type: str = PrivateAttr("base")
    channel_number: Annotated[
        int,
        Field(
            default=0,
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
            default="base",
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
        str,
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
        Filter,
        Field(
            default_factory=Filter,
            description="Filter data for the channel.",
            examples="Filter()",
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

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        """
        Validate that the value is a valid comment.
        """
        if isinstance(value, str):
            return Comment(value=value)
        return value

    @field_validator("units", mode="before")
    @classmethod
    def validate_units(cls, value: str, info: ValidationInfo) -> str:
        """
        validate units base on input string will return the long name

        Parameters
        ----------
        value : units string
            unit string separated by either '/' for division or ' ' for
            multiplication.  Or 'per' and ' ', respectively
        info : ValidationInfo
            _description_

        Returns
        -------
        str
            return the long descriptive name of the unit. For example 'kilometers'.
        """
        if value in [None, ""]:
            return ""
        try:
            unit_object = get_unit_object(value)
            return unit_object.name
        except ValueError as error:
            raise KeyError(error)
        except KeyError as error:
            raise KeyError(error)

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, value, info: ValidationInfo) -> str:
        """
        Validate that the type channel
        """
        # Get the expected filter type based on the actual class
        # Make sure derived classes define their own _filter_type as class variable
        expected_type = getattr(cls, "_channel_type", "base").default

        if value != expected_type:
            logger.warning(
                f"Channel type is set to {value}, but should be "
                f"{expected_type} for {cls.__name__}."
            )
        return expected_type

    def channel_response(self, filters_dict):
        """
        full channel response from a dictionary of filter objects
        """

        mt_filter_list = []
        for applied in self.filtered.filter_list:
            try:
                mt_filter = filters_dict[applied.name]
                mt_filter_list.append(mt_filter)
            except KeyError:
                msg = f"Could not find {applied.name} in filters dictionary, skipping"
                logger.error(msg)
                continue
        # compute instrument sensitivity and units in/out
        return ChannelResponse(filters_list=mt_filter_list)

    @property
    def unit_object(self) -> Unit:
        """
        Some channels have a unit object that is used to convert between units.
        This is a property that returns the unit object for the channel.
        The unit object is created using the units attribute of the channel.
        The unit object is used to convert between units and to get the unit

        Returns
        -------
        Unit
            BaseModel object with unit attributes
        """
        return get_unit_object(self.units)


# this would be a normal channel that has a single sensor and location.
class Channel(ChannelBase):

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

    location: Annotated[
        BasicLocation,
        Field(
            default_factory=BasicLocation,
            description="Location information for the channel.",
            examples="BasicLocation(latitude=0.0, longitude=0.0, elevation=0.0)",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
