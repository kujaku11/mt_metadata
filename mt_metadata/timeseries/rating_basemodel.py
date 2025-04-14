# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Rating(MetadataBase):
    author: Annotated[
        str | None,
        Field(
            default=None,
            description="Author of who rated the data.",
            examples="gradstudent ace",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    method: Annotated[
        str | None,
        Field(
            default=None,
            description="The method used to rate the data.",
            examples="standard deviation",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    value: Annotated[
        int,
        Field(
            default=None,
            description="A rating from 1-5 where 1 is bad and 5 is good and 0 if unrated.",
            examples="4",
            type="integer",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
