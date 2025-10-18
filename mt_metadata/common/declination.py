# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment, GeomagneticModelEnum


# =====================================================


class Declination(MetadataBase):
    comments: Annotated[
        Comment,
        Field(
            default_factory=lambda: Comment(),
            description="any comments on declination",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["estimated from WMM 2016"],
            },
        ),
    ]

    model: Annotated[
        GeomagneticModelEnum,
        Field(
            default="IGRF",
            description="geomagnetic reference model used to calculate declination",
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["WMM"],
            },
        ),
    ]

    epoch: Annotated[
        str | None,
        Field(
            default=None,
            description="Epoch for which declination was approximated in.",
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["2020"],
            },
        ),
    ]

    value: Annotated[
        float,
        Field(
            default=0.0,
            description="declination angle relative to geographic north positive clockwise",
            json_schema_extra={
                "units": "degrees",
                "required": True,
                "examples": ["12.5"],
            },
        ),
    ]

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        """
        Validate that the value is a valid comment.
        """
        if isinstance(value, str):
            return Comment(value=value)
        return value
