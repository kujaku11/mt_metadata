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
from mt_metadata import TF_XML
from mt_metadata.transfer_functions.core import TF

# =============================================================================
# EMTFXML
# =============================================================================


class TestEMTFXML(unittest.TestCase):
    def setUp(self):
        self.tf = TF(fn=TF_XML)
        self.maxDiff = None

    def test_station_metadata(self):
        meta_dict = OrderedDict(
            [
                ("acquired_by.author", "National Geoelectromagnetic Facility"),
                ("channels_recorded", sorted(["ex", "ey", "hx", "hy", "hz"])),
                ("data_type", "mt"),
                ("fdsn.id", "USMTArray.NMX20.2020"),
                ("geographic_name", "Nations Draw, NM, USA"),
                ("id", "NMX20"),
                ("location.datum", "WGS84"),
                ("location.declination.epoch", "2020.0"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", 9.09),
                ("location.elevation", 1940.05),
                ("location.latitude", 34.470528),
                ("location.longitude", -108.712288),
                ("orientation.angle_to_geographic_north", 0.0),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                ("provenance.creation_time", "2021-03-17T14:47:44+00:00"),
                ("provenance.software.author", "none"),
                ("provenance.software.name", "EMTF File Conversion Utilities 4.0"),
                ("provenance.software.version", None),
                ("provenance.submitter.author", "Anna Kelbert"),
                ("provenance.submitter.email", "akelbert@usgs.gov"),
                (
                    "provenance.submitter.organization",
                    "U.S. Geological Survey, Geomagnetism Program",
                ),
                ("run_list", ["NMX20a", "NMX20b"]),
                ("time_period.end", "2020-10-07T20:28:00+00:00"),
                ("time_period.start", "2020-09-20T19:03:06+00:00"),
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.processing_parameters", ["{type: None}"]),
                (
                    "transfer_function.remote_references",
                    [
                        "NMX20b",
                        "NMX20",
                        "NMW20",
                        "COR21",
                        "NMY21-NMX20b",
                        "NMX20",
                        "UTS18",
                    ],
                ),
                ("transfer_function.runs_processed", ["NMX20a", "NMX20b"]),
                ("transfer_function.sign_convention", "exp(+ i\\omega t)"),
            ]
        )

        self.assertDictEqual(meta_dict, self.tf.station_metadata.to_dict(single=True))

    def test_survey_metadata(self):
        meta_dict = OrderedDict(
            [
                ("acquired_by.author", "National Geoelectromagnetic Facility"),
                ("citation_dataset.doi", "doi:10.17611/DP/EMTF/USMTARRAY/SOUTH"),
                ("citation_journal.doi", None),
                (
                    "comments",
                    "The USMTArray-CONUS South campaign was carried out through a cooperative agreement between\nthe U.S. Geological Survey (USGS) and Oregon State University (OSU). A subset of 40 stations\nin the SW US were funded through NASA grant 80NSSC19K0232.\nLand permitting, data acquisition, quality control and field processing were\ncarried out by Green Geophysics with project management and instrument/engineering\nsupport from OSU and Chaytus Engineering, respectively.\nProgram oversight, definitive data processing and data archiving were provided\nby the USGS Geomagnetism Program and the Geology, Geophysics and Geochemistry Science Centers.\nWe thank the U.S. Forest Service, the Bureau of Land Management, the National Park Service,\nthe Department of Defense, numerous state land offices and the many private landowners\nwho permitted land access to acquire the USMTArray data.",
                ),
                ("country", "USA"),
                ("datum", "WGS84"),
                ("geographic_name", "CONUS South"),
                ("id", "CONUS South"),
                ("name", None),
                ("northwest_corner.latitude", 0.0),
                ("northwest_corner.longitude", 0.0),
                ("project", "USMTArray"),
                ("project_lead.email", None),
                ("project_lead.organization", None),
                ("release_license", "CC-0"),
                ("southeast_corner.latitude", 0.0),
                ("southeast_corner.longitude", 0.0),
                ("summary", "Magnetotelluric Transfer Functions"),
                ("time_period.end_date", "2020-10-07"),
                ("time_period.start_date", "2020-09-20"),
            ]
        )
        self.assertDictEqual(meta_dict, self.tf.survey_metadata.to_dict(single=True))

    def test_z(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 2, 2), self.tf.impedance.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance[0],
                    np.array(
                        [
                            [-0.1160949 - 0.2708645j, 3.143284 + 1.101737j],
                            [-2.470717 - 0.7784633j, -0.1057851 + 0.1022045j],
                        ]
                    ),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance[-1],
                    np.array(
                        [
                            [0.00483462 + 0.00983358j, 0.02643963 + 0.05098311j],
                            [-0.02203037 - 0.03744689j, -0.00295362 - 0.01293358j],
                        ]
                    ),
                ).all()
            )

    def test_sip(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 2, 2), self.tf.inverse_signal_power.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.inverse_signal_power[0],
                    np.array(
                        [
                            [0.8745101 - 2.905133e-08j, -0.4293981 + 1.663000e-01j],
                            [-0.4293981 - 1.663000e-01j, 1.39159 - 7.486698e-10j],
                        ]
                    ),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.inverse_signal_power[-1],
                    np.array(
                        [
                            [9.120293e-08 - 2.13634e-16j, 5.066908e-08 + 2.26600e-08j],
                            [5.066908e-08 - 2.26600e-08j, 1.086271e-07 + 1.02634e-16j],
                        ]
                    ),
                ).all()
            )

    def test_residual(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 3, 3), self.tf.residual_covariance.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.residual_covariance[0],
                    np.array(
                        [
                            [
                                1.28646000e-03 + 8.47032900e-22j,
                                -5.81671100e-05 + 3.34700000e-05j,
                                0.00000000e00 + 0.00000000e00j,
                            ],
                            [
                                -5.81671100e-05 - 3.34700000e-05j,
                                1.03754000e-03 + 0.00000000e00j,
                                0.00000000e00 + 0.00000000e00j,
                            ],
                            [
                                0.00000000e00 + 0.00000000e00j,
                                0.00000000e00 + 0.00000000e00j,
                                9.62300000e-05 + 0.00000000e00j,
                            ],
                        ]
                    ),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.residual_covariance[-1],
                    np.array(
                        [
                            [
                                86.38148 + 0.00000000e00j,
                                -31.70986 + 1.28100000e00j,
                                0.00000 + 0.00000000e00j,
                            ],
                            [
                                -31.70986 - 1.28100000e00j,
                                45.52852 - 2.77555800e-17j,
                                0.00000 + 0.00000000e00j,
                            ],
                            [
                                0.00000 + 0.00000000e00j,
                                0.00000 + 0.00000000e00j,
                                29820.00000 + 0.00000000e00j,
                            ],
                        ]
                    ),
                ).all()
            )

    def test_t(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((33, 1, 2), self.tf.tipper.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[0],
                    np.array([[-0.09386985 + 0.00620671j, 0.04601304 + 0.03035755j]]),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[-1],
                    np.array([[-0.03648688 + 0.08738894j, 0.1750294 + 0.1666582j]]),
                ).all()
            )


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
