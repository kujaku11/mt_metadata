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
from mt_metadata import TF_ZMM
from mt_metadata.transfer_functions import TF
from mt_metadata.transfer_functions.io.tools import get_nm_elev

# =============================================================================
# EMTFXML
# =============================================================================


class TestZMM(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_ZMM)
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
                ("northwest_corner.latitude", 34.727),
                ("northwest_corner.longitude", -115.735),
                ("project", None),
                ("project_lead.email", None),
                ("project_lead.organization", None),
                ("release_license", "CC0-1.0"),
                ("southeast_corner.latitude", 34.727),
                ("southeast_corner.longitude", -115.735),
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
                ("channels_recorded", ["ex", "ey", "hx", "hy", "hz"]),
                ("comments", "WITH FULL ERROR COVARINCE"),
                ("data_type", "MT"),
                ("geographic_name", None),
                ("id", "300"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", 13.1),
                ("location.elevation", get_nm_elev(34.727, -115.735)),
                ("location.latitude", 34.727),
                ("location.longitude", -115.735),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                ("provenance.archive.name", None),
                ("provenance.creation_time", "1980-01-01T00:00:00+00:00"),
                ("provenance.creator.name", None),
                ("provenance.software.author", None),
                ("provenance.software.name", "EMTF"),
                ("provenance.software.version", "1"),
                ("provenance.submitter.email", None),
                ("provenance.submitter.name", None),
                ("provenance.submitter.organization", None),
                ("release_license", "CC0-1.0"),
                ("run_list", ["300a"]),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "1980-01-01T00:00:00+00:00"),
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.data_quality.rating.value", 0),
                ("transfer_function.id", "300"),
                ("transfer_function.processed_by.name", None),
                ("transfer_function.processed_date", "1980-01-01"),
                ("transfer_function.processing_parameters", []),
                ("transfer_function.processing_type", ""),
                ("transfer_function.remote_references", []),
                ("transfer_function.runs_processed", ["300a"]),
                ("transfer_function.sign_convention", None),
                ("transfer_function.software.author", None),
                ("transfer_function.software.name", "EMTF"),
                ("transfer_function.software.version", "1"),
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
                ("id", "300a"),
                ("sample_rate", 8.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "1980-01-01T00:00:00+00:00"),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.tf.station_metadata.runs[0].to_dict(single=True)
        )

    def test_z(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((38, 2, 2), self.tf.impedance.shape)

        with self.subTest("has impedance"):
            self.assertTrue(self.tf.has_impedance())

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance[0],
                    np.array(
                        [
                            [
                                -5.99100018 - 5.95499992j,
                                17.27000046 + 12.72000027j,
                            ],
                            [
                                -51.59000015 - 23.03000069j,
                                -0.35179999 + 7.66300011j,
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
                                1.69399995e-04 + 0.01282j,
                                5.67400008e-02 + 0.06538j,
                            ],
                            [
                                3.78899992e-01 - 0.85600001j,
                                2.71499991e-01 - 0.4786j,
                            ],
                        ]
                    ),
                ).all()
            )

    def test_z_err(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((38, 2, 2), self.tf.impedance_error.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance_error[0],
                    np.array(
                        [[0.53822149, 1.44624196], [1.92694986, 5.17786036]]
                    ),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance_error[-1],
                    np.array(
                        [[0.00273188, 0.0020596], [1.12854018, 0.85081953]]
                    ),
                ).all()
            )

    def test_t(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((38, 1, 2), self.tf.tipper.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[0],
                    np.array(
                        [[0.25870001 - 0.18619999j, -0.05068000 + 0.0659j]]
                    ),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[-1],
                    np.array([[0.07606 + 0.1051j, 0.03506 - 0.04627j]]),
                ).all()
            )

    def test_sip(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual(
                (38, 2, 2), self.tf.inverse_signal_power.shape
            )

        with self.subTest("has inverse_signal_power"):
            self.assertTrue(self.tf.has_inverse_signal_power())

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.inverse_signal_power[0],
                    np.array(
                        [
                            [
                                18.05999947 - 4.46999991e-07j,
                                -27.14999962 + 6.88899994e00j,
                            ],
                            [
                                -27.14999962 - 6.88899994e00j,
                                130.3999939 + 2.38400006e-07j,
                            ],
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
                                1.92300007e-07 - 4.44100010e-16j,
                                3.36799992e-08 - 1.40400003e-08j,
                            ],
                            [
                                3.36799992e-08 - 1.40400003e-08j,
                                1.09299997e-07 + 0.00000000e00j,
                            ],
                        ]
                    ),
                    atol=1e-5,
                ).all()
            )

    def test_residual(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((38, 3, 3), self.tf.residual_covariance.shape)

        with self.subTest("has residual_covariance"):
            self.assertTrue(self.tf.has_residual_covariance())

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.residual_covariance[0],
                    np.array(
                        [
                            [
                                1.60399992e-02 + 0.0j,
                                2.29300000e-02 + 0.005487j,
                                -6.59599973e-05 - 0.0002254j,
                            ],
                            [
                                2.29300000e-02 - 0.005487j,
                                2.05599993e-01 + 0.0j,
                                1.45800004e-04 - 0.0009467j,
                            ],
                            [
                                -6.59599973e-05 + 0.0002254j,
                                1.45800004e-04 + 0.0009467j,
                                8.14200030e-05 + 0.0j,
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
                                3.88100014e01 + 0.00000000e00j,
                                -1.31300000e03 - 2.84700000e03j,
                                1.56499996e01 - 1.21499996e01j,
                            ],
                            [
                                -1.31300000e03 + 2.84700000e03j,
                                6.62300000e06 + 0.00000000e00j,
                                8.53800000e03 + 1.40900000e04j,
                            ],
                            [
                                1.56499996e01 + 1.21499996e01j,
                                8.53800000e03 - 1.40900000e04j,
                                1.17700000e03 + 0.00000000e00j,
                            ],
                        ]
                    ),
                ).all()
            )


class TestTFToEMTFXML(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_ZMM)
        self.tf.read()
        self.maxDiff = None

        self.zmm = self.tf.to_zmm()

    def test_survey_metadata(self):
        meta_dict = OrderedDict(
            [
                ("citation_dataset.doi", None),
                ("citation_journal.doi", None),
                ("datum", "WGS84"),
                ("geographic_name", None),
                ("id", None),
                ("name", None),
                ("northwest_corner.latitude", 34.727),
                ("northwest_corner.longitude", -115.735),
                ("project", None),
                ("project_lead.email", None),
                ("project_lead.organization", None),
                ("release_license", "CC0-1.0"),
                ("southeast_corner.latitude", 34.727),
                ("southeast_corner.longitude", -115.735),
                ("summary", None),
                ("time_period.end_date", "1980-01-01"),
                ("time_period.start_date", "1980-01-01"),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.zmm.survey_metadata.to_dict(single=True)
        )

    def test_station_metadata(self):
        meta_dict = OrderedDict(
            [
                ("channels_recorded", ["ex", "ey", "hx", "hy", "hz"]),
                ("comments", "WITH FULL ERROR COVARINCE"),
                ("data_type", "MT"),
                ("geographic_name", None),
                ("id", "300"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", 13.1),
                ("location.elevation", get_nm_elev(34.727, -115.735)),
                ("location.latitude", 34.727),
                ("location.longitude", -115.735),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                ("provenance.archive.name", None),
                ("provenance.creation_time", "1980-01-01T00:00:00+00:00"),
                ("provenance.creator.name", None),
                ("provenance.software.author", None),
                ("provenance.software.name", "EMTF"),
                ("provenance.software.version", "1"),
                ("provenance.submitter.email", None),
                ("provenance.submitter.name", None),
                ("provenance.submitter.organization", None),
                ("release_license", "CC0-1.0"),
                ("run_list", ["300a"]),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "1980-01-01T00:00:00+00:00"),
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.data_quality.rating.value", 0),
                ("transfer_function.id", "300"),
                ("transfer_function.processed_by.name", None),
                ("transfer_function.processed_date", "1980-01-01"),
                ("transfer_function.processing_parameters", []),
                ("transfer_function.processing_type", ""),
                ("transfer_function.remote_references", []),
                ("transfer_function.runs_processed", ["300a"]),
                ("transfer_function.sign_convention", None),
                ("transfer_function.software.author", None),
                ("transfer_function.software.name", "EMTF"),
                ("transfer_function.software.version", "1"),
                ("transfer_function.units", None),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.zmm.station_metadata.to_dict(single=True)
        )

    def test_run_metadata(self):
        meta_dict = OrderedDict(
            [
                ("channels_recorded_auxiliary", []),
                ("channels_recorded_electric", ["ex", "ey"]),
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
                ("id", "300a"),
                ("sample_rate", 8.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "1980-01-01T00:00:00+00:00"),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.zmm.station_metadata.runs[0].to_dict(single=True)
        )

    def test_transfer_function(self):
        self.assertTrue(
            (
                np.nan_to_num(self.tf.dataset.transfer_function.data)
                == np.nan_to_num(self.zmm.dataset.transfer_function.data)
            ).all()
        )


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
