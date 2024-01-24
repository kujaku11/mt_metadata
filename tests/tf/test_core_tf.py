# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 10:51:37 2021

@author: jpeacock
"""

import unittest
import xarray as xr
import numpy as np

from mt_metadata.transfer_functions.core import TF, TFError


class TestTFCore(unittest.TestCase):
    def setUp(self):
        self.tf = TF(some_kwarg=42)
        print(self.tf)
        print(self.tf.__repr__())
        print(self.tf.__str__())


class TestTFChannelNomenclature(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.nc = {"ex": "e1", "ey": "e2", "hx": "h1", "hy": "by", "hz": "b3"}
        self.tf = TF(channel_nomenclature=self.nc)

    def test_nomenclature(self):
        self.assertDictEqual(self.nc, self.tf.channel_nomenclature)

    def test_set_nomenclature(self):
        self.tf.channel_nomenclature = self.nc
        self.assertDictEqual(self.nc, self.tf.channel_nomenclature)

    def test_set_nomenclature_fail(self):
        def set_nc(value):
            self.tf.channel_nomenclature = value

        self.assertRaises(TypeError, set_nc, 10)

    def test_tf_initialized_output(self):
        self.assertListEqual(
            sorted(["e1", "e2", "h1", "by", "b3"]),
            sorted(self.tf._transfer_function.output.data.tolist()),
        )

    def test_tf_initialized_input(self):
        self.assertListEqual(
            sorted(["e1", "e2", "h1", "by", "b3"]),
            sorted(self.tf._transfer_function.input.data.tolist()),
        )

    def test_index_zxx(self):
        for key, index in {
            "zxx": ["hx", "ex"],
            "zxy": ["hy", "ex"],
            "zyx": ["hx", "ey"],
            "zyy": ["hy", "ey"],
            "tzx": ["hx", "hz"],
            "tzy": ["hy", "hz"],
        }.items():
            with self.subTest(key):
                self.assertDictEqual(
                    getattr(self.tf, f"index_{key}"),
                    {"input": self.nc[index[0]], "output": self.nc[index[1]]},
                )


class TestTFPeriodInput(unittest.TestCase):
    def setUp(self):
        self.n_period = 20
        self.period = np.logspace(-3, 3, self.n_period)

        self.tf = TF(period=self.period)

    def test_period_shape(self):
        self.assertEqual(self.tf.period.size, self.n_period)

    def test_tf_shape(self):
        self.assertEqual(
            self.tf.dataset.transfer_function.shape[0], self.n_period
        )

    def test_isp_shape(self):
        self.assertEqual(
            self.tf.dataset.inverse_signal_power.shape[0], self.n_period
        )

    def test_res_shape(self):
        self.assertEqual(
            self.tf.dataset.residual_covariance.shape[0], self.n_period
        )

    def test_period(self):
        self.assertTrue(np.isclose(self.period, self.tf.period).all())


class TestTFFrequencyInput(unittest.TestCase):
    def setUp(self):
        self.n_period = 20
        self.period = np.logspace(-3, 3, self.n_period)

        self.tf = TF(frequency=1.0 / self.period)

    def test_period_shape(self):
        self.assertEqual(self.tf.period.size, self.n_period)

    def test_tf_shape(self):
        self.assertEqual(
            self.tf.dataset.transfer_function.shape[0], self.n_period
        )

    def test_isp_shape(self):
        self.assertEqual(
            self.tf.dataset.inverse_signal_power.shape[0], self.n_period
        )

    def test_res_shape(self):
        self.assertEqual(
            self.tf.dataset.residual_covariance.shape[0], self.n_period
        )

    def test_period(self):
        self.assertTrue(np.isclose(self.period, self.tf.period).all())


class TestTFImpedanceInput(unittest.TestCase):
    def setUp(self):
        self.n_period = 20
        self.n_fail = 22
        self.period = np.logspace(-3, 3, self.n_period)
        self.fail_period = np.logspace(-3, 3, self.n_fail)
        self.test_z = xr.DataArray(
            data=np.random.rand(self.n_period, 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": self.period,
                "output": ["ex", "ey"],
                "input": ["hx", "hy"],
            },
            name="impedance",
        )
        self.new_z = np.random.rand(self.n_period, 2, 2)

        self.fail_z = xr.DataArray(
            data=np.random.rand(self.n_fail, 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": self.fail_period,
                "output": ["ex", "ey"],
                "input": ["hx", "hy"],
            },
            name="impedance",
        )

        self.tf = TF()
        self.tf.impedance = self.test_z

    def test_has_impedance(self):
        self.assertTrue(self.tf.has_impedance())

    def test_shape(self):
        self.assertEqual(self.tf.impedance.data.shape, (self.n_period, 2, 2))

    def test_xarray(self):
        self.assertTrue(np.all(self.tf.impedance == self.test_z))

    def test_fail(self):
        def set_value(value):
            self.tf.impedance = value

        self.assertRaises(TFError, set_value, self.fail_z)

    def test_set_from_array(self):
        self.tf.impedance = self.new_z
        self.assertTrue(np.all(self.tf.impedance.data == self.new_z))


class TestTFTipperInput(unittest.TestCase):
    def setUp(self):
        self.n_period = 20
        self.n_fail = 22
        self.period = np.logspace(-3, 3, self.n_period)
        self.fail_period = np.logspace(-3, 3, self.n_fail)
        self.test_t = xr.DataArray(
            data=np.random.rand(self.n_period, 1, 2),
            dims=["period", "output", "input"],
            coords={
                "period": self.period,
                "output": ["hz"],
                "input": ["hx", "hy"],
            },
            name="tipper",
        )
        self.new_t = np.random.rand(self.n_period, 1, 2)
        self.fail_t = xr.DataArray(
            data=np.random.rand(self.n_fail, 1, 2),
            dims=["period", "output", "input"],
            coords={
                "period": self.fail_period,
                "output": ["hz"],
                "input": ["hx", "hy"],
            },
            name="tipper",
        )

        self.tf = TF()
        self.tf.tipper = self.test_t

    def test_has_tipper(self):
        self.assertTrue(self.tf.has_tipper())

    def test_shape(self):
        self.assertEqual(self.tf.tipper.data.shape, (self.n_period, 1, 2))

    def test_xarray(self):
        self.assertTrue(np.all(self.tf.tipper == self.test_t))

    def test_fail(self):
        def set_value(value):
            self.tf.tipper = value

        self.assertRaises(TFError, set_value, self.fail_t)

    def test_set_from_array(self):
        self.tf.tipper = self.new_t
        self.assertTrue(np.all(self.tf.tipper.data == self.new_t))


class TestTFISPInput(unittest.TestCase):
    def setUp(self):
        self.n_period = 20
        self.n_fail = 22
        self.period = np.logspace(-3, 3, self.n_period)
        self.fail_period = np.logspace(-3, 3, self.n_fail)
        self.test_t = xr.DataArray(
            data=np.random.rand(self.n_period, 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": self.period,
                "output": ["hx", "hy"],
                "input": ["hx", "hy"],
            },
            name="inverse_signal_power",
        )
        self.new_t = np.random.rand(self.n_period, 2, 2)
        self.fail_t = xr.DataArray(
            data=np.random.rand(self.n_fail, 2, 2),
            dims=["period", "output", "input"],
            coords={
                "period": self.fail_period,
                "output": ["hx", "hy"],
                "input": ["hx", "hy"],
            },
            name="inverse_signal_power",
        )

        self.tf = TF()
        self.tf.inverse_signal_power = self.test_t

    def test_has_isp(self):
        self.assertTrue(self.tf.has_inverse_signal_power())

    def test_shape(self):
        self.assertEqual(
            self.tf.inverse_signal_power.data.shape, (self.n_period, 2, 2)
        )

    def test_xarray(self):
        self.assertTrue(
            np.all(self.tf.inverse_signal_power.data == self.test_t) == True
        )

    def test_fail(self):
        def set_value(value):
            self.tf.inverse_signal_power = value

        self.assertRaises(TFError, set_value, self.fail_t)

    def test_set_from_array(self):
        self.tf.inverse_signal_power = self.new_t
        self.assertTrue(
            np.all(self.tf.inverse_signal_power.data == self.new_t) == True
        )


class TestTFResidualInput(unittest.TestCase):
    def setUp(self):
        self.n_period = 20
        self.n_fail = 22
        self.period = np.logspace(-3, 3, self.n_period)
        self.fail_period = np.logspace(-3, 3, self.n_fail)
        self.test_t = xr.DataArray(
            data=np.random.rand(self.n_period, 3, 3),
            dims=["period", "output", "input"],
            coords={
                "period": self.period,
                "output": ["ex", "ey", "hz"],
                "input": ["ex", "ey", "hz"],
            },
            name="inverse_signal_power",
        )
        self.new_t = np.random.rand(self.n_period, 3, 3)
        self.fail_t = xr.DataArray(
            data=np.random.rand(self.n_fail, 3, 3),
            dims=["period", "output", "input"],
            coords={
                "period": self.fail_period,
                "output": ["ex", "ey", "hz"],
                "input": ["ex", "ey", "hz"],
            },
            name="inverse_signal_power",
        )

        self.tf = TF()
        self.tf.residual_covariance = self.test_t

    def test_has_residual(self):
        self.assertTrue(self.tf.has_residual_covariance())

    def test_shape(self):
        self.assertEqual(
            self.tf.residual_covariance.data.shape, (self.n_period, 3, 3)
        )

    def test_xarray(self):
        self.assertTrue(
            np.all(self.tf.residual_covariance.data == self.test_t) == True
        )

    def test_fail(self):
        def set_value(value):
            self.tf.residual_covariance = value

        self.assertRaises(TFError, set_value, self.fail_t)

    def test_set_from_array(self):
        self.tf.residual_covariance = self.new_t
        self.assertTrue(
            np.all(self.tf.residual_covariance.data == self.new_t) == True
        )


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
