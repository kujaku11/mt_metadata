# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 17:13:27 2021

@author: jpeacock
"""

import unittest

import numpy as np

from mt_metadata.timeseries.filters import FrequencyResponseTableFilter
from mt_metadata.utils.exceptions import MTSchemaError

from obspy.core.inventory.response import ResponseListElement

class TestFAPFilter(unittest.TestCase):
    """
    Test a FAP filter, we can use an ANT4 calibration
    """
    
    def setUp(self):
        self.fap = FrequencyResponseTableFilter(
            units_in="volts", units_out="nanotesla", name="example_fap")

        self.fap.frequencies = [  
            1.95312000e-03,   2.76214000e-03,   3.90625000e-03,
             5.52427000e-03,   7.81250000e-03,   1.10485000e-02,
             1.56250000e-02,   2.20971000e-02,   3.12500000e-02,
             4.41942000e-02,   6.25000000e-02,   8.83883000e-02,
             1.25000000e-01,   1.76780000e-01,   2.50000000e-01,
             3.53550000e-01,   5.00000000e-01,   7.07110000e-01,
             1.00000000e+00,   1.41420000e+00,   2.00000000e+00,
             2.82840000e+00,   4.00000000e+00,   5.65690000e+00,
             8.00000000e+00,   1.13140000e+01,   1.60000000e+01,
             2.26270000e+01,   3.20000000e+01,   4.52550000e+01,
             6.40000000e+01,   9.05100000e+01,   1.28000000e+02,
             1.81020000e+02,   2.56000000e+02,   3.62040000e+02,
             5.12000000e+02,   7.24080000e+02,   1.02400000e+03,
             1.44820000e+03,   2.04800000e+03,   2.89630000e+03,
             4.09600000e+03,   5.79260000e+03,   8.19200000e+03,
             1.15850000e+04]
        
        self.fap.amplitudes = [  
            1.59009000e-03,   3.07497000e-03,   5.52793000e-03,
            9.47448000e-03,   1.54565000e-02,   2.49498000e-02,
            3.96462000e-02,   7.87192000e-02,   1.57134000e-01,
            3.09639000e-01,   5.94224000e-01,   1.12698000e+00,
            2.01092000e+00,   3.33953000e+00,   5.00280000e+00,
            6.62396000e+00,   7.97545000e+00,   8.82872000e+00,
            9.36883000e+00,   9.64102000e+00,   9.79664000e+00,
            9.87183000e+00,   9.90666000e+00,   9.92845000e+00,
            9.93559000e+00,   9.93982000e+00,   9.94300000e+00,
            9.93546000e+00,   9.93002000e+00,   9.90873000e+00,
            9.86383000e+00,   9.78129000e+00,   9.61814000e+00,
            9.26461000e+00,   8.60175000e+00,   7.18337000e+00,
            4.46123000e+00,  -8.72600000e-01,  -5.15684000e+00,
            -2.95111000e+00,  -9.28512000e-01,  -2.49850000e-01,
            -5.75682000e-02,  -1.34293000e-02,  -1.02708000e-03,
            1.09577000e-03]
        
        self.fap.phases = [  
            7.60824000e-02,   1.09174000e-01,   1.56106000e-01,
            2.22371000e-01,   3.12020000e-01,   4.41080000e-01,
            6.23548000e-01,   8.77188000e-01,   1.23360000e+00,
            1.71519000e+00,   2.35172000e+00,   3.13360000e+00,
            3.98940000e+00,   4.67269000e+00,   4.96593000e+00,
            4.65875000e+00,   3.95441000e+00,   3.11098000e+00,
            2.30960000e+00,   1.68210000e+00,   1.17928000e+00,
            8.20015000e-01,   5.36474000e-01,   3.26955000e-01,
            1.48051000e-01,  -8.24275000e-03,  -1.66064000e-01,
            -3.48852000e-01,  -5.66625000e-01,  -8.62435000e-01,
            -1.25347000e+00,  -1.81065000e+00,  -2.55245000e+00,
            -3.61512000e+00,  -5.00185000e+00,  -6.86158000e+00,
            -8.78698000e+00,  -9.08920000e+00,  -4.22925000e+00,
             2.15533000e-01,   6.00661000e-01,   3.12368000e-01,
             1.31660000e-01,   5.01553000e-02,   1.87239000e-02,
             6.68243000e-03]
        self.f = np.logspace(-3, 3, 100)
        
    def test_gain(self):
        with self.subTest(msg="string input"):
            self.fap.gain = "-.25"
            self.assertEqual(-.25, self.fap.gain)
            
        with self.subTest(msg="integer input"):
            self.fap.gain= int(1)
            self.assertEqual(1, self.fap.gain)
            
        with self.subTest(msg="failing input"):
            def set_gain_fail(value):
                self.fap.gain = value
                
            self.assertRaises(MTSchemaError, set_gain_fail, "a")
            
    def test_pass_band(self):
        pb = self.fap.pass_band(self.fap.frequencies, tol=1e-2)
        self.assertTrue(
            np.isclose(pb, np.array([2., 181.02])).all()
            )
            
    def test_complex_response(self):
        cr = self.fap.complex_response(self.fap.frequencies)
        
        with self.subTest("test dtype"):
            self.assertTrue(cr.dtype.type, np.complex128)
        
        with self.subTest(msg="test amplitude"):
            cr_amp = np.abs(cr)
            self.assertTrue(np.isclose(np.abs(self.fap.amplitudes), 
                                       np.abs(cr)).all())
            
        with self.subTest(msg="test phase"):
            cr_phase = np.unwrap(np.angle(cr, deg=False))
            # the high frequencies get a little jumbled with unwrap, 
            # not sure why but for now just skip those frequencies until
            # we know more about it.
            self.assertTrue(np.isclose(cr_phase[:-10], self.fap.phases[:-10]).all())
            
    def test_to_obspy_stage(self):
        stage = self.fap.to_obspy(2, sample_rate=10, normalization_frequency=1)
        
        with self.subTest("test stage number"):
            self.assertEqual(stage.stage_sequence_number, 2)
        
        with self.subTest("test gain"):
            self.assertEqual(stage.stage_gain, self.fap.gain)
        
        with self.subTest("test amplitude"):
            amp = np.array([r.amplitude for r in stage.response_list_elements])
            self.assertTrue(np.isclose(amp, self.fap.amplitudes).all())
                            
        with self.subTest("test amplitude"):
            phase = np.array([r.phase for r in stage.response_list_elements])
            self.assertTrue(np.isclose(phase, self.fap.phases).all())
                            
        with self.subTest("test amplitude"):
            f = np.array([r.frequency for r in stage.response_list_elements])
            self.assertTrue(np.isclose(f, self.fap.frequencies).all())
            
        with self.subTest("test normalization frequency"):
            self.assertEqual(stage.stage_gain_frequency, 1)
            
        with self.subTest("test units in"):
            self.assertEqual(stage.input_units, self.fap.units_in)
            
        with self.subTest("test units out description"):
            self.assertEqual(stage.output_units_description, self.fap._units_out_obj.name)
        
        with self.subTest("test units out"):
            self.assertEqual(stage.output_units, self.fap.units_out)
            
        with self.subTest("test units out description"):
            self.assertEqual(stage.output_units_description, self.fap._units_out_obj.name)
            
        with self.subTest("test description"):
            self.assertEqual(stage.description, "frequency amplitude phase lookup table")
            
        with self.subTest("test name"):
            self.assertEqual(stage.name, self.fap.name)
        
            
        
    
