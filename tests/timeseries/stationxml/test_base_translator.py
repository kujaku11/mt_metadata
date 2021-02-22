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
        self.run_comment = Comment(
            "author: John Doe, comments: X array a 0 and 90 degrees.",
            subject="mt.run:b.metadata_by",
        )
        self.null_comment = Comment(None, subject="mt.survey.survey_id")
        self.long_comment = Comment("a: b, c: d, efg", subject="mt.run.a:comment")
        self.odd_comment = Comment("a: b: action, d: efg", subject="mt.run.odd")
        self.normal_comment = Comment("normal", subject="mt.run.comment")
        self.doi = [r"DOI:10.1234.mt/test"]

    def test_null_comment(self):
        k, v = BaseTranslator.read_xml_comment(self.null_comment)
        self.assertEqual("mt.survey.survey_id", k)
        self.assertEqual("None", v)

    def test_run_comment(self):
        k, v = BaseTranslator.read_xml_comment(self.run_comment)
        self.assertEqual(k, "mt.run:b.metadata_by")
        self.assertIsInstance(v, dict)
        self.assertDictEqual(
            v, {"author": "John Doe", "comments": "X array a 0 and 90 degrees."}
        )

    def test_long_comment(self):
        k, v = BaseTranslator.read_xml_comment(self.long_comment)
        self.assertEqual(k, "mt.run.a:comment")
        self.assertIsInstance(v, dict)
        self.assertDictEqual(v, {"a": "b", "c": "d, efg"})

    def test_odd_comment(self):
        k, v = BaseTranslator().read_xml_comment(self.odd_comment)
        self.assertEqual(k, "mt.run.odd")
        self.assertIsInstance(v, dict)
        self.assertDictEqual(v, {"a": "b-- action", "d": "efg"})

    def test_normal_comment(self):
        k, v = BaseTranslator().read_xml_comment(self.normal_comment)
        self.assertEqual(k, "mt.run.comment")
        self.assertEqual(v, "normal")
        
    def test_flip_dict(self):
        original = {"a": "b", "c": "d", "e": None, "f": "special"}
        flipped = BaseTranslator().flip_dict(original)
        self.assertDictEqual({'b': "a", "d": "c"}, flipped)
        
    def test_read_identifier(self):
        read_doi = BaseTranslator().read_xml_identifier(self.doi)
        self.assertEqual(read_doi, "10.1234.mt/test")
        


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
