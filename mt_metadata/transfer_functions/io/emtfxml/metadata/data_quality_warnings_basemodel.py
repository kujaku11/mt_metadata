# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class DataQualityWarnings(MetadataBase):
    flag: Annotated[
        int | None,
        Field(
            default=None,
            description="Flag for data quality",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
