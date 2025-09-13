# =====================================================
# Imports
# =====================================================
from typing import Annotated

from loguru import logger
from pydantic import computed_field, Field, field_validator

from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import StrEnumerationBase
from mt_metadata.processing.aurora.band_basemodel import Band
from mt_metadata.processing.aurora.channel_nomenclature_basemodel import (
    ChannelNomenclature,
)
from mt_metadata.processing.aurora.decimation_level_basemodel import DecimationLevel
from mt_metadata.processing.aurora.stations_basemodel import Stations


# =====================================================
class BandSpecificationStyleEnum(StrEnumerationBase):
    EMTF = "EMTF"
    band_edges = "band_edges"


class Processing(MetadataBase):
    decimations: Annotated[
        list[DecimationLevel],
        Field(
            default_factory=list,
            description="decimation levels",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    band_specification_style: Annotated[
        BandSpecificationStyleEnum | None,
        Field(
            default=None,
            description="describes how bands were sourced",
            examples=["EMTF"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    band_setup_file: Annotated[
        str | None,
        Field(
            default=None,
            description="the band setup file used to define bands",
            examples=["/home/user/bs_test.cfg"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    id: Annotated[
        str,
        Field(
            default="",
            description="Configuration ID",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    channel_nomenclature: Annotated[
        ChannelNomenclature,
        Field(
            default_factory=ChannelNomenclature,  # type: ignore
            description="Channel nomenclature",
            examples=["EMTF"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    stations: Annotated[
        Stations,
        Field(
            default_factory=Stations,  # type: ignore
            description="Station information",
            examples=["Station1", "Station2"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("decimations", mode="before")
    @classmethod
    def validate_decimations(cls, value, info) -> list[DecimationLevel]:
        decimation_levels = []
        if isinstance(value, DecimationLevel):
            decimation_levels.append(value)

        elif isinstance(value, dict):
            for key, obj in value.items():
                if not isinstance(obj, DecimationLevel):
                    raise TypeError(
                        f"List entry must be a DecimationLevel object not {type(obj)}"
                    )
                else:
                    decimation_levels.append(obj)

        elif isinstance(value, list):
            for obj in value:
                if isinstance(obj, DecimationLevel):
                    decimation_levels.append(obj)
            for obj in value:
                if isinstance(obj, DecimationLevel):
                    decimation_levels.append(obj)
                elif isinstance(obj, dict):
                    level = DecimationLevel()  # type: ignore
                    level.from_dict(obj)
                    decimation_levels.append(level)
                else:
                    raise TypeError(
                        f"List entry must be a DecimationLevel or dict object not {type(obj)}"
                    )
        # TODO: Add some doc describing the role of this weird check for a long string
        elif isinstance(value, str):
            if len(value) > 4:
                raise TypeError(f"Not sure what to do with {type(value)}")
            else:
                decimation_levels = []

        else:
            raise TypeError(f"Not sure what to do with {type(value)}")

        return decimation_levels

    @computed_field
    @property
    def decimations_dict(self) -> dict[int, DecimationLevel]:
        """
        need to have a dictionary, but it can't be an attribute cause that
        gets confusing when reading in a json file

        Returns
        -------
        dict[int, DecimationLevel]
            A dictionary mapping decimation levels to their corresponding DecimationLevel objects.

        """
        return dict([(d.decimation.level, d) for d in self.decimations])

    def get_decimation_level(self, level: int) -> DecimationLevel:
        """
        Get a decimation level for easy access

        Parameters
        ----------
        level: int
            The decimation level to retrieve.

        Returns
        -------
        DecimationLevel
            The DecimationLevel object corresponding to the specified level.

        """

        try:
            decimation = self.decimations_dict[level]

        except KeyError:
            raise KeyError(f"Could not find {level} in decimations.")

        if isinstance(decimation, dict):
            decimation_level = DecimationLevel()  # type: ignore
            decimation_level.from_dict(decimation)
            return decimation_level

        return decimation

    def add_decimation_level(self, decimation_level: DecimationLevel | dict):
        """
        add a decimation level

        Parameters
        ----------
        decimation_level: DecimationLevel | dict
            The decimation level to add, either as a DecimationLevel object or a dictionary.
        Returns
        -------
        None
        """

        if not isinstance(decimation_level, (DecimationLevel, dict)):
            raise TypeError(
                f"List entry must be a DecimationLevel object not {type(decimation_level)}"
            )
        if isinstance(decimation_level, dict):
            obj = DecimationLevel()  # type: ignore
            obj.from_dict(decimation_level)

        else:
            obj = decimation_level

        self.decimations.append(obj)

    @computed_field
    @property
    def band_edges_dict(self) -> dict[int, list[tuple[float, float]]]:
        band_edges_dict = {}
        for i_dec, decimation in enumerate(self.decimations):
            band_edges_dict[i_dec] = decimation.band_edges
        return band_edges_dict

    def assign_decimation_level_data_emtf(self, sample_rate: float):
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
        band_edges_dict: dict[int, list[tuple[float, float]]],
        sample_rate: float,
        decimation_factors: dict[int, int],
        num_samples_window: dict[int, int] | int = 256,
    ) -> None:
        """

        Warning: This does not actually tell us how many samples we are decimating down
        at each level.  That is assumed to be 4 but we need a way to bookkeep this in general

        Parameters
        ----------
        band_edges: dict[int, list[tuple[float, float]]]
            A dictionary mapping decimation levels to lists of frequency band edges.
            keys are integers, starting with 0, values are arrays of edges

        sample_rate: float
            The initial sampling rate of the data before any decimation.

        decimation_factors: dict[int, int]
            A dictionary mapping decimation levels to their corresponding decimation factors.

        num_samples_window: dict[int, int] | int, optional (default=256)
            The number of samples in the STFT window for each decimation level. If an integer is provided,
            it will be applied to all levels. If a dictionary is provided, it should map decimation levels to
            their corresponding number of samples.

        Returns
        -------
        None
        """
        num_decimation_levels = len(band_edges_dict.keys())
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
            decimation_obj.decimation.level = int(i_level)  # self.decimations_dict[key]
            decimation_obj.decimation.factor = d
            decimation_obj.decimation.sample_rate = sr
            decimation_obj.stft.window.num_samples = num_samples_window[i_level]
            frequencies = decimation_obj.fft_frequencies

            for low, high in band_edges:
                band = Band(  # type: ignore
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
        self.set_input_channels(self.channel_nomenclature.default_input_channels)
        self.set_output_channels(self.channel_nomenclature.default_output_channels)

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
                    logger.info("No RR station specified, switching RME_RR to RME")
                    decimation.estimator.engine = "RME"

        # Make sure that a local station is defined
        if not self.stations.local.id:
            logger.warning(
                "Local station not specified, should be set from Kernel Dataset"
            )
            self.stations.from_dataset_dataframe(kernel_dataset.df)
