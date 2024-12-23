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
from . import DecimationLevel
from .standards import SCHEMA_FN_PATHS
from typing import Optional

# =============================================================================
attr_dict = get_schema("band", SCHEMA_FN_PATHS)


# =============================================================================
class Band(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        super().__init__(attr_dict=attr_dict, **kwargs)
        self._name = None

    @property
    def lower_bound(self):
        return self.frequency_min

    @property
    def upper_bound(self):
        return self.frequency_max

    @property
    def lower_closed(self):
        return self.to_interval().closed_left

    @property
    def upper_closed(self):
        return self.to_interval().closed_right

    @property
    def name(self):
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


class FrequencyBands(object):
    """
    This is just collection of objects of class Band.
    It is intended to be used at a single decimation level, i.e. at a single sample rate.

    """

    def __init__(
        self,
        band_edges: Optional[np.ndarray] = None,
    ):
        """
        :param band_edges: 2d numpy array with one row per frequency band and two columns, one for the left-hand
        (lower bound) of the frequency band and one for the right-hand (upper bound).
        Development Note: There are some clever ways to define the bands using a 1-D array but this
        assumes the bands to be adjacent, and we do not want to bake this constriant in, thus band edges is thus 2-D.
        :type band_edges: np.ndarray

        """
        self.band_edges = band_edges

    @property
    def number_of_bands(self):
        return self.band_edges.shape[0]

    def validate(self):
        """
        Placeholder for sanity checks.
        Main reason for this is in anticipation of an append() method that accepts Band objects.
        In that case we may wish to re-order the band edges.

        """
        band_centers = self.band_centers()

        # check band centers are monotonically increasing
        monotone_condition = np.all(band_centers[1:] > band_centers[:-1])
        if monotone_condition:
            pass
        else:
            print(
                "WARNING Band Centers are Not Monotonic.  This probably means that "
                "the bands are being defined in an adhoc way"
            )
            print("This condition untested 20210720")
            print("Attempting to reorganize bands")
            # use np.argsort to rorganize the bands
            self.band_edges = self.band_edges[np.argsort(band_centers), :]

        return

    def bands(self, direction="increasing_frequency"):
        """
        make this a generator for iteration over bands
        Returns
        -------

        """
        band_indices = range(self.number_of_bands)
        if direction == "increasing_period":
            band_indices = np.flip(band_indices)
        return (self.band(i_band) for i_band in band_indices)

    def band(self, i_band):
        """
        Parameters
        ----------
        i_band: integer (zero-indexed)
            Specifies the band to return

        Returns
        -------
        frequency_band: Band()
            Class that represents a frequency band
        """

        frequency_band = Band(
            frequency_min=self.band_edges[i_band, 0],
            frequency_max=self.band_edges[i_band, 1],
        )
        return frequency_band

    def band_centers(self, frequency_or_period="frequency"):
        """
        Parameters
        ----------
        frequency_or_period : str
            One of ["frequency" , "period"].  Determines if the vector of band
            centers is returned in "Hz" or "s"

        Returns
        -------
        band_centers : numpy array
            center frequencies of the bands in Hz or in s
        """
        band_centers = np.full(self.number_of_bands, np.nan)
        for i_band in range(self.number_of_bands):
            frequency_band = self.band(i_band)
            band_centers[i_band] = frequency_band.center_frequency
        if frequency_or_period == "period":
            band_centers = 1.0 / band_centers
        return band_centers

    def from_decimation_object(self, decimation_level: DecimationLevel):
        """
        Define band_edges array from decimation_level object,

        Parameters
        ----------
        decimation_level: mt_metadata.transfer_functions.processing.aurora.decimation_level.DecimationLevel

        """
        # TODO: Consider replacing below with decimation_object.delta_frequency
        df = (
            decimation_level.decimation.sample_rate
            / decimation_level.window.num_samples
        )
        half_df = df / 2.0

        lower_edges = (decimation_level.lower_bounds * df) - half_df
        upper_edges = (decimation_level.upper_bounds * df) + half_df
        band_edges = np.vstack((lower_edges, upper_edges)).T
        self.band_edges = band_edges
