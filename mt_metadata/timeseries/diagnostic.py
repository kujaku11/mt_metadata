# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Diagnostic(MetadataBase):
    end: Annotated[
        float | None,
        Field(
            default=None,
            description="Ending value of a diagnostic measurement.",
            alias=None,
            json_schema_extra={
                "examples": "10",
                "type": "number",
                "units": None,
                "required": False,
            },
        ),
    ] = None

    start: Annotated[
        float | None,
        Field(
            default=None,
            description="Starting value of a diagnostic measurement.",
            alias=None,
            json_schema_extra={
                "examples": "12.3",
                "type": "number",
                "units": None,
                "required": False,
            },
        ),
    ] = None
