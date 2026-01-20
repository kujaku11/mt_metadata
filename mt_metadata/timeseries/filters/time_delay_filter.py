# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
from loguru import logger
from pydantic import Field, field_validator, PrivateAttr, ValidationInfo

from mt_metadata.base.helpers import requires
from mt_metadata.timeseries.filters import FilterBase, get_base_obspy_mapping


try:
    from obspy.core import inventory
except ImportError:
    inventory = None


# =====================================================
class TimeDelayFilter(FilterBase):
    _filter_type: str = PrivateAttr("time delay")
    type: Annotated[
        str,
        Field(
            default="time delay",
            description="Type of filter.  Must be 'fir'",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "time delay",
            },
        ),
    ]
    delay: Annotated[
        float,
        Field(
            default=0.0,
            description="The delay interval of the filter. This should be a single number.",
            alias=None,
            json_schema_extra={
                "units": "second",
                "required": True,
                "examples": "-0.201",
            },
        ),
    ]

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, value, info: ValidationInfo) -> str:
        """
        Validate that the type of filter is set to "time delay"
        """
        if value not in ["time delay", "time_delay"]:
            logger.warning(
                f"Filter type is set to {value}, but should be 'time delay' for TimeDelayFilter."
            )
        return "time delay"

    def make_obspy_mapping(self):
        mapping = get_base_obspy_mapping()
        mapping["decimation_delay"] = "delay"
        return mapping

    @requires(obspy=inventory)
    def to_obspy(self, stage_number=1, sample_rate=1, normalization_frequency=0):
        """
        Convert to an obspy stage

        :param stage_number: sequential stage number, defaults to 1
        :type stage_number: integer, optional
        :param normalization_frequency: Normalization frequency, defaults to 1
        :type normalization_frequency: float, optional
        :param sample_rate: sample rate, defaults to 1
        :type sample_rate: float, optional
        :return: Obspy stage filter
        :rtype: :class:`obspy.core.inventory.CoefficientsTypeResponseStage`

        """

        stage = inventory.CoefficientsTypeResponseStage(
            stage_number,
            self.gain,
            normalization_frequency,
            self.units_in_object.symbol,
            self.units_out_object.symbol,
            "DIGITAL",
            name=self.name,
            decimation_input_sample_rate=sample_rate,
            decimation_factor=1,
            decimation_offset=0,
            decimation_delay=self.delay,
            decimation_correction=0,
            numerator=[1],
            denominator=[],
            description=self.get_filter_description(),
            input_units_description=self.units_in_object.name,
            output_units_description=self.units_out_object.name,
        )

        return stage

    def complex_response(self, frequencies, **kwargs):
        """
        Computes complex response for given frequency range
        :param frequencies: array of frequencies to estimate the response
        :type frequencies: np.ndarray

        :return: complex response
        :rtype: np.ndarray

        """
        logger.debug(
            "USING FREQUENCY DOMAIN VERSION OF TIME DELAY FILTER NOT RECOMMENDED FOR MT PROCESSING"
        )

        if isinstance(frequencies, (float, int)):
            frequencies = np.array([frequencies])
        w = 2 * np.pi * frequencies
        exponent = -1.0j * w * self.delay
        spectral_shift_multiplier = np.exp(exponent)
        return spectral_shift_multiplier
