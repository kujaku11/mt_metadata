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
from mt_metadata import TF_ZSS_TIPPER
from mt_metadata.transfer_functions import TF

# =============================================================================
# EMTFXML
# =============================================================================


class TestZSS(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_ZSS_TIPPER)
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
                ("northwest_corner.latitude", 44.631),
                ("northwest_corner.longitude", -110.44),
                ("project", None),
                ("project_lead.email", None),
                ("project_lead.organization", None),
                ("release_license", "CC0-1.0"),
                ("southeast_corner.latitude", 44.631),
                ("southeast_corner.longitude", -110.44),
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
                ("channels_recorded", ["hx", "hy", "hz"]),
                ("comments", "WITH FULL ERROR COVARIANCE"),
                ("data_type", "MT"),
                ("geographic_name", None),
                ("id", "YSW212abcdefghijkl"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", 11.18),
                ("location.elevation", 0.0),
                ("location.latitude", 44.631),
                ("location.longitude", -110.44),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                (
                    "provenance.creation_time",
                    "2025-02-07T20:55:36.147846+00:00",
                ),
                ("provenance.software.author", None),
                ("provenance.software.name", "EMTF"),
                ("provenance.software.version", "1"),
                ("provenance.submitter.email", None),
                ("provenance.submitter.organization", None),
                ("release_license", "CC0-1.0"),
                ("run_list", ["ysw212abcdefghijkla"]),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "1980-01-01T00:00:00+00:00"),
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.data_quality.rating.value", 0),
                ("transfer_function.id", "ysw212abcdefghijkl"),
                ("transfer_function.processed_date", "1980-01-01"),
                ("transfer_function.processing_parameters", []),
                ("transfer_function.processing_type", "Robust Single station"),
                ("transfer_function.remote_references", []),
                ("transfer_function.runs_processed", ["ysw212abcdefghijkla"]),
                ("transfer_function.sign_convention", "+"),
                ("transfer_function.software.author", None),
                ("transfer_function.software.name", "EMTF"),
                ("transfer_function.software.version", "1"),
                ("transfer_function.units", None),
            ]
        )

        del meta_dict["provenance.creation_time"]
        s_dict = self.tf.station_metadata.to_dict(single=True)
        del s_dict["provenance.creation_time"]
        self.assertDictEqual(meta_dict, s_dict)

    def test_run_metadata(self):
        meta_dict = OrderedDict(
            [
                ("channels_recorded_auxiliary", []),
                ("channels_recorded_electric", []),
                ("channels_recorded_magnetic", ["hx", "hy", "hz"]),
                ("data_logger.firmware.author", None),
                ("data_logger.firmware.name", None),
                ("data_logger.firmware.version", None),
                ("data_logger.id", None),
                ("data_logger.manufacturer", None),
                ("data_logger.timing_system.drift", 0.0),
                ("data_logger.timing_system.type", "GPS"),
                ("data_logger.timing_system.uncertainty", 0.0),
                ("data_logger.type", None),
                ("data_type", "BBMT"),
                ("id", "ysw212abcdefghijkla"),
                ("sample_rate", 5.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "1980-01-01T00:00:00+00:00"),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.tf.station_metadata.runs[0].to_dict(single=True)
        )

    def test_z(self):
        self.assertFalse(self.tf.has_impedance())

    def test_t(self):
        with self.subTest("has tipper"):
            self.assertTrue(self.tf.has_tipper())
        with self.subTest(msg="shape"):
            self.assertTupleEqual((44, 1, 2), self.tf.tipper.shape)
        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[0],
                    np.array([[-0.20389999 + 0.09208j, 0.05996000 + 0.03177j]]),
                ).all()
            )
        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[-1],
                    np.array([[-0.01205 - 0.03873j, -0.09759 - 0.03014j]]),
                ).all()
            )

    def test_sip(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual(
                (44, 2, 2), self.tf.inverse_signal_power.shape
            )
        with self.subTest("has inverse_signal_power"):
            self.assertTrue(self.tf.has_inverse_signal_power())
        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.inverse_signal_power[0],
                    np.array(
                        [
                            [136.19999695 + 0.0j, -9.60000038 + 5.32700014j],
                            [-9.60000038 - 5.32700014j, 336.1000061 + 0.0j],
                        ]
                    ),
                    atol=1e-5,
                ).all()
            )
        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.inverse_signal_power[-1],
                    np.array(
                        [
                            [
                                3.59999990e-06 + 0.00000000e00j,
                                2.10999997e-06 + 9.44800007e-08j,
                            ],
                            [
                                2.10999997e-06 - 9.44800007e-08j,
                                4.55500003e-06 + 0.00000000e00j,
                            ],
                        ]
                    ),
                    atol=1e-5,
                ).all()
            )

    def test_residual(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((44, 3, 3), self.tf.residual_covariance.shape)
        with self.subTest("has residual_covariance"):
            self.assertTrue(self.tf.has_residual_covariance())
        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.residual_covariance[0],
                    np.array(
                        [
                            [
                                0.00000000e00 + 0.0j,
                                0.00000000e00 + 0.0j,
                                0.00000000e00 + 0.0j,
                            ],
                            [
                                0.00000000e00 + 0.0j,
                                0.00000000e00 + 0.0j,
                                0.00000000e00 + 0.0j,
                            ],
                            [
                                0.00000000e00 + 0.0j,
                                0.00000000e00 + 0.0j,
                                4.62099982e-18 + 0.0j,
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
                                0.00000000 + 0.0j,
                                0.00000000 + 0.0j,
                                0.00000000 + 0.0j,
                            ],
                            [
                                0.00000000 + 0.0j,
                                0.00000000 + 0.0j,
                                0.00000000 + 0.0j,
                            ],
                            [
                                0.00000000 + 0.0j,
                                0.00000000 + 0.0j,
                                38.70000076 + 0.0j,
                            ],
                        ]
                    ),
                ).all()
            )


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
