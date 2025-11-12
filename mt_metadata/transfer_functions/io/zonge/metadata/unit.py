# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common.units import get_unit_object


# =====================================================


class Unit(MetadataBase):
    length: Annotated[
        str,
        Field(
            default="m",
            description="Type of smoothing for phase slope algorithm",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["m"],
            },
        ),
    ]

    e: Annotated[
        str,
        Field(
            default="mV/km",
            description="Units for the electric field",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["mV/km"],
            },
        ),
    ]

    b: Annotated[
        str,
        Field(
            default="nT",
            description="Units for the magnetic field",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["nT"],
            },
        ),
    ]

    @field_validator("length", "b", "e", mode="before")
    @classmethod
    def validate_units(cls, value: str, info: ValidationInfo) -> str:
        """
        validate units base on input string will return the long name

        Parameters
        ----------
        value : units string
            unit string separated by either '/' for division or ' ' for
            multiplication.  Or 'per' and ' ', respectively
        info : ValidationInfo
            _description_

        Returns
        -------
        str
            return the long descriptive name of the unit. For example 'kilometers'.
        """
        if value in [None, ""]:
            return ""
        try:
            unit_object = get_unit_object(value)
            return unit_object.name
        except ValueError as error:
            raise KeyError(error)
        except KeyError as error:
            raise KeyError(error)
