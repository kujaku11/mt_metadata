# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:39:41 2022

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
import unittest
from collections import OrderedDict
import numpy as np

from obspy import read_inventory
from mt_metadata.timeseries.stationxml import XMLChannelMTChannel
from mt_metadata import STATIONXML_01
from mt_metadata.timeseries.filters import PoleZeroFilter

# =============================================================================


class TestXMLChannelTwoChannels(unittest.TestCase):
    """
    Test reading XML channel to MT Channel
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        for ch in self.inventory.networks[0].stations[0].channels:
            for stage in ch.response.response_stages:
                stage.name = None

        self.converter = XMLChannelMTChannel()
        self.maxDiff = None

    def test_rename_filters(self):
        mt_ch, ch_filter_dict = self.converter.xml_to_mt(
            self.inventory.networks[0].stations[0].channels[0]
        )

        self.assertListEqual(
            sorted(["zpk_00", "coefficient_00", "time delay_00"]),
            sorted(ch_filter_dict.keys()),
        )

    def test_filter_exists(self):
        pz = PoleZeroFilter(
            **OrderedDict(
                [
                    ("calibration_date", "1980-01-01"),
                    ("comments", "butterworth filter"),
                    ("gain", 1.0),
                    ("name", "zpk_00"),
                    ("normalization_factor", 1984.31439386406),
                    (
                        "poles",
                        np.array(
                            [
                                -6.283185 + 10.882477j,
                                -6.283185 - 10.882477j,
                                -12.566371 + 0.0j,
                            ]
                        ),
                    ),
                    ("type", "zpk"),
                    ("units_in", "nT"),
                    ("units_out", "V"),
                    ("zeros", np.array([], dtype="complex128")),
                ]
            )
        )
        existing_dict = {pz.name: pz}

        name, new = self.converter._add_filter_number(existing_dict, pz)
        with self.subTest("name"):
            self.assertEqual(name, pz.name)
        with self.subTest("new"):
            self.assertEqual(new, False)
