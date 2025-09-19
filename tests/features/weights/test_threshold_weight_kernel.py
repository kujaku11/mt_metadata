"""
    Unittests for the ThresholdWeightKernel class
"""

import unittest
import numpy as np

from mt_metadata.features.weights.monotonic_weight_kernel import ThresholdWeightKernel
from mt_metadata.utils.exceptions import MTSchemaError

class TestThresholdWeightKernel(unittest.TestCase):


    def test_low_cut(self):
        threshold = 0.8
        # data_dict = {
        #     "threshold": threshold,
        #     "threshold_type": "low cut"
        # }
        kernel = ThresholdWeightKernel(threshold=threshold, threshold_type="low cut")

#        kernel.from_dict(data_dict)
        values = np.array([0.7, 0.8, 0.9])
        expected = np.array([0.0, 1.0, 1.0])
        np.testing.assert_array_equal(kernel.evaluate(values), expected)

    def test_high_cut(self):
        kernel = ThresholdWeightKernel(threshold=0.8, threshold_type="high cut")
        values = np.array([0.7, 0.8, 0.9])
        expected = np.array([1.0, 1.0, 0.0])
        np.testing.assert_array_equal(kernel.evaluate(values), expected)

    def test_invalid_type(self):
        with self.assertRaises(MTSchemaError):
            kernel = ThresholdWeightKernel(0.8, threshold_type="invalid")
        # with self.assertRaises(ValueError):
        #     kernel.evaluate(np.array([0.7, 0.8, 0.9]))

if __name__ == "__main__":
    unittest.main()
