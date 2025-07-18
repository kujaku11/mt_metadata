# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class Config(MetadataBase):
    config_id: Annotated[
        str,
        Field(
            default="",
            description="ID of the configuration setup. ",
            alias=None,
            json_schema_extra={
                "examples": "['CAS04-01']",
                "units": None,
                "required": True,
            },
        ),
    ]

    longitude: Annotated[
        float,
        Field(
            default=0.0,
            description="Longitude of location in datum specified at survey level.",
            alias=["lon", "long"],
            json_schema_extra={
                "examples": "['14.23']",
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    elevation: Annotated[
        float,
        Field(
            default=0.0,
            description="Elevation of location in datum specified at survey level.",
            alias=["elev"],
            json_schema_extra={
                "examples": "['123.4']",
                "units": "meters",
                "required": True,
            },
        ),
    ]
