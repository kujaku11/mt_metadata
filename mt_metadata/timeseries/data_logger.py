# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.common import Instrument, Software
from mt_metadata.timeseries import Battery, TimingSystem


# =====================================================


class DataLogger(Instrument):
    timing_system: Annotated[
        TimingSystem,
        Field(
            default_factory=TimingSystem,
            description="Timing system of the data logger.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "TimingSystem()",
            },
        ),
    ]
    firmware: Annotated[
        Software,
        Field(
            default_factory=Software,
            description="Firmware of the data logger.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "Software()",
            },
        ),
    ]
    power_source: Annotated[
        Battery,
        Field(
            default_factory=Battery,
            description="Power source of the data logger.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "Battery()",
            },
        ),
    ]
    data_storage: Annotated[
        Instrument,
        Field(
            default_factory=Instrument,
            description="Data storage of the data logger.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "Instrument()",
            },
        ),
    ]
