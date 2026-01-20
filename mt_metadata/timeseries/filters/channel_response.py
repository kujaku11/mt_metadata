# =====================================================
# Imports
# =====================================================
from copy import deepcopy
from typing import Annotated

import numpy as np
from loguru import logger
from pydantic import (
    computed_field,
    Field,
    field_validator,
    model_validator,
    PrivateAttr,
    ValidationInfo,
)

from mt_metadata.base.helpers import object_to_array, requires
from mt_metadata.common.units import get_unit_object
from mt_metadata.timeseries.filters import (
    CoefficientFilter,
    FilterBase,
    FIRFilter,
    FrequencyResponseTableFilter,
    PoleZeroFilter,
    TimeDelayFilter,
)
from mt_metadata.timeseries.filters.plotting_helpers import plot_response

try:
    from obspy.core import inventory
except ImportError:
    inventory = None


# =====================================================


class ChannelResponse(FilterBase):
    _supported_filters: list = PrivateAttr(
        [
            PoleZeroFilter,
            CoefficientFilter,
            TimeDelayFilter,
            FrequencyResponseTableFilter,
            FIRFilter,
        ]
    )

    normalization_frequency: Annotated[
        float,
        Field(
            default=0.0,
            description="Pass band frequency",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "100",
            },
        ),
    ]

    filters_list: Annotated[
        list[
            PoleZeroFilter
            | CoefficientFilter
            | TimeDelayFilter
            | FrequencyResponseTableFilter
            | FIRFilter
        ],
        Field(
            default_factory=list,
            description="List of filters applied to the channel.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "[PoleZeroFilter, CoefficientFilter]",
            },
        ),
    ]

    frequencies: Annotated[
        np.ndarray | list[float],
        Field(
            default_factory=lambda: np.empty(0, dtype=float),
            description="The frequencies at which a calibration of the filter were performed.",
            alias=None,
            json_schema_extra={
                "units": "hertz",
                "required": True,
                "items": {"type": "number"},
                "examples": '"[-0.0001., 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.001, ... 1, 2, 5, 10]"',
            },
        ),
    ]

    def __str__(self):
        lines = ["Filters Included:\n", "=" * 25, "\n"]
        for f in self.filters_list:
            lines.append(f.__str__())
            lines.append(f"\n{'-'*20}\n")

        return "".join(lines)

    def __repr__(self):
        return self.__str__()

    @field_validator("normalization_frequency", mode="after")
    @classmethod
    def validate_normalization_frequency(
        cls, value: float, info: ValidationInfo
    ) -> float:
        """
        Validate that the normalization frequency is a positive float.
        If value is 0 or None, derive it from the pass_band.
        """
        if value in [0.0, None]:
            # Create a temporary instance to access pass_band property
            instance = cls.model_construct(**info.data)

            if hasattr(instance, "pass_band") and instance.pass_band is not None:
                pass_band = instance.pass_band
                # Calculate geometric mean of pass band
                norm_freq = np.round(10 ** np.mean(np.log10(pass_band)), 3)
                logger.info(
                    f"Setting normalization frequency to {norm_freq} Hz based on pass band"
                )
                return norm_freq

        return value

    @field_validator("frequencies", mode="before")
    @classmethod
    def validate_frequencies(cls, value: np.ndarray | list[float]) -> np.ndarray:
        """
        Validate that the frequencies are a numpy array or list of floats.
        """
        return object_to_array(value, dtype=float)

    @field_validator("filters_list", mode="before")
    @classmethod
    def validate_filters_list(cls, value: list) -> list:
        """
        Validate that the filters_list is a list of filter objects.
        """
        if not isinstance(value, list):
            raise ValueError("filters_list must be a list of filter objects.")

        value = cls._validate_filters_list(value)
        value = cls._check_consistency_of_units(value)
        return value

    @model_validator(mode="after")
    def update_units_and_normalization_frequency_from_filters_list(
        self,
    ) -> "ChannelResponse":
        """Update units_in and units_out based on filters_list."""
        if self.filters_list:
            object.__setattr__(self, "units_in", self.filters_list[0].units_in)
            object.__setattr__(self, "units_out", self.filters_list[-1].units_out)
            if self.normalization_frequency == 0.0:
                pass_band = self.pass_band
                if pass_band is not None:
                    # Calculate geometric mean of pass band
                    with np.errstate(divide="ignore"):
                        norm_freq = np.round(10 ** np.mean(np.log10(pass_band)), 3)
                    logger.debug(
                        f"Setting normalization frequency to {norm_freq} Hz based on pass band"
                    )
                    # Set normalization frequency to the gain of the first filter
                    object.__setattr__(self, "normalization_frequency", norm_freq)
        return self

    @classmethod
    def _validate_filters_list(cls, filters_list):
        """
        make sure the filters list is valid.

        :param filters_list: DESCRIPTION
        :type filters_list: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        def is_supported_filter(item):
            # Convert the list to a tuple of filter classes
            supported_filter_types = tuple(cls._supported_filters.default)
            # Check if item is an instance of any of the supported filter types
            return isinstance(item, supported_filter_types)

        if filters_list in [[], None]:
            return []

        if not isinstance(filters_list, list):
            msg = f"Input filters list must be a list not {type(filters_list)}"
            logger.error(msg)
            raise TypeError(msg)

        fails = []
        return_list = []
        for item in filters_list:
            if is_supported_filter(item):
                return_list.append(item)
            else:
                fails.append(f"Item is not a supported filter type, {type(item)}")

        if fails:
            raise TypeError(", ".join(fails))

        return return_list

    @classmethod
    def _check_consistency_of_units(cls, filters_list):
        """
        confirms that the input and output units of each filter state are consistent
        """
        if len(filters_list) > 1:
            previous_units = filters_list[0].units_out
            for mt_filter in filters_list[1:]:
                if mt_filter.units_in != previous_units:
                    msg = (
                        "Unit consistency is incorrect. "
                        f"The input units for {mt_filter.name} should be "
                        f"{previous_units} not {mt_filter.units_in}"
                    )
                    logger.error(msg)
                    raise ValueError(msg)
                previous_units = mt_filter.units_out

        return filters_list

    @computed_field
    @property
    def names(self) -> list[str]:
        """names of the filters"""
        names = []
        if self.filters_list:
            names = [f.name for f in self.filters_list]
        return names

    @computed_field
    @property
    def pass_band(self) -> list[float]:
        """estimate pass band for all filters in frequency"""
        if self.frequencies is None:
            logger.debug("No frequencies provided, cannot calculate pass band")
            return None

        if len(self.frequencies) == 0:
            logger.debug("No frequencies provided, cannot calculate pass band")
            return None

        pb = []
        for f in self.filters_list:
            if hasattr(f, "pass_band"):
                f_pb = f.pass_band(self.frequencies)
                if f_pb is None:
                    continue
                pb.append((f_pb.min(), f_pb.max()))

        if pb != []:
            pb = np.array(pb)
            return np.array([pb[:, 0].max(), pb[:, 1].min()])
        return None

    @computed_field
    @property
    def non_delay_filters(self) -> list:
        """

        :return: all the non-time_delay filters as a list

        """
        non_delay_filters = [x for x in self.filters_list if x.type != "time delay"]
        return non_delay_filters

    @computed_field
    @property
    def delay_filters(self) -> list[TimeDelayFilter]:
        """

        :return: all the time delay filters as a list

        """
        delay_filters = [x for x in self.filters_list if x.type == "time delay"]
        return delay_filters

    @computed_field
    @property
    def total_delay(self) -> float:
        """

        :return: the total delay of all filters

        """
        delay_filters = self.delay_filters
        total_delay = 0.0
        for delay_filter in delay_filters:
            total_delay += delay_filter.delay
        return total_delay

    def get_indices_of_filters_to_remove(
        self, include_decimation=False, include_delay=False
    ):
        indices = list(np.arange(len(self.filters_list)))

        if not include_delay:
            indices = [i for i in indices if self.filters_list[i].type != "time delay"]

        if not include_decimation:
            indices = [i for i in indices if not self.filters_list[i].decimation_active]

        return indices

    def get_list_of_filters_to_remove(
        self, include_decimation=False, include_delay=False
    ):
        """

        :param include_decimation: bool
        :param include_delay: bool
        :return:

        # Experimental snippet if we want to allow filters with the opposite convention
        # into channel response -- I don't think we do.
        # if self.correction_operation == "multiply":
        #     inverse_filters = [x.inverse() for x in self.filters_list]
        #     self.filters_list = inverse_filters
        """
        indices = self.get_indices_of_filters_to_remove(
            include_decimation=include_decimation, include_delay=include_delay
        )
        return [self.filters_list[i] for i in indices]

    def complex_response(
        self,
        frequencies=None,
        filters_list=None,
        include_decimation=False,
        include_delay=False,
        normalize=False,
        **kwargs,
    ):
        """
        Computes the complex response of self.
        Allows the user to optionally supply a subset of filters

        :param frequencies: frequencies to compute complex response,
         defaults to None
        :type frequencies: np.ndarray, optional
        :param include_delay: include delay in complex response,
         defaults to False
        :type include_delay: bool, optional
        :param include_decimation: Include decimation in response,
         defaults to True
        :type include_decimation: bool, optional
        :param normalize: normalize the response to 1, defaults to False
        :type normalize: bool, optional
        :return: complex response along give frequency array
        :rtype: np.ndarray

        """
        if frequencies is not None:
            self.frequencies = frequencies

        # make filters list if not supplied
        if filters_list is None:
            logger.warning(
                "Filters list not provided, building list assuming all are applied"
            )
            filters_list = self.get_list_of_filters_to_remove(
                include_decimation=include_decimation,
                include_delay=include_delay,
            )

        if len(filters_list) == 0:
            logger.warning(f"No filters associated with {self.__class__}, returning 1")
            return np.ones(len(self.frequencies), dtype=complex)

        # define the product of all filters as the total response function
        result = filters_list[0].complex_response(self.frequencies)
        for ff in filters_list[1:]:
            result *= ff.complex_response(self.frequencies)

        if normalize:
            result /= np.max(np.abs(result))
        return result

    def compute_instrument_sensitivity(self, normalization_frequency=None, sig_figs=6):
        """
        Compute the StationXML instrument sensitivity for the given normalization frequency

        :param normalization_frequency: DESCRIPTION
        :type normalization_frequency: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if normalization_frequency is not None:
            self.normalization_frequency = normalization_frequency
        sensitivity = 1.0
        for mt_filter in self.filters_list:
            complex_response = mt_filter.complex_response(self.normalization_frequency)
            sensitivity *= complex_response.astype(complex)
        try:
            sensitivity = np.abs(sensitivity[0])
        except (IndexError, TypeError):
            sensitivity = np.abs(sensitivity)

        if sensitivity == 0.0:
            logger.warning(
                "Sensitivity is zero, cannot compute instrument sensitivity. "
                "Returning 1.0"
            )
            return 1.0
        if np.isnan(sensitivity):
            logger.warning("Sensitivity is NaN, setting to 1.0")
            sensitivity = 1.0
        return round(sensitivity, sig_figs - int(np.floor(np.log10(abs(sensitivity)))))

    def compute_total_gain(self, sig_figs=16):
        """
        Computing the total sensitivity seems to be different than just adding all the gains together.
        Overall the total sensitivity is useless for MT cause they don't have the ability to use the units.
        So if a person downloads data from the DMC, they will simply use the filters provided.

        Parameters
        ----------
        sig_figs : int, optional
            _description_, by default 6

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        ValueError
            _description_
        """
        total_gain = 1
        for mt_filter in self.filters_list:
            total_gain *= mt_filter.gain

        return round(total_gain, sig_figs - int(np.floor(np.log10(abs(total_gain)))))

    @requires(obspy=inventory)
    def to_obspy(self, sample_rate=1):
        """
        Output :class:`obspy.core.inventory.InstrumentSensitivity` object that
        can be used in a stationxml file.

        :param normalization_frequency: DESCRIPTION
        :type normalization_frequency: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        total_sensitivity = self.compute_instrument_sensitivity()
        total_gain = self.compute_total_gain()

        if total_sensitivity != total_gain:
            logger.info(
                f"total sensitivity {total_sensitivity} != total gain {total_gain}. Using total_gain."
            )
            total_sensitivity = total_gain

        units_in_obj = get_unit_object(self.units_in)
        units_out_obj = get_unit_object(self.units_out)

        total_response = inventory.Response()
        total_response.instrument_sensitivity = inventory.InstrumentSensitivity(
            total_sensitivity,
            self.normalization_frequency,
            units_in_obj.symbol,
            units_out_obj.symbol,
            input_units_description=units_in_obj.name,
            output_units_description=units_out_obj.name,
        )

        for ii, f in enumerate(self.filters_list, 1):
            if f.type in ["coefficient"]:
                if f.units_out not in ["count", "digital counts"]:
                    logger.debug(f"converting CoefficientFilter {f.name} to PZ")
                    pz = PoleZeroFilter()
                    pz.gain = f.gain
                    pz.units_in = f.units_in
                    pz.units_out = f.units_out
                    pz.comments = f.comments
                    pz.name = f.name
                else:
                    pz = f

                total_response.response_stages.append(
                    pz.to_obspy(
                        stage_number=ii,
                        normalization_frequency=self.normalization_frequency,
                        sample_rate=sample_rate,
                    )
                )
            else:
                total_response.response_stages.append(
                    f.to_obspy(
                        stage_number=ii,
                        normalization_frequency=self.normalization_frequency,
                        sample_rate=sample_rate,
                    )
                )

        return total_response

    def plot_response(
        self,
        frequencies=None,
        x_units="period",
        unwrap=True,
        pb_tol=1e-1,
        interpolation_method="slinear",
        include_delay=False,
        include_decimation=False,
    ):
        """
        Plot the response

        :param frequencies: frequencies to compute response, defaults to None
        :type frequencies: np.ndarray, optional
        :param x_units: [ period | frequency ], defaults to "period"
        :type x_units: string, optional
        :param unwrap: Unwrap phase, defaults to True
        :type unwrap: bool, optional
        :param pb_tol: pass band tolerance, defaults to 1e-1
        :type pb_tol: float, optional
        :param interpolation_method: Interpolation method see scipy.signal.interpolate
         [ slinear | nearest | cubic | quadratic | ], defaults to "slinear"
        :type interpolation_method: string, optional
        :param include_delay: include delays in response, defaults to False
        :type include_delay: bool, optional
        :param include_decimation: Include decimation in response,
         defaults to True
        :type include_decimation: bool, optional

        """

        if frequencies is not None:
            self.frequencies = frequencies

        # get only the filters desired
        if include_delay:
            filters_list = deepcopy(self.filters_list)
        else:
            filters_list = deepcopy(self.non_delay_filters)

        if not include_decimation:
            filters_list = deepcopy(
                [x for x in filters_list if not x.decimation_active]
            )

        cr_kwargs = {"interpolation_method": interpolation_method}

        # get response of individual filters
        cr_list = [
            f.complex_response(self.frequencies, **cr_kwargs) for f in filters_list
        ]

        # compute total response
        cr_kwargs["include_delay"] = include_delay
        cr_kwargs["include_decimation"] = include_decimation
        complex_response = self.complex_response(self.frequencies, **cr_kwargs)

        cr_list.append(complex_response)
        labels = [f.name for f in filters_list] + ["Total Response"]

        # plot with proper attributes.
        kwargs = {
            "title": f"Channel Response: [{', '.join([f.name for f in filters_list])}]",
            "unwrap": unwrap,
            "x_units": x_units,
            "pass_band": self.pass_band,
            "label": labels,
            "normalization_frequency": self.normalization_frequency,
        }

        plot_response(self.frequencies, cr_list, **kwargs)
