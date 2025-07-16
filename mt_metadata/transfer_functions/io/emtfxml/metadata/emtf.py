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
        str,
        Field(
            default="",
            description="description of what is in the file; default is magnetotelluric transfer functions",
            examples=["Magnetotelluric Transfer Functions"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    product_id: Annotated[
        str,
        Field(
            default="",
            description="ID given as the archive ID of the station",
            examples=["USMTArray.NVS11.2020"],
            alias=None,
            pattern="^[a-zA-Z0-9._]*$",
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    tags: Annotated[
        str,
        Field(
            default="",
            description="tags that help describe the data",
            examples=["impedance, induction vectors"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    sub_type: Annotated[
        DataTypeEnum,
        Field(
            default="MT_TF",
            description="subject data type",
            examples=["MT_TF"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    notes: Annotated[
        str | None,
        Field(
            default=None,
            description="any notes applicable to the user on data present in the file",
            examples=["these are notes"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
