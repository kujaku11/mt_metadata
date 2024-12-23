# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 15:20:59 2022

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import numpy as np
import pandas as pd
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from typing import Optional

# =============================================================================
attr_dict = get_schema("band", SCHEMA_FN_PATHS)


# =============================================================================
class Band(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        """
            Constructor.

            :param kwargs: TODO description here
        """

        super().__init__(attr_dict=attr_dict, **kwargs)
        self._name = None

    @property
    def lower_bound(self) -> float:
        return self.frequency_min

    @property
    def upper_bound(self) -> float:
        return self.frequency_max

    @property
    def lower_closed(self) -> bool:
        return self.to_interval().closed_left

    @property
    def upper_closed(self) -> bool:
        return self.to_interval().closed_right

    @property
    def name(self) -> str:
        """
        :return: The name of the frequency band (currently defaults to fstring with 6 decimal places.
        :rtype: str
        """
        if self._name is None:
            self._name = f"{self.center_frequency:.6f}"
        return self._name


    @name.setter
    def name(self, value):
        self._name = value

    def _indices_from_frequencies(self, frequencies):
        """

        Parameters
        ----------
        frequencies: numpy array
            Intended to represent the one-sided (positive) frequency axis of
            the data that has been FFT-ed

        Returns
        -------
        indices: numpy array of integers
            Integer indices of the fourier coefficients associated with the
            frequecies passed as input argument
        """
        if self.lower_closed:
            cond1 = frequencies >= self.lower_bound
        else:
            cond1 = frequencies > self.lower_bound
        if self.upper_closed:
            cond2 = frequencies <= self.upper_bound
        else:
            cond2 = frequencies < self.upper_bound

        indices = np.where(cond1 & cond2)[0]
        return indices

    def set_indices_from_frequencies(self, frequencies):
        """assumes min/max freqs are defined"""
        indices = self._indices_from_frequencies(frequencies)
        self.index_min = indices[0]
        self.index_max = indices[-1]

    def to_interval(self):
        return pd.Interval(
            self.frequency_min, self.frequency_max, closed=self.closed
        )

    @property
    def harmonic_indices(self):
        """
        Assumes all harmincs between min and max are present in the band

        Returns
        -------
        numpy array of integers corresponding to harminic indices
        """
        return np.arange(self.index_min, self.index_max + 1)

    def in_band_harmonics(self, frequencies):
        """
        Parameters
        ----------
        frequencies: array-like, floating poirt

        Returns: numpy array
            the actual harmonics or frequencies in band, rather than the indices.
        -------

        """
        indices = self._indices_from_frequencies(frequencies)
        harmonics = frequencies[indices]
        return harmonics

    @property
    def center_frequency(self):
        """
        Returns
        -------
        center_frequency: float
            The frequency associated with the band center.
        """
        if self.center_averaging_type == "geometric":
            return np.sqrt(self.lower_bound * self.upper_bound)
        elif self.center_averaging_type == "arithmetic":
            return (self.lower_bound + self.upper_bound) / 2

    @property
    def center_period(self):
        return 1.0 / self.center_frequency
