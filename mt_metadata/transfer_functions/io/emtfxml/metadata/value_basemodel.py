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
            examples=["tx"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    output: Annotated[
        str,
        Field(
            default="",
            description="output field component",
            examples=["ex"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    input: Annotated[
        str,
        Field(
            default="",
            description="input field component",
            examples=["hy"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    value: Annotated[
        str,
        Field(
            default="",
            description="value of the estimate",
            examples=["10.1 + 11j"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
