# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

# =============================================================================
#
# =============================================================================
import unittest

import numpy as np
from collections import OrderedDict
from mt_metadata.transfer_functions.io.emtfxml import EMTFXML
from mt_metadata import TF_POOR_XML

# =============================================================================
# EMTFXML
# =============================================================================


class TestEMTFXML(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.xml = EMTFXML(fn=TF_POOR_XML)
        self.maxDiff = None

    def test_basics(self):
        test_dict = OrderedDict(
            [
                ("description", "Magnetotelluric Transfer Functions"),
                ("product_id", "USMTArray.CAS04.2020"),
                ("sub_type", "MT_TF"),
                ("tags", "impedance,tipper"),
            ]
        )

        self.assertDictEqual(test_dict, self.xml.to_dict(single=True))

    def test_attachments(self):
        test_dict = OrderedDict(
            [
                ("description", "The original used to produce the XML"),
                ("filename", "CAS04-CAS04bcd_REV06-CAS04bcd_NVR08.zmm"),
            ]
        )

        self.assertDictEqual(
            test_dict, self.xml.attachment.to_dict(single=True)
        )

    def test_external_url(self):
        test_dict = OrderedDict(
            [
                ("description", "IRIS DMC MetaData"),
                ("url", "http://www.iris.edu/mda/8P/CAS04"),
            ]
        )

        self.assertDictEqual(
            test_dict, self.xml.external_url.to_dict(single=True)
        )

    def test_primary_data(self):
        test_dict = OrderedDict(
            [("filename", "CAS04-CAS04bcd_REV06-CAS04bcd_NVR08.png")]
        )

        self.assertDictEqual(
            test_dict, self.xml.primary_data.to_dict(single=True)
        )

    def test_provenance(self):
        test_dict = OrderedDict(
            [
                ("create_time", "2021-09-23T19:45:02+00:00"),
                ("creating_application", "EMTF File Conversion Utilities 4.0"),
                ("creator.email", "pbedrosian@usgs.gov"),
                (
                    "creator.name",
                    "Jade Crosbie, Paul Bedrosian and Anna Kelbert",
                ),
                ("creator.org", "U.S. Geological Survey"),
                (
                    "creator.org_url",
                    "https://www.usgs.gov/natural-hazards/geomagnetism",
                ),
                ("submitter.email", "akelbert@usgs.gov"),
                ("submitter.name", "Anna Kelbert"),
                (
                    "submitter.org",
                    "U.S. Geological Survey, Geomagnetism Program",
                ),
                (
                    "submitter.org_url",
                    "https://www.usgs.gov/natural-hazards/geomagnetism",
                ),
            ]
        )

        self.assertDictEqual(
            test_dict, self.xml.provenance.to_dict(single=True)
        )

    def test_copyright(self):
        test_dict = OrderedDict(
            [
                (
                    "acknowledgement",
                    "The USMTArray-CONUS South campaign was carried out through "
                    "a cooperative agreement between\nthe U.S. Geological Survey "
                    "(USGS) and Oregon State University (OSU). A subset of 40 "
                    "stations\nin the SW US were funded through NASA grant "
                    "80NSSC19K0232.\nLand permitting, data acquisition, quality "
                    "control and field processing were\ncarried out by Green "
                    "Geophysics with project management and "
                    "instrument/engineering\nsupport from OSU and Chaytus "
                    "Engineering, respectively.\nProgram oversight, definitive "
                    "data processing and data archiving were provided\nby the "
                    "USGS Geomagnetism Program and the Geology, Geophysics and "
                    "Geochemistry Science Centers.\nWe thank the U.S. Forest "
                    "Service, the Bureau of Land Management, the National Park "
                    "Service,\nthe Department of Defense, numerous state land "
                    "offices and the many private landowners\nwho permitted "
                    "land access to acquire the USMTArray data.",
                ),
                (
                    "citation.authors",
                    "Schultz, A., Pellerin, L., Bedrosian, P., Kelbert, A., Crosbie, J.",
                ),
                (
                    "citation.survey_d_o_i",
                    "doi:10.17611/DP/EMTF/USMTARRAY/SOUTH",
                ),
                (
                    "citation.title",
                    "USMTArray South Magnetotelluric Transfer Functions",
                ),
                ("citation.year", "2020-2023"),
                (
                    "conditions_of_use",
                    "All data and metadata for this survey are available free "
                    "of charge and may be copied freely, duplicated and further "
                    "distributed provided that this data set is cited as the "
                    "reference, and that the author(s) contributions are "
                    "acknowledged as detailed in the Acknowledgements. Any "
                    "papers cited in this file are only for reference. There "
                    "is no requirement to cite these papers when the data are "
                    "used. Whenever possible, we ask that the author(s) are "
                    "notified prior to any publication that makes use of these "
                    "data.\n While the author(s) strive to provide data and "
                    "metadata of best possible quality, neither the author(s) "
                    "of this data set, nor IRIS make any claims, promises, or "
                    "guarantees about the accuracy, completeness, or adequacy "
                    "of this information, and expressly disclaim liability for "
                    "errors and omissions in the contents of this file. "
                    "Guidelines about the quality or limitations of the data "
                    "and metadata, as obtained from the author(s), are included "
                    "for informational purposes only.",
                ),
                ("release_status", "Unrestricted Release"),
            ]
        )

        self.assertDictEqual(test_dict, self.xml.copyright.to_dict(single=True))

    def test_site(self):
        test_dict = OrderedDict(
            [
                ("acquired_by", "National Geoelectromagnetic Facility"),
                (
                    "data_quality_notes.comments.author",
                    "Jade Crosbie, Paul Bedrosian and Anna Kelbert",
                ),
                (
                    "data_quality_notes.comments.value",
                    "good TF from 10 to 10000 secs",
                ),
                ("data_quality_notes.rating", 4),
                ("data_quality_warnings.flag", 0),
                ("end", "2020-07-13T21:46:12+00:00"),
                ("id", "CAS04"),
                ("location.elevation", 329.387),
                ("location.latitude", 37.63335),
                ("location.longitude", -121.46838),
                ("name", "Corral Hollow, CA, USA"),
                ("orientation.angle_to_geographic_north", 0.0),
                ("orientation.layout", "orthogonal"),
                ("project", "USMTArray"),
                ("run_list", "CAS04a CAS04b CAS04c CAS04d"),
                ("start", "2020-06-02T18:41:43+00:00"),
                ("survey", "CONUS South"),
                ("year_collected", 2020),
            ]
        )

        self.assertDictEqual(test_dict, self.xml.site.to_dict(single=True))

    def test_field_notes(self):
        test_dict = OrderedDict()
        og_dict = self.xml.field_notes.to_dict(single=True)
        try:
            og_dict.pop("extra_attribute")
        except KeyError:
            pass

        self.assertDictEqual(test_dict, og_dict)

    def test_statistical_estimates(self):
        test_dict = OrderedDict([("estimates_list", [])])
        og_dict = self.xml.statistical_estimates.to_dict(single=True)
        try:
            og_dict.pop("extra_attribute")
        except KeyError:
            pass

        self.assertDictEqual(test_dict, og_dict)

    def test_data_types(self):
        test_dict = OrderedDict(
            [
                (
                    "data_types_list",
                    [
                        {
                            "data_type": OrderedDict(
                                [
                                    ("description", "MT impedance"),
                                    (
                                        "external_url",
                                        "http://www.iris.edu/dms/products/emtf/impedance.html",
                                    ),
                                    ("input", "H"),
                                    ("intention", "primary data type"),
                                    ("name", "Z"),
                                    ("output", "E"),
                                    ("tag", "impedance"),
                                    ("type", "complex"),
                                    ("units", "[mV/km]/[nT]"),
                                ]
                            )
                        },
                        {
                            "data_type": OrderedDict(
                                [
                                    (
                                        "description",
                                        "Vertical Field Transfer Functions (Tipper)",
                                    ),
                                    (
                                        "external_url",
                                        "http://www.iris.edu/dms/products/emtf/tipper.html",
                                    ),
                                    ("input", "H"),
                                    ("intention", "primary data type"),
                                    ("name", "T"),
                                    ("output", "H"),
                                    ("tag", "tipper"),
                                    ("type", "complex"),
                                    ("units", "[]"),
                                ]
                            )
                        },
                    ],
                )
            ]
        )

        self.assertDictEqual(
            test_dict, self.xml.data_types.to_dict(single=True)
        )

    def test_site_layout(self):
        test_dict = OrderedDict(
            [
                (
                    "input_channels",
                    [
                        {
                            "magnetic": OrderedDict(
                                [
                                    ("name", "Hx"),
                                    ("orientation", 13.2),
                                    ("x", 0.0),
                                    ("y", 0.0),
                                    ("z", 0.0),
                                ]
                            )
                        },
                        {
                            "magnetic": OrderedDict(
                                [
                                    ("name", "Hy"),
                                    ("orientation", 103.2),
                                    ("x", 0.0),
                                    ("y", 0.0),
                                    ("z", 0.0),
                                ]
                            )
                        },
                    ],
                ),
                (
                    "output_channels",
                    [
                        {
                            "magnetic": OrderedDict(
                                [
                                    ("name", "Hz"),
                                    ("orientation", 13.2),
                                    ("x", 0.0),
                                    ("y", 0.0),
                                    ("z", 0.0),
                                ]
                            )
                        },
                        {
                            "electric": OrderedDict(
                                [
                                    ("name", "Ex"),
                                    ("orientation", 13.2),
                                    ("x", -46.0),
                                    ("x2", 46.0),
                                    ("y", 0.0),
                                    ("y2", 0.0),
                                    ("z", 0.0),
                                    ("z2", 0.0),
                                ]
                            )
                        },
                        {
                            "electric": OrderedDict(
                                [
                                    ("name", "Ey"),
                                    ("orientation", 103.2),
                                    ("x", 0.0),
                                    ("x2", 0.0),
                                    ("y", -46.0),
                                    ("y2", 46.0),
                                    ("z", 0.0),
                                    ("z2", 0.0),
                                ]
                            )
                        },
                    ],
                ),
            ]
        )

        self.assertDictEqual(
            test_dict, self.xml.site_layout.to_dict(single=True)
        )

    def test_processing_info(self):
        test_dict = OrderedDict(
            [
                ("process_date", "1980-01-01"),
                ("processing_software.last_mod", "2015-08-26"),
                ("processing_software.name", "EMTF"),
                ("processing_tag", "CAS04-CAS04bcd_REV06-CAS04bcd_NVR08"),
                ("remote_info.site.id", "REV06"),
                ("remote_info.site.location.elevation", 61.05),
                ("remote_info.site.location.latitude", 35.71262),
                ("remote_info.site.location.longitude", -119.466415),
                ("remote_info.site.name", "Poso Creek, CA, USA"),
                ("remote_info.site.orientation.angle_to_geographic_north", 0.0),
                ("remote_info.site.orientation.layout", "orthogonal"),
                ("remote_info.site.year_collected", 1980),
                ("remote_ref.type", "Robust Remote Reference"),
                ("sign_convention", "exp(+ i\\omega t)"),
            ]
        )

        self.assertDictEqual(
            test_dict, self.xml.processing_info.to_dict(single=True)
        )

    def test_period_range(self):
        test_dict = OrderedDict([("max", 29127.11), ("min", 4.65455)])

        self.assertDictEqual(
            test_dict, self.xml.period_range.to_dict(single=True)
        )

    def test_z(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 2, 2), self.xml.data.z.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.z[0],
                    np.array(
                        [
                            [0.05218971 - 0.493787j, 1.004782 + 1.873659j],
                            [-0.8261183 + 1.226159j, 1.36161 - 1.376113j],
                        ]
                    ),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.z[-1],
                    np.array(
                        [
                            [
                                0.03680307 + 0.00131353j,
                                0.06559774 + 0.00177508j,
                            ],
                            [
                                -0.05877226 - 0.02631392j,
                                -0.01419307 - 0.03934453j,
                            ],
                        ]
                    ),
                ).all()
            )

    def test_z_sip(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 2, 2), self.xml.data.z_invsigcov.shape)

        with self.subTest(msg="zero"):
            self.assertTrue(np.all(self.xml.data.z_invsigcov == 0))

    def test_z_residual(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 2, 2), self.xml.data.z_residcov.shape)

        with self.subTest(msg="zero"):
            self.assertTrue(np.all(self.xml.data.z_residcov == 0))

    def test_t(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 1, 2), self.xml.data.t.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.t[0],
                    np.array([[-0.5953611 - 1.984346j, -1.313187 + 1.159378j]]),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.t[-1],
                    np.array(
                        [[-0.02102757 - 0.06664169j, 0.5568553 + 0.1630035j]]
                    ),
                ).all()
            )

    def test_t_sip(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 2, 2), self.xml.data.t_invsigcov.shape)

        with self.subTest(msg="zero"):
            self.assertTrue(np.all(self.xml.data.t_invsigcov == 0))

    def test_t_residual(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 1, 1), self.xml.data.t_residcov.shape)

        with self.subTest(msg="zero"):
            self.assertTrue(np.all(self.xml.data.t_residcov == 0))


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
