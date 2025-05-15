# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Header(MetadataBase):
    title: Annotated[
        str,
        Field(
            default="",
            description="title of file",
            examples="BIRRP Version 5 basic mode output",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    station: Annotated[
        str,
        Field(
            default="",
            description="station name",
            examples="mt001",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    azimuth: Annotated[
        float,
        Field(
            default=0.0,
            description="rotation of full impedance tensor",
            examples="0",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]
