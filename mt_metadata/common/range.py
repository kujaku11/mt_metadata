# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import AliasChoices, Field

from mt_metadata.base import MetadataBase


# =====================================================
class MinMaxRange(MetadataBase):
    """
    Range of values.

    Attributes
    ----------
    minimum : float
        Minimum value of the range.
    maximum : float
        Maximum value of the range.
    """

    minimum: Annotated[
        float,
        Field(
            default=0.0,
            description="Minimum value of the range.",
            validation_alias=AliasChoices("minimum", "min"),
            json_schema_extra={
                "examples": "1.0",
                "type": "number",
                "units": None,
                "required": True,
            },
        ),
    ]
    maximum: Annotated[
        float,
        Field(
            default=0.0,
            description="Maximum value of the range.",
            validation_alias=AliasChoices("maximum", "max"),
            json_schema_extra={
                "examples": "1.0",
                "type": "number",
                "units": None,
                "required": True,
            },
        ),
    ]


class StartEndRange(MetadataBase):
    """
    Range of values.

    Attributes
    ----------
    start : float
        starting value of the range.
    end : float
        Ending value of the range.
    """

    start: Annotated[
        float,
        Field(
            default=0.0,
            description="Starting value.",
            validation_alias=AliasChoices("start", "beginning"),
            json_schema_extra={
                "examples": "1.0",
                "type": "number",
                "units": None,
                "required": True,
            },
        ),
    ]
    end: Annotated[
        float,
        Field(
            default=0.0,
            description="Ending value of the range.",
            validation_alias=AliasChoices("end", "finish"),
            json_schema_extra={
                "examples": "1.0",
                "type": "number",
                "units": None,
                "required": True,
            },
        ),
    ]
