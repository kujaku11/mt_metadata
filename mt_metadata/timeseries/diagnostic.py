# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Diagnostic(MetadataBase):
    end: Annotated[
        float | None,
        Field(
            default=None,
            description="Ending value of a diagnostic measurement.",
            examples="10",
            type="number",
            alias=None,
            json_schema_extra={
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
            examples="12.3",
            type="number",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None
