# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Magnetic(MetadataBase):
    h_field_min.start: Annotated[
        float | None,
        Field(
            default=None,
            description="Minimum magnetic field strength at beginning of measurement.",
            examples="40345.1",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "nt",
                "required": False,
            },
        ),
    ] = None

    h_field_min.end: Annotated[
        float | None,
        Field(
            default=None,
            description="Minimum magnetic field strength at end of measurement.",
            examples="50453.2",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "nt",
                "required": False,
            },
        ),
    ] = None

    h_field_max.start: Annotated[
        float | None,
        Field(
            default=None,
            description="Maximum magnetic field strength at beginning of measurement.",
            examples="34565.2",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "nt",
                "required": False,
            },
        ),
    ] = None

    h_field_max.end: Annotated[
        float | None,
        Field(
            default=None,
            description="Maximum magnetic field strength at end of measurement.",
            examples="34526.1",
            type="number",
            alias=None,
            json_schema_extra={
                "units": "nt",
                "required": False,
            },
        ),
    ] = None
