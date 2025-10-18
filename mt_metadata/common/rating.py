# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo

from mt_metadata import NULL_VALUES
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
        int | None | str,
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

    @field_validator("value", mode="before")
    @classmethod
    def validate_value(
        cls, value: int | None | str, info: ValidationInfo
    ) -> int | None | str:
        if isinstance(value, str):
            try:
                value = int(value)
                if value < 0 or value > 5:
                    raise ValueError("Invalid rating value must be between 0 and 5.")

            except ValueError:
                if value in NULL_VALUES:
                    value = None
                else:
                    raise ValueError(f"Invalid rating value: {value}")
        elif isinstance(value, int):
            if value < 0 or value > 5:
                raise ValueError("Invalid rating value must be between 0 and 5.")
        elif value is not None:
            raise ValueError(f"Invalid rating value: {value}")
        return value
