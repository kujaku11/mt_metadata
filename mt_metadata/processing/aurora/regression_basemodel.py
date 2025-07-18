# =====================================================
# Imports
# =====================================================
from typing import Annotated, Any

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Regression(MetadataBase):
    minimum_cycles: Annotated[
        int,
        Field(
            default=None,
            description="Minimum number of cycles in the regression",
            alias=None,
            json_schema_extra={
                "examples": "['10']",
                "units": None,
                "required": True,
            },
        ),
    ]

    max_iterations: Annotated[
        int,
        Field(
            default=None,
            description="Max iterations of the regression",
            alias=None,
            json_schema_extra={
                "examples": "['10']",
                "units": None,
                "required": True,
            },
        ),
    ]

    max_redescending_iterations: Annotated[
        int,
        Field(
            default=None,
            description="Max redescending iterations of the regression",
            alias=None,
            json_schema_extra={
                "examples": "['2']",
                "units": None,
                "required": True,
            },
        ),
    ]

    r0: Annotated[
        Any,
        Field(
            default=1.5,
            description="The number of standard deviations where the influence function changes from linear to quadratic",
            alias=None,
            json_schema_extra={
                "examples": "['1.4']",
                "units": None,
                "required": True,
            },
        ),
    ]

    u0: Annotated[
        Any,
        Field(
            default=2.8,
            description="Control for redescending Huber regression weights.",
            alias=None,
            json_schema_extra={
                "examples": "['2.8']",
                "units": None,
                "required": True,
            },
        ),
    ]

    tolerance: Annotated[
        Any,
        Field(
            default=0.005,
            description="Control for convergence of RME algorithm.  Lower means more iterations",
            alias=None,
            json_schema_extra={
                "examples": "['0.005']",
                "units": None,
                "required": True,
            },
        ),
    ]

    verbosity: Annotated[
        Any,
        Field(
            default=0,
            description="Control for logging messages during regression -- Higher means more messages",
            alias=None,
            json_schema_extra={
                "examples": "['1']",
                "units": None,
                "required": True,
            },
        ),
    ]
