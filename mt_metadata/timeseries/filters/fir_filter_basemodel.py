# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class SymmetryEnum(str, Enum):
    NONE = "NONE"
    ODD = "ODD"
    EVEN = "EVEN"


class FirFilter(MetadataBase):
    coefficients: Annotated[
        float,
        Field(
            default=[],
            items={"type": "number"},
            description="The FIR coefficients associated with the filter stage response.",
            examples='"[0.25, 0.5, 0.25]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    decimation_factor: Annotated[
        int | None,
        Field(
            default=None,
            description="Downsample factor.",
            examples="16",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    decimation_input_sample_rate: Annotated[
        float | None,
        Field(
            default=None,
            description="Sample rate of FIR taps.",
            examples="2000.0",
            alias=None,
            json_schema_extra={
                "units": "samples per second",
                "required": False,
            },
        ),
    ]

    gain_frequency: Annotated[
        float,
        Field(
            default=0.0,
            description="Frequency of the reference gain, usually in passband.",
            examples="0.0",
            alias=None,
            json_schema_extra={
                "units": "hertz",
                "required": True,
            },
        ),
    ]

    symmetry: Annotated[
        SymmetryEnum,
        Field(
            default=NONE,
            description="Symmetry of FIR coefficients",
            examples="NONE",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
