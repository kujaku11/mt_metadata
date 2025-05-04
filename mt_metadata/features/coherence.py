# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 13:39:39 2025

@author: jpeacock

This module contains the simplest coherence feature.
The feature is computed with scipy.signal coherence.

The Window object is used to taper the time series before FFT.

Development Notes:
Coherence extends the BaseFeature class.  This means that it should have
all the attrs that a BaseFeature instance does, as well as its own unique ones.
When setting up the attr_dict, one is confronted with the question of adding
BaseFeatures attrs one of two ways:
- To add the features directly, use:
attr_dict.add_dict(get_schema("base_feature", SCHEMA_FN_PATHS))
{
    "coherence": {
        "ch1": "ex",
        "ch2": "hy",
        "description": "Simple coherence between two channels derived directly from scipy.signal.coherence applied to time domain data",
        "domain": "frequency",
        "name": "coherence",
        "window.clock_zero_type": "ignore",
        "window.normalized": true,
        "window.num_samples": 512,
        "window.overlap": 128,
        "window.type": "hamming"
    }
}
- To nest the features use:
attr_dict.add_dict(BaseFeature()._attr_dict, "base_feature")
{
    "coherence": {
        "base_feature.description": null,
        "base_feature.domain": null,
        "base_feature.name": null,
        "ch1": "ex",
        "ch2": "hy",
        "window.clock_zero_type": "ignore",
        "window.normalized": true,
        "window.num_samples": 512,
        "window.overlap": 128,
        "window.type": "hamming"
    }
}

"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema
from mt_metadata.transfer_functions.processing.window import Window
from .base_feature import BaseFeature
from .standards import SCHEMA_FN_PATHS
from typing import Tuple

import numpy as np
import scipy.signal as ssig

# =============================================================================
attr_dict = get_schema("coherence", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("base_feature", SCHEMA_FN_PATHS))
# attr_dict.add_dict(BaseFeature()._attr_dict, "base_feature")
attr_dict.add_dict(Window()._attr_dict, "window")

# Set the defaults for the coherence calculation parameters to scipys defaults
DEFAULT_SCIPY_WINDOW = Window()
DEFAULT_SCIPY_WINDOW.type = "hann"
DEFAULT_SCIPY_WINDOW.num_samples = 256
DEFAULT_SCIPY_WINDOW.overlap = 128


# =============================================================================
class Coherence(BaseFeature):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.window = Window()
        self._detrend = None
        BaseFeature.__init__(self, **kwargs)  # attr_dict=attr_dict,
        self._attr_dict = attr_dict
        self.name = "coherence"
        self.domain = "frequency"
        self.description = "Simple coherence between two channels derived " \
                           "directly from scipy.signal.coherence applied to " \
                           "time domain data"
        self.window = DEFAULT_SCIPY_WINDOW
        # self._attr_dict = attr_dict

    @property
    def detrend(self):
        return self._detrend

    @detrend.setter
    def detrend(self, value):
        self._detrend = value

    @property
    def channel_pair_str(self) -> str:
        return f"{self.ch1}, {self.ch2}"


    def compute(
        self,
        ts_1: np.ndarray,
        ts_2: np.ndarray
    ) -> Tuple[np.ndarray]:
        """
            Calls scipy's coherence function.
            TODO: Consider making this return an xarray indexed by frequency.

            Parameters
            ----------
            ts_1
            ts_2

            Returns
            -------

        """
        frequencies, coh_squared = ssig.coherence(
            ts_1,
            ts_2,
            window=self.window.type,
            nperseg=self.window.num_samples,
            noverlap=self.window.overlap,
            detrend=self.detrend,
        )
        return frequencies, coh_squared

