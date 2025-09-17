"""This module contains the simplest coherence feature.
The feature is computed with scipy.signal coherence.

Note that this coherence is one number for the entire time-series (per frequency), i.e.

The Window object is used to taper the time series before FFT.

Development Notes:
Coherence extends the Feature class.  This means that it should have
all the attrs that a Feature instance does, as well as its own unique ones.
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

# =====================================================
# Imports
# =====================================================
from typing import Annotated, Optional, Tuple

import numpy as np
import scipy.signal as ssig
from loguru import logger
from pydantic import computed_field, Field, model_validator

from mt_metadata.common.enumerations import StrEnumerationBase
from mt_metadata.features.feature import Feature
from mt_metadata.processing.window import Window


# =====================================================
class DetrendEnum(StrEnumerationBase):
    linear = "linear"
    constant = "constant"


class Coherence(Feature):
    channel_1: Annotated[
        str,
        Field(
            default="",
            description="The first channel of two channels in the coherence calculation.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["ex"],
            },
        ),
    ]

    channel_2: Annotated[
        str,
        Field(
            default="",
            description="The second channel of two channels in the coherence calculation.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["hy"],
            },
        ),
    ]

    detrend: Annotated[
        DetrendEnum,
        Field(
            default="linear",
            description="How to detrend the data segments before fft.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["constant"],
            },
        ),
    ]

    station_1: Annotated[
        str | None,
        Field(
            default=None,
            description="The station associated with the first channel in the coherence calculation.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["PKD"],
            },
        ),
    ]

    station_2: Annotated[
        str | None,
        Field(
            default=None,
            description="The station associated with the second channel in the coherence calculation.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["SAO"],
            },
        ),
    ]

    window: Annotated[
        Window,
        Field(
            default=Window(num_samples=256, overlap=128, type="hamming"),  # type: ignore
            description="The window function to apply to the data segments before fft.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": [{"type": "hamming", "num_samples": 256, "overlap": 128}],
            },
        ),
    ]

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, data: dict) -> dict:
        data["name"] = "coherence"
        data["domain"] = "frequency"
        data["description"] = (
            "Simple coherence between two channels derived "
            "directly from scipy.signal.coherence applied to "
            "time domain data"
        )
        return data

    @computed_field
    @property
    def channel_pair_str(self) -> str:
        return f"{self.channel_1}, {self.channel_2}"

    def validate_station_ids(
        self, local_station_id: str, remote_station_id: Optional[str] = None
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

        # if the feature has a station_1, check that it is in the list of active stations
        if self.station_1:  # not "" or None
            if self.station_1 not in active_stations:
                msg = "station_1 not in expected stations -- setting to None"
                logger.warning(msg)
                self.station_1 = None

        if self.station_2:  # not "" or None
            if self.station_2 not in active_stations:
                msg = "station_2 not in expected stations -- setting to None"
                logger.warning(msg)
                self.station_2 = None

        if not self.station_1:
            if self.channel_1[0].lower() != "r":
                self.station_1 = local_station_id
            else:
                self.station_1 = remote_station_id

        if not self.station_2:
            if self.channel_2[0].lower() != "r":
                self.station_2 = local_station_id
            else:
                self.station_2 = remote_station_id

        # by this time, all stations should be set.  Confirm that we do not have a station that is None
        # TODO Consider returning False if exception encountered here.
        try:
            assert self.station_1 is not None
        except Exception as e:
            msg = "station_1 is not set -- perhaps it was set to a remote that does not exist?"
            logger.error(msg)
        try:
            assert self.station_2 is not None
        except Exception as e:
            msg = "station_2 is not set -- perhaps it was set to a remote that does not exist?"
            logger.error(msg)

    def compute(
        self, ts_1: np.ndarray, ts_2: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
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
