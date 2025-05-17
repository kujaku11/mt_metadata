"""
    Tests for the MonotonicWeightKernel.
"""

import numpy as np
import unittest

from mt_metadata.features.weights.monotonic_weight_kernel import MonotonicWeightKernel

"""
    Tests for the MonotonicWeightKernel.
"""

import numpy as np
import unittest

from mt_metadata.features.weights.monotonic_weight_kernel import MonotonicWeightKernel

class TestMonotonicWeightKernel(unittest.TestCase):

    def test_init_defaults(self):
        # Should initialize with defaults from schema
        kernel = MonotonicWeightKernel()
        self.assertIsInstance(kernel, MonotonicWeightKernel)

    def test_monotonic_weight_kernel_low_cut(self):
        kernel_dict = {
            "transition_lower_bound": 0.3,
            "transition_upper_bound": 0.8,
            "half_window_style": "hann",
            "threshold": "low cut"
        }
        kernel = MonotonicWeightKernel()
        kernel.from_dict(kernel_dict)
        test_values = np.array([0.1, 0.3, 0.5, 0.8, 1.0])
        weights = kernel.evaluate(test_values)
        self.assertEqual(weights[0], 0.0)
        self.assertEqual(weights[-1], 1.0)
        self.assertEqual(len(weights), len(test_values))

    def test_monotonic_weight_kernel_high_cut(self):
        kernel_dict = {
            "transition_lower_bound": 0.3,
            "transition_upper_bound": 0.8,
            "half_window_style": "hann",
            "threshold": "high cut"
        }
        kernel = MonotonicWeightKernel()
        kernel.from_dict(kernel_dict)
        test_values = np.array([0.1, 0.3, 0.5, 0.8, 1.0])
        weights = kernel.evaluate(test_values)
        self.assertEqual(weights[0], 1.0)
        self.assertEqual(weights[-1], 0.0)
        self.assertEqual(len(weights), len(test_values))


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
