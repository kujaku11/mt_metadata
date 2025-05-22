# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class DataTypes(MetadataBase):
    data_types_list: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="list of data types",
            examples=["[Z T]"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
