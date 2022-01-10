# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 17:13:27 2021

@author: jpeacock
"""

import unittest

import numpy as np

from mt_metadata.timeseries.filters import TimeDelayFilter
from mt_metadata.utils.exceptions import MTSchemaError

from obspy.core.inventory.response import CoefficientsTypeResponseStage


class TestTimeDelayFilter(unittest.TestCase):
    """
    Test a time delay filter, this one is pretty basic, just a delay value
    """

    def setUp(self):
        self.td = TimeDelayFilter(
            units_in="v", units_out="v", name="time delay", delay=-0.250,
        )
        self.f = np.logspace(-5, 5, 100)

    def test_delay(self):
        with self.subTest(msg="string input"):
            self.td.delay = "-.25"
            self.assertEqual(-0.25, self.td.delay)

        with self.subTest(msg="integer input"):
            self.td.delay = int(1)
            self.assertEqual(1, self.td.delay)

        with self.subTest(msg="failing input"):

            def set_gain_fail(value):
                self.td.delay = value

            self.assertRaises(MTSchemaError, set_gain_fail, "a")

    def test_complex_response(self):
        cr = self.td.complex_response(self.f)

        with self.subTest("test dtype"):
            self.assertTrue(cr.dtype.type, np.complex128)

        with self.subTest(msg="test amplitude"):
            cr_amp = np.abs(cr)
            amp = np.repeat(1, self.f.size)
            self.assertTrue(np.isclose(cr_amp, amp,).all() == True)

        with self.subTest(msg="test phase"):
            cr_phase = np.angle(cr, deg=True)
            phase = np.repeat(0, self.f.size)
            self.assertFalse(np.isclose(cr_phase, phase).all() == True)

    def test_pass_band(self):
        pb = self.td.pass_band(self.f)
        self.assertTrue(np.isclose(pb, np.array([self.f.min(), self.f.max()])).all())

    def test_to_obspy_stage(self):
        stage = self.td.to_obspy(2, sample_rate=10, normalization_frequency=1)

        with self.subTest("test stage number"):
            self.assertEqual(stage.stage_sequence_number, 2)

        with self.subTest("test gain"):
            self.assertEqual(stage.stage_gain, self.td.gain)

        with self.subTest("test decimation delay"):
            self.assertEqual(stage.decimation_delay, self.td.delay)

        with self.subTest("test normalization frequency"):
            self.assertEqual(stage.stage_gain_frequency, 1)

        with self.subTest("test units in"):
            self.assertEqual(stage.input_units, self.td.units_in)

        with self.subTest("test units out description"):
            self.assertEqual(
                stage.output_units_description, self.td._units_out_obj.name
            )

        with self.subTest("test units out"):
            self.assertEqual(stage.output_units, self.td.units_out)

        with self.subTest("test units out description"):
            self.assertEqual(
                stage.output_units_description, self.td._units_out_obj.name
            )

        with self.subTest("test description"):
            self.assertEqual(stage.description, "time delay filter")

        with self.subTest("test name"):
            self.assertEqual(stage.name, self.td.name)

        with self.subTest("test type"):
            self.assertIsInstance(stage, CoefficientsTypeResponseStage)
