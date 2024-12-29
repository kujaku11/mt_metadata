# -*- coding: utf-8 -*-
"""
    This module contains the DecimationLevel class.
    TODO: Factor or rename.  The decimation level class here has information about the entire processing.

Created on Thu Feb 17 14:15:20 2022

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import numpy as np
import pandas as pd

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.transfer_functions.processing.fourier_coefficients import (
            Decimation as FCDecimation,
        )
from typing import List, Union

from .band import Band
from ..time_series_decimation import TimeSeriesDecimation as Decimation
from ..short_time_fourier_transform import ShortTimeFourierTransform as STFT
from .estimator import Estimator
from .frequency_bands import FrequencyBands
from .regression import Regression
from .standards import SCHEMA_FN_PATHS
from .window import Window

# =============================================================================
attr_dict = get_schema("decimation_level", SCHEMA_FN_PATHS)
attr_dict.add_dict(Decimation()._attr_dict, "decimation")
attr_dict.add_dict(STFT()._attr_dict, "stft")
attr_dict.add_dict(get_schema("window", SCHEMA_FN_PATHS), "window")
attr_dict.add_dict(get_schema("regression", SCHEMA_FN_PATHS), "regression")
attr_dict.add_dict(get_schema("estimator", SCHEMA_FN_PATHS), "estimator")


# =============================================================================


def df_from_bands(band_list: List[Union[Band, dict, None]]) -> pd.DataFrame:
    """
    Utility function that transforms a list of bands into a dataframe

    Note: The decimation_level here is +1 to agree with EMTF convention.
        Not clear this is really necessary
    TODO: Consider making this a method of FrequencyBands() class.
    TODO: Check typehint -- should None be allowed value in the band_list?

    Parameters
    ----------
    band_list: list
        obtained from mt_metadata.transfer_functions.processing.aurora.decimation_level.DecimationLevel.bands

    Returns
    -------
    out_df: pd.Dataframe
        Same format as that generated by EMTFBandSetupFile.get_decimation_level()
    """
    df_columns = [
        "decimation_level",
        "lower_bound_index",
        "upper_bound_index",
        "frequency_min",
        "frequency_max",
    ]
    n_rows = len(band_list)
    df_columns_dict = {}
    for col in df_columns:
        df_columns_dict[col] = n_rows * [None]
    for i_band, band in enumerate(band_list):
        df_columns_dict["decimation_level"][i_band] = band.decimation_level + 1
        df_columns_dict["lower_bound_index"][i_band] = band.index_min
        df_columns_dict["upper_bound_index"][i_band] = band.index_max
        df_columns_dict["frequency_min"][i_band] = band.frequency_min
        df_columns_dict["frequency_max"][i_band] = band.frequency_max
    out_df = pd.DataFrame(data=df_columns_dict)
    out_df.sort_values(by="lower_bound_index", inplace=True)
    out_df.reset_index(inplace=True, drop=True)
    return out_df


class DecimationLevel(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.window = Window()
        self.decimation = Decimation()
        self.regression = Regression()
        self.estimator = Estimator()
        self.stft = STFT()

        self._bands = []

        super().__init__(attr_dict=attr_dict, **kwargs)

        # if self.decimation.level == 0:
        #     self.anti_alias_filter = None

    @property
    def anti_alias_filter(self) -> str:
        """
        get anti_alais_filter from TimeSeriesDecimation.

        """
        return self.decimation.anti_alias_filter

    @property
    def bands(self) -> list:
        """
        get bands, something weird is going on with appending.

        """
        return_list = []
        for band in self._bands:
            if isinstance(band, dict):
                b = Band()
                b.from_dict(band)
            elif isinstance(band, Band):
                b = band
            return_list.append(b)
        return return_list

    @bands.setter
    def bands(self, value):
        """
        Set bands make sure they are a band object

        :param value: list of bands
        :type value: list, Band

        """

        if isinstance(value, Band):
            self._bands = [value]

        elif isinstance(value, list):
            self._bands = []
            for obj in value:
                if not isinstance(obj, (Band, dict)):
                    raise TypeError(
                        f"List entry must be a Band object not {type(obj)}"
                    )
                if isinstance(obj, dict):
                    band = Band()
                    band.from_dict(obj)

                else:
                    band = obj

                self._bands.append(band)
        else:
            raise TypeError(f"Not sure what to do with {type(value)}")

    def add_band(self, band: Union[Band, dict]) -> None:
        """
        add a band
        """

        if not isinstance(band, (Band, dict)):
            raise TypeError(
                f"List entry must be a Band object not {type(band)}"
            )
        if isinstance(band, dict):
            obj = Band()
            obj.from_dict(band)

        else:
            obj = band

        self._bands.append(obj)

    @property
    def lower_bounds(self) -> np.ndarray:
        """
        get lower bounds index values into an array.
        """

        return np.array(sorted([band.index_min for band in self.bands]))

    @property
    def upper_bounds(self) -> np.ndarray:
        """
        get upper bounds index values into an array.
        """

        return np.array(sorted([band.index_max for band in self.bands]))

    @property
    def bands_dataframe(self) -> pd.DataFrame:
        """
        Utility function that transforms a list of bands into a dataframe

        Note: The decimation_level here is +1 to agree with EMTF convention.
        Not clear this is really necessary

        TODO: Consider adding columns lower_closed, upper_closed to df

        Returns
        -------
        bands_df: pd.Dataframe
            Same format as that generated by EMTFBandSetupFile.get_decimation_level()
        """
        bands_df = df_from_bands(self.bands)
        return bands_df

    @property
    def frequency_sample_interval(self) -> float:
        """
            Returns the delta_f in frequency domain df = 1 / (N * dt)
            Here dt is the sample interval after decimation
        """
        return self.sample_rate_decimation / self.window.num_samples

    @property
    def band_edges(self) -> np.ndarray:
        """
            Returns the band edges as a numpy array
            :return band_edges: 2D numpy array, one row per frequency band and two columns
            :rtype band_edges: np.ndarray
        """
        bands_df = self.bands_dataframe
        band_edges = np.vstack(
            (bands_df.frequency_min.values, bands_df.frequency_max.values)
        ).T
        return band_edges

    def frequency_bands_obj(self) -> FrequencyBands:  #  TODO: FIXME circular import when correctly dtyped -> FrequencyBands:
        """
        Gets a FrequencyBands object that is used as input to processing.

        Used by Aurora.

        TODO: consider adding .to_frequency_bands() method directly to self.bands

        Returns
        -------
        frequency_bands:  FrequencyBands
            A FrequencyBands object that can be used as an iterator for processing.

        """
        frequency_bands = FrequencyBands(band_edges=self.band_edges)
        return frequency_bands

    # # TODO: FIXME WIP
    # def to_frequency_bands_obj(self):
    #     """
    #         Define band_edges array from decimation_level object,
    #
    #     Development Notes.
    #       This function was originally in FrequencyBands class, it was called:
    #        from_decimation_object.  Circular imports were encountered when it was correctly dtyped.
    #        There is no reason to have FrequencyBands.from_decimation_object(decimation_level)
    #        _and_ decimation_level.to_frequency_bands_obj()
    #        The function above already does the task of generating a frequency bands.
    #        Keeping this commented until documentation improves.
    #        Below looks like an alternative, and more readable way to get band_edges,
    #        without passing through the dataframe.  At a minimum a test should be created
    #        that makes band edges both ways and asserts equal.
    #        (a few command line tests showed that they are, Dec 2024).
    #
    #     """
    #     df = self.frequency_sample_interval
    #     half_df = df / 2.0
    #
    #     lower_edges = (self.lower_bounds * df) - half_df
    #     upper_edges = (self.upper_bounds * df) + half_df
    #     band_edges = np.vstack((lower_edges, upper_edges)).T
    #     return FrequencyBands(band_edges=band_edges)


    @property
    def fft_frequencies(self) -> np.ndarray:
        """
            Gets the harmonics of the STFT.

            :return freqs: The frequencies at which the stft will be available.
            :rtype freqs: np.ndarray
        """
        freqs = self.window.fft_harmonics(self.decimation.sample_rate)
        return freqs

    @property
    def sample_rate_decimation(self) -> float:
        """
            Returns the sample rate of the data after decimation.
            TODO: Delete this method and replace calls to self.sample_rate_decimation with self.decimation.sample_rate

        """
        return self.decimation.sample_rate

    @property
    def harmonic_indices(self) -> List[int]:
        """
            Loops over all bands and returns a list of the harminic indices.
            TODO: Distinguish the bands which are a processing construction vs harmonic indices which are FFT info.
            :return: list of fc indices (integers)
            :rtype: List[int]
        """
        return_list = []
        for band in self.bands:
            fc_indices = band.harmonic_indices
            return_list += fc_indices.tolist()
        return_list.sort()
        return return_list

    @property
    def local_channels(self):
        return self.input_channels + self.output_channels

    def to_fc_decimation(
        self,
        remote: bool = False,
        ignore_harmonic_indices: bool = True,
    ) -> FCDecimation:
        """
        Generates a FC Decimation() object for use with FC Layer in mth5.

        Ignoring for now these properties
        "time_period.end": "1980-01-01T00:00:00+00:00",
        "time_period.start": "1980-01-01T00:00:00+00:00",

        TODO: FIXME: Assignment of TSDecimation can be done in one shot once #235 is addressed.

        Parameters
        ----------
        remote: bool
            If True, use reference channels, if False, use local_channels.  We may wish to not pass remote=True when
            _building_ FCs however, because then not all channels will get built.
        ignore_harmonic_indices: bool
            If True, leave harmonic indices at default [-1,], which means all indices.  If False, only the specific
            harmonic indices needed for processing will be stored.  Thus, when building FCs, it maybe best to leave
            this as True, that way all FCs will be stored, so if the band setup is changed, the FCs will still be there.

        Returns:
            fc_dec_obj:mt_metadata.transfer_functions.processing.fourier_coefficients.decimation.Decimation
            A decimation object configured for STFT processing

        """

        fc_dec_obj = FCDecimation()
        fc_dec_obj.time_series_decimation.anti_alias_filter = self.anti_alias_filter
        if remote:
            fc_dec_obj.channels_estimated = self.reference_channels
        else:
            fc_dec_obj.channels_estimated = self.local_channels
        fc_dec_obj.time_series_decimation.factor = self.decimation.factor
        fc_dec_obj.time_series_decimation.level = self.decimation.level
        if ignore_harmonic_indices:
            pass
        else:
            fc_dec_obj.stft.harmonic_indices = self.harmonic_indices()
        fc_dec_obj.id = f"{self.decimation.level}"
        fc_dec_obj.stft.method = self.stft.method
        fc_dec_obj.stft.pre_fft_detrend_type = self.stft.pre_fft_detrend_type
        fc_dec_obj.stft.prewhitening_type = self.stft.prewhitening_type
        fc_dec_obj.stft.recoloring = self.stft.recoloring
        fc_dec_obj.time_series_decimation.sample_rate = self.sample_rate_decimation
        fc_dec_obj.window = self.window

        return fc_dec_obj
