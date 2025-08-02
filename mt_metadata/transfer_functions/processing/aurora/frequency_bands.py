"""
Module containing FrequencyBands class representing a collection of Frequency Band objects.
"""
from typing import Literal, Optional, Generator, Union, List
import pandas as pd
import numpy as np
import warnings
from loguru import logger

from . import Band


class FrequencyBands:
    """
    Collection of Band objects, typically used at a single decimation level.

    Attributes
    ----------
    _band_edges : pd.DataFrame
        DataFrame with columns ['lower_bound', 'upper_bound'] containing
        frequency band boundaries
    """

    def __init__(
        self,
        band_edges: Optional[Union[np.ndarray, pd.DataFrame]] = None,
    ):
        """
        Parameters
        ----------
        band_edges : np.ndarray or pd.DataFrame, optional
            If numpy array: 2D array with columns [lower_bound, upper_bound]
            If DataFrame: Must have columns ['lower_bound', 'upper_bound']
        """
        if band_edges is not None:
            self.band_edges = band_edges
        else:
            self._band_edges = pd.DataFrame(columns=['lower_bound', 'upper_bound'])

    def __str__(self) -> str:
        """Returns a Description of frequency bands"""
        intro = "Frequency Bands:"
        return f"{intro} \n{self._band_edges}"

    def __repr__(self):
        return self.__str__()

    @property
    def band_edges(self) -> pd.DataFrame:
        """Get band edges as a DataFrame"""
        return self._band_edges

    @band_edges.setter
    def band_edges(self, value: Union[np.ndarray, pd.DataFrame]) -> None:
        """
        Set band edges from either numpy array or DataFrame

        Parameters
        ----------
        value : np.ndarray or pd.DataFrame
            Band edge definitions
        """
        if isinstance(value, np.ndarray):
            if value.ndim != 2 or value.shape[1] != 2:
                raise ValueError("band_edges array must be 2D with shape (n_bands, 2)")
            self._band_edges = pd.DataFrame(
                value,
                columns=['lower_bound', 'upper_bound']
            )
        elif isinstance(value, pd.DataFrame):
            required_cols = ['lower_bound', 'upper_bound']
            if not all(col in value.columns for col in required_cols):
                raise ValueError(
                    f"DataFrame must contain columns {required_cols}"
                )
            self._band_edges = value[required_cols].copy()
        else:
            raise TypeError(
                "band_edges must be numpy array or DataFrame"
            )

        # Reset index to ensure 0-based integer indexing
        self._band_edges.reset_index(drop=True, inplace=True)

    @property
    def number_of_bands(self) -> int:
        """Number of frequency bands"""
        return len(self._band_edges)

    @property
    def array(self) -> np.ndarray:
        """Get band edges as numpy array"""
        return self._band_edges.values

    def sort(self, by: str = "center_frequency", ascending: bool = True) -> None:
        """
        Sort bands by specified criterion.

        Parameters
        ----------
        by : str
            Criterion to sort by:
            - "lower_bound": Sort by lower frequency bound
            - "upper_bound": Sort by upper frequency bound
            - "center_frequency": Sort by geometric center frequency (default)
        ascending : bool
            If True, sort in ascending order, else descending
        """
        if by in ["lower_bound", "upper_bound"]:
            self._band_edges.sort_values(by=by, ascending=ascending, inplace=True)
        elif by == "center_frequency":
            centers = self.band_centers()
            self._band_edges = self._band_edges.iloc[
                np.argsort(centers)[::(-1 if not ascending else 1)]
            ].reset_index(drop=True)
        else:
            raise ValueError(
                f"Invalid sort criterion: {by}. Must be one of: "
                "'lower_bound', 'upper_bound', 'center_frequency'"
            )

    def bands(
        self,
        direction: str = "increasing_frequency",
        sortby: Optional[str] = None,
        rtype: str = "list"
    ) -> Union[List[Band], Generator[Band, None, None]]:
        """
        Generate Band objects in specified order.

        Parameters
        ----------
        direction : str
            Order of iteration: "increasing_frequency" or "increasing_period"
        sortby : str, optional
            Sort bands before iteration:
            - "lower_bound": Sort by lower frequency bound
            - "upper_bound": Sort by upper frequency bound
            - "center_frequency": Sort by geometric center frequency
            If None, uses existing order
        rtype : str
            Return type: "list" or "generator". Default is "list" for easier reuse.
            Use "generator" for memory efficiency when bands are only iterated once.

        Returns
        -------
        Union[List[Band], Generator[Band, None, None]]
            Band objects for each frequency band, either as a list or generator
            depending on rtype parameter.
        """
        if sortby is not None or direction == "increasing_period":
            # Create a copy to avoid modifying original
            temp_bands = FrequencyBands(self._band_edges.copy())
            temp_bands.sort(
                by=sortby or "center_frequency",
                ascending=(direction == "increasing_frequency")
            )
            bands_to_iterate = temp_bands
        else:
            bands_to_iterate = self

        # Create generator
        def band_generator():
            for idx in range(bands_to_iterate.number_of_bands):
                yield bands_to_iterate.band(idx)

        # Return as requested type
        if rtype == "generator":
            return band_generator()
        elif rtype == "list":
            return list(band_generator())
        else:
            raise ValueError("rtype must be either 'list' or 'generator'")

    def band(self, i_band: int) -> Band:
        """
        Get specific frequency band.

        Parameters
        ----------
        i_band : int
            Index of band to return (zero-based)

        Returns
        -------
        Band
            Frequency band object
        """
        row = self._band_edges.iloc[i_band]
        return Band(
            frequency_min=row['lower_bound'],
            frequency_max=row['upper_bound']
        )

    def band_centers(self, frequency_or_period: str = "frequency") -> np.ndarray:
        """
        Calculate center frequencies/periods for all bands.

        Parameters
        ----------
        frequency_or_period : str
            Return values in "frequency" (Hz) or "period" (s)

        Returns
        -------
        np.ndarray
            Center frequencies/periods for each band
        """
        band_centers = np.array([
            self.band(i).center_frequency
            for i in range(self.number_of_bands)
        ])

        if frequency_or_period == "period":
            band_centers = 1.0 / band_centers

        return band_centers

    def validate(self) -> None:
        """
        Validate and potentially reorder bands based on center frequencies.
        """
        band_centers = self.band_centers()

        # Check if band centers are monotonically increasing
        if not np.all(band_centers[1:] > band_centers[:-1]):
            logger.warning(
                "Band centers are not monotonic. Attempting to reorganize bands."
            )
            self.sort(by="center_frequency")
