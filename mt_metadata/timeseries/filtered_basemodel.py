# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Filtered(MetadataBase):
    name: Annotated[
        str,
        Field(
            default=[],
            type="string",
            items={"type": "string"},
            description="Name of filter applied or to be applied. If more than one filter input as a comma separated list.",
            examples='"[counts2mv, lowpass_magnetic]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    applied: Annotated[
        bool,
        Field(
            default=False,
            type="boolean",
            items={"type": "boolean"},
            description="Boolean if filter has been applied or not. If more than one filter input as a comma separated list.  Needs to be the same length as name or if only one entry is given it is assumed to apply to all filters listed.",
            examples='"[True, False]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    comments: Annotated[
        str | None,
        Field(
            default=None,
            description="Any comments on filters.",
            examples="low pass is not calibrated",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None
