# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from mt_metadata.common import Comment, GeomagneticModelEnum
from pydantic import Field, field_validator, ValidationInfo


# =====================================================


class Declination(MetadataBase):
    comments: Annotated[
        Comment | str,
        Field(
            default_factory=lambda: Comment(),
            description="any comments on declination",
            examples="estimated from WMM 2016",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    model: Annotated[
        GeomagneticModelEnum,
        Field(
            default="IGRF",
            description="geomagnetic reference model used to calculate declination",
            examples="WMM",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    epoch: Annotated[
        str | None,
        Field(
            default=None,
            description="Epoch for which declination was approximated in.",
            examples="2020",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    value: Annotated[
        float,
        Field(
            default=0.0,
            description="declination angle relative to geographic north positive clockwise",
            examples="12.3",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
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
