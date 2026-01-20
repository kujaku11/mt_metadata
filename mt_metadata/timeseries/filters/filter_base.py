# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
from loguru import logger
from pydantic import computed_field, Field, field_validator, PrivateAttr, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.base.helpers import filter_descriptions, requires
from mt_metadata.common import Comment
from mt_metadata.common.mttime import MTime
from mt_metadata.common.units import get_unit_object, Unit
from mt_metadata.timeseries.filters.plotting_helpers import plot_response

try:
    from obspy.core.inventory.response import ResponseListResponseStage, ResponseStage

    obspy_import = True
except ImportError:
    ResponseListResponseStage = None
    ResponseStage = None
    obspy_import = False


# =====================================================


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
    mapping["stage_sequence_number"] = "sequence_number"
    return mapping


class FilterBase(MetadataBase):
    _obspy_mapping: dict = PrivateAttr({})
    _filter_type: str = PrivateAttr("base")
    name: Annotated[
        str,
        Field(
            default="",
            description="Name of filter applied or to be applied. If more than one filter input as a comma separated list.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": '"lowpass_magnetic"',
            },
        ),
    ]

    comments: Annotated[
        Comment,
        Field(
            default_factory=lambda: Comment(),
            description="Any comments about the filter.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "ambient air temperature",
            },
        ),
    ]

    type: Annotated[
        str,
        Field(
            default="base",
            description="Type of filter, must be one of the available filters.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "fap_table",
            },
        ),
    ]

    units_in: Annotated[
        str,
        Field(
            default="",
            description="Name of the input units to the filter. Should be all lowercase and separated with an underscore, use 'per' if units are divided and '-' if units are multiplied.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "count",
            },
        ),
    ]

    units_out: Annotated[
        str,
        Field(
            default="",
            description="Name of the output units.  Should be all lowercase and separated with an underscore, use 'per' if units are divided and '-' if units are multiplied.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "millivolt",
            },
        ),
    ]

    calibration_date: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Most recent date of filter calibration in ISO format of YYY-MM-DD.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": "2020-01-01",
            },
        ),
    ]

    gain: Annotated[
        float,
        Field(
            default=1.0,
            description="scalar gain of the filter across all frequencies, producted with any frequency depenendent terms",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": "1.0",
            },
        ),
    ]

    sequence_number: Annotated[
        int,
        Field(
            default=0,
            description="Sequence number of the filter in the processing chain.",
            alias=None,
            ge=0,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": 1,
            },
        ),
    ]

    @field_validator("calibration_date", mode="before")
    @classmethod
    def validate_calibration_date(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        return MTime(time_stamp=field_value)

    @field_validator("comments", mode="before")
    @classmethod
    def validate_comments(cls, value, info: ValidationInfo) -> Comment:
        if isinstance(value, str):
            return Comment(value=value)
        return value

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, value, info: ValidationInfo) -> str:
        """
        Validate that the type of filter is set to "fir"
        """
        # Get the expected filter type based on the actual class
        # Make sure derived classes define their own _filter_type as class variable
        expected_type = getattr(cls, "_filter_type", "base").default

        if value != expected_type:
            logger.warning(
                f"Filter type is set to {value}, but should be "
                f"{expected_type} for {cls.__name__}."
            )
        return expected_type

    @field_validator("units_in", "units_out", mode="before")
    @classmethod
    def validate_units(cls, value: str, info: ValidationInfo) -> str:
        """
        validate units base on input string will return the long name

        Parameters
        ----------
        value : units string
            unit string separated by either '/' for division or ' ' for
            multiplication.  Or 'per' and ' ', respectively
        info : ValidationInfo
            _description_

        Returns
        -------
        str
            return the long descriptive name of the unit. For example 'kilometers'.
        """

        try:
            unit_object = get_unit_object(value, allow_none=False)
            return unit_object.name
        except ValueError as error:
            raise KeyError(error)
        except KeyError as error:
            raise KeyError(error)

    @property
    def units_in_object(self) -> Unit:
        return get_unit_object(self.units_in, allow_none=False)

    @property
    def units_out_object(self) -> Unit:
        return get_unit_object(self.units_out, allow_none=False)

    def make_obspy_mapping(self):
        mapping = get_base_obspy_mapping()
        return mapping

    @property
    def obspy_mapping(self):
        """

        :return: mapping to an obspy filter
        :rtype: dict

        """
        if self._obspy_mapping == {}:
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
            logger.error(msg)
            raise TypeError(msg)

        self._obspy_mapping = obspy_dict

    @computed_field
    @property
    def total_gain(self) -> float:
        """

        :return: Total gain of the filter
        :rtype: float

        """
        return self.gain

    def get_filter_description(self):
        """

        :return: predetermined filter description based on the
            type of filter
        :rtype: string

        """

        if self.comments.value is None:
            return filter_descriptions[self.type]

        return self.comments

    @requires(obspy=obspy_import)
    @classmethod
    def from_obspy_stage(
        cls,
        stage,  #   : Union[ResponseStage, ResponseListResponseStage],
        mapping: dict = None,
    ) -> "FilterBase":
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

        if mapping is None:
            mapping = cls().make_obspy_mapping()
        kwargs = {"name": ""}

        if not isinstance(stage, (ResponseListResponseStage, ResponseStage)):
            msg = f"Expected a ResponseStage and got a {type(stage)}"
            logger.error(msg)
            raise TypeError(msg)

        if isinstance(stage, ResponseListResponseStage):
            frequencies = []
            amplitudes = []
            phases = []
            for element in stage.response_list_elements:
                frequencies.append(element.frequency)
                amplitudes.append(element.amplitude)
                phases.append(element.phase)
            kwargs["frequencies"] = np.array(frequencies)
            kwargs["amplitudes"] = np.array(amplitudes)
            kwargs["phases"] = np.array(phases)

        for obspy_label, mth5_label in mapping.items():
            if obspy_label in ["amplitudes", "phases", "frequencies"]:
                continue
            if mth5_label == "comments" or obspy_label == "description":
                kwargs[mth5_label] = Comment(value=getattr(stage, obspy_label))
            else:
                try:
                    kwargs[mth5_label] = getattr(stage, obspy_label)

                except AttributeError:
                    logger.warning(
                        f"Attribute {obspy_label} not found in stage object, skipping."
                    )
            if kwargs.get("name") is None:
                kwargs["name"] = ""
        return cls(**kwargs)

    def complex_response(self, frqs):
        msg = f"complex_response not defined for {self.__class__.__name__} class"
        logger.info(msg)
        return None

    def pass_band(
        self, frequencies: np.ndarray, window_len: int = 5, tol: float = 0.5, **kwargs
    ) -> np.ndarray:
        """
        Fast passband estimation using decimation (10-100x faster than original).

        Caveat: This should work for most Fluxgate and feedback coil magnetometers, and basically most filters
        having a "low" number of poles and zeros.  This method is not 100% robust to filters with a notch in them.

        Try to estimate pass band of the filter from the flattest spots in
        the amplitude. Instead of checking every frequency point, this decimates the
        frequency array and only checks a subset of windows. The pass band
        region is then interpolated across the full array.

        The flattest spot is determined by calculating a sliding window
        with length `window_len` and estimating normalized std.

        ..note:: This only works for simple filters with on flat pass band.

        :param frequencies: array of frequencies
        :type frequencies: np.ndarray

        :param window_len: length of sliding window in points
        :type window_len: integer

        :param tol: the ratio of the mean/std should be around 1
         tol is the range around 1 to find the flat part of the curve.
        :type tol: float

        :return: pass band frequencies [f_start, f_end]
        :rtype: np.ndarray or None

        """

        f = np.array(frequencies)
        if f.size == 0:
            logger.warning("Frequency array is empty, returning None")
            return None
        elif f.size == 1:
            logger.warning("Frequency array is too small, returning None")
            return f

        cr = self.complex_response(f, **kwargs)
        if cr is None:
            logger.warning(
                "complex response is None, cannot estimate pass band. Returning None"
            )
            return None

        amp = np.abs(cr)

        # precision is apparently an important variable here
        if np.round(amp, 6).all() == np.round(amp.mean(), 6):
            return np.array([f.min(), f.max()])

        # Decimate frequency array for faster processing
        # If array is large, sample every Nth point
        decimate_factor = max(1, f.size // 1000)  # Keep ~1000 points for analysis
        if decimate_factor > 1:
            f_dec = f[::decimate_factor]
            amp_dec = amp[::decimate_factor]
        else:
            f_dec = f
            amp_dec = amp

        n_windows = f_dec.size - window_len
        if n_windows <= 0:
            return np.array([f.min(), f.max()])

        # Vectorized window analysis on decimated array
        try:
            from numpy.lib.stride_tricks import as_strided

            shape = (n_windows, window_len)
            strides = (amp_dec.strides[0], amp_dec.strides[0])
            amp_windows = as_strided(amp_dec, shape=shape, strides=strides)

            window_mins = np.min(amp_windows, axis=1)
            window_maxs = np.max(amp_windows, axis=1)

            with np.errstate(divide="ignore", invalid="ignore"):
                ratios = np.log10(window_mins) / np.log10(window_maxs)
                ratios = np.nan_to_num(ratios, nan=np.inf)
                test_values = np.abs(1 - ratios)

            passing_windows = test_values <= tol

            if not passing_windows.any():
                # If no windows pass, return full frequency range
                return np.array([f.min(), f.max()])

            # Find first and last passing windows
            passing_indices = np.where(passing_windows)[0]
            start_idx = passing_indices[0]
            end_idx = passing_indices[-1] + window_len

            # Map back to original frequency array
            start_freq_idx = start_idx * decimate_factor
            end_freq_idx = min(end_idx * decimate_factor, f.size - 1)

            return np.array([f[start_freq_idx], f[end_freq_idx]])

        except Exception as e:
            logger.debug(f"Decimated passband method failed: {e}, returning full range")
            return np.array([f.min(), f.max()])

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
