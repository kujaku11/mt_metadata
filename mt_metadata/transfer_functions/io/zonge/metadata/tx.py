# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class TypeEnum(str, Enum):
    natural = "natural"
    controlled_source = "controlled source"


class Tx(MetadataBase):
    type: Annotated[
        TypeEnum,
        Field(
            default="natural",
            description="Type of EM source",
            examples=["natural"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
