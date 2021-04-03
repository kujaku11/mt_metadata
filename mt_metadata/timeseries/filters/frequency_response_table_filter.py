"""
20210323: Considerations:
Input units will typically be Volts and outputs nT, but this is configurable.

This could be populated by frequency or Period and phase could have units of radians or degrees.
Rather than build all the possible conversions/cases into the class, suggest fix the class
so that it takes as input frequency - amplitude - phase (radians) "FAP" format.
We can than use a FAPFormatter() class to address casting received tables into the desired formats.

The table should have default outputs, suggested frequency, amplitude, phase (degrees)

"""
import copy
import numpy as np
from obspy.core import inventory
from scipy.interpolate import InterpolatedUnivariateSpline

from mt_metadata.base import get_schema
from mt_metadata.timeseries.filters.filter_base import FilterBase
from mt_metadata.timeseries.filters.filter_base import OBSPY_MAPPING
from mt_metadata.timeseries.filters.frequency_response_table import FrequencyResponseTable
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS

obspy_mapping = copy.deepcopy(OBSPY_MAPPING)

# =============================================================================
attr_dict = get_schema("filter_base", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("frequency_response_table_filter", SCHEMA_FN_PATHS))


# =============================================================================



class FrequencyResponseTableFilter(FilterBase):

    def __init__(self, **kwargs):
        self.type = 'frequency response table'
        self.instrument_type = None #FGM or FBC or other?
        #self.log_interpolate = None
        self.gain = 1.0
        super(FilterBase, self).__init__(attr_dict=attr_dict, **kwargs)
        self.obspy_mapping = obspy_mapping
        self._empirical_frequencies = kwargs.get('empirical_frequencies', None)
        self._empirical_amplitudes = kwargs.get('empirical_amplitudes', None)
        self._empirical_phases = kwargs.get('empirical_phases', None)
        self.amplitude_response = None
        self.phase_response = None
        self._total_response_function = None




    @property
    def frequencies(self):
        return self._empirical_frequencies

    @property
    def amplitudes(self):
        return self._empirical_amplitudes

    @property
    def phases(self):
        return self._empirical_phases

    @property
    def min_frequency(self):
        return np.min(self._empirical_frequencies)

    @property
    def max_frequency(self):
        return np.max(self._empirical_frequencies)

    def total_response_function(self, frequencies):
        return self._total_response_function(frequencies)


    def complex_response(self, frequencies, k=3, ext=2):
        """

        Parameters
        ----------
        frequencies: numpy array of frequencies, expected in Hz

        Returns
        -------
        h : numpy array of (possibly complex-valued) frequency response at the input frequencies

        #I would like a separate step that calculates self._total_response_function
        and stores it but the validator doesn't seem to like when I assign that attribute
        """
        if np.min(frequencies) < self.min_frequency:
            print("Extrapolation warning ")

        if np.max(frequencies) > self.max_frequency:
            print("Extrapolation warning ")
        phase_response = InterpolatedUnivariateSpline(self.frequencies, self.phases, k=k, ext=ext)
        amplitude_response = InterpolatedUnivariateSpline(self.frequencies, self.amplitudes, k=k, ext=ext)
        total_response_function = lambda f: amplitude_response(f) * np.exp(1.j * phase_response(f))

        return self.gain * total_response_function(frequencies)





def main():
    import pandas as pd

    #<READ FAP FILE>
    from mth5_test_data.util import MTH5_TEST_DATA_DIR
    qf_ant4_dir = MTH5_TEST_DATA_DIR.joinpath("calibration_files/qf/ant4")
    qf_ant4_filebase = "1304_0_0.csv"
    qf_ant4_filepath = qf_ant4_dir.joinpath(qf_ant4_filebase)
    fap_table = FrequencyResponseTable()
    df = fap_table.load_from_csv(qf_ant4_filepath)
    x = df['frequency'][2:].to_numpy()
    y = df['amplitude'][2:].to_numpy()
    z = df['phase'][2:].to_numpy()
    #</READ FAP FILE>

    fap_filter = FrequencyResponseTableFilter(empirical_frequencies=x, empirical_amplitudes=y, empirical_phases=z)
    xx = np.logspace(-1.6, 2, 10000)
    fap_filter.plot_complex_response(xx)

    # spl = InterpolatedUnivariateSpline(x, y, k=3, ext=2)
    # loglog_spl = InterpolatedUnivariateSpline(np.log10(x), np.log10(y), k=K)
    # # #<LINEAR>
    # # plt.figure(1)
    # # plt.plot(df['frequency'][2:], df['amplitude'][2:], 'b*')#, markersize=2)
    # # xx = np.logspace(-1.6, 2, 10000)
    # # plt.plot(xx, spl(xx), 'blue')
    # # plt.xlabel(' frequency (Hz)')
    # # plt.ylabel(' amplitude (V/nT)')
    # # plt.title("Linear Scales on both axes")
    # # plt.show()
    # # #</LINEAR>
    #
    # #<SEMILOGX>
    # plt.figure(2)
    # plt.plot(np.log10(df['frequency'][2:]), df['amplitude'][2:], 'b*')  # , markersize=2)
    # xx = np.logspace(-1.9, 2, 10000)
    # plt.plot(np.log10(xx), spl(xx), 'blue')
    # plt.xlabel(' frequency (Hz)')
    # plt.ylabel(' amplitude (V/nT)')
    # plt.title("Semilog X ")
    # plt.show()
    # #</SEMILOGX>


if __name__ == "__main__":
    main()

    # def to_obspy(self, stage_number=1, cf_type="DIGITAL", sample_rate=1,
    #              gain_frequency=0):
    #     """
    #     stage_sequence_number,
    #     stage_gain,
    #     stage_gain_frequency,
    #     input_units,
    #     output_units,
    #     cf_transfer_function_type,
    #     resource_id=None,
    #     resource_id2=None,
    #     name=None,
    #     numerator=None,
    #     denominator=None,
    #     input_units_description=None,
    #     output_units_description=None,
    #     description=None,
    #     decimation_input_sample_rate=None,
    #     decimation_factor=None,
    #     decimation_offset=None,
    #     decimation_delay=None,
    #     decimation_correction=None
    #
    #     :param stage_number: DESCRIPTION, defaults to 1
    #     :type stage_number: TYPE, optional
    #     :param cf_type: DESCRIPTION, defaults to "DIGITAL"
    #     :type cf_type: TYPE, optional
    #     :param sample_rate: DESCRIPTION, defaults to 1
    #     :type sample_rate: TYPE, optional
    #     :return: DESCRIPTION
    #     :rtype: TYPE
    #
    #     """
    #
    #     stage = inventory.CoefficientsTypeResponseStage(
    #         stage_number,
    #         self.gain,
    #         gain_frequency,
    #         self.units_in,
    #         self.units_out,
    #         cf_type,
    #         name=self.name,
    #         decimation_input_sample_rate=sample_rate,
    #         decimation_factor=1,
    #         decimation_offset=0,
    #         decimation_delay=0,
    #         decimation_correction=0,
    #         numerator=[],
    #         denominator=[])
    #
    #     return stage
