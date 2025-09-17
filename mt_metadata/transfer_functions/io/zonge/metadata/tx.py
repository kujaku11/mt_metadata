# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import StrEnumerationBase


# =====================================================
class TypeEnum(StrEnumerationBase):
    natural = "natural"
    controlled_source = "controlled source"


class Tx(MetadataBase):
    type: Annotated[
        TypeEnum,
        Field(
            default="natural",
            description="Type of EM source",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["natural"],
            },
        ),
    ]
