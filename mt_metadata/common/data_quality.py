# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment, Rating


# =====================================================
class DataQuality(MetadataBase):
    warnings: Annotated[
        str | None,
        Field(
            default=None,
            description="any warnings about the data that should be noted",
            examples=["periodic pipeline noise"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

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

    flag: Annotated[
        int | None,
        Field(
            default=None,
            description="Flag for data quality",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=Comment,  # type: ignore
            description="any comments about the data quality",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    rating: Annotated[
        Rating,
        Field(
            default_factory=Rating,  # type: ignore
            description="rating of the data quality",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        """
        Validate that the value is a valid string.
        """
        if isinstance(value, str):
            return Comment(value=value)  # type: ignore[return-value]
        return value
