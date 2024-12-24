# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 14:15:20 2022

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

import numpy as np
# =============================================================================
attr_dict = get_schema("window", SCHEMA_FN_PATHS)
# =============================================================================
class Window(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        super().__init__(attr_dict=attr_dict, **kwargs)
        self.additional_args = {}

    @property
    def additional_args(self):
        return self._additional_args

    @additional_args.setter
    def additional_args(self, args):
        if not isinstance(args, dict):
            raise TypeError("additional_args must be a dictionary")
        self._additional_args = args

    @property
    def num_samples_advance(self):
        return self.num_samples - self.overlap

    def fft_harmonics(self, sample_rate: float) -> np.ndarray:
        """
            Returns the frequencies for an fft..
        :param sample_rate:
        :return:
        """
        return get_fft_harmonics(
            samples_per_window=self.num_samples,
            sample_rate=sample_rate
        )


def get_fft_harmonics(
    samples_per_window: int,
    sample_rate: float
) -> np.ndarray:
    """
    Works for odd and even number of points.

    Development notes:
    - Could be modified with arguments to support one_sided, two_sided, ignore_dc
    ignore_nyquist, and etc.  Consider taking FrequencyBands as an argument.
    - This function was in decimation_level, but there were circular import issues.
    The function needs only a window length and sample rate, so putting it here for now.
    - TODO: switch to using np.fft.rfftfreq

    Parameters
    ----------
    samples_per_window: int
        Number of samples in a window that will be Fourier transformed.
    sample_rate: float
            Inverse of time step between samples; Samples per second in Hz.

    Returns
    -------
    harmonic_frequencies: numpy array
        The frequencies that the fft will be computed.
        These are one-sided (positive frequencies only)
        Does _not_ return Nyquist
        Does return DC component
    """
    delta_t = 1.0 / sample_rate
    harmonic_frequencies = np.fft.fftfreq(samples_per_window, d=delta_t)
    n_fft_harmonics = int(samples_per_window / 2)  # no bin at Nyquist,
    harmonic_frequencies = harmonic_frequencies[0:n_fft_harmonics]
    return harmonic_frequencies
