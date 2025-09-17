# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import YesNoEnum


# =====================================================


class Auto(MetadataBase):
    phase_flip: Annotated[
        YesNoEnum,
        Field(
            default="yes",
            description="Was phase automatically flipped in processing",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["yes"],
            },
        ),
    ]
