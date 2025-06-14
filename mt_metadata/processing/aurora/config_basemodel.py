# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Config(MetadataBase):
    config_id: Annotated[
        str,
        Field(
            default="",
            description="ID of the configuration setup. ",
            examples="CAS04-01",
            alias=None,
            json_schema_extra={
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
            examples="14.23",
            alias=["lon", "long"],
            json_schema_extra={
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
            examples="123.4",
            alias=["elev"],
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]
