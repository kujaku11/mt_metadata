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
from mt_metadata import TF_AVG_TIPPER
from mt_metadata.transfer_functions.core import TF

# =============================================================================
# EMTFXML
# =============================================================================


class TestEMTFXML(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_AVG_TIPPER)
        self.tf.read_tf_file()
        self.maxDiff = None

    def test_survey_metadata(self):
        meta_dict = OrderedDict(
            [
                ("citation_dataset.doi", None),
                ("citation_journal.doi", None),
                ("datum", "WGS84"),
                ("geographic_name", None),
                ("id", None),
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
                ("channels_recorded", ["ex", "ey", "hx", "hy", "hz"]),
                ("data_type", "mt"),
                ("geographic_name", None),
                ("id", "22"),
                ("location.datum", "WGS84"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", 0.0),
                ("location.elevation", 1548.1),
                ("location.latitude", 38.6653467),
                ("location.longitude", -113.1690717),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                ("provenance.creation_time", "1980-01-01T00:00:00+00:00"),
                ("provenance.software.author", None),
                ("provenance.software.name", None),
                ("provenance.software.version", None),
                ("provenance.submitter.email", None),
                ("provenance.submitter.organization", None),
                ("release_license", "CC0-1.0"),
                ("run_list", ["001"]),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.id", "22"),
                ("transfer_function.processed_date", None),
                (
                    "transfer_function.processing_parameters",
                    [
                        "mtedit.auto.phase_flip=no",
                        "mtedit.d_plus.use=no",
                        "mtedit.phase_slope.smooth=minimal",
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
                ("channels_recorded_electric", ["ex", "ey"]),
                ("channels_recorded_magnetic", ["hx", "hy", "hz"]),
                ("data_logger.firmware.author", None),
                ("data_logger.firmware.name", None),
                ("data_logger.firmware.version", None),
                ("data_logger.id", "17"),
                ("data_logger.manufacturer", "Zonge International"),
                ("data_logger.timing_system.drift", 0.0),
                ("data_logger.timing_system.type", "GPS"),
                ("data_logger.timing_system.uncertainty", 0.0),
                ("data_logger.type", "ZEN"),
                ("data_type", "BBMT"),
                ("id", "001"),
                ("sample_rate", 0.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.tf.station_metadata.runs[0].to_dict(single=True)
        )

    def test_ex_metadata(self):
        meta_dict = OrderedDict(
            [
                ("channel_id", "22"),
                ("channel_number", 0),
                ("component", "ex"),
                ("data_quality.rating.value", 0),
                ("dipole_length", 100.0),
                ("filter.applied", [False]),
                ("filter.name", []),
                ("measurement_azimuth", 11.3),
                ("measurement_tilt", 0.0),
                ("negative.elevation", 0.0),
                ("negative.id", None),
                ("negative.latitude", 0.0),
                ("negative.longitude", 0.0),
                ("negative.manufacturer", None),
                ("negative.type", None),
                ("positive.elevation", 0.0),
                ("positive.id", None),
                ("positive.latitude", 0.0),
                ("positive.longitude", 0.0),
                ("positive.manufacturer", None),
                ("positive.type", None),
                ("sample_rate", 0.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 11.3),
                ("translated_tilt", 0.0),
                ("type", "electric"),
                ("units", None),
            ]
        )

        self.assertDictEqual(
            meta_dict,
            self.tf.station_metadata.runs[0].channels[0].to_dict(single=True),
        )

    def test_ey_metadata(self):
        meta_dict = OrderedDict(
            [
                ("channel_id", "22"),
                ("channel_number", 0),
                ("component", "ey"),
                ("data_quality.rating.value", 0),
                ("dipole_length", 100.0),
                ("filter.applied", [False]),
                ("filter.name", []),
                ("measurement_azimuth", 101.3),
                ("measurement_tilt", 0.0),
                ("negative.elevation", 0.0),
                ("negative.id", None),
                ("negative.latitude", 0.0),
                ("negative.longitude", 0.0),
                ("negative.manufacturer", None),
                ("negative.type", None),
                ("positive.elevation", 0.0),
                ("positive.id", None),
                ("positive.latitude", 0.0),
                ("positive.longitude", 0.0),
                ("positive.manufacturer", None),
                ("positive.type", None),
                ("sample_rate", 0.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 101.3),
                ("translated_tilt", 0.0),
                ("type", "electric"),
                ("units", None),
            ]
        )

        self.assertDictEqual(
            meta_dict,
            self.tf.station_metadata.runs[0].channels[1].to_dict(single=True),
        )

    def test_hx_metadata(self):
        meta_dict = OrderedDict(
            [
                ("channel_id", "1"),
                ("channel_number", 0),
                ("component", "hx"),
                ("data_quality.rating.value", 0),
                ("filter.applied", [False]),
                ("filter.name", []),
                ("location.elevation", 0.0),
                ("location.latitude", 0.0),
                ("location.longitude", 0.0),
                ("measurement_azimuth", 11.3),
                ("measurement_tilt", 0.0),
                ("sample_rate", 0.0),
                ("sensor.id", "2374"),
                ("sensor.manufacturer", None),
                ("sensor.type", None),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 11.3),
                ("translated_tilt", 0.0),
                ("type", "magnetic"),
                ("units", None),
            ]
        )

        self.assertDictEqual(
            meta_dict,
            self.tf.station_metadata.runs[0].channels[2].to_dict(single=True),
        )

    def test_hy_metadata(self):
        meta_dict = OrderedDict(
            [
                ("channel_id", "2"),
                ("channel_number", 0),
                ("component", "hy"),
                ("data_quality.rating.value", 0),
                ("filter.applied", [False]),
                ("filter.name", []),
                ("location.elevation", 0.0),
                ("location.latitude", 0.0),
                ("location.longitude", 0.0),
                ("measurement_azimuth", 101.3),
                ("measurement_tilt", 0.0),
                ("sample_rate", 0.0),
                ("sensor.id", "287"),
                ("sensor.manufacturer", None),
                ("sensor.type", None),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 101.3),
                ("translated_tilt", 0.0),
                ("type", "magnetic"),
                ("units", None),
            ]
        )

        self.assertDictEqual(
            meta_dict,
            self.tf.station_metadata.runs[0].channels[3].to_dict(single=True),
        )

    def test_hz_metadata(self):
        meta_dict = OrderedDict(
            [
                ("channel_id", "3"),
                ("channel_number", 0),
                ("component", "hz"),
                ("data_quality.rating.value", 0),
                ("filter.applied", [False]),
                ("filter.name", []),
                ("location.elevation", 0.0),
                ("location.latitude", 0.0),
                ("location.longitude", 0.0),
                ("measurement_azimuth", 11.3),
                ("measurement_tilt", 0.0),
                ("sample_rate", 0.0),
                ("sensor.id", "2374"),
                ("sensor.manufacturer", None),
                ("sensor.type", None),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 11.3),
                ("translated_tilt", 0.0),
                ("type", "magnetic"),
                ("units", None),
            ]
        )

        self.assertDictEqual(
            meta_dict,
            self.tf.station_metadata.runs[0].channels[4].to_dict(single=True),
        )

    def test_z(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((51, 2, 2), self.tf.impedance.shape)
        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance[0],
                    np.array(
                        [
                            [
                                -0.42514998 - 1.2095569j,
                                52.05528553 + 4.76589728j,
                            ],
                            [
                                0.21016642 + 0.49228452j,
                                -10.16752339 - 2.70034593j,
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
                                -112.92397163 + 35.82342154j,
                                -1051.1278249 + 1808.8705608j,
                            ],
                            [
                                116.01781236 + 128.3445648j,
                                51.80694503 - 42.43686378j,
                            ],
                        ]
                    ),
                ).all()
            )

    def test_z_err(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((51, 2, 2), self.tf.impedance_error.shape)
        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance_error[0],
                    np.array(
                        [[1.66174935, 67.73395417], [0.69379092, 13.50078836]]
                    ),
                ).all()
            )
        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance_error[-1],
                    np.array(
                        [[22.16312252, 362.35893807], [9.4763284, 22.00814395]]
                    ),
                ).all()
            )

    def test_t(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((51, 1, 2), self.tf.tipper.shape)
        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[0],
                    np.array(
                        [
                            [
                                22.74427485 + 18.94823397j,
                                -923.7823987 + 524.50678723j,
                            ]
                        ]
                    ),
                ).all()
            )
        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper[-1],
                    np.array(
                        [[0.30581038 - 0.60563024j, -3.71315818 - 10.6661564j]]
                    ),
                ).all()
            )

    def test_t_err(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((51, 1, 2), self.tf.tipper_error.shape)
        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper_error[0],
                    np.array([[29.603, 1062.3]]),
                ).all()
            )
        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.tipper_error[-1],
                    np.array([[0.67846, 11.294]]),
                ).all()
            )

    def test_sip(self):
        self.assertFalse(self.tf.has_inverse_signal_power())

    def test_residual(self):
        self.assertFalse(self.tf.has_residual_covariance())


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
