# =====================================================
# Imports
# =====================================================
from loguru import logger
from typing import Annotated

from pydantic import Field, computed_field, field_validator, ValidationInfo, PrivateAttr

from mt_metadata.timeseries.filters import FilterBase, get_base_obspy_mapping

import matplotlib.pyplot as plt
import numpy as np

from mt_metadata.base.helpers import requires

try:
    from obspy.core.inventory.response import FIRResponseStage
except ImportError:
    FIRResponseStage = None
import scipy.signal as signal

from mt_metadata.common import SymmetryEnum


# =====================================================


class FIRFilter(FilterBase):
    _filter_type: str = PrivateAttr("fir")
    type: Annotated[
        str,
        Field(
            default="fir",
            description="Type of filter.  Must be 'fir'",
            examples="fir",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]
    coefficients: Annotated[
        np.ndarray | list[float],
        Field(
            default_factory=lambda: np.empty(0),
            items={"type": "number"},
            description="The FIR coefficients associated with the filter stage response.",
            examples='"[0.25, 0.5, 0.25]"',
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    decimation_factor: Annotated[
        float,
        Field(
            default=1.0,
            description="Downsample factor.",
            examples="16",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    decimation_input_sample_rate: Annotated[
        float,
        Field(
            default=1.0,
            description="Sample rate of FIR taps.",
            examples="2000",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @computed_field
    @property
    def output_sampling_rate(self) -> float:
        return self.decimation_input_sample_rate / self.decimation_factor

    gain_frequency: Annotated[
        float,
        Field(
            default=0.0,
            description="Frequency of the reference gain, usually in passband.",
            examples="0.0",
            alias=None,
            json_schema_extra={
                "units": "hertz",
                "required": True,
            },
        ),
    ]

    symmetry: Annotated[
        SymmetryEnum,
        Field(
            default="NONE",
            description="Symmetry of FIR coefficients",
            examples="NONE",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("coefficients")
    @classmethod
    def validate_coefficients(
        cls, value: list[float], info: ValidationInfo
    ) -> list[float]:
        """
        Validate the coefficients to ensure they are a list of floats.
        :param value: The value to validate.
        :param info: Validation information.
        :return: The validated value.
        """
        if isinstance(value, (list, tuple, np.ndarray)):
            return np.array(value, dtype=float)
        elif isinstance(value, str):
            return np.array(value.split(","), dtype=float)
        else:
            raise ValueError("Coefficients must be a list, tuple, or string.")

    def make_obspy_mapping(self):
        mapping = get_base_obspy_mapping()
        mapping["_symmetry"] = "symmetry"
        mapping["_coefficients"] = "coefficients"
        mapping["decimation_factor"] = "decimation_factor"
        mapping["decimation_input_sample_rate"] = "decimation_input_sample_rate"
        mapping["stage_gain_frequency"] = "gain_frequency"
        return mapping

    @property
    def symmetry_corrected_coefficients(self):
        if self.symmetry == "EVEN":
            return np.hstack((self.coefficients, np.flipud(self.coefficients)))
        elif self.symmetry == "ODD":
            return np.hstack((self.coefficients, np.flipud(self.coefficients[1:])))
        else:
            return self.coefficients

    @property
    def coefficient_gain(self):
        """
        The gain at the reference frequency due only to the coefficients
        Sometimes this is different from the gain in the stationxml and a
        corrective scalar must be applied
        """
        if self.gain_frequency == 0.0:
            coefficient_gain = self.symmetry_corrected_coefficients.sum()
        else:
            # estimate the gain from the coefficeints at gain_frequency
            ww, hh = signal.freqz(
                self.symmetry_corrected_coefficients,
                worN=2 * np.pi * self.gain_frequency,
                fs=2 * np.pi * self.decimation_input_sample_rate,
            )
            coefficient_gain = np.abs(hh)
        return coefficient_gain

    @property
    def n_coefficients(self):
        return len(self.coefficients)

    @property
    def corrective_scalar(self):
        """ """
        if self.coefficient_gain != self.gain:
            return self.coefficient_gain / self.total_gain
        else:
            return 1.0

    def plot_fir_response(self):
        w, h = signal.freqz(self.full_coefficients)
        fig = plt.figure()
        plt.title("Digital filter frequency response")
        ax1 = fig.add_subplot(111)
        plt.plot(w, 20 * np.log10(abs(h)), "b")
        plt.ylabel("Amplitude [dB]", color="b")
        plt.xlabel("Frequency [rad/sample]")

        ax2 = ax1.twinx()
        angles = np.unwrap(np.angle(h))
        plt.plot(w, angles, "g")
        plt.ylabel("Angle (radians)", color="g")
        plt.grid()
        plt.axis("tight")
        plt.show()

        return fig

    @requires(obspy=FIRResponseStage)
    def to_obspy(
        self,
        stage_number=1,
        normalization_frequency=1,
        sample_rate=1,
    ):
        """
        create an obspy stage

        :return: DESCRIPTION
        :rtype: TYPE

        """

        rs = FIRResponseStage(
            stage_number,
            self.gain,
            normalization_frequency,
            self.units_in,
            self.units_out,
            normalization_frequency,
            self.coefficients,
            name=self.name,
            description=self.get_filter_description(),
            input_units_description=self._units_in_obj.name,
            output_units_description=self._units_out_obj.name,
        )

        return rs

    def unscaled_complex_response(self, frequencies):
        """
        need this to avoid RecursionError.
        The problem is that some FIRs need a scale factor to make their gains be
        the same as those reported in the stationXML.  The pure coefficients
        themselves sometimes result in pass-band gains that differ from the
        gain in the XML.  For example filter fs2d5 has a passband gain of 0.5
        based on the coefficients alone, but the cited gain in the xml is
        almost 1.

        I wanted to scale the coefficients so they equal the gain... but maybe
        we can add the gain in complex response
        :param frequencies:
        :return:
        """
        angular_frequencies = 2 * np.pi * frequencies
        w, h = signal.freqz(
            self.symmetry_corrected_coefficients,
            worN=angular_frequencies,
            fs=2 * np.pi * self.decimation_input_sample_rate,
        )
        return h

    def complex_response(self, frequencies, **kwargs):
        """

        Parameters
        ----------
        frequencies: numpy array of frequencies, expected in Hz

        Returns
        -------
        h : numpy array of (possibly complex-valued) frequency response at the input frequencies

        """
        # fir_filter.full_coefficients
        angular_frequencies = 2 * np.pi * frequencies
        w, h = signal.freqz(
            self.symmetry_corrected_coefficients,
            worN=angular_frequencies,
            fs=2 * np.pi * self.decimation_input_sample_rate,
        )
        h /= self.corrective_scalar

        return h
