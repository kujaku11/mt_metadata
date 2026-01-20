# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import computed_field, Field, field_validator, PrivateAttr

from mt_metadata.base import MetadataBase

# =====================================================


class HMeasurement(MetadataBase):
    id: Annotated[
        float | str | None,
        Field(
            default=0.0,
            description="Channel number, could be location.channel_number.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["1"],
            },
        ),
    ]

    chtype: Annotated[
        str,
        Field(
            default="",
            description="channel type, should start with an 'h' or 'b'",
            alias=None,
            pattern=r"^(RR|rr|[hHbB])[a-zA-Z0-9_]+$",
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["hx"],
            },
        ),
    ]

    x: Annotated[
        float,
        Field(
            default=0.0,
            description="location of sensor relative center point in north direction",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
                "examples": ["100.0"],
            },
        ),
    ]

    y: Annotated[
        float,
        Field(
            default=0.0,
            description="location of sensor relative center point in east direction",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
                "examples": ["100.0"],
            },
        ),
    ]

    z: Annotated[
        float,
        Field(
            default=0.0,
            description="location of sensor relative center point in depth",
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": True,
                "examples": ["100.0"],
            },
        ),
    ]

    azm: Annotated[
        float,
        Field(
            default=0.0,
            description="orientation of the sensor relative to coordinate system, clockwise positive.",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
                "examples": ["100.0"],
            },
        ),
    ]

    dip: Annotated[
        float,
        Field(
            default=0.0,
            description="orientation of the sensor relative to horizontal = 0",
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
                "examples": ["100.0"],
            },
        ),
    ]

    acqchan: Annotated[
        str,
        Field(
            default="",
            description="description of acquired channel",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["100.0"],
            },
        ),
    ]

    _fmt_dict: dict[str, str] = PrivateAttr(
        default={
            "id": "<",
            "chtype": "<",
            "x": "<.2f",
            "y": "<.2f",
            "z": "<.2f",
            "azm": "<.2f",
            "dip": "<.2f",
            "acqchan": "<",
        }
    )

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, value: float | str | None) -> float:
        """Ensure id is a float or None, convert if necessary"""
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                raise ValueError("id must be a number or convertible to float")
        elif not isinstance(value, (float, int, type(None))):
            raise TypeError("id must be a number or None")
        if value is None:
            value = 0.0  # Default to 0.0 if None
        return value

    def __str__(self):
        return "\n".join([f"{k} = {v}" for k, v in self.to_dict(single=True).items()])

    def __repr__(self):
        return self.__str__()

    @computed_field
    @property
    def channel_number(self) -> int:
        """Extract channel number from acqchan."""
        if self.acqchan is not None:
            if not isinstance(self.acqchan, (int, float)):
                try:
                    return int("".join(i for i in self.acqchan if i.isdigit()))
                except (IndexError, ValueError):
                    return 0
            return int(self.acqchan)
        return 0

    def write_meas_line(self):
        """
        write string
        :return: DESCRIPTION
        :rtype: TYPE

        """

        line = [">hmeas".upper()]

        for mkey, mfmt in self._fmt_dict.items():
            try:
                line.append(f"{mkey.upper()}={getattr(self, mkey):{mfmt}}")
            except (ValueError, TypeError):
                line.append(f"{mkey.upper()}={0.0:{mfmt}}")

        return f"{' '.join(line)}\n"
