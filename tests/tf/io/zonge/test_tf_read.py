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
from mt_metadata import TF_AVG
from mt_metadata.transfer_functions import TF

# =============================================================================
# EMTFXML
# =============================================================================


class TestAVG(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_AVG)
        self.tf.read()
        self.maxDiff = None

    def test_survey_metadata(self):
        meta_dict = OrderedDict(
            [
                ("citation_dataset.doi", None),
                ("citation_journal.doi", None),
                ("datum", "WGS84"),
                ("geographic_name", None),
                ("id", "0"),
                ("name", None),
                ("northwest_corner.latitude", 0.0),
                ("northwest_corner.longitude", 0.0),
                ("project", None),
                ("project_lead.email", None),
                ("project_lead.organization", None),
                ("release_license", "CC0-1.0"),
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
                ("channels_recorded", ["ex", "ey", "hx", "hy"]),
                ("data_type", "nsamt"),
                ("geographic_name", None),
                ("id", "24"),
                ("location.datum", "WGS84"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", 0.0),
                ("location.elevation", 1414.37487793),
                ("location.latitude", 32.83331167),
                ("location.longitude", -107.08305667),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                ("provenance.archive.name", None),
                ("provenance.creation_time", "1980-01-01T00:00:00+00:00"),
                ("provenance.creator.name", None),
                ("provenance.software.author", None),
                ("provenance.software.name", None),
                ("provenance.software.version", None),
                ("provenance.submitter.name", None),
                ("release_license", "CC0-1.0"),
                ("run_list", ["001"]),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "1980-01-01T00:00:00+00:00"),
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.data_quality.rating.value", 0),
                ("transfer_function.id", "24"),
                ("transfer_function.processed_by.name", None),
                ("transfer_function.processed_date", "1980-01-01"),
                (
                    "transfer_function.processing_parameters",
                    [
                        "mtedit.auto.phase_flip=yes",
                        "mtedit.d_plus.use=no",
                        "mtedit.phase_slope.smooth=robust",
                        "mtedit.phase_slope.to_z_mag=no",
                    ],
                ),
                ("transfer_function.processing_type", None),
                ("transfer_function.remote_references", []),
                ("transfer_function.runs_processed", ["001"]),
                ("transfer_function.sign_convention", None),
                ("transfer_function.software.author", "Zonge International"),
                ("transfer_function.software.last_updated", "2021/01/27"),
                ("transfer_function.software.name", "MTEdit"),
                ("transfer_function.software.version", "3.10m"),
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
                ("channels_recorded_electric", ["ex", "ey"]),
                ("channels_recorded_magnetic", ["hx", "hy"]),
                ("data_logger.firmware.author", None),
                ("data_logger.firmware.name", None),
                ("data_logger.firmware.version", None),
                ("data_logger.id", None),
                ("data_logger.manufacturer", "Zonge International"),
                ("data_logger.timing_system.drift", 0.0),
                ("data_logger.timing_system.type", "GPS"),
                ("data_logger.timing_system.uncertainty", 0.0),
                ("data_logger.type", None),
                ("data_type", "BBMT"),
                ("id", "001"),
                ("sample_rate", 0.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "1980-01-01T00:00:00+00:00"),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.tf.station_metadata.runs[0].to_dict(single=True)
        )

    def test_z(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((28, 2, 2), self.tf.impedance.shape)
        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance[0],
                    np.array(
                        [
                            [
                                -0.85198341 - 1.1020768j,
                                -1.76236149 - 1.89288924j,
                            ],
                            [
                                -0.17290554 - 0.45221147j,
                                -0.16184071 - 0.1545914j,
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
                                -1.90536913 - 22.95806911j,
                                147.51100994 + 280.66686097j,
                            ],
                            [
                                -164.60236806 - 270.77480464j,
                                9.34354731 + 12.52851806j,
                            ],
                        ]
                    ),
                ).all()
            )

    def test_z_err(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((28, 2, 2), self.tf.impedance_error.shape)
        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance_error[0],
                    np.array(
                        [[1.38180502, 2.05773344], [0.21920379, 0.16689004]]
                    ),
                ).all()
            )
        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance_error[-1],
                    np.array(
                        [[16.14211287, 31.70665545], [62.57734798, 5.69963839]]
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
