# =====================================================
# Imports
# =====================================================
from typing import Annotated
from loguru import logger

import numpy as np
from scipy.interpolate import interp1d

from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.timeseries.filters import FilterBase, get_base_obspy_mapping
from mt_metadata.base.helpers import requires, object_to_array

try:
    from obspy.core.inventory.response import (
        ResponseListResponseStage,
        ResponseListElement,
    )
except ImportError:
    ResponseListResponseStage = ResponseListElement = None


# =====================================================


class FrequencyResponseTableFilter(FilterBase):
    _filter_type: str = "fap"
    type: Annotated[
        str,
        Field(
            default="fap",
            description="Type of filter.  Must be 'fap' or 'frequency amplitude table'",
            examples="fap",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
    frequencies: Annotated[
        np.ndarray | list[float],
        Field(
            default_factory=lambda: np.empty(0, dtype=float),
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
            default_factory=lambda: np.empty(0, dtype=float),
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
            default_factory=lambda: np.empty(0, dtype=float),
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
        str,
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
        mapping["amplitudes"] = "amplitudes"
        mapping["frequencies"] = "frequencies"
        mapping["phases"] = "phases"
        return mapping

    @field_validator("frequencies", "amplitudes", mode="before")
    @classmethod
    def validate_input_arrays(cls, value, info: ValidationInfo) -> np.ndarray:
        """
        Validate that the input is a list, tuple, or np.ndarray and convert to np.ndarray.
        """
        return object_to_array(value)

    @field_validator("phases", mode="before")
    @classmethod
    def validate_phases(cls, value, info: ValidationInfo) -> np.ndarray:
        """
        Validate that the input is a list, tuple, or np.ndarray and convert to np.ndarray.
        """
        value = object_to_array(value)
        if value.size > 0:
            if value.max() > 1000 * np.pi / 2:
                logger.warning(
                    "self.phases appear to be in milli radians attempting to convert to radians"
                )
                return value / 1000

            elif np.abs(value).max() > 6 * np.pi:
                logger.warning(
                    "self.phases appear to be in degrees attempting to convert to radians"
                )
                return np.deg2rad(value)

            else:
                return value
        return value

    @property
    def min_frequency(self):
        """

        :return: minimum frequency
        :rtype: float

        """
        if self.frequencies is None:
            return 0.0
        elif self.frequencies.size == 0:
            return 0.0
        return float(self.frequencies.min())

    @property
    def max_frequency(self):
        """

        :return: maximum frequency
        :rtype: float

        """
        if self.frequencies is None:
            return 0.0
        elif self.frequencies.size == 0:
            return 0.0
        return float(self.frequencies.max())

    @requires(obspy=(ResponseListResponseStage and ResponseListElement))
    def to_obspy(
        self,
        stage_number=1,
        normalization_frequency=1,
        sample_rate=1,
    ):
        """
        Convert to an obspy stage

        :param stage_number: sequential stage number, defaults to 1
        :type stage_number: integer, optional
        :param normalization_frequency: Normalization frequency, defaults to 1
        :type normalization_frequency: float, optional
        :param sample_rate: sample rate, defaults to 1
        :type sample_rate: float, optional
        :return: Obspy stage filter
        :rtype: :class:`obspy.core.inventory.ResponseListResponseStage`

        """
        response_elements = []
        for f, a, p in zip(self.frequencies, self.amplitudes, self.phases):
            element = ResponseListElement(f, a, p)
            response_elements.append(element)

        rs = ResponseListResponseStage(
            stage_number,
            self.gain,
            normalization_frequency,
            self.units_in_object.symbol,
            self.units_out_object.symbol,
            name=self.name,
            description=self.get_filter_description(),
            input_units_description=self.units_in_object.name,
            output_units_description=self.units_out_object.name,
            response_list_elements=response_elements,
        )

        return rs

    def complex_response(self, frequencies, interpolation_method="slinear"):
        """
        Computes complex response for given frequency range
        :param frequencies: array of frequencies to estimate the response
        :type frequencies: np.ndarray
        :return: complex response
        :rtype: np.ndarray

        """
        if np.min(frequencies) < self.min_frequency:
            # if there is a dc component skip it.
            if np.min(frequencies) != 0:
                logger.warning(
                    f"Extrapolating frequencies smaller ({np.min(frequencies)} Hz) "
                    f"than table frequencies ({self.min_frequency} Hz)."
                )
        if np.max(frequencies) > self.max_frequency:
            logger.warning(
                f"Extrapolating frequencies larger ({np.max(frequencies)} Hz) "
                f"than table frequencies ({self.max_frequency} Hz)."
            )

        phase_response = interp1d(
            self.frequencies,
            self.phases,
            kind=interpolation_method,
            fill_value="extrapolate",
        )

        amplitude_response = interp1d(
            self.frequencies,
            self.amplitudes,
            kind=interpolation_method,
            fill_value="extrapolate",
        )
        total_response_function = lambda f: amplitude_response(f) * np.exp(
            1.0j * phase_response(f)
        )

        return self.gain * total_response_function(frequencies)
