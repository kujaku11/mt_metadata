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
from mt_metadata import TF_JFILE
from mt_metadata.transfer_functions import TF

# =============================================================================
# EMTFXML
# =============================================================================


class TestEMTFXML(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_JFILE)
        self.tf.read()
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
                ("channels_recorded", ["ex", "ey", "hx", "hy"]),
                ("data_type", "MT"),
                ("geographic_name", None),
                ("id", "BP05"),
                ("location.declination.model", "WMM"),
                ("location.declination.value", 0.0),
                ("location.elevation", 0.0),
                ("location.latitude", 0.0),
                ("location.longitude", 0.0),
                ("orientation.method", None),
                ("orientation.reference_frame", "geographic"),
                ("provenance.creation_time", "1980-01-01T00:00:00+00:00"),
                ("provenance.software.author", None),
                ("provenance.software.name", "BIRRP"),
                ("provenance.software.version", "5"),
                ("provenance.submitter.email", None),
                ("provenance.submitter.organization", None),
                ("release_license", "CC0-1.0"),
                ("run_list", ["001"]),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "1980-01-01T00:00:00+00:00"),
                ("transfer_function.coordinate_system", "geopgraphic"),
                ("transfer_function.id", "BP05"),
                ("transfer_function.processed_date", "2023-04-21"),
                (
                    "transfer_function.processing_parameters",
                    [
                        "ainlin = -999.0",
                        "ainuin = 0.999",
                        "c2threshe = 0.7",
                        "c2threshe1 = 0.0",
                        "deltat = 0.1",
                        "imode = 2",
                        "inputs = 2",
                        "jmode = 0",
                        "nar = 3",
                        "ncomp = 0",
                        "nf1 = 4",
                        "nfft = 5164.0",
                        "nfinc = 2",
                        "nfsect = 2",
                        "npcs = 1",
                        "nsctinc = 2.0",
                        "nsctmax = 7.0",
                        "nz = 0",
                        "outputs = 2",
                        "references = 2",
                        "tbw = 2.0",
                        "uin = 0.0",
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
                ("channels_recorded_magnetic", ["hx", "hy"]),
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
                ("id", "001"),
                ("sample_rate", 10.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "1980-01-01T00:00:00+00:00"),
            ]
        )

        self.assertDictEqual(
            meta_dict, self.tf.station_metadata.runs[0].to_dict(single=True)
        )

    def test_z(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((12, 2, 2), self.tf.impedance.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance[0],
                    np.array(
                        [
                            [8.260304 + 9.270211j, 24.263760 - 26.85942j],
                            [-24.241310 + 38.11477j, -2.271694 - 8.677796j],
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
                            [112.484200 + 217.4326j, -152.321200 - 887.0555j],
                            [-15.030780 + 1970.297j, -4.158936 + 241.5985j],
                        ]
                    ),
                ).all()
            )

    def test_z_err(self):
        with self.subTest(msg="shape"):
            self.assertTupleEqual((12, 2, 2), self.tf.impedance_error.shape)

        with self.subTest(msg="first element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance_error[0],
                    np.array([[0.9625573, 2.303654], [0.8457434, 1.930154]]),
                ).all()
            )

        with self.subTest(msg="last element"):
            self.assertTrue(
                np.isclose(
                    self.tf.impedance_error[-1],
                    np.array([[88.76002, 115.9577], [75.17097, 121.1623]]),
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
