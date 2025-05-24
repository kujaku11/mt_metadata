"""
    Tests for the MonotonicWeightKernel.
"""

import numpy as np
import unittest

from mt_metadata.features.weights.monotonic_weight_kernel import BaseMonotonicWeightKernel
from mt_metadata.features.weights.monotonic_weight_kernel import TaperMonotonicWeightKernel
from mt_metadata.features.weights.monotonic_weight_kernel import ActivationMonotonicWeightKernel

class TestBaseMonotonicWeightKernel(unittest.TestCase):

    def test_init_defaults(self):
        # Should initialize with defaults from schema
        kernel = BaseMonotonicWeightKernel()
        self.assertIsInstance(kernel, BaseMonotonicWeightKernel)

    def test_base_monotonic_weight_kernel_low_cut(self):
        kernel_dict = {
            "transition_lower_bound": 0.3,
            "transition_upper_bound": 0.8,
            "threshold": "low cut"
        }
        kernel = BaseMonotonicWeightKernel()
        kernel.from_dict(kernel_dict)

    def test_taper_monotonic_weight_kernel(self):
        # test  high cut
        kernel_dict = {
            "transition_lower_bound": 0.3,
            "transition_upper_bound": 0.8,
            "half_window_style": "hann",
            "threshold": "high cut"
        }
        kernel = TaperMonotonicWeightKernel()
        kernel.from_dict(kernel_dict)
        test_values = np.array([0.1, 0.3, 0.5, 0.8, 1.0])
        weights = kernel.evaluate(test_values)
        self.assertEqual(weights[0], 1.0)
        self.assertEqual(weights[-1], 0.0)
        self.assertEqual(len(weights), len(test_values))

        # test low cut
        kernel_dict = {
            "transition_lower_bound": 0.3,
            "transition_upper_bound": 0.8,
            "half_window_style": "hann",
            "threshold": "low cut"
        }
        kernel = TaperMonotonicWeightKernel()
        kernel.from_dict(kernel_dict)
        test_values = np.array([0.1, 0.3, 0.5, 0.8, 1.0])
        weights = kernel.evaluate(test_values)
        self.assertEqual(weights[0], 0.0)
        self.assertEqual(weights[-1], 1.0)
        self.assertEqual(len(weights), len(test_values))

    def test_activation_monotonic_weight_kernel(self):
        # test high cut
        kernel_dict = {
            "transition_lower_bound": 0.3,
            "transition_upper_bound": 0.8,
            "activation_style": "sigmoid",
            "threshold": "high cut"
        }
        kernel = ActivationMonotonicWeightKernel()
        kernel.from_dict(kernel_dict)
        test_values = np.array([0.1, 0.3, 0.5, 0.8, 1.0])
        weights = kernel.evaluate(test_values)
        self.assertAlmostEqual(weights[0], 1.0, places=1)
        self.assertAlmostEqual(weights[-1], 0.0, places=1)
        self.assertEqual(len(weights), len(test_values))

        # test low cut
        kernel_dict = {
            "transition_lower_bound": 0.3,
            "transition_upper_bound": 0.8,
            "activation_style": "sigmoid",
            "threshold": "low cut"
        }
        kernel = ActivationMonotonicWeightKernel()
        kernel.from_dict(kernel_dict)
        test_values = np.array([0.1, 0.3, 0.5, 0.8, 1.0])
        weights = kernel.evaluate(test_values)
        self.assertAlmostEqual(weights[0], 0.0, places=1)
        self.assertAlmostEqual(weights[-1], 1.0, places=1)
        self.assertEqual(len(weights), len(test_values))


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
