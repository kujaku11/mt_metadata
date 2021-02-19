# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 16:33:42 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

import unittest
from mt_metadata.timeseries.stationxml.utils import BaseTranslator
from obspy.core.inventory import Comment

class TestReadXMLComment(unittest.TestCase):
    """
    test reading different comments
    """
    
    def setUp(self):
        self.run_comment = Comment("author: Kristin Pratscher, comments: X array a 0 and 90 degreest. Site in rocky drainage basin proximal to basalt lava flows. L", subject="mt.run:b.metadata_by") 
    def test_run_comment(self):
        k, v = BaseTranslator.read_xml_comment(self.run_commment)
        self.assertEqual(k, "b.metadata_by")
        
# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()