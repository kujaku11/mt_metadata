# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 17:13:27 2021

@author: jpeacock
"""

import unittest

import numpy as np

from mt_metadata.timeseries.filters import PoleZeroFilter
from mt_metadata.utils.exceptions import MTSchemaError

from obspy.core.inventory.response import PolesZerosResponseStage

class TestZPKFilter(unittest.TestCase):
    """
    Test a ZPK filter, use a low pass from a NIMS
    """
    
    def setUp(self):
        self.pz = PoleZeroFilter(units_in="volts", units_out="nanotesla", name="example_zpk_response")
        self.pz.poles = [(-6.283185+10.882477j), (-6.283185-10.882477j), (-12.566371+0j)]
        self.pz.zeros = []
        self.pz.normalization_factor = 2002.269

        self.f = np.logspace(-5, 5, 500)
        
    def test_gain(self):
        with self.subTest(msg="string input"):
            self.pz.gain = "-.25"
            self.assertEqual(-.25, self.pz.gain)
            
        with self.subTest(msg="integer input"):
            self.pz.gain= int(1)
            self.assertEqual(1, self.pz.gain)
            
        with self.subTest(msg="failing input"):
            def set_gain_fail(value):
                self.pz.gain = value
                
            self.assertRaises(MTSchemaError, set_gain_fail, "a")
            
    def test_poles_type(self):
        self.assertIsInstance(self.pz.poles, np.ndarray)
        
    def test_zeros_type(self):
        self.assertIsInstance(self.pz.zeros, np.ndarray)
            
    def test_pass_band(self):
        pb = self.pz.pass_band(self.f, tol=1e-2)
        self.assertTrue(
            np.isclose(pb, np.array([1.00000000e-05, 5.36363132e-01])).all()
            )
            
    def test_complex_response(self):
        cr = self.pz.complex_response(self.f)
        pb = self.pz.pass_band(self.f, tol=1e-2)
        index_0 = np.where(self.f == pb[0])[0][0]
        index_1 = np.where(self.f == pb[-1])[0][0]
        
        with self.subTest("test dtype"):
            self.assertTrue(cr.dtype.type, np.complex128)
        
        with self.subTest(msg="test amplitude"):
            cr_amp = np.abs(cr)
            # check the slope in the passband
            slope = np.log10(cr_amp[index_1]/cr_amp[index_0]) / np.log10(self.f[index_1] / self.f[index_0])
            self.assertTrue(abs(slope) < 1e-4)
            
        with self.subTest(msg="test phase"):
            cr_phase = np.unwrap(np.angle(cr, deg=False))
            slope = (cr_phase[index_1] - cr_phase[index_0]) / np.log10(self.f[index_1] / self.f[index_0])
            self.assertTrue(abs(slope) < 1)
            
    def test_to_obspy_stage(self):
        stage = self.pz.to_obspy(2, sample_rate=10, normalization_frequency=1)
        
        with self.subTest("test instance"):
            self.assertIsInstance(stage, PolesZerosResponseStage)
        
        with self.subTest("test stage number"):
            self.assertEqual(stage.stage_sequence_number, 2)
        
        with self.subTest("test gain"):
            self.assertEqual(stage.stage_gain, self.pz.gain)
        
        with self.subTest("test poles"):
            self.assertTrue(np.isclose(self.pz.poles, stage.poles).all())
                            
        with self.subTest("test zeros"):
            self.assertTrue(np.isclose(self.pz.zeros, stage.zeros).all())
            
        with self.subTest("test normalization frequency"):
            self.assertEqual(stage.stage_gain_frequency, 1)
            
        with self.subTest("test units in"):
            self.assertEqual(stage.input_units, self.pz.units_in)
            
        with self.subTest("test units out description"):
            self.assertEqual(stage.output_units_description, self.pz._units_out_obj.name)
        
        with self.subTest("test units out"):
            self.assertEqual(stage.output_units, self.pz.units_out)
            
        with self.subTest("test units out description"):
            self.assertEqual(stage.output_units_description, self.pz._units_out_obj.name)
            
        with self.subTest("test description"):
            self.assertEqual(stage.description, "poles and zeros filter")
            
        with self.subTest("test name"):
            self.assertEqual(stage.name, self.pz.name)
        
            
        
    
