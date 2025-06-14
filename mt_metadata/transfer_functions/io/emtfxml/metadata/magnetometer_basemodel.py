# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Magnetometer(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="instrument ID number can be serial number or a designated ID",
            examples=["mt01"],
            alias=["serial"],
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    manufacturer: Annotated[
        str,
        Field(
            default="",
            description="who manufactured the instrument",
            examples=["mt gurus"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    type: Annotated[
        str,
        Field(
            default="",
            description="instrument type",
            examples=["broadband 32-bit"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    model: Annotated[
        str | None,
        Field(
            default=None,
            description="model version of the instrument",
            examples=["falcon5"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    name: Annotated[
        str | None,
        Field(
            default=None,
            description="Name of the model of the instrument",
            examples=["falcon5"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    settings: Annotated[
        str | None,
        Field(
            default=None,
            description="Any settings for the instrument",
            examples=["notch filter applied"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
