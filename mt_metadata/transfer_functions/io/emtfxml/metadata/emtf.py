# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import DataTypeEnum


# =====================================================


class EMTF(MetadataBase):
    description: Annotated[
        str | None,
        Field(
            default="",
            description="description of what is in the file; default is magnetotelluric transfer functions",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["Magnetotelluric Transfer Functions"],
            },
        ),
    ]

    product_id: Annotated[
        str | None,
        Field(
            default="",
            description="ID given as the archive ID of the station",
            alias=None,
            pattern="^[a-zA-Z0-9._-]*$",
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["USMTArray.NVS11.2020"],
            },
        ),
    ]

    tags: Annotated[
        str | None,
        Field(
            default="",
            description="tags that help describe the data",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["impedance, induction vectors"],
            },
        ),
    ]

    sub_type: Annotated[
        DataTypeEnum,
        Field(
            default=DataTypeEnum.MT_TF,
            description="subject data type",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["MT_TF"],
            },
        ),
    ]

    notes: Annotated[
        str | None,
        Field(
            default=None,
            description="any notes applicable to the user on data present in the file",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["these are notes"],
            },
        ),
    ]
