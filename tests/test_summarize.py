# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 11:26:01 2023

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import unittest

import numpy as np
import pandas as pd

from mt_metadata.utils import summarize
from mt_metadata.base.schema import BaseDict
from mt_metadata import __version__

# =============================================================================


class TestSummarizeTimeSeries(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ts_dict = summarize.summarize_timeseries_standards()

    def test_not_empty(self):
        self.assertTrue(len(self.ts_dict.keys()) > 0)

    def test_it_base_dict(self):
        self.assertIsInstance(self.ts_dict, BaseDict)

    def test_keys(self):
        for key in [
            "survey",
            "station",
            "run",
            "electric",
            "magnetic",
            "auxiliary",
            "pole_zero_filter",
            "frequency_amplitude_phase_filter",
            "coefficient_filter",
            "fir_filter",
            "time_delay_filter",
        ]:
            self.assertIn(key, self.ts_dict.keys())


class TestSummaryToArray(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.entries = summarize.summary_to_array(
            summarize.summarize_timeseries_standards()
        )

    def test_is_np_array(self):
        self.assertIsInstance(self.entries, np.ndarray)

    def test_first_entry_attribute(self):
        self.assertEqual(
            self.entries[0]["attribute"], "mt_metadata.standards.version"
        )

    def test_first_entry_description(self):
        self.assertEqual(
            self.entries[0]["description"],
            f"Metadata standards version {__version__}",
        )


class TestSummarizeStandards(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.df = summarize.summarize_standards()

    def test_is_dataframe(self):
        self.assertIsInstance(self.df, pd.DataFrame)

    def test_first_entry_attribute(self):
        self.assertEqual(
            self.df.loc[0, "attribute"], "mt_metadata.standards.version"
        )

    def test_first_entry_description(self):
        self.assertEqual(
            self.df.loc[0, "description"],
            f"Metadata standards version {__version__}",
        )


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
