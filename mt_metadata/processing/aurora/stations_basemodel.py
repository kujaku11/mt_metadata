# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.processing.aurora.station_basemodel import Station


# =====================================================
class Stations(MetadataBase):
    remote: Annotated[
        list[Station],
        Field(
            default_factory=list,
            description="list of remote sites",
            examples=["10"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    local: Annotated[
        Station,
        Field(
            default_factory=Station,  # type: ignore
            description="local site",
            examples=["10"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
