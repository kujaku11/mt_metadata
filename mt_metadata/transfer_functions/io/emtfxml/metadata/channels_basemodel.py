# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.utils.units import get_unit_object


# =====================================================
class Channels(MetadataBase):
    ref: Annotated[
        str,
        Field(
            default="",
            description="reference to the site name",
            examples="site",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    units: Annotated[
        str,
        Field(
            default="",
            description="units of the distance coordinates",
            examples="site",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("units", mode="before")
    @classmethod
    def validate_units(cls, value: str) -> str:
        if value in [None, ""]:
            return ""
        try:
            unit_object = get_unit_object(value)
            return unit_object.name
        except ValueError as error:
            raise KeyError(error)
        except KeyError as error:
            raise KeyError(error)
