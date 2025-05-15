# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class UseEnum(str, Enum):
    no = "no"
    yes = "yes"


class DPlus(MetadataBase):
    use: Annotated[
        UseEnum,
        Field(
            default="no",
            description="Was D+ used to smooth the response",
            examples="no",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
