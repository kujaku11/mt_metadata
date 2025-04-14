# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Instrument(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="Instrument ID number can be serial number or a designated ID.",
            examples="mt01",
            type="string",
            alias=["serial"],
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    manufacturer: Annotated[
        str,
        Field(
            default="",
            description="Who manufactured the instrument.",
            examples="mt gurus",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    type: Annotated[
        str,
        Field(
            default="",
            description="Description of the instrument type.",
            examples="broadband 32-bit",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    model: Annotated[
        str | None,
        Field(
            default=None,
            description="Model version of the instrument.",
            examples="falcon5",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    name: Annotated[
        str | None,
        Field(
            default=None,
            description="Standard marketing name of the instrument.",
            examples="falcon5",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None
