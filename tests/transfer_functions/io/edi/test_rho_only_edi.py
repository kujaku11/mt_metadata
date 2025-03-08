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
from mt_metadata.transfer_functions.io import edi
from mt_metadata.transfer_functions import TF
from mt_metadata import TF_EDI_RHO_ONLY

# =============================================================================
# Metronix
# =============================================================================
class TestMetronixEDI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_RHO_ONLY)

    def test_header(self):
        head = OrderedDict(
            [
                ("acqby", "UofAdel,Scripps,GA,GSSA,AuScope"),
                ("acqdate", "2020-10-11T00:00:00+00:00"),
                ("coordinate_system", "geographic"),
                ("dataid", "s08"),
                ("datum", "WGS84"),
                ("elevation", 0),
                ("empty", 1e32),
                ("fileby", "DataManager"),
                ("latitude", -34.646),
                ("loc", "Spencer Gulf"),
                ("longitude", 137.006),
                ("prospect", "Spencer Gulf"),
                ("stdvers", "SEG 1.0"),
            ]
        )

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

    def test_info(self):
        info_list = sorted(
            [
                "SURVEY ID=Spencer Gulf",
                "EASTING=683849",
                "NORTHING=6.16438E+06",
            ]
        )

        self.assertListEqual(info_list, self.edi_obj.Info.info_list)

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "EX"),
                ("id", 103.001),
                ("x", -5.0),
                ("x2", 5.0),
                ("y", 0.0),
                ("y2", 0.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_ex.to_dict(single=True)
        )

    def test_measurement_ey(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 90.0),
                ("chtype", "EY"),
                ("id", 104.001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", -5.0),
                ("y2", 5.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_ey.to_dict(single=True)
        )

    def test_measurement_hx(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "HX"),
                ("dip", 0.0),
                ("id", 101.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hx.to_dict(single=True)
        )

    def test_measurement_hy(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 90.0),
                ("chtype", "HY"),
                ("dip", 0.0),
                ("id", 102.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hy.to_dict(single=True)
        )

    def test_measurement(self):
        m_list = [
            "MAXCHAN=4",
            "MAXRUN=999",
            "MAXMEAS=9999",
            "UNITS=M",
            "REFTYPE=CART",
            "REFLOC=s08",
            "REFLAT=-34.64600",
            "REFLONG=137.00600",
            "REFELEV=0",
        ]

        self.assertListEqual(
            m_list, self.edi_obj.Measurement.measurement_list[0 : len(m_list)]
        )

    def test_data_section(self):
        d_list = OrderedDict(
            [
                ("ex", "103.001"),
                ("ey", "104.001"),
                ("hx", "101.001"),
                ("hy", "102.001"),
                ("hz", "0"),
                ("maxblocks", 999),
                ("nchan", 0),
                ("nfreq", 28),
                ("rrhx", "0"),
                ("rrhy", "0"),
                ("sectid", "s08"),
            ]
        )

        self.assertDictEqual(d_list, self.edi_obj.Data.to_dict(single=True))

        for ch in ["hx", "hy", "ex", "ey"]:
            with self.subTest(ch):
                self.assertEqual(d_list[ch], getattr(self.edi_obj.Data, ch))

    def test_z(self):
        with self.subTest("zxx"):
            self.assertTrue((self.edi_obj.z[:, 0, 0] == 0).all())

        with self.subTest("zyy"):
            self.assertTrue((self.edi_obj.z[:, 1, 1] == 0).all())

        with self.subTest("zxy"):
            self.assertTrue((self.edi_obj.z[:, 0, 1] != 0).all())

        with self.subTest("zyx"):
            self.assertTrue((self.edi_obj.z[:, 1, 0] != 0).all())

    def test_rhoxy(self):
        rho_xy = np.array(
            [
                0.2818635,
                0.3512951,
                0.3714305,
                0.4108465,
                0.5248638,
                0.7726143,
                1.108641,
                1.672007,
                2.658779,
                3.556539,
                4.978607,
                6.450729,
                8.247861,
                10.09688,
                42.33246,
                113.28,
                62.97522,
                31.13647,
                38.18653,
                34.51625,
                39.07644,
                41.12259,
                48.43526,
                58.42656,
                54.0161,
                72.11851,
                72.32678,
                109.5934,
            ]
        )

        rxy = (0.2 / self.edi_obj.frequency) * np.abs(
            self.edi_obj.z[:, 0, 1]
        ) ** 2
        self.assertTrue(np.isclose(rho_xy, rxy).all())

    def test_phsxy(self):
        phase_xy = np.array(
            [
                35.75853,
                42.20026,
                36.66419,
                28.80162,
                21.99871,
                15.28629,
                11.75614,
                10.3068,
                9.962963,
                11.06905,
                12.87484,
                10.27247,
                14.81129,
                17.90185,
                12.38906,
                28.05279,
                -3.029796,
                26.9273,
                30.46892,
                35.27853,
                36.07981,
                36.34399,
                35.09986,
                34.32266,
                35.62811,
                37.02072,
                34.78629,
                33.30714,
            ]
        )

        pxy = np.rad2deg(
            np.arctan2(
                self.edi_obj.z[:, 0, 1].imag, self.edi_obj.z[:, 0, 1].real
            )
        )

        self.assertTrue(np.isclose(phase_xy, pxy).all())

    def test_rhoyx(self):
        rho_yx = np.array(
            [
                2.581770e-01,
                3.444989e-01,
                3.612809e-01,
                4.231358e-01,
                5.520689e-01,
                8.359045e-01,
                1.257848e00,
                2.410778e00,
                3.774356e00,
                5.379387e00,
                1.055388e01,
                1.551731e02,
                1.879535e01,
                4.052773e01,
                6.593614e03,
                6.227474e04,
                2.134522e04,
                4.830593e01,
                4.689244e01,
                4.055480e01,
                3.560237e01,
                3.621749e01,
                4.141123e01,
                4.527979e01,
                4.039037e01,
                2.454437e01,
                2.248866e01,
                1.399194e01,
            ]
        )

        ryx = (0.2 / self.edi_obj.frequency) * np.abs(
            self.edi_obj.z[:, 1, 0]
        ) ** 2
        self.assertTrue(np.isclose(rho_yx, ryx).all())

    def test_phsyx(self):
        phase_yx = np.array(
            [
                36.69456,
                42.27999,
                35.73111,
                27.35834,
                20.00085,
                13.55288,
                10.96114,
                15.85582,
                19.43036,
                20.81004,
                18.32144,
                57.72337,
                51.8989,
                22.68562,
                -61.66165,
                -21.01045,
                -36.26306,
                35.76523,
                42.78572,
                47.3067,
                46.58979,
                45.80391,
                47.74424,
                50.75497,
                54.45707,
                53.5037,
                55.26363,
                -85.40018,
            ]
        )

        pyx = np.rad2deg(
            np.arctan2(
                self.edi_obj.z[:, 1, 0].imag, self.edi_obj.z[:, 1, 0].real
            )
        )

        self.assertTrue(np.isclose(phase_yx % -180, pyx % -180).all())


class TestToTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi = edi.EDI(fn=TF_EDI_RHO_ONLY)
        self.tf = TF(fn=TF_EDI_RHO_ONLY)
        self.tf.read()

    def test_station_metadata(self):
        edi_st = self.edi.station_metadata.to_dict(single=True)
        tf_st = self.tf.station_metadata.to_dict(single=True)
        for edi_key, edi_value in edi_st.items():
            with self.subTest(edi_key):
                self.assertEqual(edi_value, tf_st[edi_key])

    def test_survey_metadata(self):
        edi_st = self.edi.survey_metadata.to_dict(single=True)
        tf_st = self.tf.survey_metadata.to_dict(single=True)
        for edi_key, edi_value in edi_st.items():
            with self.subTest(edi_key):
                self.assertEqual(edi_value, tf_st[edi_key])

    def test_has_impedance(self):
        self.assertTrue(self.tf.has_impedance())

    def test_impedance_error(self):
        self.assertTrue((self.tf.impedance_error[:, 0, 1] != 0).all())
        self.assertTrue((self.tf.impedance_error[:, 1, 0] != 0).all())

    def test_has_tipper(self):
        self.assertFalse(self.tf.has_tipper())

    def test_has_isp(self):
        self.assertFalse(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertFalse(self.tf.has_residual_covariance())


class TestFromTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_EDI_RHO_ONLY)
        self.tf.read()

        self.edi = self.tf.to_edi()
        self.maxDiff = None

    def test_station_metadata(self):
        edi_st = self.edi.station_metadata.to_dict(single=True)
        tf_st = self.tf.station_metadata.to_dict(single=True, required=False)
        for edi_key, edi_value in edi_st.items():
            if edi_key in [
                "comments",
                "transfer_function.remote_references",
            ]:
                with self.subTest(edi_key):
                    self.assertNotEqual(edi_value, tf_st[edi_key])
            else:
                with self.subTest(edi_key):
                    self.assertEqual(edi_value, tf_st[edi_key])

    def test_survey_metadata(self):
        edi_st = self.edi.survey_metadata.to_dict(single=True)
        tf_st = self.tf.survey_metadata.to_dict(single=True)
        for edi_key, edi_value in edi_st.items():
            with self.subTest(edi_key):
                self.assertEqual(edi_value, tf_st[edi_key])

    def test_has_impedance(self):
        self.assertTrue(self.tf.has_impedance())

    def test_impedance_error(self):
        self.assertTrue((self.tf.impedance_error[:, 0, 1] != 0).all())
        self.assertTrue((self.tf.impedance_error[:, 1, 0] != 0).all())

    def test_has_tipper(self):
        self.assertFalse(self.tf.has_tipper())

    def test_has_isp(self):
        self.assertFalse(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertFalse(self.tf.has_residual_covariance())


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
