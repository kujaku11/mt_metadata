# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 13:39:39 2025

@author: jpeacock

This module contains the simplest coherence feature.
The feature is computed with scipy.signal coherence.

Note that this coherence is one number for the entire time-series (per frequency), i.e.

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

Development Note (2025-05-24):
    Note that the simple coherence as computed here, just returns one number per frequency.
    It is the average coherence over the entire run, and is not innately a "per-time-window feature".

    To make it a per-time-window feature, we need to apply the transform on individual windows (not the whole run).
    i.e. chunk a run into sub-windows, and then compute coherence on each of those individually.  To accomplish this
    we must shorten the window.num_samples to be smaller than the sub-window size, otherwise, coherence
    degenerates to 1 everywhere. (Recall coherenc is th average cross-power over average sqrt auto-powers, and having
    only one spectral estimate means there is no averaging).
    Selection of an appropriate "window-within-the-sub-window" for spectral esimation comes with some caveats;

    The length of the window-within-the-window must be small enough to get at least a few)
    spectral estimates, meaning that the frequency content will not mirror that of the FFT
    That said, we can know our lowest frequency of TF estimation (usually no fewer than 5 cycles),
    so we could set the window-within-window width to be, say 1/5 the FFT window length, and then we'll get
    something we can use, although it will be somwhat unrealiable at long period (but so is everything else:/).
    Note that when we are using long FFT windows (such as for HF data processing) this is not such a concern

    Way Forward: A "StridingWindowCoherence" (effectively a spectrogram of coherence) can be an extension of the
    Cohernece feature.  It will have the same properties, but will also have a "SubWindow".  The SubWindow will be
    another window function object, but it can be parameterized, for example, as a fraction of the
    "Spectrogram Sliding Window".

    The compute function could possibly be done by computing Coherence on each sub-window (kinda elegant
    but may wind up being a bit slow with all the for-looping)

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

        # by this time, all stations should be set.  Confirm that we do not have a station that is None
        # TODO Consier returning False if exception encountered here.
        try:
            assert self.station1 is not None
        except Exception as e:
            msg = "station1 is not set -- perhaps it was set to a remote that does not exist?"
            logger.error(msg)
        try:
            assert self.station2 is not None
        except Exception as e:
            msg = "station2 is not set -- perhaps it was set to a remote that does not exist?"
            logger.error(msg)

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


class StridingWindowCoherence(Coherence):
    """
    Computes coherence for each sub-window (FFT window) across the time series.
    Returns a 2D array: (window index, frequency).
    """
    def __init__(self, subwindow=None, stride=None, **kwargs):
        super().__init__(**kwargs)
        self.subwindow = subwindow if subwindow is not None else Window()
        # Ensure stride is always an integer
        if stride is not None:
            self.stride = int(stride)
        else:
            self.stride = int(self.subwindow.num_samples // 2)

    def set_subwindow_from_window(self, fraction=0.2):
        """
        Set the subwindow as a fraction of the main window.
        """
        self.subwindow = Window()
        self.subwindow.type = self.window.type
        self.subwindow.num_samples = int(self.window.num_samples * fraction)
        self.subwindow.overlap = int(self.subwindow.num_samples // 2)
        # Update stride to be int if it was set as a string elsewhere
        self.stride = int(self.stride)

    def compute(self, ts_1: np.ndarray, ts_2: np.ndarray):
        """
        For each main window (length self.window.num_samples, stride self.stride),
        compute coherence using the subwindow parameters (self.subwindow) within that main window.
        Returns:
            frequencies: 1D array of frequencies
            coherences: 2D array (n_main_windows, n_frequencies)
        """
        n = len(ts_1)
        main_win_len = self.window.num_samples
        main_stride = int(self.stride)
        results = []
        for start in range(0, n - main_win_len + 1, main_stride):
            end = start + main_win_len
            seg1 = ts_1[start:end]
            seg2 = ts_2[start:end]
            f, coh = ssig.coherence(
                seg1,
                seg2,
                window=self.subwindow.type,
                nperseg=self.subwindow.num_samples,
                noverlap=self.subwindow.overlap,
                detrend=self.detrend,
            )
            results.append(coh)
        return f, np.array(results)

