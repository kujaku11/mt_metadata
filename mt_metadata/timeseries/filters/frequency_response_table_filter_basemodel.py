# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

import numpy as np
from scipy.interpolate import interp1d

from pydantic import Field

from mt_metadata.base import MetadataBase
from mt_metadata.timeseries.filters import FilterBase
from mt_metadata.timeseries.filters.filter_base import get_base_obspy_mapping

try:
    from obspy.core.inventory.response import (
        ResponseListResponseStage,
        ResponseListElement,
    )
except ImportError:
    ResponseListResponseStage = ResponseListElement = None


# =====================================================
class InstrumentTypeEnum(str, Enum):
    other = "other"


class FrequencyResponseTableFilter(FilterBase):
    frequencies: Annotated[
        np.ndarray | list[float],
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
        ),
    ]

    amplitudes: Annotated[
        np.ndarray | list[float],
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
        ),
    ]

    phases: Annotated[
        np.ndarray | list[float],
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
        ),
    ]

    def make_obspy_mapping(self):
        mapping = get_base_obspy_mapping()
        mapping["amplitudes"] = "_empirical_amplitudes"
        mapping["frequencies"] = "_empirical_frequencies"
        mapping["phases"] = "_empirical_phases"
        return mapping
