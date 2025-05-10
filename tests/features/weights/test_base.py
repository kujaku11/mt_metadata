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


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
