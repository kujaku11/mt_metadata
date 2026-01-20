# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import computed_field, Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import StrEnumerationBase
from mt_metadata.transfer_functions import CHANNEL_MAPS


# =====================================================
class ExEnum(StrEnumerationBase):
    ex = "ex"
    e1 = "e1"
    e2 = "e2"
    e3 = "e3"
    e4 = "e4"


class EyEnum(StrEnumerationBase):
    ey = "ey"
    e1 = "e1"
    e2 = "e2"
    e3 = "e3"
    e4 = "e4"


class HxEnum(StrEnumerationBase):
    bx = "bx"
    hx = "hx"
    h1 = "h1"
    h2 = "h2"
    h3 = "h3"


class HyEnum(StrEnumerationBase):
    by = "by"
    hy = "hy"
    h1 = "h1"
    h2 = "h2"
    h3 = "h3"


class HzEnum(StrEnumerationBase):
    bz = "bz"
    hz = "hz"
    h1 = "h1"
    h2 = "h2"
    h3 = "h3"


class SupportedNomenclatureEnum(StrEnumerationBase):
    default = "default"
    lemi12 = "lemi12"
    lemi34 = "lemi34"
    musgraves = "musgraves"
    phoenix123 = "phoenix123"


class ChannelNomenclature(MetadataBase):
    ex: Annotated[
        ExEnum,
        Field(
            default="ex",
            description="label for the X electric field channel, X is assumed to be North",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["ex"],
            },
        ),
    ]

    ey: Annotated[
        EyEnum,
        Field(
            default="ey",
            description="label for the Y electric field channel, Y is assumed to be East",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["ey"],
            },
        ),
    ]

    hx: Annotated[
        HxEnum,
        Field(
            default="hx",
            description="label for the X magnetic field channel, X is assumed to be North",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["hx"],
            },
        ),
    ]

    hy: Annotated[
        HyEnum,
        Field(
            default="hy",
            description="label for the Y magnetic field channel, Y is assumed to be East",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["hy"],
            },
        ),
    ]

    hz: Annotated[
        HzEnum,
        Field(
            default="hz",
            description="label for the Z magnetic field channel, Z is assumed to be vertical Down",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["hz"],
            },
        ),
    ]

    keyword: Annotated[
        SupportedNomenclatureEnum,
        Field(
            default=SupportedNomenclatureEnum.default,
            description="Keyword for the channel nomenclature system",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["default", "lemi12", "lemi34", "musgraves", "phoenix123"],
            },
        ),
    ]

    @field_validator("keyword", mode="before")
    @classmethod
    def check_keyword(cls, value, info: ValidationInfo):
        if value is None:
            value = "default"
        return value

    @computed_field
    @property
    def ex_ey(self) -> list[str]:
        return [self.ex.value, self.ey.value]

    @computed_field
    @property
    def hx_hy(self) -> list[str]:
        return [self.hx.value, self.hy.value]

    @computed_field
    @property
    def hx_hy_hz(self) -> list[str]:
        return [self.hx.value, self.hy.value, self.hz.value]

    @computed_field
    @property
    def ex_ey_hz(self) -> list[str]:
        return [self.ex.value, self.ey.value, self.hz.value]

    @computed_field
    @property
    def default_input_channels(self) -> list[str]:
        return self.hx_hy

    @computed_field
    @property
    def default_output_channels(self) -> list[str]:
        return self.ex_ey_hz

    @computed_field
    @property
    def default_reference_channels(self) -> list[str]:
        return self.hx_hy

    def get_channel_map(self) -> dict[str, str]:
        """
        Based on self.keyword return the mapping between conventional channel names and
        the custom channel names in the particular nomenclature.

        """
        try:
            return CHANNEL_MAPS[self.keyword.lower()]
        except KeyError:
            msg = f"channel mt_system {self.keyword} unknown)"
            raise NotImplementedError(msg)

    def update(self) -> None:
        """
        Assign values to standard channel names "ex", "ey" etc based on channel_map dict
        """
        channel_map = self.get_channel_map()
        self.ex = channel_map["ex"]  # type: ignore
        self.ey = channel_map["ey"]  # type: ignore
        self.hx = channel_map["hx"]  # type: ignore
        self.hy = channel_map["hy"]  # type: ignore
        self.hz = channel_map["hz"]  # type: ignore

    def unpack(self) -> tuple:
        return self.ex.value, self.ey.value, self.hx.value, self.hy.value, self.hz.value

    @computed_field
    @property
    def channels(self) -> list[str]:
        channels = list(self.get_channel_map().values())
        return channels

    def __setattr__(self, name, value):
        """Override setattr to automatically update channels when keyword changes."""
        # Call parent setattr first
        super().__setattr__(name, value)

        # If keyword was changed and this is not during initial construction,
        # update the channel mappings
        if (
            name == "keyword"
            and hasattr(self, "_initialized")
            and getattr(self, "_initialized", False)
        ):
            self.update()

    def model_post_init(self, __context):
        """Called after model initialization to set up auto-update and do initial update."""
        self._initialized = True
        self.update()
