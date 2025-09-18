# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import YesNoEnum


# =====================================================


class DPlus(MetadataBase):
    use: Annotated[
        YesNoEnum,
        Field(
            default=YesNoEnum.no,
            description="Was D+ used to smooth the response",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["no"],
            },
        ),
    ]
