"""
Module containing FrequencyBands class representing a collection of Frequency Band objects.
"""
from typing import Optional, Generator, Union
import pandas as pd
import numpy as np
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
            # Reorder bands based on center frequencies
            self._band_edges = self._band_edges.iloc[np.argsort(band_centers)].reset_index(drop=True)

    def bands(self, direction: str = "increasing_frequency") -> Generator[Band, None, None]:
        """
        Generate Band objects in specified order.

        Parameters
        ----------
        direction : str
            Order of iteration: "increasing_frequency" or "increasing_period"

        Yields
        ------
        Band
            Band object for each frequency band
        """
        indices = range(self.number_of_bands)
        if direction == "increasing_period":
            indices = reversed(indices)
            
        for idx in indices:
            yield self.band(idx)

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
