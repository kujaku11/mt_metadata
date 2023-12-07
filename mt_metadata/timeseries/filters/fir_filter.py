import matplotlib.pyplot as plt
import numpy as np
from obspy.core.inventory.response import FIRResponseStage
import scipy.signal as signal

from mt_metadata.base import get_schema
from mt_metadata.timeseries.filters.filter_base import FilterBase
from mt_metadata.timeseries.filters.filter_base import get_base_obspy_mapping
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("filter_base", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("fir_filter", SCHEMA_FN_PATHS))
# =============================================================================



class FIRFilter(FilterBase):
    """
    Note: Regarding the symmetery property the json standard indicates that
    we expect the values "NONE", "ODD", "EVEN".  These are obspy standards.
    StationXML gives options: "A", "B", "C".  A:NONE, B:ODD, C:EVEN
    """

    def __init__(self, **kwargs):
        super().__init__()

        super(FilterBase, self).__init__(attr_dict=attr_dict, **kwargs)
        self.type = "fir"
        if not self.decimation_factor:
            self.decimation_factor = 1.0


    def make_obspy_mapping(self):
        mapping = get_base_obspy_mapping()
        mapping["_symmetry"] = "symmetry"
        mapping["_coefficients"] = "coefficients"
        mapping["decimation_factor"] = "decimation_factor"
        mapping["decimation_input_sample_rate"] = "decimation_input_sample_rate"
        mapping["stage_gain_frequency"] = "gain_frequency"
        return mapping

    @property
    def output_sampling_rate(self):
        return self.decimation_input_sample_rate / self.decimation_factor

    @property
    def coefficients(self):
        return self._coefficients

    @coefficients.setter
    def coefficients(self, value):
        """
        Set the coefficients, make sure the input is validated
        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if isinstance(value, (list, tuple, np.ndarray)):
            self._coefficients = np.array(value, dtype=float)

        elif isinstance(value, str):
            self._coefficients = np.array(value.split(","), dtype=float)

        else:
            self._coefficients = np.empty(0)

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
        return len(self._coefficients)

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

    def to_obspy(
        self, stage_number=1, normalization_frequency=1, sample_rate=1,
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
