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

from .band import Band
from .channel_nomenclature import ChannelNomenclature
from .decimation_level import DecimationLevel
from .standards import SCHEMA_FN_PATHS
from .stations import Stations


# =============================================================================
attr_dict = get_schema("processing", SCHEMA_FN_PATHS)
attr_dict.add_dict(Stations()._attr_dict, "stations")
attr_dict.add_dict(ChannelNomenclature()._attr_dict, "channel_nomenclature")


# =============================================================================
class Processing(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.stations = Stations()
        self._decimations = []
        self.channel_nomenclature = ChannelNomenclature()

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def decimations(self):
        return_list = []
        for item in self._decimations:
            if isinstance(item, dict):
                level = DecimationLevel()
                level.from_dict(item)
            elif isinstance(item, DecimationLevel):
                level = item
            return_list.append(level)

        return return_list

    @decimations.setter
    def decimations(self, value):
        """
        dictionary of decimations levels

        :param value: dict of decimation levels
        :type value: dict

        """

        if isinstance(value, DecimationLevel):
            self._decimations.append(value)

        elif isinstance(value, dict):
            self._decimations = []
            for key, obj in value.items():
                if not isinstance(obj, DecimationLevel):
                    raise TypeError(
                        f"List entry must be a DecimationLevel object not {type(obj)}"
                    )
                else:
                    self._decimations.append(obj)

        elif isinstance(value, list):
            self._decimations = []
            for obj in value:
                if isinstance(value, DecimationLevel):
                    self._decimations.append(obj)

                elif isinstance(obj, dict):
                    level = DecimationLevel()
                    level.from_dict(obj)
                    self._decimations.append(level)
                else:
                    raise TypeError(
                        f"List entry must be a DecimationLevel or dict object not {type(obj)}"
                    )

        elif isinstance(value, str):
            if len(value) > 4:
                raise TypeError(f"Not sure what to do with {type(value)}")
            else:
                self._decimations = []

        else:
            raise TypeError(f"Not sure what to do with {type(value)}")

    @property
    def decimations_dict(self):
        """
        need to have a dictionary, but it can't be an attribute cause that
        gets confusing when reading in a json file

        :return: DESCRIPTION
        :rtype: TYPE

        """
        return dict([(d.decimation.level, d) for d in self.decimations])

    def get_decimation_level(self, level):
        """
        Get a decimation level for easy access

        :param level: DESCRIPTION
        :type level: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        try:
            decimation = self.decimations_dict[level]

        except KeyError:
            raise KeyError(f"Could not find {level} in decimations.")

        if isinstance(decimation, dict):
            decimation_level = DecimationLevel()
            decimation_level.from_dict(decimation)
            return decimation_level

        return decimation

    def add_decimation_level(self, decimation_level):
        """
        add a decimation level
        """

        if not isinstance(decimation_level, (DecimationLevel, dict)):
            raise TypeError(
                f"List entry must be a DecimationLevel object not {type(decimation_level)}"
            )
        if isinstance(decimation_level, dict):
            obj = DecimationLevel()
            obj.from_dict(decimation_level)

        else:
            obj = decimation_level

        self._decimations.append(obj)

    @property
    def band_edges_dict(self):
        band_edges_dict = {}
        for i_dec, decimation in enumerate(self.decimations):
            band_edges_dict[i_dec] = decimation.band_edges
        return band_edges_dict

    def assign_decimation_level_data_emtf(self, sample_rate):
        """

        Warning: This does not actually tell us how many samples we are decimating down
        at each level.  That is assumed to be 4 but we need a way to bookkeep this in general

        Parameters
        ----------
        sample_rate: float
            The initial sampling rate of the data before any decimation

        """
        for key in sorted(self.decimations_dict.keys()):
            if key in [0, "0"]:
                d = 1
                sr = sample_rate
            else:
                # careful with this hardcoded assumption of decimation by 4
                d = 4
                sr = sample_rate / (d ** int(key))
            decimation_obj = self.decimations_dict[key]
            decimation_obj.decimation.factor = d
            decimation_obj.decimation.sample_rate = sr

    def assign_bands(
        self,
        band_edges_dict,
        sample_rate,
        decimation_factors,
        num_samples_window,
    ):
        """

        Warning: This does not actually tell us how many samples we are decimating down
        at each level.  That is assumed to be 4 but we need a way to bookkeep this in general

        Parameters
        ----------
        band_edges: dict
            keys are integers, starting with 0, values are arrays of edges

        """
        num_decimation_levels = len(band_edges_dict)
        if isinstance(num_samples_window, int):
            num_samples_window = num_decimation_levels * [num_samples_window]

        for i_level in sorted(band_edges_dict.keys()):
            band_edges = band_edges_dict[i_level]
            if i_level in [0, "0"]:
                d = decimation_factors[i_level]  # 1
                sr = sample_rate
            else:
                # careful with this hardcoded assumption of decimation by 4
                d = decimation_factors[i_level]  # 4
                sr = 1.0 * sample_rate / (d ** int(i_level))
            decimation_obj = DecimationLevel()
            decimation_obj.decimation.level = int(
                i_level
            )  # self.decimations_dict[key]
            decimation_obj.decimation.factor = d
            decimation_obj.decimation.sample_rate = sr
            decimation_obj.stft.window.num_samples = num_samples_window[i_level]
            frequencies = decimation_obj.fft_frequencies

            for low, high in band_edges:
                band = Band(
                    decimation_level=i_level,
                    frequency_min=low,
                    frequency_max=high,
                )
                band.set_indices_from_frequencies(frequencies)
                decimation_obj.add_band(band)
            self.add_decimation_level(decimation_obj)

    def json_fn(self):
        json_fn = self.id + "_processing_config.json"
        return json_fn

    @property
    def num_decimation_levels(self):
        return len(self.decimations)

    def drop_reference_channels(self):
        for decimation in self.decimations:
            decimation.reference_channels = []
        return

    def set_input_channels(self, channels):
        for decimation in self.decimations:
            decimation.input_channels = channels

    def set_output_channels(self, channels):
        for decimation in self.decimations:
            decimation.output_channels = channels

    def set_reference_channels(self, channels):
        for decimation in self.decimations:
            decimation.reference_channels = channels

    def set_default_input_output_channels(self):
        self.set_input_channels(
            self.channel_nomenclature.default_input_channels
        )
        self.set_output_channels(
            self.channel_nomenclature.default_output_channels
        )

    def set_default_reference_channels(self):
        self.set_reference_channels(
            self.channel_nomenclature.default_reference_channels
        )

    def validate_processing(self, kernel_dataset):
        """
        Placeholder.  Some of the checks and methods here maybe better placed in
        TFKernel, which would validate the dataset against the processing config.

        Things that are validated:
        1. The default estimation engine from the json file is "RME_RR", which is fine (
        we expect to in general to do more RR processing than SS) but if there is only
        one station (no remote)then the RME_RR should be replaced by default with "RME".

        2. make sure local station id is defined (correctly from kernel dataset)
        """

        # Make sure a RR method is not being called for a SS config
        if not self.stations.remote:
            for decimation in self.decimations:
                if decimation.estimator.engine == "RME_RR":
                    self.logger.info(
                        "No RR station specified, switching RME_RR to RME"
                    )
                    decimation.estimator.engine = "RME"

        # Make sure that a local station is defined
        if not self.stations.local.id:
            self.logger.warning(
                "Local station not specified, should be set from Kernel Dataset"
            )
            self.stations.from_dataset_dataframe(kernel_dataset.df)
