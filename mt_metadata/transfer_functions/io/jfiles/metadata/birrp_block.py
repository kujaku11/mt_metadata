# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator

from mt_metadata.base import MetadataBase


# =====================================================
class BirrpBlock(MetadataBase):
    filnam: Annotated[
        str,
        Field(
            default="",
            description="File name of data block",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["hx.dat"],
            },
        ),
    ]

    nskip: Annotated[
        int,
        Field(
            default=None,
            description="number of points to skip",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["0"],
            },
        ),
    ]

    nread: Annotated[
        int,
        Field(
            default=None,
            description="number of points to read",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["10000"],
            },
        ),
    ]

    ncomp: Annotated[
        int,
        Field(
            default=0,
            description="number of components in file",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["4"],
            },
        ),
    ]

    indices: Annotated[
        list[int] | int | str,
        Field(
            default_factory=list,
            description="index values to use",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["[1, 2]"],
            },
        ),
    ]

    @field_validator("indices", mode="before")
    @classmethod
    def validate_indices(cls, value):
        """Ensure indices is a list of integers or a single integer."""
        # Handle None or empty values
        if value is None:
            return []

        # Handle float values (convert to int first)
        if isinstance(value, float):
            return [int(value)]

        if isinstance(value, str):
            # If it's a string, try to parse it as a list
            try:
                return [
                    int(i) for i in value.strip("[]").split(",") if i.strip().isdigit()
                ]
            except ValueError:
                raise ValueError(f"Invalid string format for indices: {value}")
        if isinstance(value, int):
            return [value]
        if isinstance(value, list):
            try:
                return [int(i) for i in value]
            except ValueError:
                raise ValueError(f"Invalid list format for indices: {value}")

        # If we get here, the type is unsupported
        raise ValueError(f"Unsupported type for indices: {type(value)}, value: {value}")
