# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Regression(MetadataBase):
    minimum_cycles: Annotated[
        int,
        Field(
            default=1,
            description="Minimum number of cycles in the regression",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["10"],
            },
        ),
    ]

    max_iterations: Annotated[
        int,
        Field(
            default=10,
            description="Max iterations of the regression",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["10"],
            },
        ),
    ]

    max_redescending_iterations: Annotated[
        int,
        Field(
            default=2,
            description="Max redescending iterations of the regression",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2"],
            },
        ),
    ]

    r0: Annotated[
        float,
        Field(
            default=1.5,
            description="The number of standard deviations where the influence function changes from linear to quadratic",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["1.4"],
            },
        ),
    ]

    u0: Annotated[
        float,
        Field(
            default=2.8,
            description="Control for redescending Huber regression weights.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2.8"],
            },
        ),
    ]

    tolerance: Annotated[
        float,
        Field(
            default=0.005,
            description="Control for convergence of RME algorithm.  Lower means more iterations",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["0.005"],
            },
        ),
    ]

    verbosity: Annotated[
        int,
        Field(
            default=1,
            description="Control for logging messages during regression -- Higher means more messages",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["1"],
            },
        ),
    ]
