# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Electric(MetadataBase):
    dipole_length: Annotated[
        float,
        Field(
            default=0.0,
            description="Length of the dipole as measured in a straight line from electrode to electrode.",
            examples="55.25",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    contact_resistance.start: Annotated[
        float | None,
        Field(
            default=None,
            type="number",
            items={"type": "number"},
            description="Starting contact resistance; if more than one measurement input as a list of number [1 2 3 ...].",
            examples='"[1.2, 1.4]"',
            alias=None,
            json_schema_extra={
                "units": "ohms",
                "required": False,
            },
        ),
    ] = None

    contact_resistance.end: Annotated[
        float | None,
        Field(
            default=None,
            type="number",
            items={"type": "number"},
            description="Ending contact resistance; if more than one measurement input as a list of number [1 2 3 ...].",
            examples='"[1.5, 1.8]"',
            alias=None,
            json_schema_extra={
                "units": "ohms",
                "required": False,
            },
        ),
    ] = None

    ac.start: Annotated[
        float | None,
        Field(
            default=None,
            description="Starting AC value; if more than one measurement input as a list of number [1 2 3 ...].",
            examples='"[52.1, 55.8]"',
            type="number",
            alias=None,
            json_schema_extra={
                "units": "volts",
                "required": False,
            },
        ),
    ] = None

    ac.end: Annotated[
        float | None,
        Field(
            default=None,
            description="Ending AC value; if more than one measurement input as a list of number [1 2 3 ...].",
            examples='"[45.3, 49.5]"',
            type="number",
            alias=None,
            json_schema_extra={
                "units": "volts",
                "required": False,
            },
        ),
    ] = None

    dc.start: Annotated[
        float | None,
        Field(
            default=None,
            description="Starting DC value; if more than one measurement input as a list of number [1 2 3 ...].",
            examples="1.1",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "volts",
                "required": False,
            },
        ),
    ] = None

    dc.end: Annotated[
        float | None,
        Field(
            default=None,
            description="Ending DC value; if more than one measurement input as a list of number [1 2 3 ...].",
            examples="1.5",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "volts",
                "required": False,
            },
        ),
    ] = None
