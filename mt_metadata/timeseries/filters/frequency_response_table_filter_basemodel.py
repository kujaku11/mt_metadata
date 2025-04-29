# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase


# =====================================================
class InstrumentTypeEnum(str, Enum):
    other = "other"


class FrequencyResponseTableFilter(MetadataBase):
    frequencies: Annotated[
        float,
        Field(
            default=[],
            items={"type": "number"},
            description="The frequencies at which a calibration of the filter were performed.",
            examples='"[-0.0001., 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.001, ... 1, 2, 5, 10]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
            {TAB},
        ),
    ]

    amplitudes: Annotated[
        float,
        Field(
            default=[],
            items={"type": "number"},
            description="The amplitudes for each calibration frequency.",
            examples='"[1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 1.0, ... 1.0, 1.0, 1.0, 1.0]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
            {TAB},
        ),
    ]

    phases: Annotated[
        float,
        Field(
            default=[],
            items={"type": "number"},
            description="The phases for each calibration frequency.",
            examples='"[-90, -90, -88, -80, -60, -30, 30, ... 50.0, 90.0, 90.0, 90.0]"',
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
            {TAB},
        ),
    ]

    instrument_type: Annotated[
        InstrumentTypeEnum,
        Field(
            default="",
            description="The type of instrument the FAP table is associated with. ",
            examples="fluxgate magnetometer",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
            {TAB},
        ),
    ]
