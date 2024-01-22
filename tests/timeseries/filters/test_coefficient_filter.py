# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 17:13:27 2021

@author: jpeacock
"""

import unittest

import numpy as np

from mt_metadata.timeseries.filters import CoefficientFilter
from mt_metadata.timeseries.filters.helper_functions import MT2SI_ELECTRIC_FIELD_FILTER
from mt_metadata.timeseries.filters.helper_functions import MT2SI_MAGNETIC_FIELD_FILTER
from mt_metadata.utils.exceptions import MTSchemaError

from obspy.core.inventory.response import CoefficientsTypeResponseStage


class TestCoefficientFilter(unittest.TestCase):
    """
    Test a coefficient filter, this one is pretty basic, just a gain value.
    """

    def setUp(self):
        self.cf = CoefficientFilter(
            units_in="v", units_out="v", name="coefficient", gain=10,
        )
        self.f = np.logspace(-5, 5, 100)

    def test_gain(self):
        with self.subTest(msg="string input"):
            self.cf.gain = "10.5"
            self.assertEqual(10.5, self.cf.gain)

        with self.subTest(msg="integer input"):
            self.cf.gain = int(10)
            self.assertEqual(10.0, self.cf.gain)

        with self.subTest(msg="failing input"):

            def set_gain_fail(value):
                self.cf.gain = value

            self.assertRaises(MTSchemaError, set_gain_fail, "a")

    def test_complex_response(self):
        cr = self.cf.complex_response(self.f)

        with self.subTest("test dtype"):
            self.assertTrue(cr.dtype.type, np.complex128)

        with self.subTest(msg="test amplitude"):
            cr_amp = np.abs(cr)
            amp = np.repeat(10, self.f.size)
            self.assertTrue(np.isclose(cr_amp, amp,).all() == True)

        with self.subTest(msg="test phase"):
            cr_phase = np.angle(cr, deg=True)
            phase = np.repeat(0, self.f.size)
            self.assertTrue(np.isclose(cr_phase, phase).all() == True)

    def test_to_obspy_stage(self):
        stage = self.cf.to_obspy(2, sample_rate=10, normalization_frequency=1)

        with self.subTest("test stage number"):
            self.assertEqual(stage.stage_sequence_number, 2)

        with self.subTest("test_gain"):
            self.assertEqual(stage.stage_gain, self.cf.gain)

        with self.subTest("test normalization frequency"):
            self.assertEqual(stage.stage_gain_frequency, 1)

        with self.subTest("test units in"):
            self.assertEqual(stage.input_units, self.cf.units_in)

        with self.subTest("test units out description"):
            self.assertEqual(
                stage.output_units_description, self.cf._units_out_obj.name
            )

        with self.subTest("test units out"):
            self.assertEqual(stage.output_units, self.cf.units_out)

        with self.subTest("test units out description"):
            self.assertEqual(
                stage.output_units_description, self.cf._units_out_obj.name
            )

        with self.subTest("test description"):
            self.assertEqual(stage.description, "coefficient filter")

        with self.subTest("test name"):
            self.assertEqual(stage.name, self.cf.name)

    def test_helper_functions(self):
        assert MT2SI_MAGNETIC_FIELD_FILTER.units_in == "nT"



# if __name__ == "__main__":
#     unittest.main()
