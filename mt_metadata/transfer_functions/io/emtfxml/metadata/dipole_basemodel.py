# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class Dipole(MetadataBase):
    manfacturer: Annotated[
        str | None,
        Field(
            default=None,
            description="Name of the manufacturer of the instrument",
            examples=["MT Gurus"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    length: Annotated[
        float | None,
        Field(
            default=None,
            description="Dipole length",
            examples=["10"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    azimuth: Annotated[
        float | None,
        Field(
            default=None,
            description="Azimuth of the dipole relative to coordinate system",
            examples=["90"],
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    name: Annotated[
        str | None,
        Field(
            default=None,
            description="Name of the dipole",
            examples=["ex"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    type: Annotated[
        str | None,
        Field(
            default=None,
            description="type of dipole",
            examples=["wire"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
