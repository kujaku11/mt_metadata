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
from mt_metadata import TF_XML

# =============================================================================
# EMTFXML
# =============================================================================


class TestEMTFXML(unittest.TestCase):
    def setUp(self):
        self.xml = EMTFXML(fn=TF_XML)
        self.maxDiff = None

    def test_basics(self):
        test_dict = OrderedDict(
            [
                ("description", "Magnetotelluric Transfer Functions"),
                ("product_id", "USMTArray.NMX20.2020"),
                ("sub_type", "MT_TF"),
                ("tags", "impedance,tipper"),
            ]
        )

        self.assertDictEqual(test_dict, self.xml.to_dict(single=True))

    def test_attachments(self):
        test_dict = OrderedDict(
            [
                ("description", "The original used to produce the XML"),
                ("filename", "NMX20b_NMX20_NMW20_COR21_NMY21-NMX20b_NMX20_UTS18.zmm"),
            ]
        )

        self.assertDictEqual(test_dict, self.xml.attachment.to_dict(single=True))

    def test_external_url(self):
        test_dict = OrderedDict(
            [
                ("description", "IRIS DMC MetaData"),
                ("url", "http://www.iris.edu/mda/ZU/NMX20"),
            ]
        )

        self.assertDictEqual(test_dict, self.xml.external_url.to_dict(single=True))

    def test_primary_data(self):
        test_dict = OrderedDict(
            [("filename", "NMX20b_NMX20_NMW20_COR21_NMY21-NMX20b_NMX20_UTS18.png")]
        )

        self.assertDictEqual(test_dict, self.xml.primary_data.to_dict(single=True))

    def test_provenance(self):
        test_dict = OrderedDict(
            [
                ("create_time", "2021-03-17T14:47:44+00:00"),
                ("creating_application", "EMTF File Conversion Utilities 4.0"),
                ("creator.email", "pbedrosian@usgs.gov"),
                ("creator.name", "Jade Crosbie, Paul Bedrosian and Anna Kelbert"),
                ("creator.org", "U.S. Geological Survey"),
                (
                    "creator.org_url",
                    "https://www.usgs.gov/natural-hazards/geomagnetism",
                ),
                ("submitter.email", "akelbert@usgs.gov"),
                ("submitter.name", "Anna Kelbert"),
                ("submitter.org", "U.S. Geological Survey, Geomagnetism Program"),
                (
                    "submitter.org_url",
                    "https://www.usgs.gov/natural-hazards/geomagnetism",
                ),
            ]
        )

        self.assertDictEqual(test_dict, self.xml.provenance.to_dict(single=True))

    def test_copyright(self):
        test_dict = OrderedDict(
            [
                (
                    "acknowledgement",
                    "The USMTArray-CONUS South campaign was carried out through a cooperative agreement between\nthe U.S. Geological Survey (USGS) and Oregon State University (OSU). A subset of 40 stations\nin the SW US were funded through NASA grant 80NSSC19K0232.\nLand permitting, data acquisition, quality control and field processing were\ncarried out by Green Geophysics with project management and instrument/engineering\nsupport from OSU and Chaytus Engineering, respectively.\nProgram oversight, definitive data processing and data archiving were provided\nby the USGS Geomagnetism Program and the Geology, Geophysics and Geochemistry Science Centers.\nWe thank the U.S. Forest Service, the Bureau of Land Management, the National Park Service,\nthe Department of Defense, numerous state land offices and the many private landowners\nwho permitted land access to acquire the USMTArray data.",
                ),
                (
                    "citation.authors",
                    "Schultz, A., Pellerin, L., Bedrosian, P., Kelbert, A., Crosbie, J.",
                ),
                ("citation.survey_d_o_i", "doi:10.17611/DP/EMTF/USMTARRAY/SOUTH"),
                (
                    "citation.title",
                    "USMTArray South Magnetotelluric Transfer Functions",
                ),
                ("citation.year", "2020-2023"),
                (
                    "conditions_of_use",
                    "All data and metadata for this survey are available free of charge and may be copied freely, duplicated and further distributed provided that this data set is cited as the reference, and that the author(s) contributions are acknowledged as detailed in the Acknowledgements. Any papers cited in this file are only for reference. There is no requirement to cite these papers when the data are used. Whenever possible, we ask that the author(s) are notified prior to any publication that makes use of these data.\n While the author(s) strive to provide data and metadata of best possible quality, neither the author(s) of this data set, nor IRIS make any claims, promises, or guarantees about the accuracy, completeness, or adequacy of this information, and expressly disclaim liability for errors and omissions in the contents of this file. Guidelines about the quality or limitations of the data and metadata, as obtained from the author(s), are included for informational purposes only.",
                ),
                ("release_status", "Unrestricted Release"),
            ]
        )

        self.assertDictEqual(test_dict, self.xml.copyright.to_dict(single=True))

    def test_site(self):
        test_dict = OrderedDict(
            [
                ("acquired_by", "National Geoelectromagnetic Facility"),
                ("country", "USA"),
                (
                    "data_quality_notes.comments.author",
                    "Jade Crosbie, Paul Bedrosian and Anna Kelbert",
                ),
                (
                    "data_quality_notes.comments.value",
                    "great TF from 10 to 10000 secs (or longer)",
                ),
                ("data_quality_notes.good_from_period", 5.0),
                ("data_quality_notes.good_to_period", 29127.0),
                ("data_quality_notes.rating", 5),
                ("end", "2020-10-07T20:28:00+00:00"),
                ("id", "NMX20"),
                ("location.datum", "WGS84"),
                ("location.declination.epoch", "2020.0"),
                ("location.declination.model", "EMAG2"),
                ("location.declination.value", 9.09),
                ("location.elevation", 1940.05),
                ("location.latitude", 34.470528),
                ("location.longitude", -108.712288),
                ("name", "Nations Draw, NM, USA"),
                ("orientation.angle_to_geographic_north", 0.0),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                ("orientation.value", "orthogonal"),
                ("project", "USMTArray"),
                ("run_list", "NMX20a NMX20b"),
                ("start", "2020-09-20T19:03:06+00:00"),
                ("survey", "CONUS South"),
                ("year_collected", 2020),
            ]
        )

        self.assertDictEqual(test_dict, self.xml.site.to_dict(single=True))

    def test_field_notes(self):
        test_list = [
            OrderedDict(
                [
                    ("comments.author", "Isaac Sageman"),
                    (
                        "comments.value",
                        "X array at 0 deg rotation. All e-lines 50m. Soft sandy dirt. Water tank ~400m NE. County Rd 601 ~200m SE. Warm sunny day.",
                    ),
                    ("end", "2020-09-20T19:29:28+00:00"),
                    ("instrument.id", "2612-01"),
                    ("instrument.manufacturer", "Barry Narod"),
                    ("instrument.name", "NIMS"),
                    ("instrument.type", None),
                    ("run", "NMX20a"),
                    ("sampling_rate", 1.0),
                    ("start", "2020-09-20T19:03:06+00:00"),
                ]
            ),
            OrderedDict(
                [
                    ("comments.author", "Isaac Sageman"),
                    (
                        "comments.value",
                        "X array at 0 deg rotation. All e-lines 50m. Soft sandy dirt. Water tank ~400m NE. County Rd 601 ~200m SE. Warm sunny day.",
                    ),
                    ("end", "2020-10-07T20:28:00+00:00"),
                    (
                        "errors",
                        "Found data gaps (2). Gaps of unknown length: 1 [1469160].]",
                    ),
                    ("instrument.id", "2612-01"),
                    ("instrument.manufacturer", "Barry Narod"),
                    ("instrument.name", "NIMS"),
                    ("instrument.type", None),
                    ("run", "NMX20b"),
                    ("sampling_rate", 1.0),
                    ("start", "2020-09-20T20:12:29+00:00"),
                ]
            ),
        ]

        for ii, item in enumerate(test_list):
            with self.subTest(msg=ii):
                self.assertDictEqual(
                    item, self.xml.field_notes[ii].to_dict(single=True)
                )

    def test_statistical_estimates(self):
        test_dict = OrderedDict(
            [
                (
                    "estimates_list",
                    [
                        "estimate:\n\tdescription = Variance\n\texternal_url = http://www.iris.edu/dms/products/emtf/variance.html\n\tintention = error estimate\n\tname = VAR\n\ttag = variance\n\ttype = real",
                        "estimate:\n\tdescription = Full covariance between each two TF components\n\texternal_url = http://www.iris.edu/dms/products/emtf/covariance.html\n\tintention = error estimate\n\tname = COV\n\ttag = covariance\n\ttype = complex",
                        "estimate:\n\tdescription = Inverse Coherent Signal Power Matrix (S)\n\texternal_url = http://www.iris.edu/dms/products/emtf/inverse_signal_covariance.html\n\tintention = signal power estimate\n\tname = INVSIGCOV\n\ttag = inverse_signal_covariance\n\ttype = complex",
                        "estimate:\n\tdescription = Residual Covariance (N)\n\texternal_url = http://www.iris.edu/dms/products/emtf/residual_covariance.html\n\tintention = error estimate\n\tname = RESIDCOV\n\ttag = residual_covariance\n\ttype = complex",
                        "estimate:\n\tdescription = Coherence\n\texternal_url = http://www.iris.edu/dms/products/emtf/coherence.html\n\tintention = signal coherence\n\tname = COH\n\ttag = coherence\n\ttype = complex",
                        "estimate:\n\tdescription = Multiple Coherence\n\texternal_url = http://www.iris.edu/dms/products/emtf/multiple_coherence.html\n\tintention = signal coherence\n\tname = PREDCOH\n\ttag = multiple_coherence\n\ttype = complex",
                        "estimate:\n\tdescription = Signal Amplitude\n\texternal_url = http://www.iris.edu/dms/products/emtf/signal_amplitude.html\n\tintention = signal power estimate\n\tname = SIGAMP\n\ttag = signal_amplitude\n\ttype = complex",
                        "estimate:\n\tdescription = Signal Noise\n\texternal_url = http://www.iris.edu/dms/products/emtf/signal_noise.html\n\tintention = error estimate\n\tname = SIGNOISE\n\ttag = signal_noise\n\ttype = complex",
                    ],
                )
            ]
        )

        self.assertDictEqual(
            test_dict, self.xml.statistical_estimates.to_dict(single=True)
        )

    def test_data_types(self):
        test_dict = OrderedDict(
            [
                (
                    "data_types_list",
                    [
                        "data_type:\n\tdescription = MT impedance\n\texternal_url = http://www.iris.edu/dms/products/emtf/impedance.html\n\tinput = H\n\tintention = primary data type\n\tname = Z\n\toutput = E\n\ttag = impedance\n\ttype = complex\n\tunits = [mV/km]/[nT]",
                        "data_type:\n\tdescription = Vertical Field Transfer Functions (Tipper)\n\texternal_url = http://www.iris.edu/dms/products/emtf/tipper.html\n\tinput = H\n\tintention = primary data type\n\tname = T\n\toutput = H\n\ttag = tipper\n\ttype = complex\n\tunits = []",
                    ],
                )
            ]
        )

        self.assertDictEqual(test_dict, self.xml.data_types.to_dict(single=True))

    def test_site_layout(self):
        test_dict = OrderedDict(
            [
                (
                    "input_channels",
                    [
                        "magnetic:\n\tname = Hx\n\torientation = 9.1\n\tx = 0.0\n\ty = 0.0\n\tz = 0.0",
                        "magnetic:\n\tname = Hy\n\torientation = 99.1\n\tx = 0.0\n\ty = 0.0\n\tz = 0.0",
                    ],
                ),
                (
                    "output_channels",
                    [
                        "magnetic:\n\tname = Hz\n\torientation = 9.1\n\tx = 0.0\n\ty = 0.0\n\tz = 0.0",
                        "electric:\n\tname = Ex\n\torientation = 9.1\n\tx = -50.0\n\tx2 = 50.0\n\ty = 0.0\n\ty2 = 0.0\n\tz = 0.0\n\tz2 = 0.0",
                        "electric:\n\tname = Ey\n\torientation = 99.1\n\tx = 0.0\n\tx2 = 0.0\n\ty = -50.0\n\ty2 = 50.0\n\tz = 0.0\n\tz2 = 0.0",
                    ],
                ),
            ]
        )

        self.assertDictEqual(test_dict, self.xml.site_layout.to_dict(single=True))

    def test_period_range(self):
        test_dict = OrderedDict([("max", 29127.11), ("min", 4.65455)])

        self.assertDictEqual(test_dict, self.xml.period_range.to_dict(single=True))

    def test_z(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 2, 2), self.xml.data.z.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.z[0],
                    np.array(
                        [
                            [-0.1160949 - 0.2708645j, 3.143284 + 1.101737j],
                            [-2.470717 - 0.7784633j, -0.1057851 + 0.1022045j],
                        ]
                    )
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.z[-1],
                    np.array(
                        [
                            [0.00483462 + 0.00983358j, 0.02643963 + 0.05098311j],
                            [-0.02203037 - 0.03744689j, -0.00295362 - 0.01293358j],
                        ]
                    )
                ).all()
            )
            
    def test_z_sip(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 2, 2), self.xml.data.z_invsigcov.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.z_invsigcov[0],
                    np.array([[ 0.8745101-2.905133e-08j, -0.4293981+1.663000e-01j],
                           [-0.4293981-1.663000e-01j,  1.39159  -7.486698e-10j]])
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.z_invsigcov[-1],
                    np.array([[9.120293e-08-2.13634e-16j, 5.066908e-08+2.26600e-08j],
                           [5.066908e-08-2.26600e-08j, 1.086271e-07+1.02634e-16j]])
                ).all()
            )
            
    def test_z_residual(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 2, 2), self.xml.data.z_residcov.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.z_residcov[0],
                    np.array([[ 1.286460e-03+8.470329e-22j, -5.816711e-05+3.347000e-05j],
                           [-5.816711e-05-3.347000e-05j,  1.037540e-03+0.000000e+00j]])
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.z_residcov[-1],
                    np.array([[ 86.38148+0.000000e+00j, -31.70986+1.281000e+00j],
                           [-31.70986-1.281000e+00j,  45.52852-2.775558e-17j]])
                ).all()
            )

    def test_t(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 1, 2), self.xml.data.t.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.t[0],
                    np.array([[-0.09386985 + 0.00620671j, 0.04601304 + 0.03035755j]])
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.t[-1],
                    np.array([[-0.03648688 + 0.08738894j, 0.1750294 + 0.1666582j]])
                ).all()
            )
            
    def test_t_sip(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 2, 2), self.xml.data.t_invsigcov.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.t_invsigcov[0],
                    np.array([[ 0.8745101-2.905133e-08j, -0.4293981+1.663000e-01j],
                           [-0.4293981-1.663000e-01j,  1.39159  -7.486698e-10j]])
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.t_invsigcov[-1],
                    np.array([[9.120293e-08-2.13634e-16j, 5.066908e-08+2.26600e-08j],
                           [5.066908e-08-2.26600e-08j, 1.086271e-07+1.02634e-16j]])
                ).all()
            )
            
    def test_t_residual(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 1, 1), self.xml.data.t_residcov.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.t_residcov[0],
                    np.array([[9.623e-05+0.j]])
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.xml.data.t_residcov[-1],
                    np.array([[29820.+0.j]])
                ).all()
            )
            



# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
