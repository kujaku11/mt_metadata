# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 10:51:37 2021

@author: jpeacock
"""

import unittest
import xarray as xr
import numpy as np

from mt_metadata.transfer_functions.core import TF, TFError

class TestTFPeriodInput(unittest.TestCase):
    def setUp(self):
        self.n_period = 20
        self.period = np.logspace(-3, 3, self.n_period)
        
        self.tf = TF()
        self.tf.period = self.period
    def test_period_shape(self):

        self.assertEqual(self.tf.period.size, self.n_period)
        
    def test_tf_shape(self):
        self.assertEqual(self.tf.dataset.transfer_function.shape[0], 
                          self.n_period)
        
    def test_isp_shape(self):
        self.assertEqual(self.tf.dataset.inverse_signal_power.shape[0], 
                          self.n_period)
        
    def test_res_shape(self):
        self.assertEqual(self.tf.dataset.residual_covariance.shape[0], 
                          self.n_period)


class TestTFImpedanceInput(unittest.TestCase):
    
    def setUp(self):
        self.n_period = 20
        self.n_fail = 22
        self.period = np.logspace(-3, 3, self.n_period)
        self.fail_period = np.logspace(-3, 3, self.n_fail)
        self.test_z = xr.DataArray(
            data=np.random.rand(self.n_period, 2, 2), 
            dims=["period", "output", "input"],
            coords={"period": self.period, 
                    "output": ['ex', 'ey'],
                    "input":["hx", "hy"]},
            name="impedance")
        
        self.fail_z = xr.DataArray(
            data=np.random.rand(self.n_fail, 2, 2), 
            dims=["period", "output", "input"],
            coords={"period": self.fail_period, 
                    "output": ['ex', 'ey'],
                    "input":["hx", "hy"]},
            name="impedance")

        self.tf = TF()
        self.tf.impedance = self.test_z

    def test_has_impedance(self):
        
        self.assertTrue(self.tf.has_impedance())
    
    def test_shape(self):
        self.assertEqual(self.tf.impedance.impedance.data.shape,
                         (self.n_period, 2, 2))
        
    def test_xarray(self):
        self.assertEqual(self.tf.impedance, self.test_z)
        
    def test_fail(self):
        def set_value(value):
            self.tf.impedance = value
        self.assertRaises(TFError, set_value, self.fail_z)
        
        
class TestTFTipperInput(unittest.TestCase):
    
    def setUp(self):
        self.n_period = 20
        self.n_fail = 22
        self.period = np.logspace(-3, 3, self.n_period)
        self.fail_period = np.logspace(-3, 3, self.n_fail)
        self.test_t = xr.DataArray(
            data=np.random.rand(self.n_period, 1, 2), 
            dims=["period", "output", "input"],
            coords={"period": self.period, 
                    "output": ["hz"],
                    "input":["hx", "hy"]},
            name="tipper")
        
        self.fail_t = xr.DataArray(
            data=np.random.rand(self.n_fail, 1, 2), 
            dims=["period", "output", "input"],
            coords={"period": self.fail_period, 
                    "output": ["hz"],
                    "input":["hx", "hy"]},
            name="tipper")

        self.tf = TF()
        self.tf.tipper = self.test_t

    def test_has_tipper(self):
        
        self.assertTrue(self.tf.has_tipper())
    
    def test_shape(self):
        self.assertEqual(self.tf.tipper.tipper.data.shape,
                         (self.n_period, 1, 2))
        
    def test_xarray(self):
        self.assertEqual(self.tf.tipper, self.test_t)
        
    def test_fail(self):
        def set_value(value):
            self.tf.tipper = value
        self.assertRaises(TFError, set_value, self.fail_t)
        
# def test_tipper_input(self):
#     self.tf.tipper = self.test_t
#     self.assertTrue(self.tf.has_tipper())
#     self.assertEqual(self.tf.tipper.tipper.data.shape, (self.n_period, 1, 2))
#     self.assertEqual(self.tf.tipper, self.test_t)
  
 

       


# self.test_isp = xr.DataArray(
#     data=np.random.rand(self.n_period, 2, 2), 
#     dims=["period", "output", "input"],
#     coords={"period": self.period, 
#             "output": ["hx", "hy"],
#             "input":["hx", "hy"]},
#     name="inverse_signal_power")

# self.test_res = xr.DataArray(
#     data=np.random.rand(self.n_period, 3, 3), 
#     dims=["period", "output", "input"],
#     coords={"period": self.period, 
#             "output": ["ex", "ey", "hz"],
#             "input":["ex", "ey", "hz"]},
#     name="inverse_signal_power")
        
# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
        