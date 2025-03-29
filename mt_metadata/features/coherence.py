# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 13:39:39 2025

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from ..transfer_functions.processing.window import Window
from typing import Tuple

import numpy as np
import scipy.signal as ssig

# =============================================================================
attr_dict = get_schema("feature", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("coherence", SCHEMA_FN_PATHS), None)
attr_dict.add_dict(Window()._attr_dict, "window")

# Set the defaults for the coherence calculation parameters to scipys defaults
DEFAULT_SCIPY_WINDOW = Window()
DEFAULT_SCIPY_WINDOW.type = "hann"
DEFAULT_SCIPY_WINDOW.num_samples = 256
DEFAULT_SCIPY_WINDOW.overlap = 128


# =============================================================================
class Coherence(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.window = Window()

        super().__init__(attr_dict=attr_dict, **kwargs)

        self.name = "coherence"
        self.domain = "frequency"
        self.description = "Simple coherence between two channels derived " \
                           "directly from scipy.signal.coherence applied to " \
                           "time domain data"
        self.window = DEFAULT_SCIPY_WINDOW

    @property
    def channel_pair_str(self) -> str:
        return f"{self.channel_1}, {self.channel_2}"


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

