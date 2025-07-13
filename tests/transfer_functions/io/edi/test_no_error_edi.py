# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

# =============================================================================
#
# =============================================================================
import unittest
from collections import OrderedDict

from mt_metadata import TF_EDI_NO_ERROR
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io import edi


# =============================================================================
# CGG
# =============================================================================
class TestNoErrorEDI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.edi_obj = edi.EDI(fn=TF_EDI_NO_ERROR)
        cls.maxDiff = None

    def test_header(self):
        head = OrderedDict(
            [
                ("acqby", "PSJ"),
                ("acqdate", "2020-04-28T00:00:00+00:00"),
                ("coordinate_system", "geographic"),
                ("dataid", "21PBS_FJM"),
                ("datum", "WGS 84"),
                ("declination.model", "IGRF"),
                ("declination.value", 0.0),
                ("elevation", 0.0),
                ("empty", 1e32),
                ("enddate", "2020-04-28T00:00:00+00:00"),
                ("fileby", "PSJ"),
                ("filedate", "2021-03-25"),
                ("latitude", 0.0),
                ("longitude", 0.0),
                ("progdate", "2013-07-03"),
                ("progname", "mt_metadata"),
                ("progvers", "0.1.6"),
                ("stdvers", "SEG 1.0"),
                ("units", "milliVolt per kilometer per nanoTesla"),
            ]
        )

        for key, value in head.items():
            with self.subTest(key):
                h_value = self.edi_obj.Header.get_attr_from_name(key)
                self.assertEqual(h_value, value)

    def test_info(self):
        self.assertDictEqual({"maxinfo": "500"}, self.edi_obj.Info.info_dict)

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", "ADU07/UNKN_E/0/"),
                ("azm", 0.0),
                ("chtype", "EX"),
                ("id", 1211.001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", 0.0),
                ("y2", 0.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.measurements["ex"].to_dict(single=True)
        )

    def test_measurement_ey(self):
        ch = OrderedDict(
            [
                ("acqchan", "ADU07/UNKN_E/0/"),
                ("azm", 0.0),
                ("chtype", "EY"),
                ("id", 1212.001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", 0.0),
                ("y2", 0.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.measurements["ey"].to_dict(single=True)
        )

    def test_measurement_hx(self):
        ch = OrderedDict(
            [
                ("acqchan", "ADU07/UNKN_H/0/"),
                ("azm", 0.0),
                ("chtype", "HX"),
                ("dip", 0.0),
                ("id", 1213.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.measurements["hx"].to_dict(single=True)
        )

    def test_measurement_hy(self):
        ch = OrderedDict(
            [
                ("acqchan", "ADU07/UNKN_H/0/"),
                ("azm", 0.0),
                ("chtype", "HY"),
                ("dip", 0.0),
                ("id", 1214.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.measurements["hy"].to_dict(single=True)
        )

    def test_measurement_hz(self):
        ch = OrderedDict(
            [
                ("acqchan", "ADU07/UNKN_H/0/"),
                ("azm", 0.0),
                ("chtype", "HZ"),
                ("dip", 0.0),
                ("id", 1215.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.measurements["hz"].to_dict(single=True)
        )

    def test_measurement(self):
        m_list = [
            "\n>=DEFINEMEAS\n",
            "    MAXCHAN=9\n",
            "    MAXRUN=999\n",
            "    MAXMEAS=1000\n",
            "    REFLAT=0:00:0.000000\n",
            "    REFLON=0:00:0.000000\n",
            "    REFELEV=0.0\n",
            "    REFTYPE=CART\n",
            "    UNITS=m\n",
            "\n",
            ">EMEAS ID=1211.001 CHTYPE=EX X=0.00 Y=0.00 Z=0.00 X2=0.00 Y2=0.00 Z2=0.00 AZM=0.00 ACQCHAN=ADU07/UNKN_E/0/\n",
            ">EMEAS ID=1212.001 CHTYPE=EY X=0.00 Y=0.00 Z=0.00 X2=0.00 Y2=0.00 Z2=0.00 AZM=0.00 ACQCHAN=ADU07/UNKN_E/0/\n",
            ">HMEAS ID=1213.001 CHTYPE=HX X=0.00 Y=0.00 Z=0.00 AZM=0.00 DIP=0.00 ACQCHAN=ADU07/UNKN_H/0/\n",
            ">HMEAS ID=1214.001 CHTYPE=HY X=0.00 Y=0.00 Z=0.00 AZM=0.00 DIP=0.00 ACQCHAN=ADU07/UNKN_H/0/\n",
            ">HMEAS ID=1215.001 CHTYPE=HZ X=0.00 Y=0.00 Z=0.00 AZM=0.00 DIP=0.00 ACQCHAN=ADU07/UNKN_H/0/\n",
        ]

        self.assertListEqual(m_list, self.edi_obj.Measurement.write_measurement())

        with self.subTest("reflat"):
            self.assertAlmostEqual(0, self.edi_obj.Measurement.reflat, 5)

        with self.subTest("reflon"):
            self.assertAlmostEqual(0, self.edi_obj.Measurement.reflon, 5)

        with self.subTest("refelev"):
            self.assertAlmostEqual(0, self.edi_obj.Measurement.refelev, 2)

    def test_data_section(self):
        d_list = [
            "\n>=MTSECT\n",
            "    NFREQ=47\n",
            "    SECTID=L1.S21.R1001\n",
            "    NCHAN=0\n",
            "    MAXBLOCKS=999\n",
            "    EX=1211.001\n",
            "    EY=1212.001\n",
            "    HX=1213.001\n",
            "    HY=1214.001\n",
            "    HZ=1215.001\n",
            "\n",
        ]

        self.assertListEqual(d_list, self.edi_obj.Data.write_data())

    def test_impedance(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.z.shape, (47, 2, 2))

        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.z_err.shape, (47, 2, 2))

        with self.subTest("has zero"):
            self.assertEqual(self.edi_obj.z_err[0, 0, 0], 0)

        with self.subTest("not zero"):
            self.assertNotEqual(self.edi_obj.z[1, 0, 0], 0 + 0j)

    def test_tipper(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.t.shape, (47, 1, 2))
        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.t_err.shape, (47, 1, 2))
        with self.subTest("has zero"):
            self.assertEqual(self.edi_obj.t_err[0, 0, 0], 0)

    def test_rotation_angle(self):
        with self.subTest("all zeros"):
            self.assertTrue((self.edi_obj.rotation_angle == 0).all())

        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.rotation_angle.shape, (47,))


class TestToTF(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.edi = edi.EDI(fn=TF_EDI_NO_ERROR)
        cls.tf = TF(fn=TF_EDI_NO_ERROR)
        cls.tf.read()

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
        self.assertTrue((self.tf.impedance_error.data[:, 0, 0] == 0).all())

    def test_has_tipper(self):
        self.assertTrue(self.tf.has_tipper())

    def test_has_isp(self):
        self.assertFalse(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertFalse(self.tf.has_residual_covariance())


class TestFromTF(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tf = TF(fn=TF_EDI_NO_ERROR)
        cls.tf.read()

        cls.edi = cls.tf.to_edi()
        cls.maxDiff = None

    def test_station_metadata(self):
        edi_st = self.edi.station_metadata.to_dict(single=True)
        tf_st = self.tf.station_metadata.to_dict(single=True, required=False)
        for edi_key, edi_value in edi_st.items():
            if edi_key in ["comments"]:
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
        self.assertTrue((self.tf.impedance_error.data[:, 0, 0] == 0).all())

    def test_has_tipper(self):
        self.assertTrue(self.tf.has_tipper())

    def test_has_isp(self):
        self.assertFalse(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertFalse(self.tf.has_residual_covariance())


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
