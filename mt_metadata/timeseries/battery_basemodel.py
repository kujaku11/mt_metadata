# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from mt_metadata.timeseries.range_basemodel import StartEndRange
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

    voltage: Annotated[
        StartEndRange,
        Field(
            default=StartEndRange(),
            description="Range of voltages.",
            examples="Range(minimum=0.0, maximum=1.0)",
            type="object",
            alias=None,
            json_schema_extra={
                "units": "volts",
                "required": False,
            },
        ),
    ]

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
