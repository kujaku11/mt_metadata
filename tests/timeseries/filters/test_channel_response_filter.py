# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 17:13:27 2021

@author: jpeacock
"""

import unittest

import numpy as np

from mt_metadata.timeseries.filters import (
    FrequencyResponseTableFilter,
    PoleZeroFilter,
    CoefficientFilter,
    ChannelResponse,
    TimeDelayFilter,
)
from mt_metadata.utils.exceptions import MTSchemaError

from obspy.core.inventory.response import ResponseListResponseStage


class TestFAPFilter(unittest.TestCase):
    """
    Test a FAP filter, we can use an ANT4 calibration
    """

    def setUp(self):

        self.td = TimeDelayFilter(
            units_in="volts", units_out="volts", delay=-0.25, name="example_time_delay"
        )
        self.fap = FrequencyResponseTableFilter(
            units_in="volts", units_out="volts", name="example_fap"
        )

        self.fap.frequencies = [
            1.95312000e-03,
            2.76214000e-03,
            3.90625000e-03,
            5.52427000e-03,
            7.81250000e-03,
            1.10485000e-02,
            1.56250000e-02,
            2.20971000e-02,
            3.12500000e-02,
            4.41942000e-02,
            6.25000000e-02,
            8.83883000e-02,
            1.25000000e-01,
            1.76780000e-01,
            2.50000000e-01,
            3.53550000e-01,
            5.00000000e-01,
            7.07110000e-01,
            1.00000000e00,
            1.41420000e00,
            2.00000000e00,
            2.82840000e00,
            4.00000000e00,
            5.65690000e00,
            8.00000000e00,
            1.13140000e01,
            1.60000000e01,
            2.26270000e01,
            3.20000000e01,
            4.52550000e01,
            6.40000000e01,
            9.05100000e01,
            1.28000000e02,
            1.81020000e02,
            2.56000000e02,
            3.62040000e02,
            5.12000000e02,
            7.24080000e02,
            1.02400000e03,
            1.44820000e03,
            2.04800000e03,
            2.89630000e03,
            4.09600000e03,
            5.79260000e03,
            8.19200000e03,
            1.15850000e04,
        ]

        self.fap.amplitudes = [
            1.59009000e-03,
            3.07497000e-03,
            5.52793000e-03,
            9.47448000e-03,
            1.54565000e-02,
            2.49498000e-02,
            3.96462000e-02,
            7.87192000e-02,
            1.57134000e-01,
            3.09639000e-01,
            5.94224000e-01,
            1.12698000e00,
            2.01092000e00,
            3.33953000e00,
            5.00280000e00,
            6.62396000e00,
            7.97545000e00,
            8.82872000e00,
            9.36883000e00,
            9.64102000e00,
            9.79664000e00,
            9.87183000e00,
            9.90666000e00,
            9.92845000e00,
            9.93559000e00,
            9.93982000e00,
            9.94300000e00,
            9.93546000e00,
            9.93002000e00,
            9.90873000e00,
            9.86383000e00,
            9.78129000e00,
            9.61814000e00,
            9.26461000e00,
            8.60175000e00,
            7.18337000e00,
            4.46123000e00,
            -8.72600000e-01,
            -5.15684000e00,
            -2.95111000e00,
            -9.28512000e-01,
            -2.49850000e-01,
            -5.75682000e-02,
            -1.34293000e-02,
            -1.02708000e-03,
            1.09577000e-03,
        ]

        self.fap.phases = [
            7.60824000e-02,
            1.09174000e-01,
            1.56106000e-01,
            2.22371000e-01,
            3.12020000e-01,
            4.41080000e-01,
            6.23548000e-01,
            8.77188000e-01,
            1.23360000e00,
            1.71519000e00,
            2.35172000e00,
            3.13360000e00,
            3.98940000e00,
            4.67269000e00,
            4.96593000e00,
            4.65875000e00,
            3.95441000e00,
            3.11098000e00,
            2.30960000e00,
            1.68210000e00,
            1.17928000e00,
            8.20015000e-01,
            5.36474000e-01,
            3.26955000e-01,
            1.48051000e-01,
            -8.24275000e-03,
            -1.66064000e-01,
            -3.48852000e-01,
            -5.66625000e-01,
            -8.62435000e-01,
            -1.25347000e00,
            -1.81065000e00,
            -2.55245000e00,
            -3.61512000e00,
            -5.00185000e00,
            -6.86158000e00,
            -8.78698000e00,
            -9.08920000e00,
            -4.22925000e00,
            2.15533000e-01,
            6.00661000e-01,
            3.12368000e-01,
            1.31660000e-01,
            5.01553000e-02,
            1.87239000e-02,
            6.68243000e-03,
        ]

        self.pz = PoleZeroFilter(
            units_in="volts", units_out="volts", name="example_zpk_response"
        )
        self.pz.poles = [
            (-6.283185 + 10.882477j),
            (-6.283185 - 10.882477j),
            (-12.566371 + 0j),
        ]
        self.pz.zeros = []
        self.pz.normalization_factor = 2002.269

        self.cf = CoefficientFilter(
            units_in="v", units_out="v", name="example_coefficient", gain=10,
        )

        self.cr = ChannelResponseFilter(
            filters_list=[self.pz, self.fap, self.cf, self.td]
        )
        self.cr.frequencies = np.logspace(-5, 5, 500)

    def test_pass_band(self):
        self.assertTrue(
            np.isclose(self.cr.pass_band, np.array([0.1018629, 1.02334021])).all()
        )

    def test_complex_response(self):
        cr = self.cr.complex_response()
        pb = self.cr.pass_band
        index_0 = np.where(self.cr.frequencies == pb[0])[0][0]
        index_1 = np.where(self.cr.frequencies == pb[-1])[0][0]

        with self.subTest("test dtype"):
            self.assertTrue(cr.dtype.type, np.complex128)

        with self.subTest(msg="test amplitude"):
            cr_amp = np.abs(cr)
            # check the slope in the passband
            slope = np.log10(cr_amp[index_1] / cr_amp[index_0]) / np.log10(
                self.cr.frequencies[index_1] / self.cr.frequencies[index_0]
            )
            self.assertTrue(abs(slope) < 1)

        with self.subTest(msg="test phase"):
            cr_phase = np.unwrap(np.angle(cr, deg=False))
            slope = (cr_phase[index_1] - cr_phase[index_0]) / np.log10(
                self.cr.frequencies[index_1] / self.cr.frequencies[index_0]
            )
            self.assertTrue(abs(slope) < np.pi)

    def test_unit_fail(self):
        cr1 = CoefficientFilter(units_in="volts", units_out="mv")
        cr2 = CoefficientFilter(units_in="nanotesla", units_out="counts")

        def set_filters_list(cr1, cr2):
            self.cr.filters_list = [cr1, cr2]

        self.assertRaises(ValueError, set_filters_list, cr1, cr2)

    def test_delay_filters(self):
        delay_names = [f.name for f in self.cr.delay_filters]
        self.assertListEqual(delay_names, [self.td.name])

    def test_non_delay_filters(self):
        non_delay_names = [f.name for f in self.cr.non_delay_filters]
        self.assertListEqual(
            non_delay_names, [self.pz.name, self.fap.name, self.cf.name]
        )

    def test_names(self):
        self.assertListEqual(
            self.cr.names, [self.pz.name, self.fap.name, self.cf.name, self.td.name]
        )

    def test_total_delay(self):
        self.assertEqual(self.cr.total_delay, self.td.delay)

    def test_normalization_frequency(self):
        self.assertEqual(np.round(self.cr.normalization_frequency, 3), 0.323)

    def test_instrument_sensitivity(self):
        s = 62.01227179
        for sig_figs in [3, 6, 9]:
            print(self.cr.compute_instrument_sensitivity(sig_figs=sig_figs))
            with self.subTest(msg=f"significant_digits {sig_figs}"):
                self.assertAlmostEqual(
                    self.cr.compute_instrument_sensitivity(sig_figs=sig_figs),
                    round(s, sig_figs - 1),
                    sig_figs,
                )

    def test_units_in(self):
        self.assertEqual(self.cr.units_in, self.pz.units_in)

    def test_units_out(self):
        self.assertEqual(self.cr.units_out, self.td.units_out)

    # def test_to_obspy_stage(self):
    #     stage = cr.frequenciesap.to_obspy(2, sample_rate=10, normalization_frequency=1)

    #     with self.subTest("test instance"):
    #         self.assertIsInstance(stage, ResponseListResponseStage)

    #     with self.subTest("test stage number"):
    #         self.assertEqual(stage.stage_sequence_number, 2)

    #     with self.subTest("test gain"):
    #         self.assertEqual(stage.stage_gain, cr.frequenciesap.gain)

    #     with self.subTest("test amplitude"):
    #         amp = np.array([r.amplitude for r in stage.response_list_elements])
    #         self.assertTrue(np.isclose(amp, cr.frequenciesap.amplitudes).all())

    #     with self.subTest("test phase"):
    #         phase = np.array([r.phase for r in stage.response_list_elements])
    #         self.assertTrue(np.isclose(phase, cr.frequenciesap.phases).all())

    #     with self.subTest("test frequency"):
    #         f = np.array([r.frequency for r in stage.response_list_elements])
    #         self.assertTrue(np.isclose(f, cr.frequenciesap.frequencies).all())

    #     with self.subTest("test normalization frequency"):
    #         self.assertEqual(stage.stage_gain_frequency, 1)

    #     with self.subTest("test units in"):
    #         self.assertEqual(stage.input_units, cr.frequenciesap.units_in)

    #     with self.subTest("test units out description"):
    #         self.assertEqual(stage.output_units_description, cr.frequenciesap._units_out_obj.name)

    #     with self.subTest("test units out"):
    #         self.assertEqual(stage.output_units, cr.frequenciesap.units_out)

    #     with self.subTest("test units out description"):
    #         self.assertEqual(stage.output_units_description, cr.frequenciesap._units_out_obj.name)

    #     with self.subTest("test description"):
    #         self.assertEqual(stage.description, "frequency amplitude phase lookup table")

    #     with self.subTest("test name"):
    #         self.assertEqual(stage.name, cr.frequenciesap.name)

# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
