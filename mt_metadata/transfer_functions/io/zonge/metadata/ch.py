# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase


# =====================================================
class CH(MetadataBase):
    a_d_card_s_n: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="serial number of ad card for local and remote stations",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["6545BAC6,BE380864"],
            },
        ),
    ]

    gdp_box: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="Box number for local and remote stations",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["18,15"],
            },
        ),
    ]

    stn: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="station number of local and remote",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["1,2"],
            },
        ),
    ]

    number: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="channel number for local and coil number of remote",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["1, 2284"],
            },
        ),
    ]

    cmp: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="component of local and remote stations",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["ex,hy"],
            },
        ),
    ]

    c_res: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="contact resistance for local and remote sensors",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["0,0"],
            },
        ),
    ]

    azimuth: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="azimuth for local and remote sensors",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["12.1,12.1"],
            },
        ),
    ]

    incl: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="Inclination ",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["335754.685:4263553.435:1650.2"],
            },
        ),
    ]

    @field_validator(
        "a_d_card_s_n",
        "gdp_box",
        "stn",
        "number",
        "cmp",
        "c_res",
        "azimuth",
        "incl",
        mode="before",
    )
    @classmethod
    def validate_comma_separated_fields(cls, v):
        """
        Validate fields that may contain comma-separated values.
        Returns a list when commas are found, otherwise returns the string as-is.
        """
        if v is None:
            return None
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # If the value contains a comma, split into a list
            if "," in v:
                parts = [part.strip() for part in v.split(",") if part.strip()]
                # Return list if we have multiple parts, otherwise return single string
                return parts if len(parts) > 1 else (parts[0] if parts else None)
            return v
        return str(v)
