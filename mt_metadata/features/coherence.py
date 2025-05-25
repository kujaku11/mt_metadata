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

Devlopment Notes:
    To specify a channel in the context of tf processing we need station and channel names.
    I have been fighting the use of `rx` and `ry` for several reasons, including that the [ex, ey, hx, hy, hz, rx, ry]
    convention forces the assumption that remote channels are remote magnetics, and are overly specific to the remote
    reference processing convention.
    Hoever, for a feature like this, it could seem to be a hassle to update the processing config with the station name all over the
    feature definations.  So, it seems that we should have a station field, and a channel field.
    If the user wishes to specify station and channel, fine.  If the user prefers the more general,
    but less well defined [ex, ey, hx, hy, hz, rx, ry] nomenclature, then we can ddeduce this for them.

"""

# =============================================================================
# Imports
# =============================================================================
from loguru import logger
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema
from mt_metadata.transfer_functions.processing.window import Window
from .base_feature import BaseFeature
from .standards import SCHEMA_FN_PATHS
from typing import Optional, Tuple

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
        self.station1 = ""
        self.station2 = ""
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

    def validate_station_ids(
        self,
        local_station_id: str,
        remote_station_id: Optional[str] = None
    ) -> None:
        """
        Make sure that ch1, ch2 are unambiguous.

        Ideally the station for each channel is specified, but if not,
        try deducing the channel.

        Parameters
        ----------
        local_station_id: str
            The name of the local station for a TF calculation
        remote_station_id: Optional[str]
            The name of the remote station for a TF calculation

        """

        # validate the station names:
        active_stations = [local_station_id]
        if remote_station_id:
            active_stations.append(remote_station_id)

        # if the feature has a station1, check that it is in the list of active stations
        if self.station1:  # not "" or None
            if self.station1 not in active_stations:
                msg = f"station1 not in expected stations -- setting to None"
                logger.warning(msg)
                self.station1 = None

        if self.station2:  # not "" or None
            if self.station2 not in active_stations:
                msg = f"station1 not in expected stations -- setting to None"
                logger.warning(msg)
                self.station2 = None

        if not self.station1:
             if self.ch1[0].lower() != "r":
                  self.station1 = local_station_id
             else:
                  self.station1 = remote_station_id

        if not self.station2:
             if self.ch2[0].lower() != "r":
                  self.station2 = local_station_id
             else:
                  self.station2 = remote_station_id

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

