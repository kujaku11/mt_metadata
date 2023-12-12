# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright:
    Jared Peacock (jpeacock@usgs.gov)
    Karl Kappler

:license: MIT

This is a base class for filters associated with calibration and instrument
and acquistion system responses. We will extend this class for each specific
type of filter we need to implement. Typical filters we will want to support:

 - PoleZero (or 'zpk') responses like those provided by IRIS
 - Frequency-Amplitude-Phase (FAP) tables: look up tables from laboratory
   calibrations via frequency sweep on a spectrum analyser.
 - Time Delay Filters: can come about in decimation, or from general
   timing errors that have been characterized
 - Coefficient multipliers, i.e. frequency independent gains
 - FIR filters
 - IIR filters

Many filters can be represented in more than one of these forms. For example
a Coefficient Multiplier can be seen as an FIR with a single coefficient.
Similarly, an FIR can be represented as a 'zpk' filter with no poles.  An
IIR filter can also be associated with a zpk representation.  However, solving
for the 'zpk' representation can be tedious and approximate and if we have for
example, the known FIR coefficients, or FAP lookup table, then there is little
to be gained by changing the representation.

The 'stages' that are described in the IRIS StationXML documentation appear
to cover all possible linear time invariant filter types we are likely to
encounter.

A FilterBase object has a direction, defined by has units_in and units_out attrs.
These are the units before and after multiplication by the complex_response
of the filter in frequency domain.  It is very similar to an "obspy filter stage"

"""
# =============================================================================
# Imports
# =============================================================================
import copy
import obspy
import numpy as np

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.base.helpers import filter_descriptions
from mt_metadata.utils.units import get_unit_object, Unit
from mt_metadata.timeseries.filters.plotting_helpers import plot_response
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS
from mt_metadata.utils.mttime import MTime


# =============================================================================
attr_dict = get_schema("filter_base", SCHEMA_FN_PATHS)
# =============================================================================

def get_base_obspy_mapping():
    """
    Different filters have different mappings, but the attributes mapped here are common to all of them.
    Hence the name "base obspy mapping"
    Note: If we wanted to support inverse forms of these filters, and argument specifying filter direction could be added.

    :return: mapping to an obspy filter, mapping['obspy_label'] = 'mt_metadata_label'
    :rtype: dict
    """
    mapping = {}
    mapping["description"] = "comments"
    mapping["name"] = "name"
    mapping["stage_gain"] = "gain"
    mapping["input_units"] = "units_in"
    mapping["output_units"] = "units_out"
    return mapping


class FilterBase(Base):
    """
    bstract base class is used to represent various forms of linear, time invariant (LTI) filters.
    By convention, forward application of the filter is equivalent to multiplication in frequency domain by the
    filter's complex response.  Removing the filter (applying the inverse) can be achieved by divding by the
    filter's complex response.

    This class is intended to support the calibration of data from archived units to physical units, although
    it may find more application in future.

    """
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._units_in_obj = Unit()
        self._units_out_obj = Unit()

        self._calibration_dt = MTime()
        self.comments = None
        self._obspy_mapping = None
        self.gain = 1.0

        super().__init__(attr_dict=attr_dict, **kwargs)

        if self.gain == 0.0:
            self.gain = 1.0

    def make_obspy_mapping(self):
        mapping = get_base_obspy_mapping()
        return mapping

    @property
    def obspy_mapping(self):
        """

        :return: mapping to an obspy filter
        :rtype: dict

        """
        if self._obspy_mapping is None:
            self._obspy_mapping = self.make_obspy_mapping()
        return self._obspy_mapping

    @obspy_mapping.setter
    def obspy_mapping(self, obspy_dict):
        """
        set the obspy mapping: this is a dictionary relating attribute labels from obspy stage objects to
        mt_metadata filter objects.
        """
        if not isinstance(obspy_dict, dict):
            msg = f"Input must be a dictionary not {type(obspy_dict)}"
            self.logger.error(msg)
            raise TypeError(msg)

        self._obspy_mapping = obspy_dict

    @property
    def name(self):
        """

        :return: name of the filter
        :rtype: str

        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set filter name

        :param value: name of filter
        :type value: sting

        """
        if value is not None:
            self._name = str(value).lower().replace("/", " per ")
        else:
            self._name = None


    @property
    def calibration_date(self):
        """

        :return: calibration date (YYYY-MM-DD)
        :rtype: string

        """
        return self._calibration_dt.date

    @calibration_date.setter
    def calibration_date(self, value):
        """

        :param value: set calibration date (YYYY-MM-DD)
        :type value: string

        """
        self._calibration_dt.parse(value)

    @property
    def total_gain(self):
        """

        :return: Total gain of the filter
        :rtype: float

        """
        return self.gain

    @property
    def units_in(self):
        """

        :return: Input units of the filter
        :rtype: string

        """
        return self._units_in_obj.abbreviation

    @units_in.setter
    def units_in(self, value):
        """

        :param value: input units of the filter
        :type value: string

        """
        self._units_in_obj = get_unit_object(value)

    @property
    def units_out(self):
        """

        :return: Output units of the filter
        :rtype: string

        """
        return self._units_out_obj.abbreviation

    @units_out.setter
    def units_out(self, value):
        """

        :param value: output units of the filter
        :type value: string

        """
        self._units_out_obj = get_unit_object(value)

    def get_filter_description(self):
        """

        :return: predetermined filter description based on the
            type of filter
        :rtype: string

        """

        if self.comments is None:
            return filter_descriptions[self.type]

        return self.comments

    @classmethod
    def from_obspy_stage(cls, stage, mapping=None):
        """
        Expected to return a multiply operation function

        :param cls: a filter object
        :type cls: filter object
        :param stage: Obspy stage filter
        :type stage: :class:`obspy.inventory.response.ResponseStage`
        :param mapping: dictionary for mapping from an obspy stage,
            defaults to None
        :type mapping: dict, optional
        :raises TypeError: If stage is not a
            :class:`obspy.inventory.response.ResponseStage`
        :return: the appropriate mt_metadata.timeseries.filter object
        :rtype: mt_metadata.timeseries.filter object

        """

        if not isinstance(stage, obspy.core.inventory.response.ResponseStage):
            msg = f"Expected a Stage and got a {type(stage)}"
            cls.logger.error(msg)
            raise TypeError(msg)

        if mapping is None:
            mapping = cls().make_obspy_mapping()
        kwargs = {}
        for obspy_label, mth5_label in mapping.items():
            try:
                kwargs[mth5_label] = stage.__dict__[obspy_label]
            except KeyError:
                print(f"Key {obspy_label} not found in stage object")
                raise Exception
        return cls(**kwargs)

    def complex_response(self, frqs):
        msg = f"complex_response not defined for {self._class_name} class"
        self.logger.info(msg)
        return None

    def pass_band(self, frequencies, window_len=5, tol=0.5, **kwargs):
        """

        Caveat: This should work for most Fluxgate and feedback coil magnetometers, and basically most filters
        having a "low" number of poles and zeros.  This method is not 100% robust to filters with a notch in them.

        Try to estimate pass band of the filter from the flattest spots in
        the amplitude.

        The flattest spot is determined by calculating a sliding window
        with length `window_len` and estimating normalized std.

        ..note:: This only works for simple filters with
         on flat pass band.

        :param window_len: length of sliding window in points
        :type window_len: integer

        :param tol: the ratio of the mean/std should be around 1
         tol is the range around 1 to find the flat part of the curve.
        :type tol: float

        :return: pass band frequencies
        :rtype: np.ndarray

        """

        f = frequencies
        cr = self.complex_response(f, **kwargs)
        amp = np.abs(cr)
        # precision is apparently an important variable here
        if np.round(amp, 6).all() == np.round(amp.mean(), 6):
            return np.array([f.min(), f.max()])

        f_true = np.zeros_like(frequencies)
        for ii in range(0, f.size - window_len, 1):
            cr_window = np.array(
                amp[ii : ii + window_len]
            )  # / self.amplitudes.max()
            test = abs(
                1 - np.log10(cr_window.min()) / np.log10(cr_window.max())
            )

            if test <= tol:
                f_true[(f >= f[ii]) & (f <= f[ii + window_len])] = 1

        pb_zones = np.reshape(
            np.diff(np.r_[0, f_true, 0]).nonzero()[0], (-1, 2)
        )

        if pb_zones.shape[0] > 1:
            self.logger.debug(
                f"Found {pb_zones.shape[0]} possible pass bands, using the longest. "
                "Use the estimated pass band with caution."
            )
        # pick the longest
        try:
            longest = np.argmax(np.diff(pb_zones, axis=1))
            if pb_zones[longest, 1] >= f.size:
                pb_zones[longest, 1] = f.size - 1
        except ValueError:
            self.logger.warning(
                "No pass band could be found within the given frequency range. Returning None"
            )
            return None

        return np.array([f[pb_zones[longest, 0]], f[pb_zones[longest, 1]]])

    def generate_frequency_axis(self, sampling_rate, n_observations):
        dt = 1.0 / sampling_rate
        frequency_axis = np.fft.fftfreq(n_observations, d=dt)
        frequency_axis = np.fft.fftshift(frequency_axis)
        return frequency_axis

    def plot_response(
        self,
        frequencies,
        x_units="period",
        unwrap=True,
        pb_tol=1e-1,
        interpolation_method="slinear",
    ):
        if frequencies is None:
            frequencies = self.generate_frequency_axis(10.0, 1000)
            x_units = "frequency"

        kwargs = {
            "title": self.name,
            "unwrap": unwrap,
            "x_units": x_units,
            "label": self.name,
        }

        complex_response = self.complex_response(
            frequencies, **{"interpolation_method": interpolation_method}
        )
        if hasattr(self, "poles"):
            kwargs["poles"] = self.poles
            kwargs["zeros"] = self.zeros

        if hasattr(self, "pass_band"):
            kwargs["pass_band"] = self.pass_band(
                frequencies,
                tol=pb_tol,
                **{"interpolation_method": interpolation_method},
            )

        plot_response(frequencies, complex_response, **kwargs)

    @property
    def decimation_active(self):
        """

        :return: if decimation is prescribed
        :rtype: bool

        """
        if hasattr(self, "decimation_factor"):
            if self.decimation_factor != 1.0:
                return True
        return False

