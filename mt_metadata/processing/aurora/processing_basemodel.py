# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class BandSpecificationStyleEnum(str, Enum):
    EMTF = "EMTF"
    band_edges = "band_edges"


class Processing(MetadataBase):
    decimations: Annotated[
        str,
        Field(
            default="[]",
            items={"type": "string"},
            description="decimation levels",
            alias=None,
            json_schema_extra={
                "examples": "['0']",
                "units": None,
                "required": True,
            },
        ),
    ]

    band_specification_style: Annotated[
        BandSpecificationStyleEnum | None,
        Field(
            default=None,
            description="describes how bands were sourced",
            alias=None,
            json_schema_extra={
                "examples": "['EMTF']",
                "units": None,
                "required": False,
            },
        ),
    ]

    band_setup_file: Annotated[
        str | None,
        Field(
            default=None,
            description="the band setup file used to define bands",
            alias=None,
            json_schema_extra={
                "examples": "['/home/user/bs_test.cfg']",
                "units": None,
                "required": False,
            },
        ),
    ]

    id: Annotated[
        str,
        Field(
            default="",
            description="Configuration ID",
            alias=None,
            json_schema_extra={
                "examples": "['0']",
                "units": None,
                "required": True,
            },
        ),
    ]
