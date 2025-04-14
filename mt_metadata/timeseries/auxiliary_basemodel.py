# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.base import MetadataBase
from pydantic import Field


# =====================================================
class ComponentEnum(str, Enum):
    Ex = "Ex"
    Ey = "Ey"
    Hx = "Hx"
    Hy = "Hy"
    Hz = "Hz"
    T = "T"
    Battery = "Battery"
    other = "other"


class UnitsEnum(str, Enum):
    metric = "metric"
    celsius = "celsius"
    meters = "meters"
    degrees = "degrees"
    kilograms = "kilograms"
    other = "other"


class Auxiliary(MetadataBase):
    channel_number: Annotated[
        int,
        Field(
            default=None,
            description="Channel number on the data logger.",
            examples="1",
            type="integer",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    comments: Annotated[
        str | None,
        Field(
            default=None,
            description="Any comments about the channel.",
            examples="ambient air temperature was chilly, ice on cables",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ] = None

    component: Annotated[
        ComponentEnum,
        Field(
            default="",
            description="Name of the component measured, can be uppercase and/or lowercase.  For now electric channels should start with an 'e' and magnetic channels start with an 'h', followed by the component. If there are multiples of the same channel the name could include an integer.  {type}{component}{number} --> Ex01.",
            examples="T",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    measurement_azimuth: Annotated[
        float,
        Field(
            default=0.0,
            description="Azimuth of channel in measurement coordinate system spcified in station.orientation.reference_frame.  Default reference from is a geographic right-handed coordinate system with north=0, east=90, vertical=+ downward.",
            examples="0",
            type="number",
            alias=["azimuth"],
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    measurement_tilt: Annotated[
        float,
        Field(
            default=0.0,
            description="Tilt of channel in measurement coordinate system spcified in station.orientation.reference_frame.  Default reference from is a geographic right-handed coordinate system with north=0, east=90, vertical=+ downward.",
            examples="0",
            type="number",
            alias=["dip"],
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    sample_rate: Annotated[
        float,
        Field(
            default=0.0,
            description="Digital sample rate",
            examples="8",
            type="number",
            alias=["sampling_rate"],
            json_schema_extra={
                "units": "samples per second",
                "required": True,
            },
        ),
    ]

    translated_azimuth: Annotated[
        float | None,
        Field(
            default=None,
            description="Azimuth of channel in translated coordinate system, this should only be used for derived product.  For instance if you collected your data in geomagnetic coordinates and then translated them to geographic coordinates you would set measurement_azimuth=0, translated_azimuth=-12.5 for a declination angle of N12.5E.",
            examples="0",
            type="number",
            alias=["azimuth"],
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ] = None

    translated_tilt: Annotated[
        float | None,
        Field(
            default=None,
            description="Tilt of channel in translated coordinate system, this should only be used for derived product.  For instance if you collected your data in a tripod you would set measurement_tilt=45, translated_tilt=0 for a vertical component.",
            examples="0",
            type="number",
            alias=["dip"],
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ] = None

    type: Annotated[
        str,
        Field(
            default=auxiliary,
            description="Data type for the channel, should be a descriptive word that a user can understand.",
            examples="temperature",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    units: Annotated[
        UnitsEnum,
        Field(
            default="",
            description="Units of the data, should be in SI units and represented as the full name of the unit all lowercase.  If a complex unit use 'per' and '-'.",
            examples="celsius",
            type="string",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
