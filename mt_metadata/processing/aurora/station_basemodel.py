# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Station(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="Station ID",
            examples=["mt001"],
            alias=None,
            json_schema_extra={
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
            examples=["/home/mt/experiment_01.h5"],
            alias=None,
            json_schema_extra={
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
            examples=["False"],
            alias=None,
            json_schema_extra={
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
            examples=["001"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
