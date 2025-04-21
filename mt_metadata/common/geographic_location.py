# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class GeographicLocation(MetadataBase):
    country: Annotated[
        str | None,
        Field(
            default=None,
            type="string",
            items={"type": "string"},
            description="Country of the geographic location, should be spelled out in full. Can be a list of countries.",
            examples="United States of America",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    state: Annotated[
        str | None,
        Field(
            default=None,
            type="string",
            items={"type": "string"},
            description="State or province of the geographic location, should be spelled out in full. Can be a list of states or provinces.",
            examples="[Colorado, Utah]",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    county: Annotated[
        str | None,
        Field(
            default=None,
            type="string",
            items={"type": "string"},
            description="County of the geographic location, should be spelled out in full. Can be a list of counties.",
            examples="[Douglass, Fayet]",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    township: Annotated[
        str | None,
        Field(
            default=None,
            description="Township or city name or code.",
            examples="090",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    section: Annotated[
        str | None,
        Field(
            default=None,
            description="Section name or code.",
            examples="012",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    quarter: Annotated[
        str | None,
        Field(
            default=None,
            description="Quarter section code.",
            examples="400",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    parcel: Annotated[
        str | None,
        Field(
            default=None,
            description="Land parcel ID.",
            examples="46b29a",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None
