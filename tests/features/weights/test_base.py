# -*- coding: utf-8 -*-
"""
    Tests for the weights base class

"""

import unittest

import numpy as np
from mt_metadata.features.weights.base import BaseWeightKernel


class TestBaseWeightKernel(unittest.TestCase):

    def test_init(self):
        base_instance = BaseWeightKernel()
        self.assertIsInstance(base_instance, BaseWeightKernel)

    def test_evaluate_not_implemented(self):
        base_instance = BaseWeightKernel()
        with self.assertRaises(NotImplementedError):
            base_instance.evaluate(np.array([1, 2, 3]))


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
