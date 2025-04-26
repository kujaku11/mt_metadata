# -*- coding: utf-8 -*-
"""
    This module contains the DecimationLevel class.
    TODO: Factor or rename.  The decimation level class here has information about the entire processing.

Created on Thu Feb 17 14:15:20 2022

@author: jpeacock


TODO: Make/Import  class ChannelWeightSpec():
    def __init__(self, **kwargs):
        pass

- DecimationLevel will have a _channel_weight_specs property, which is the list of ChannelWeightSpec objects

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
from mt_metadata.features.weights.channel_weight_spec import ChannelWeightSpec

# =============================================================================
attr_dict = get_schema("decimation_level", SCHEMA_FN_PATHS)
attr_dict.add_dict(Decimation()._attr_dict, "decimation")
attr_dict.add_dict(STFT()._attr_dict, "stft")
attr_dict.add_dict(get_schema("regression", SCHEMA_FN_PATHS), "regression")
attr_dict.add_dict(get_schema("estimator", SCHEMA_FN_PATHS), "estimator")


# =============================================================================


class DecimationLevel(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.decimation = Decimation()
        self.regression = Regression()
        self.estimator = Estimator()
        self.stft = STFT()

        self._bands = []
        self._channel_weight_specs = []

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def bands(self) -> List[Band]:
        """
            Return bands.

        """
        return self._bands

    @bands.setter
    def bands(self, value):
        """
        Set bands make sure they are a band object

        :param value: list of bands
        :type value: list, Band

        """
        # Handle singleton cases
        if isinstance(value, (Band, dict)):
            value = [value, ]

        if not isinstance(value, list):
            raise TypeError(f"Not sure what to do with {type(value)}")

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

    # @property
    # def channel_weight_specs(self) -> List[ChannelWeightSpec]:
    #     """
    #         Return the channel weight spec objects.
    #         If they are in dict form, cast them to ChannelWeightSpec objects before returning.
    #
    #     TODO: Consider making the channel_weight_specs setter cast everything from dict to
    #      ChannelWeightSpec when setting. Then this method can be replaced by a simple
    #      `return self._channel_weight_specs`
    #      Reason: We access channel_weight_specs much more frequently than we assign them.
    #
    #     """
    #     return_list = []
    #     for channel_weight_spec in self._channel_weight_specs:
    #         if isinstance(channel_weight_spec, dict):
    #             cws = ChannelWeightSpec()
    #             cws.from_dict(channel_weight_spec)
    #         elif isinstance(channel_weight_spec, ChannelWeightSpec):
    #             cws = channel_weight_spec
    #         return_list.append(cws)
    #     return return_list
    #
    # @channel_weight_specs.setter
    # def bands(self, value: List[Union[dict, ChannelWeightSpec]]):
    #     """
    #     Set channel_weight_specs make sure they are a ChannelWeightSpec object
    #
    #     :param value: list of ChannelWeightSpec objects
    #     :type value: list, Band
    #
    #     """
    #
    #     if isinstance(value, ChannelWeightSpec):
    #         self._channel_weight_specs = [value]
    #
    #     elif isinstance(value, list):
    #         self._bands = []
    #         for obj in value:
    #             if not isinstance(obj, (Band, dict)):
    #                 raise TypeError(
    #                     f"List entry must be a Band object not {type(obj)}"
    #                 )
    #             if isinstance(obj, dict):
    #                 band = Band()
    #                 band.from_dict(obj)
    #
    #             else:
    #                 band = obj
    #
    #             self._bands.append(band)
    #     else:
    #         raise TypeError(f"Not sure what to do with {type(value)}")

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

        See notes in `_df_from_bands`.

        Returns
        -------
        bands_df: pd.Dataframe
            Same format as that generated by EMTFBandSetupFile.get_decimation_level()
        """
        bands_df = _df_from_bands(self.bands)
        return bands_df

    @property
    def frequency_sample_interval(self) -> float:
        """
            Returns the delta_f in frequency domain df = 1 / (N * dt)
            Here dt is the sample interval after decimation
        """
        return self.decimation.sample_rate / self.stft.window.num_samples

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

    def frequency_bands_obj(self) -> FrequencyBands:
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

    @property
    def fft_frequencies(self) -> np.ndarray:
        """
            Gets the harmonics of the STFT.

            :return freqs: The frequencies at which the stft will be available.
            :rtype freqs: np.ndarray
        """
        freqs = self.stft.window.fft_harmonics(self.decimation.sample_rate)
        return freqs

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

    def is_consistent_with_archived_fc_parameters(
        self,
        fc_decimation: FCDecimation,
        remote: bool
    ):
        """
            Usage: For an already existing spectrogram stored in an MTH5 archive, this compares the metadata
            within the archive (fc_decimation) with an aurora decimation level (self), and tells whether the
            parameters are in agreement. If True, this allows aurora to skip the calculation of FCs and instead
            read them from the archive.

            TODO: Merge all checks of TimeSeriesDecimation parameters into a single check.
            - e.g. Compress all decimation checks to: assert fc_decimation.decimation == self.decimation

            Parameters
            ----------
            decimation_level: FCDecimation
                metadata describing the parameters used to compute an archived spectrogram
            remote: bool
                If True, we are looking for reference channels, not local channels in the FCGroup.

            Iterates over FCDecimation attributes:
                "channels_estimated": to ensure all expected channels are in the group
                "decimation.anti_alias_filter": check that the expected AAF was applied
                "decimation.sample_rate,
                "decimation.method",
                "stft.prewhitening_type",
                "stft.recoloring",
                "stft.pre_fft_detrend_type",
                "stft.min_num_stft_windows",
                "stft.window",
                "stft.harmonic_indices",
        Returns
        -------

        :return:
        """
        # channels_estimated: Checks that the archived spectrogram has the required channels
        if remote:
            required_channels = self.reference_channels
        else:
            required_channels = self.local_channels
        try:
            assert set(required_channels).issubset(fc_decimation.channels_estimated)
        except AssertionError:
            msg = (
                f"required_channels for processing {required_channels} not available"
                f"-- fc channels estimated are {fc_decimation.channels_estimated}"
            )
            self.logger.info(msg)
            return False

        # anti_alias_filter: Check that the data were filtered the same way
        try:
            assert fc_decimation.time_series_decimation.anti_alias_filter == self.decimation.anti_alias_filter
        except AssertionError:
            cond1 = self.time_series_decimation.anti_alias_filter == "default"
            cond2 = fc_decimation.time_series_decimation.anti_alias_filter is None
            if cond1 & cond2:
                pass
            else:
                msg = (
                    "Antialias Filters Not Compatible -- need to add handling for "
                    f"{msg} FCdec {fc_decimation.time_series_decimation.anti_alias_filter} and "
                    f"{msg} processing config:{self.decimation.anti_alias_filter}"
                )
                raise NotImplementedError(msg)

        # sample_rate
        try:
            assert (
                fc_decimation.time_series_decimation.sample_rate
                == self.decimation.sample_rate
            )
        except AssertionError:
            msg = (
                f"Sample rates do not agree: fc {fc_decimation.time_series_decimation.sample_rate} differs from "
                f"processing config {self.decimation.sample_rate}"
            )
            self.logger.info(msg)
            return False

        # transform method (fft, wavelet, etc.)
        try:
            assert fc_decimation.short_time_fourier_transform.method == self.stft.method  # FFT, Wavelet, etc.
        except AssertionError:
            msg = (
                "Transform methods do not agree: "
                f"fc {fc_decimation.short_time_fourier_transform.method} != processing config {self.stft.method}"
            )
            self.logger.info(msg)
            return False

        # prewhitening_type
        try:
            assert fc_decimation.stft.prewhitening_type == self.stft.prewhitening_type
        except AssertionError:
            msg = (
                "prewhitening_type does not agree "
                f"fc {fc_decimation.stft.prewhitening_type} != processing config {self.stft.prewhitening_type}"
            )
            self.logger.info(msg)
            return False

        # recoloring
        try:
            assert fc_decimation.stft.recoloring == self.stft.recoloring
        except AssertionError:
            msg = (
                "recoloring does not agree "
                f"fc {fc_decimation.stft.recoloring} != processing config {self.stft.recoloring}"
            )
            self.logger.info(msg)
            return False

        # pre_fft_detrend_type
        try:
            assert (
                fc_decimation.stft.pre_fft_detrend_type
                == self.stft.pre_fft_detrend_type
            )
        except AssertionError:
            msg = (
                "pre_fft_detrend_type does not agree "
                f"fc {fc_decimation.stft.pre_fft_detrend_type} != processing config {self.stft.pre_fft_detrend_type}"
            )
            self.logger.info(msg)
            return False

        # min_num_stft_windows
        try:
            assert (
                fc_decimation.stft.min_num_stft_windows
                == self.stft.min_num_stft_windows
            )
        except AssertionError:
            msg = (
                "min_num_stft_windows do not agree "
                f"fc {fc_decimation.stft.min_num_stft_windows} != processing config {self.stft.min_num_stft_windows}"
            )
            self.logger.info(msg)
            return False

        # window
        try:
            assert fc_decimation.stft.window == self.stft.window
        except AssertionError:
            msg = "window does not agree: "
            msg = f"{msg} FC Group: {fc_decimation.stft.window} "
            msg = f"{msg} Processing Config  {self.stft.window}"
            self.logger.info(msg)
            return False

        if -1 in fc_decimation.stft.harmonic_indices:
            # if harmonic_indices is -1, it means the archive kept all so we can skip this check.
            pass
        else:
            msg = "WIP: harmonic indices in AuroraDecimationlevel are derived from processing bands -- Not robustly tested to compare with FCDecimation"
            self.logger.debug(msg)
            harmonic_indices_requested = self.harmonic_indices
            fcdec_group_set = set(fc_decimation.stft.harmonic_indices)
            processing_set = set(harmonic_indices_requested)
            if processing_set.issubset(fcdec_group_set):
                pass
            else:
                msg = (
                    f"Processing FC indices {processing_set} is not contained "
                    f"in FC indices {fcdec_group_set}"
                )
                self.logger.info(msg)
                return False

        # Getting here means no checks were failed. The FCDecimation supports the processing config
        return True

    def to_fc_decimation(
        self,
        remote: bool = False,
        ignore_harmonic_indices: bool = True,
    ) -> FCDecimation:
        """
        Generates a FC Decimation() object for use with FC Layer in mth5.

        TODO: this is being tested only in aurora -- move a test to mt_metadata or move the method.
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
        fc_dec_obj.time_series_decimation.anti_alias_filter = self.decimation.anti_alias_filter
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
        fc_dec_obj.time_series_decimation.sample_rate = self.decimation.sample_rate
        fc_dec_obj.stft.window = self.stft.window

        return fc_dec_obj


def _df_from_bands(band_list: List[Union[Band, dict, None]]) -> pd.DataFrame:
    """
    Utility function that transforms a list of bands into a dataframe

    Note: The decimation_level here is +1 to agree with EMTF convention.
        Not clear this is really necessary
    TODO: Consider making this a method of FrequencyBands() class.
    TODO: Check typehint -- should None be allowed value in the band_list?
    TODO: Consider adding columns lower_closed, upper_closed to df

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
