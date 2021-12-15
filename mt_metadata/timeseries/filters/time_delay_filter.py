# -*- coding: utf-8 -*-
"""
.. py:module:: Time Delay Filter
    :synopsis: Time delay filter

.. codeauthor:: Jared Peacock <jpeacock@usgs.gov>
.. codeauthor:: Karl Kappler

"""

import copy
import numpy as np
from obspy.core import inventory

from mt_metadata.base import get_schema
from mt_metadata.timeseries.filters.filter_base import FilterBase
from mt_metadata.timeseries.filters.filter_base import OBSPY_MAPPING
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS

obspy_mapping = copy.deepcopy(OBSPY_MAPPING)
obspy_mapping["decimation_delay"] = "delay"
# =============================================================================
attr_dict = get_schema("filter_base", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("time_delay_filter", SCHEMA_FN_PATHS))
# =============================================================================


class TimeDelayFilter(FilterBase):
    def __init__(self, **kwargs):
        super().__init__()

        super(FilterBase, self).__init__(attr_dict=attr_dict, **kwargs)
        if self.gain == 0.0:
            self.gain = 1.0
        self.type = "time delay"
        self.obspy_mapping = obspy_mapping

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
            self.units_in,
            self.units_out,
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
            input_units_description=self._units_in_obj.name,
            output_units_description=self._units_out_obj.name,
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
        self.logger.debug(
            "USING FREQUENCY DOMAIN VERSION OF TIME DELAY FILTER NOT RECOMMENDED FOR MT PROCESSING"
        )

        if isinstance(frequencies, (float, int)):
            frequencies = np.array([frequencies])
        w = 2 * np.pi * frequencies
        exponent = -1.0j * w * self.delay
        spectral_shift_multiplier = np.exp(exponent)
        return spectral_shift_multiplier
