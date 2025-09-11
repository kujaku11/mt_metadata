# =====================================================
# Imports
# =====================================================
from typing import Annotated, Union

from pydantic import computed_field, Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import TimePeriod
from mt_metadata.processing.aurora.channel_basemodel import Channel


# =====================================================
class Run(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="run ID",
            examples=["001"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    input_channels: Annotated[
        list[Channel],
        Field(
            default_factory=list,
            description="List of input channels (source)",
            examples=["hx, hy"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    output_channels: Annotated[
        list[Channel],
        Field(
            default_factory=list,
            description="List of output channels (response)",
            examples=["ex, ey, hz"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    time_periods: Annotated[
        list[TimePeriod],
        Field(
            default_factory=list,
            description="List of time periods to process",
            examples=[
                "[{'start': '2020-01-01T00:00:00', 'end': '2020-01-01T01:00:00'}]"
            ],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    sample_rate: Annotated[
        float,
        Field(
            default=1.0,
            description="sample rate of the run",
            examples=["1"],
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    @field_validator("input_channels", "output_channels", mode="before")
    @classmethod
    def validate_channel_list(
        cls, values: Union[list, str, Channel, dict], info: ValidationInfo
    ) -> list[Channel]:
        channels = []
        if not isinstance(values, list):
            values = [values]

        for item in values:
            if isinstance(item, str):
                ch = Channel(id=item)
            elif isinstance(item, Channel):
                ch = item

            elif isinstance(item, dict):
                ch = Channel()
                ch.from_dict(item)

            else:
                raise TypeError(f"not sure what to do with type {type(item)}")

            channels.append(ch)

        return channels

    @field_validator("time_periods", mode="before")
    @classmethod
    def validate_time_periods(
        cls, values: Union[list, dict, TimePeriod], info: ValidationInfo
    ) -> list[TimePeriod]:
        time_periods = []
        if not isinstance(values, list):
            values = [values]

        for item in values:
            if isinstance(item, TimePeriod):
                tp = item

            elif isinstance(item, dict):
                tp = TimePeriod()
                tp.from_dict(item)

            else:
                raise TypeError(f"not sure what to do with type {type(item)}")

            time_periods.append(tp)

        return time_periods

    @computed_field
    @property
    def channel_scale_factors(self) -> dict[str, float]:
        scale_factors = {}
        for ch in self.input_channels + self.output_channels:
            if ch.scale_factor is not None:
                scale_factors[ch.id] = ch.scale_factor
        return scale_factors

    def set_channel_scale_factors(self, values: Union[dict, float]):
        """
        Validate and process channel scale factors.

        Parameters
        ----------
        values : Union[dict, float]
            The scale factors for the channels.

        Raises
        ------
        TypeError
            If the input is not a dictionary or float.
        """
        if not isinstance(values, dict):
            raise TypeError(f"not sure what to do with type {type(values)}")
        for i, channel in enumerate(self.input_channels):
            if channel.id in values.keys():
                self.input_channels[i].scale_factor = values[channel.id]
        for i, channel in enumerate(self.output_channels):
            if channel.id in values.keys():
                self.output_channels[i].scale_factor = values[channel.id]
