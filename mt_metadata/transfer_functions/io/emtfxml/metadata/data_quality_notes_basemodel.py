# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class DataQualityNotes(MetadataBase):
    good_from_period: Annotated[
        float | None,
        Field(
            default=None,
            description="Data are good for periods larger than this number",
            examples=["0.01"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    good_to_period: Annotated[
        float | None,
        Field(
            default=None,
            description="Data are good for periods smaller than this number",
            examples=["1000"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    rating: Annotated[
        int | None,
        Field(
            default=None,
            description="Rating of the data from 0 to 5 where 5 is the best and 0 is unrated",
            examples=["4"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
