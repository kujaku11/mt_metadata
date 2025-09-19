# =====================================================
# Imports
# =====================================================
from typing import Annotated

from mt_metadata.common import (
    Instrument,
    Software,
)
from mt_metadata.timeseries import Battery, TimingSystem
from pydantic import Field


# =====================================================


class DataLogger(Instrument):
    timing_system: Annotated[
        TimingSystem,
        Field(
            default_factory=TimingSystem,
            description="Timing system of the data logger.",
            examples="TimingSystem()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
    firmware: Annotated[
        Software,
        Field(
            default_factory=Software,
            description="Firmware of the data logger.",
            examples="Software()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
    power_source: Annotated[
        Battery,
        Field(
            default_factory=Battery,
            description="Power source of the data logger.",
            examples="Battery()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
    data_storage: Annotated[
        Instrument,
        Field(
            default_factory=Instrument,
            description="Data storage of the data logger.",
            examples="Instrument()",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]
