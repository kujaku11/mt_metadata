# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Value(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="name of value estimate",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["tx"],
            },
        ),
    ]

    output: Annotated[
        str,
        Field(
            default="",
            description="output field component",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["ex"],
            },
        ),
    ]

    input: Annotated[
        str,
        Field(
            default="",
            description="input field component",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["hy"],
            },
        ),
    ]

    value: Annotated[
        str,
        Field(
            default="",
            description="value of the estimate",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["10.1 + 11j"],
            },
        ),
    ]
