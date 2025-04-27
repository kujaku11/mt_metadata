# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class GeographicLocation(MetadataBase):
    country: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="Country of the geographic location, should be spelled out in full. Can be a list of countries.",
            examples="United States of America",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    state: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="State or province of the geographic location, should be spelled out in full. Can be a list of states or provinces.",
            examples="[Colorado, Utah]",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    county: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="County of the geographic location, should be spelled out in full. Can be a list of counties.",
            examples="[Douglass, Fayet]",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    township: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="Township or city name or code.",
            examples="090",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    section: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="Section name or code.",
            examples="012",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    quarter: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="Quarter section code.",
            examples="400",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    parcel: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="Land parcel ID.",
            examples="46b29a",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
