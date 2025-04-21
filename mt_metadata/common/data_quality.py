# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class DataQuality(MetadataBase):
    warnings: Annotated[
        str | None,
        Field(
            default=None,
            description="any warnings about the data that should be noted",
            examples="periodic pipeline noise",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    good_from_period: Annotated[
        float | None,
        Field(
            default=None,
            description="Data are good for periods larger than this number",
            examples="0.01",
            type="number",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    good_to_period: Annotated[
        float | None,
        Field(
            default=None,
            description="Data are good for periods smaller than this number",
            examples="1000",
            type="number",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    flag: Annotated[
        int | None,
        Field(
            default=None,
            description="Flag for data quality",
            examples="0",
            type="integer",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    comments: Annotated[
        str | None,
        Field(
            default=None,
            description="any comments about the data quality",
            examples="0",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None
