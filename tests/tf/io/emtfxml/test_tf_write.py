# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 08:52:43 2023

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
import unittest

import numpy as np
from collections import OrderedDict
from mt_metadata import TF_XML
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io.emtfxml import EMTFXML

# =============================================================================


class TestWriteEMTFXML(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_XML)
        self.tf.read_tf_file()
        self.x1 = self.tf.write_tf_file(file_type="xml")
        self.maxDiff = None

        self.x0 = EMTFXML(TF_XML)

    def test_description(self):
        self.assertEqual(self.x0.description, self.x1.description)

    def test_product_id(self):
        self.assertEqual(self.x0.product_id, self.x1.product_id)

    def test_sub_type(self):
        self.assertEqual(self.x0.sub_type, self.x1.sub_type)

    def test_notes(self):
        self.assertEqual(self.x0.notes, self.x1.notes)

    def test_tags(self):
        self.assertListEqual(
            [v.strip() for v in self.x0.tags.split(",")],
            [v.strip() for v in self.x1.tags.split(",")],
        )

    def test_external_url(self):
        with self.subTest("attribute"):
            self.assertEqual(self.x0.external_url, self.x1.external_url)

        with self.subTest("to_xml"):
            self.assertEqual(
                self.x0.external_url.to_xml(string=True),
                self.x1.external_url.to_xml(string=True),
            )

    def test_primary_data(self):
        with self.subTest("attribute"):
            self.assertEqual(self.x0.primary_data, self.x1.primary_data)

        with self.subTest("to_xml"):
            self.assertEqual(
                self.x0.primary_data.to_xml(string=True),
                self.x1.primary_data.to_xml(string=True),
            )

    def test_attachment(self):
        with self.subTest("attribute"):
            self.assertEqual(self.x0.attachment, self.x1.attachment)

        with self.subTest("to_xml"):
            self.assertEqual(
                self.x0.attachment.to_xml(string=True),
                self.x1.attachment.to_xml(string=True),
            )

    def test_provenance(self):
        d0 = self.x0.provenance.to_dict(single=True)
        d1 = self.x1.provenance.to_dict(single=True)

        for key in ["create_time", "creating_application"]:
            d0.pop(key)
            d1.pop(key)

        self.assertDictEqual(d0, d1)

    # def test_element_object(self):
    #     for key in self.x1.element_keys:
    #         with self.subTest(key):
    #             if key in ["provenance", "statistical_estimates"]:
    #                 self.assertNotEqual(
    #                     getattr(self.x0, key), getattr(self.x1, key)
    #                 )
    #             elif key in ["tags"]:
    #
    #             else:
    #                 self.assertEqual(
    #                     getattr(self.x0, key), getattr(self.x1, key)
    #                 )


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
