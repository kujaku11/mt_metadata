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
from mt_metadata import TF_AVG_NEWER
from mt_metadata.transfer_functions.core import TF

# =============================================================================
# EMTFXML
# =============================================================================


class TestEMTFXML(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_AVG_NEWER)
        self.tf.read_tf_file(z_positive="up")
        self.maxDiff = None

    def test_survey_metadata(self):
        meta_dict = OrderedDict(
            [
                ("citation_dataset.doi", None),
                ("citation_journal.doi", None),
                ("country", None),
                ("datum", "WGS84"),
                ("geographic_name", None),
                ("id", None),
                ("name", None),
                ("northwest_corner.latitude", 0.0),
                ("northwest_corner.longitude", 0.0),
                ("project", None),
                ("project_lead.email", None),
                ("project_lead.organization", None),
                ("release_license", "CC-0"),
                ("southeast_corner.latitude", 0.0),
                ("southeast_corner.longitude", 0.0),
                ("summary", None),
                ("time_period.end_date", "1980-01-01"),
                ("time_period.start_date", "1980-01-01"),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.tf.survey_metadata.to_dict(single=True)
        )

    def test_station_metadata(self):
        meta_dict = OrderedDict(
            [
                ("channels_recorded", []),
                ("data_type", "mt"),
                ("geographic_name", None),
                ("id", "2813"),
                ("location.datum", "WGS84"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", 0.0),
                ("location.elevation", 0.0),
                ("location.latitude", 44.1479163),
                ("location.longitude", -111.0497517),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                ("provenance.creation_time", "1980-01-01T00:00:00+00:00"),
                ("provenance.software.author", "none"),
                ("provenance.software.name", None),
                ("provenance.software.version", None),
                ("provenance.submitter.email", None),
                ("provenance.submitter.organization", None),
                ("run_list", ["001"]),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2017-06-30T21:30:19+00:00"),
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.id", "2813"),
                ("transfer_function.processed_date", None),
                (
                    "transfer_function.processing_parameters",
                    [
                        "mtedit.auto.phase_flip=no",
                        "mtedit.d_plus.use=no",
                        "mtedit.phase_slope.smooth=robust",
                        "mtedit.phase_slope.to_z_mag=no",
                    ],
                ),
                ("transfer_function.remote_references", []),
                ("transfer_function.runs_processed", ["001"]),
                ("transfer_function.sign_convention", None),
                ("transfer_function.units", None),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.tf.station_metadata.to_dict(single=True)
        )

    def test_run_metadata(self):
        meta_dict = OrderedDict(
            [
                ("channels_recorded_auxiliary", []),
                ("channels_recorded_electric", []),
                ("channels_recorded_magnetic", []),
                ("data_logger.firmware.author", None),
                ("data_logger.firmware.name", None),
                ("data_logger.firmware.version", None),
                ("data_logger.id", None),
                ("data_logger.manufacturer", "Zonge International"),
                ("data_logger.timing_system.drift", 0.0),
                ("data_logger.timing_system.type", "GPS"),
                ("data_logger.timing_system.uncertainty", 0.0),
                ("data_logger.type", "ZEN"),
                ("data_type", "BBMT"),
                ("id", "001"),
                ("sample_rate", 0.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2017-06-30T21:30:19+00:00"),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.tf.station_metadata.runs[0].to_dict(single=True)
        )

    def test_z(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((37, 2, 2), self.tf.impedance.shape)
        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance[0],
                    np.array(
                        [
                            [
                                -0.0477167 - 0.04384979j,
                                0.06316246 + 0.10325301j,
                            ],
                            [
                                -0.15458447 - 0.13410915j,
                                0.05249684 + 0.06373682j,
                            ],
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
                            [
                                -134.88329222 + 96.31326534j,
                                185.76082467 + 426.12021604j,
                            ],
                            [
                                -56.74596843 - 551.65911573j,
                                -30.66729089 - 24.60693054j,
                            ],
                        ]
                    ),
                ).all()
            )

    def test_z_err(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((37, 2, 2), self.tf.impedance_error.shape)
        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance_error[0],
                    np.array(
                        [[0.0660245, 0.07098981], [0.09707527, 0.05116877]]
                    ),
                ).all()
            )
        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance_error[-1],
                    np.array(
                        [[23.43822519, 29.39997279], [42.95754183, 8.61436196]]
                    ),
                ).all()
            )

    def test_t(self):
        self.assertFalse(self.tf.has_tipper())

    def test_sip(self):
        self.assertFalse(self.tf.has_inverse_signal_power())

    def test_residual(self):
        self.assertFalse(self.tf.has_residual_covariance())


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
