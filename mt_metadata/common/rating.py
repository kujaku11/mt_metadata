# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Rating(MetadataBase):
    author: Annotated[
        str | None,
        Field(
            default=None,
            description="Author of who rated the data.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "gradstudent ace",
            },
        ),
    ]

    method: Annotated[
        str | None,
        Field(
            default=None,
            description="The method used to rate the data.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "standard deviation",
            },
        ),
    ]

    value: Annotated[
        int | None,
        Field(
            default=None,
            description="A rating from 1-5 where 1 is bad and 5 is good and 0 if unrated.",
            ge=0,
            le=5,
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "4",
            },
        ),
    ]
