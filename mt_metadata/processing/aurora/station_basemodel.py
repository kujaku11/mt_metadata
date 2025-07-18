# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Station(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="Station ID",
            alias=None,
            json_schema_extra={
                "examples": "['mt001']",
                "units": None,
                "required": True,
            },
        ),
    ]

    mth5_path: Annotated[
        str,
        Field(
            default="",
            description="full path to MTH5 file where the station data is contained",
            alias=None,
            json_schema_extra={
                "examples": "['/home/mt/experiment_01.h5']",
                "units": None,
                "required": True,
            },
        ),
    ]

    remote: Annotated[
        bool,
        Field(
            default=False,
            description="remote station (True) or local station (False)",
            alias=None,
            json_schema_extra={
                "examples": "['False']",
                "units": None,
                "required": True,
            },
        ),
    ]

    runs: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="List of runs to process",
            alias=None,
            json_schema_extra={
                "examples": "['001']",
                "units": None,
                "required": True,
            },
        ),
    ]
