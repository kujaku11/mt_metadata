# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field, AliasChoices


# =====================================================
class Range(MetadataBase):
    """
    Range of values.

    Attributes
    ----------
    min : float
        Minimum value of the range.
    max : float
        Maximum value of the range.
    """

    minimum: Annotated[
        float,
        Field(
            default=0.0,
            description="Minimum value of the range.",
            examples="1.0",
            type="number",
            validation_alias=AliasChoices("start", "minimum", "min"),
            json_schema_extra={
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
            examples="1.0",
            type="number",
            validation_alias=AliasChoices("end", "maximum", "max"),
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
