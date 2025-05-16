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

from mt_metadata import TF_XML_COMPLETE_REMOTE_INFO
from mt_metadata.transfer_functions import TF
from mt_metadata.transfer_functions.io.emtfxml import EMTFXML


# =============================================================================


class TestWriteEMTFXML(unittest.TestCase):
    """
    Compare the translation from an EMTF XML object to and MT object and back
    to an EMTF XML object.
    """

    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_XML_COMPLETE_REMOTE_INFO)
        self.tf.read()
        self.x1 = self.tf.to_emtfxml()
        self.maxDiff = None

        self.x0 = EMTFXML(TF_XML_COMPLETE_REMOTE_INFO)

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
            self.assertMultiLineEqual(
                self.x0.external_url.to_xml(string=True),
                self.x1.external_url.to_xml(string=True),
            )

    def test_primary_data(self):
        with self.subTest("attribute"):
            self.assertEqual(self.x0.primary_data, self.x1.primary_data)

        with self.subTest("to_xml"):
            self.assertMultiLineEqual(
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

    def test_copyright(self):
        with self.subTest("attribute"):
            self.assertEqual(self.x0.copyright, self.x1.copyright)

        with self.subTest("to_xml"):
            self.assertMultiLineEqual(
                self.x0.copyright.to_xml(string=True),
                self.x1.copyright.to_xml(string=True),
            )

    def test_site(self):
        with self.subTest("attribute"):
            self.assertDictEqual(
                self.x0.site.to_dict(single=True),
                self.x1.site.to_dict(single=True),
            )

        with self.subTest("to_xml"):
            self.assertEqual(
                self.x0.site.to_xml(string=True),
                self.x1.site.to_xml(string=True),
            )

    def test_field_notes(self):
        with self.subTest("attribute"):
            self.assertDictEqual(
                self.x0.field_notes.to_dict(single=True),
                self.x1.field_notes.to_dict(single=True),
            )

        # The rounding is not the same
        with self.subTest("to_xml"):
            self.assertNotEqual(
                self.x0.field_notes.to_xml(string=True),
                self.x1.field_notes.to_xml(string=True),
            )

    def test_processing_info(self):
        d0 = self.x0.processing_info.to_dict(single=True)
        d1 = self.x1.processing_info.to_dict(single=True)

        for key, value_0 in d0.items():
            value_1 = d1[key]
            with self.subTest(f"{key}"):
                if "tag" in key:
                    self.assertNotEqual(value_0, value_1)
                else:
                    self.assertEqual(value_0, value_1)

    def test_processing_info_to_xml(self):
        x0 = self.x0.processing_info.to_xml(string=True).split("\n")
        x1 = self.x1.processing_info.to_xml(string=True).split("\n")

        for line_0, line_1 in zip(x0, x1):
            with self.subTest(line_0):
                if "ProcessingTag" in line_0:
                    self.assertNotEqual(line_0, line_1)
                else:
                    self.assertEqual(line_0, line_1)

    def test_statistical_estimates(self):
        for estimate_01 in self.x0.statistical_estimates.estimates_list:
            for estimate_02 in self.x1.statistical_estimates.estimates_list:
                with self.subTest(estimate_02):
                    self.assertIn(
                        estimate_02,
                        self.x0.statistical_estimates.estimates_list,
                    )
                if estimate_01 == estimate_02:
                    with self.subTest(f"{estimate_02}.to_xml"):
                        self.assertMultiLineEqual(
                            estimate_01.to_xml(string=True),
                            estimate_02.to_xml(string=True),
                        )

    def test_data_types(self):
        with self.subTest("attribute"):
            self.assertDictEqual(
                self.x0.data_types.to_dict(single=True),
                self.x1.data_types.to_dict(single=True),
            )

        # The rounding is not the same
        with self.subTest("to_xml"):
            self.assertMultiLineEqual(
                self.x0.data_types.to_xml(string=True),
                self.x1.data_types.to_xml(string=True),
            )

    def test_site_layout(self):
        with self.subTest("attribute"):
            self.assertDictEqual(
                self.x0.site_layout.to_dict(single=True),
                self.x1.site_layout.to_dict(single=True),
            )

        # The rounding is not the same
        with self.subTest("to_xml"):
            self.assertMultiLineEqual(
                self.x0.site_layout.to_xml(string=True),
                self.x1.site_layout.to_xml(string=True),
            )

    def test_data_z(self):
        self.assertTrue(np.all(np.isclose(self.x0.data.z, self.x1.data.z)))

    def test_data_z_var(self):
        self.assertTrue(np.all(np.isclose(self.x0.data.z_var, self.x1.data.z_var)))

    def test_data_z_invsigcov(self):
        self.assertTrue(
            np.all(np.isclose(self.x0.data.z_invsigcov, self.x1.data.z_invsigcov))
        )

    def test_data_z_residcov(self):
        self.assertTrue(
            np.all(np.isclose(self.x0.data.z_residcov, self.x1.data.z_residcov))
        )

    def test_data_t(self):
        self.assertTrue(np.all(np.isclose(self.x0.data.t, self.x1.data.t)))

    def test_data_t_var(self):
        self.assertTrue(np.all(np.isclose(self.x0.data.t_var, self.x1.data.t_var)))

    def test_data_t_invsigcov(self):
        self.assertTrue(
            np.all(np.isclose(self.x0.data.t_invsigcov, self.x1.data.t_invsigcov))
        )

    def test_data_t_residcov(self):
        self.assertTrue(
            np.all(np.isclose(self.x0.data.t_residcov, self.x1.data.t_residcov))
        )

    def test_period_range(self):
        with self.subTest("attribute"):
            self.assertDictEqual(
                self.x0.period_range.to_dict(single=True),
                self.x1.period_range.to_dict(single=True),
            )

        # The rounding is not the same
        with self.subTest("to_xml"):
            self.assertMultiLineEqual(
                self.x0.period_range.to_xml(string=True),
                self.x1.period_range.to_xml(string=True),
            )


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
