# -*- coding: utf-8 -*-
"""
Stub for CrossPowers feature.
"""

# ==============================================================================
# Imports
# ==============================================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.features.feature import Feature


# ==============================================================================
class CrossPowers(Feature):
    """
    Stub feature class for cross powers.
    """

    name: Annotated[
        str,
        Field(
            default="cross_powers",
            description="Name of the feature",
            json_schema_extra={
                "required": True,
                "units": None,
                "example": ["cross_powers"],
            },
        ),
    ]
