# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class PoleZeroFilter(MetadataBase):
    poles: Annotated[
        float,
        Field(
            default=[],
            items={"type": "number"},
            description="The complex-valued poles associated with the filter response.",
            examples='"[-1/4., -0.1+j*0.3, -0.1-j*0.3]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
            {TAB},
        ),
    ]

    zeros: Annotated[
        float,
        Field(
            default=[],
            items={"type": "number"},
            description="The complex-valued zeros associated with the filter response.",
            examples='"[0.0, ]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
            {TAB},
        ),
    ]

    normalization_factor: Annotated[
        float,
        Field(
            default=1.0,
            description="The scale factor to apply to the monic response.",
            examples='"[-1000.1]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
            {TAB},
        ),
    ]
