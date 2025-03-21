"""
==========================
Channel Response Filter
==========================

Combines all filters for a given channel into a total response that can be used in
the frequency domain.

.. note:: Time Delay filters should be applied in the time domain
    otherwise bad things can happen.
"""

# =============================================================================
# Imports
# =============================================================================
from copy import deepcopy
import numpy as np

from mt_metadata.base import Base, get_schema
from mt_metadata.base.helpers import requires
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS
from mt_metadata.timeseries.filters import (
    PoleZeroFilter,
    CoefficientFilter,
    TimeDelayFilter,
    FrequencyResponseTableFilter,
    FIRFilter,
)

from mt_metadata.utils.units import get_unit_object
from mt_metadata.timeseries.filters.plotting_helpers import plot_response
try:
    from obspy.core import inventory
except ImportError:
    inventory = None

# =============================================================================
attr_dict = get_schema("channel_response", SCHEMA_FN_PATHS)
# =============================================================================


class ChannelResponse(Base):
    """
    This class holds a list of all the filters associated with a channel.
    The list should be ordered to match the order in which the filters are applied to the signal.

    It has methods for combining the responses of all the filters into a total
    response that we will apply to a data segment.
    """

    def __init__(self, **kwargs):
        self.filters_list = []
        self.frequencies = np.logspace(-4, 4, 100)
        self.normalization_frequency = None

        super().__init__(attr_dict=attr_dict)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        lines = ["Filters Included:\n", "=" * 25, "\n"]
        for f in self.filters_list:
            lines.append(f.__str__())
            lines.append(f"\n{'-'*20}\n")

        return "".join(lines)

    def __repr__(self):
        return self.__str__()

    @property
    def filters_list(self):
        """filters list"""
        return self._filters_list

    @filters_list.setter
    def filters_list(self, filters_list):
        """set the filters list and validate the list"""
        self._filters_list = self._validate_filters_list(filters_list)
        self._check_consistency_of_units()

    @property
    def frequencies(self):
        """frequencies to estimate filters"""
        return self._frequencies

    @frequencies.setter
    def frequencies(self, value):
        """
        Set the frequencies, make sure the input is validated

        Linear frequencies
        :param value: Linear Frequencies
        :type value: iterable

        """
        if value is None:
            self._frequencies = None

        elif isinstance(value, (list, tuple, np.ndarray)):
            self._frequencies = np.array(value, dtype=float)
        else:
            msg = f"input values must be an list, tuple, or np.ndarray, not {type(value)}"
            self.logger.error(msg)
            raise TypeError(msg)

    @property
    def names(self):
        """names of the filters"""
        names = []
        if self.filters_list:
            names = [f.name for f in self.filters_list]
        return names

    def _validate_filters_list(self, filters_list):
        """
        make sure the filters list is valid.

        :param filters_list: DESCRIPTION
        :type filters_list: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        supported_filters = [
            PoleZeroFilter,
            CoefficientFilter,
            TimeDelayFilter,
            FrequencyResponseTableFilter,
            FIRFilter,
        ]

        def is_supported_filter(item):
            if isinstance(item, tuple(supported_filters)):
                return True
            else:
                return False

        if filters_list in [[], None]:
            return []

        if not isinstance(filters_list, list):
            msg = f"Input filters list must be a list not {type(filters_list)}"
            self.logger.error(msg)
            raise TypeError(msg)

        fails = []
        return_list = []
        for item in filters_list:
            if is_supported_filter(item):
                return_list.append(item)
            else:
                fails.append(
                    f"Item is not a supported filter type, {type(item)}"
                )

        if fails:
            raise TypeError(", ".join(fails))

        return return_list

    @property
    def pass_band(self):
        """estimate pass band for all filters in frequency"""
        if self.frequencies is None:
            raise ValueError(
                "frequencies are None, must be input to calculate pass band"
            )
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

    @property
    def normalization_frequency(self):
        """get normalization frequency from ZPK or FAP filter"""

        if self._normalization_frequency in [0.0, None]:
            if self.pass_band is not None:
                return np.round(10 ** np.mean(np.log10(self.pass_band)), 3)

        return self._normalization_frequency

    @normalization_frequency.setter
    def normalization_frequency(self, value):
        """Set normalization frequency if input"""

        self._normalization_frequency = value

    @property
    def non_delay_filters(self):
        """

        :return: all the non-time_delay filters as a list

        """
        non_delay_filters = [
            x for x in self.filters_list if x.type != "time delay"
        ]
        return non_delay_filters

    @property
    def delay_filters(self):
        """

        :return: all the time delay filters as a list

        """
        delay_filters = [x for x in self.filters_list if x.type == "time delay"]
        return delay_filters

    @property
    def total_delay(self):
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
            indices = [
                i for i in indices if self.filters_list[i].type != "time delay"
            ]

        if not include_decimation:
            indices = [
                i for i in indices if not self.filters_list[i].decimation_active
            ]

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
            self.logger.warning(
                "Filters list not provided, building list assuming all are applied"
            )
            filters_list = self.get_list_of_filters_to_remove(
                include_decimation=include_decimation,
                include_delay=include_delay,
            )

        if len(filters_list) == 0:
            self.logger.warning(
                f"No filters associated with {self.__class__}, returning 1"
            )
            return np.ones(len(self.frequencies), dtype=complex)

        # define the product of all filters as the total response function
        result = filters_list[0].complex_response(self.frequencies)
        for ff in filters_list[1:]:
            result *= ff.complex_response(self.frequencies)

        if normalize:
            result /= np.max(np.abs(result))
        return result

    def compute_instrument_sensitivity(
        self, normalization_frequency=None, sig_figs=6
    ):
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
            complex_response = mt_filter.complex_response(
                self.normalization_frequency
            )
            sensitivity *= complex_response.astype(complex)
        try:
            sensitivity = np.abs(sensitivity[0])
        except (IndexError, TypeError):
            sensitivity = np.abs(sensitivity)

        return round(
            sensitivity, sig_figs - int(np.floor(np.log10(abs(sensitivity))))
        )

    @property
    def units_in(self):
        """
        :return: the units of the channel
        """
        if self.filters_list is [] or len(self.filters_list) == 0:
            return None
        else:
            return self.filters_list[0].units_in

    @property
    def units_out(self):
        """
        :return: the units of the channel
        """
        if self.filters_list is [] or len(self.filters_list) == 0:
            return None
        else:
            return self.filters_list[-1].units_out

    def _check_consistency_of_units(self):
        """
        confirms that the input and output units of each filter state are consistent
        """
        if len(self._filters_list) > 1:
            previous_units = self._filters_list[0].units_out
            for mt_filter in self._filters_list[1:]:
                if mt_filter.units_in != previous_units:
                    msg = (
                        "Unit consistency is incorrect. "
                        f"The input units for {mt_filter.name} should be "
                        f"{previous_units} not {mt_filter.units_in}"
                    )
                    self.logger.error(msg)
                    raise ValueError(msg)
                previous_units = mt_filter.units_out

        return True

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

        units_in_obj = get_unit_object(self.units_in)
        units_out_obj = get_unit_object(self.units_out)

        total_response = inventory.Response()
        total_response.instrument_sensitivity = inventory.InstrumentSensitivity(
            total_sensitivity,
            self.normalization_frequency,
            units_in_obj.abbreviation,
            units_out_obj.abbreviation,
            input_units_description=units_in_obj.name,
            output_units_description=units_out_obj.name,
        )

        for ii, f in enumerate(self.filters_list, 1):
            if f.type in ["coefficient"]:
                if f.units_out not in ["count"]:
                    self.logger.debug(
                        f"converting CoefficientFilter {f.name} to PZ"
                    )
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
            f.complex_response(self.frequencies, **cr_kwargs)
            for f in filters_list
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
