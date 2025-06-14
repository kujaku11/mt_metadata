# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Electric(MetadataBase):
    name: Annotated[
        str,
        Field(
            default="",
            description="Name of the channel",
            examples=["hx"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    orientation: Annotated[
        float,
        Field(
            default=0.0,
            description="orientation angle relative to geographic north",
            examples=["11.9"],
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    x: Annotated[
        float,
        Field(
            default=0.0,
            description="location of negative sensor relative center point in north direction",
            examples=["100.0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    x2: Annotated[
        float,
        Field(
            default=0.0,
            description="location of positive sensor relative center point in north direction",
            examples=["100.0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    y: Annotated[
        float,
        Field(
            default=0.0,
            description="location of negative sensor relative center point in east direction",
            examples=["100.0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    y2: Annotated[
        float,
        Field(
            default=0.0,
            description="location of positive sensor relative center point in east direction",
            examples=["100.0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    z: Annotated[
        float,
        Field(
            default=0.0,
            description="location of negative sensor relative center point in depth",
            examples=["100.0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]

    z2: Annotated[
        float,
        Field(
            default=0.0,
            description="location of positive sensor relative center point in depth",
            examples=["100.0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
            },
        ),
    ]
