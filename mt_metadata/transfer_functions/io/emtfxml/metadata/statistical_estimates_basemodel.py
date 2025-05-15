# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class StatisticalEstimates(MetadataBase):
    estimates_list: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="list of statistical estimates",
            examples="[var cov]",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
