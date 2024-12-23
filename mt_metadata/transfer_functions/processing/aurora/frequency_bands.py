"""
    This module contains a class FrequencyBands whic represents a collection of Frequency Band objects.
"""
from . import Band
from . import DecimationLevel
from typing import Optional

import numpy as np


class FrequencyBands(object):
    """
    This is just collection of objects of class Band.
    It is intended to be used at a single decimation level, i.e. at a single sample rate.

    TODO: Housekeeping, band_edges could be labelled data with lower_bounds and upper bounds
     explicit instead of implicit.  Consider making it a df or xr.

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
    def number_of_bands(self) -> int:
        return self.band_edges.shape[0]

    def validate(self) -> None:
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

    def bands(self, direction: str ="increasing_frequency"):
        """

        TODO: make this a generator for iteration over bands
        TODO: make direction a Literal ["increasing frequency", "increasing period",
                                        "decreasing frequency", "decreasing period",]

        Returns
        -------

        """
        band_indices = range(self.number_of_bands)
        if direction == "increasing_period":
            band_indices = np.flip(band_indices)
        return (self.band(i_band) for i_band in band_indices)

    def band(self, i_band: int) -> Band:
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

    def band_centers(self, frequency_or_period="frequency") -> np.ndarray:
        """
        Parameters
        ----------
        TODO: Make this typing.Literal
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
        TODO: FIXME This is causing circular imports when it is correctly dtyped.

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
