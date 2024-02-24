# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:11:24 2022

@author: kkappler
"""

import unittest
from mt_metadata.transfer_functions.processing.aurora import ChannelNomenclature
from mt_metadata.transfer_functions.processing.aurora.channel_nomenclature import load_channel_maps

class TestChannelNomenclature(unittest.TestCase):
    """
    Test ChannelNomenclature
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.channel_maps = load_channel_maps()

    def setUp(self):
        pass

    def testLoadChannelMaps(self):
        self.assertIsInstance(self.channel_maps, dict)


    def test_initialization(self):
        for keyword in self.channel_maps:
            ch_nom = ChannelNomenclature(keyword=keyword)
            cond = self.channel_maps[keyword] == ch_nom.get_channel_map()
            self.assertTrue(cond)

    def test_channel_sets(self):
        keyword = list(self.channel_maps.keys())[0]
        ch_nom = ChannelNomenclature(keyword=keyword)
        assert len(ch_nom.ex_ey) == 2
        assert len(ch_nom.ex_ey_hz) == 3
        assert len(ch_nom.hx_hy) == 2
        assert len(ch_nom.channels) == 5

    def test_repr(self):
        """ Takes the __repr__ string, and casts to a dict (via json), and compares to channel_map attr"""
        import json
        for keyword in self.channel_maps:
            ch_nom = ChannelNomenclature(keyword=keyword)
            channel_map = ch_nom.get_channel_map() # dict
            repr = json.loads(ch_nom.__repr__())["channel_nomenclature"]
            assert channel_map == repr


if __name__ == "__main__":
    unittest.main()
