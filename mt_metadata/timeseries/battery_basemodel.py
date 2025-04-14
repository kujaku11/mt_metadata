# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Battery(MetadataBase):
    type: Annotated[
        str | None,
        Field(
            default=None,
            description="Description of battery type.",
            examples="pb-acid gel cell",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    id: Annotated[
        str | None,
        Field(
            default=None,
            description="battery id",
            examples="battery01",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    voltage.start: Annotated[
        float | None,
        Field(
            default=None,
            description="Starting voltage",
            examples="14.3",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "volts",
                "required": False,
            },
        ),
    ] = None

    voltage.end: Annotated[
        float | None,
        Field(
            default=None,
            description="Ending voltage",
            examples="12.1",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "volts",
                "required": False,
            },
        ),
    ] = None

    comments: Annotated[
        str | None,
        Field(
            default=None,
            description="Any comments about the battery.",
            examples="discharged too quickly",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None
