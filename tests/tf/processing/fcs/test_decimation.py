# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 12:12:41 2023

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
import unittest
from mt_metadata.transfer_functions.processing.fourier_coefficients import (
    Decimation,
    Channel,
)
from mt_metadata.transfer_functions.processing.aurora import DecimationLevel

# =============================================================================


class TestDecimationInitialization(unittest.TestCase):
    """
    Test Station metadata
    """

    def setUp(self):
        self.decimation = Decimation()

    def test_initialization(self):
        """
            Tests that class attributes from standards .json initialize to the default values

        """
        for key in self.decimation.get_attribute_list():
            with self.subTest(key):
                self.assertEqual(
                    self.decimation.get_attr_from_name(key),
                    self.decimation._attr_dict[key]["default"],
                )


class TestDecimation(unittest.TestCase):
    """
    Test Station metadata
    """

    @classmethod
    def setUpClass(self):

        self.dl = Decimation()
        self.dl.decimation_factor = 4
        self.dl.decimation_level = 1
        self.dl.id = 1
        self.dl.time_series_decimation.sample_rate = 16.0

        self.start = "2020-01-01T00:00:00+00:00"
        self.end = "2020-01-01T00:20:00+00:00"

        self.ex = Channel(component="ex")
        self.ex.time_period.start = self.start
        self.ex.time_period.end = self.end
        self.ex.sample_rate_window_step = 32
        self.ex.sample_rate_decimation_level = 16

        self.hy = Channel(component="hy")
        self.hy.time_period.start = self.start
        self.hy.time_period.end = self.end
        self.hy.sample_rate_window_step = 32
        self.hy.sample_rate_decimation_level = 16

        self.dl.add_channel(self.ex)
        self.dl.add_channel(self.hy)
        self.dl.update_time_period()

    def test_length(self):
        self.assertEqual(len(self.dl), 2)

    def test_add_channel(self):
        dl1 = self.dl.copy()
        dl2 = self.dl.copy()
        dl2.channels.remove("ex")
        ch_ey = self.ex.copy()
        ch_ey.component = "ey"
        dl2.add_channel(ch_ey)

        dl3 = dl1 + dl2

        self.assertEqual(len(dl3), 3)

        with self.assertRaises(ValueError):
            dl1.add_channel(None)
        with self.assertRaises(TypeError):
            dl3 = dl1 + None

    def test_remove_channel(self):
        dl1 = self.dl.copy()
        dl1.remove_channel("ex")
        assert ("ex" not in dl1.channels_estimated)
        dl1.remove_channel("hz")

    def test_update(self):
        dl1 = self.dl.copy()
        dl2 = self.dl.copy()
        dl2.channels.remove("ex")
        ch_ey = self.ex.copy()
        ch_ey.component = "ey"
        dl2.add_channel(ch_ey)

        dl1.update(dl2)

        self.assertEqual(len(dl1), 3)

        with self.assertRaises(AttributeError):
            dl1.update(None)

    def test_fft_frequencies(self):
        dl1 = self.dl.copy()
        freqs = dl1.fft_frequencies
        assert (len(freqs) == dl1.window.num_samples/2)


    def test_update_with_match(self):
        dl1 = self.dl.copy()
        dl2 = self.dl.copy()
        dl2.channels.remove("ex")
        ch_ey = self.ex.copy()
        ch_ey.component = "ey"
        dl2.add_channel(ch_ey)
        dl1.update(dl2, match=[
            "short_time_fourier_transform.method",
            "short_time_fourier_transform.recoloring"
        ])
        self.assertEqual(len(dl1), 3)

        dl1 = self.dl.copy()
        dl1.short_time_fourier_transform.method = "wavelet"
        with self.assertRaises(ValueError):
            dl1.update(dl2, match=[
                "short_time_fourier_transform.method",
                "short_time_fourier_transform.recoloring"
            ])


    def test_channels_estimated(self):
        self.assertListEqual(["ex", "hy"], self.dl.channels_estimated)


    def test_set_channels_estimated(self):
        dl1 = Decimation()
        dl1.channels_estimated = ["ex", "hy"]

        self.assertListEqual(["ex", "hy"], dl1.channels_estimated)

        # elicit some debug messages and errors
        dl1.channels_estimated = None #["ex", "hy"]
        with self.assertRaises(ValueError):
            dl1.channels_estimated = 77

    def test_has_channel(self):
        self.assertTrue(self.dl.has_channel("ex"))

    def test_channel_index(self):
        self.assertEqual(0, self.dl.channel_index("ex"))

    def test_get_channel(self):
        self.assertEqual(self.ex, self.dl.get_channel("ex"))

    def test_set_channels(self):
        dl1 = self.dl.copy()
        # set using a normal list
        channels = [dl1.channels[0], dl1.channels[1]]
        dl1.channels = channels

        with self.assertRaises(TypeError):
            dl1.channels = None




    def test_n_channels(self):
        self.assertEqual(2, self.dl.n_channels)

    def test_time_period(self):
        with self.subTest("start"):
            self.assertEqual(self.start, self.dl.time_period.start)
        with self.subTest("end"):
            self.assertEqual(self.end, self.dl.time_period.end)

    def test_factor(self):
        self.assertEqual(self.dl.decimation_factor, self.dl.factor)

    def test_window_length_true(self):
        self.assertEqual(True, self.dl.is_valid_for_time_series_length(4096))

    def test_window_length_false(self):
        self.assertEqual(False, self.dl.is_valid_for_time_series_length(46))


class TestDecimationAuroraDecimationLevel(unittest.TestCase):
    def setUp(self):

        self.dl = Decimation()
        self.dl.decimation_factor = 4
        self.dl.decimation_level = 1
        self.dl.id = 1
        self.dl.sample_rate_decimation = 16
        for ch in ["ex", "ey", "hx", "hy", "hz"]:
            self.dl.add_channel(Channel(component=ch))

        self.adl = DecimationLevel()
        self.adl.decimation.sample_rate = 16

    def test_has_required_channels_false(self):
        dl = Decimation()
        self.assertEqual(
            False, dl.has_fcs_for_aurora_processing(self.adl, None)
        )

    def test_has_required_channels_true(self):
        self.assertEqual(
            True, self.dl.has_fcs_for_aurora_processing(self.adl, None)
        )

    def test_sample_rate_false(self):
        self.adl.decimation.sample_rate = 24
        self.assertEqual(
            False, self.dl.has_fcs_for_aurora_processing(self.adl, None)
        )

    def test_decimation_method_false(self):
        self.adl.method = "other"
        self.assertEqual(
            False, self.dl.has_fcs_for_aurora_processing(self.adl, None)
        )

    def test_prewhitening_type_false(self):
        self.adl.prewhitening_type = "other"
        self.assertEqual(
            False, self.dl.has_fcs_for_aurora_processing(self.adl, None)
        )

    def test_recoloring_false(self):
        self.adl.stft.recoloring = False
        self.assertEqual(
            False, self.dl.has_fcs_for_aurora_processing(self.adl, None)
        )

    def test_pre_fft_detrend_type_false(self):
        self.adl.pre_fft_detrend_type = "other"
        self.assertEqual(
            False, self.dl.has_fcs_for_aurora_processing(self.adl, None)
        )

    def test_window_false(self):
        self.adl.window.type = "dpss"
        self.assertEqual(
            False, self.dl.has_fcs_for_aurora_processing(self.adl, None)
        )


# =============================================================================
if __name__ == "__main__":
    unittest.main()
