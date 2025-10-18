# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class GeographicLocation(MetadataBase):
    country: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="Country of the geographic location, should be spelled out in full. Can be a list of countries.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "United States of America",
            },
        ),
    ]

    state: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="State or province of the geographic location, should be spelled out in full. Can be a list of states or provinces.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "[Colorado, Utah]",
            },
        ),
    ]

    county: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="County of the geographic location, should be spelled out in full. Can be a list of counties.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "[Douglass, Fayet]",
            },
        ),
    ]

    township: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="Township or city name or code.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "090",
            },
        ),
    ]

    section: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="Section name or code.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "012",
            },
        ),
    ]

    quarter: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="Quarter section code.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "400",
            },
        ),
    ]

    parcel: Annotated[
        str | list[str] | None,
        Field(
            default=None,
            description="Land parcel ID.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "46b29a",
            },
        ),
    ]
