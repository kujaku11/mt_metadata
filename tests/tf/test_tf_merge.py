# -*- coding: utf-8 -*-
"""

Created on Wed May  3 19:08:34 2023

:author: Jared Peacock

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
import unittest
import numpy as np

from mt_metadata.transfer_functions.core import TF

# =============================================================================
np.random.seed(0)


class TestTFMerge(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.maxDiff = None
        self.n = 20
        self.tf_01 = TF()
        self.tf_01.station = "test"
        self.tf_01.survey = "a"
        self.tf_01.period = np.logspace(-3, 1, self.n)
        self.tf_01.impedance = np.random.rand(
            self.n, 2, 2
        ) + 1j * np.random.rand(self.n, 2, 2)

        self.tf_02 = TF()
        self.tf_02.station = "test"
        self.tf_02.survey = "a"
        self.tf_02.tf_id = "tfa"
        self.tf_02.period = np.logspace(1, 3, self.n)
        self.tf_02.impedance = np.random.rand(
            self.n, 2, 2
        ) + 1j * np.random.rand(self.n, 2, 2)

    def test_basic_merge(self):
        merged = self.tf_01.merge(self.tf_02)

        with self.subTest("periods"):

            self.assertTrue(
                np.allclose(
                    np.append(self.tf_01.period, self.tf_02.period),
                    merged.period,
                )
            )
        with self.subTest("survey_metadata"):
            self.assertDictEqual(
                self.tf_01.survey_metadata.to_dict(single=True),
                merged.survey_metadata.to_dict(single=True),
            )
        with self.subTest("station_metadata"):
            # merged.station_metadata.run_list =
            self.assertDictEqual(
                self.tf_01.station_metadata.to_dict(single=True),
                merged.station_metadata.to_dict(single=True),
            )

    def test_self_limit_periods_merge(self):
        merged = self.tf_01.merge(self.tf_02, period_min=0.001, period_max=9.9)

        with self.subTest("periods"):

            self.assertTrue(
                np.allclose(
                    np.append(self.tf_01.period[:-1], self.tf_02.period),
                    merged.period,
                )
            )
        with self.subTest("survey_metadata"):
            self.assertDictEqual(
                self.tf_01.survey_metadata.to_dict(single=True),
                merged.survey_metadata.to_dict(single=True),
            )
        with self.subTest("station_metadata"):
            # merged.station_metadata.run_list = [None]
            self.assertDictEqual(
                self.tf_01.station_metadata.to_dict(single=True),
                merged.station_metadata.to_dict(single=True),
            )

    def test_dict_input_merge(self):
        merged = self.tf_01.merge(
            {"tf": self.tf_02, "period_min": 10, "period_max": 100},
            period_min=0.001,
            period_max=9.9,
        )

        with self.subTest("periods"):

            self.assertTrue(
                np.allclose(
                    np.append(self.tf_01.period[:-1], self.tf_02.period[0:10]),
                    merged.period,
                )
            )
        with self.subTest("survey_metadata"):
            self.assertDictEqual(
                self.tf_01.survey_metadata.to_dict(single=True),
                merged.survey_metadata.to_dict(single=True),
            )
        with self.subTest("station_metadata"):
            # merged.station_metadata.run_list = [None]
            self.assertDictEqual(
                self.tf_01.station_metadata.to_dict(single=True),
                merged.station_metadata.to_dict(single=True),
            )

    def test_dict_fail(self):
        self.assertRaises(ValueError, self.tf_01.merge, {"a": 0})

    def test_item_fail(self):
        self.assertRaises(TypeError, self.tf_01.merge, 10)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
