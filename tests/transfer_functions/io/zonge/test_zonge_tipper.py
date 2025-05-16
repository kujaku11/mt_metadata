# -*- coding: utf-8 -*-
"""
Test newer versions of AVG files with tipper

Created on Wed Dec  8 11:29:57 2021

:author: Jared Peacock

:license: MIT

"""
# =============================================================================
#
# =============================================================================
import unittest
from collections import OrderedDict

import numpy as np

from mt_metadata import TF_AVG_TIPPER
from mt_metadata.transfer_functions.io.zonge import ZongeMTAvg
from mt_metadata.transfer_functions.io.zonge.metadata import Header


# =============================================================================


class TestAVGHeader(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.header = Header()
        with open(TF_AVG_TIPPER, "r") as fid:
            self.lines = fid.readlines()

        self.header.read_header(self.lines)
        self.maxDiff = None

    def test_survey(self):
        s = OrderedDict(
            [
                ("array", "tensor"),
                ("datum", "wgs84"),
                ("proj", "utm"),
                ("type", "mt"),
                ("u_t_m_zone", "12"),
            ]
        )
        self.assertDictEqual(s, self.header.survey.to_dict(single=True))

    def test_tx(self):
        tx = OrderedDict([("type", "natural")])
        self.assertDictEqual(tx, self.header.tx.to_dict(single=True))

    def test_mt_edit(self):
        mt_edit = OrderedDict(
            [
                ("auto.phase_flip", "no"),
                ("d_plus.use", "no"),
                ("phase_slope.smooth", "minimal"),
                ("phase_slope.to_z_mag", "no"),
                ("version", "3.11n applied 2022/08/02"),
            ]
        )

        self.assertDictEqual(mt_edit, self.header.m_t_edit.to_dict(single=True))

    def test_line(self):
        line = OrderedDict([("name", '"0"'), ("number", 0)])
        self.assertDictEqual(line, self.header.line.to_dict(single=True))

    def test_rx(self):
        rx = OrderedDict(
            [
                ("a_space", "100 m"),
                ("gdp_stn", "22"),
                ("h_p_r", [11.0, 0.0, 180.0]),
                ("length", 0.0),
                ("s_space", "100"),
            ]
        )

        self.assertDictEqual(rx, self.header.rx.to_dict(single=True))

    def test_gdp(self):
        gdp = OrderedDict(
            [
                ("date", "05/16/2022"),
                ("prog_ver", "4457:zenacqv5.22"),
                ("time", "23:46:18.000"),
                ("type", "zen"),
            ]
        )

        self.assertDictEqual(gdp, self.header.g_d_p.to_dict(single=True))

    def test_unit(self):
        unit = OrderedDict([("b", "nt"), ("e", "uv/m"), ("length", "m")])
        self.assertDictEqual(unit, self.header.unit.to_dict(single=True))

    def test_stn(self):
        stn = OrderedDict([("name", "22")])
        self.assertDictEqual(stn, self.header.stn.to_dict(single=True))

    def test_gps(self):
        gps = OrderedDict(
            [
                ("datum", "wgs84"),
                ("lat", 38.6653467),
                ("lon", -113.1690717),
                ("u_t_m_zone", "12"),
            ]
        )

        self.assertDictEqual(gps, self.header.g_p_s.to_dict(single=True))

    def test_zxx(self):
        zxx_rx = OrderedDict(
            [
                ("center", "311288:4281879:1548.1 m"),
                ("gdp_stn", None),
                ("h_p_r", [0.0, 0.0, 180.0]),
                ("length", 100.0),
                (
                    "u_t_m1",
                    ["311278.21:4281829.97:1548.1", "311288:4281879:1548.1"],
                ),
                ("x_y_z1", ["311278.21:4281829.97:0", "311288:4281879:0"]),
                ("x_y_z2", ["311297.79:4281928.03:0", "311288:4281879:0"]),
            ]
        )
        with self.subTest("zxx_rx"):
            self.assertDictEqual(
                zxx_rx,
                self.header._comp_dict["zxx"]["rx"].to_dict(single=True),
            )

        zxx_ch = OrderedDict(
            [
                ("a_d_card_s_n", ["7a07b42b", "5ee2ee6b"]),
                ("azimuth", ["11.3", "11.3"]),
                ("c_res", ["0", "0"]),
                ("cmp", ["ex", "hx"]),
                ("gdp_box", ["17", "17"]),
                ("incl", ["0", "0"]),
                ("number", ["22", "2374"]),
                ("stn", ["22", "22"]),
            ]
        )

        with self.subTest("zxx_ch"):
            self.assertDictEqual(
                zxx_ch,
                self.header._comp_dict["zxx"]["ch"].to_dict(single=True),
            )

    def test_zxy(self):
        zxy_rx = OrderedDict(
            [
                ("center", "311288:4281879:1548.1 m"),
                ("gdp_stn", None),
                ("h_p_r", [0.0, 0.0, 180.0]),
                ("length", 100.0),
                (
                    "u_t_m1",
                    ["311278.21:4281829.97:1548.1", "311288:4281879:1548.1"],
                ),
                ("x_y_z1", ["311278.21:4281829.97:0", "311288:4281879:0"]),
                ("x_y_z2", ["311297.79:4281928.03:0", "311288:4281879:0"]),
            ]
        )
        with self.subTest("zxy_rx"):
            self.assertDictEqual(
                zxy_rx,
                self.header._comp_dict["zxy"]["rx"].to_dict(single=True),
            )

        zxy_ch = OrderedDict(
            [
                ("a_d_card_s_n", ["7a07b42b", "2ee08e36"]),
                ("azimuth", ["11.3", "101.3"]),
                ("c_res", ["0", "0"]),
                ("cmp", ["ex", "hy"]),
                ("gdp_box", ["17", "17"]),
                ("incl", ["0", "0"]),
                ("number", ["22", "287"]),
                ("stn", ["22", "22"]),
            ]
        )

        with self.subTest("zxy_ch"):
            self.assertDictEqual(
                zxy_ch,
                self.header._comp_dict["zxy"]["ch"].to_dict(single=True),
            )

    def test_zyx(self):
        zyx_rx = OrderedDict(
            [
                ("center", "311288:4281879:1548.1 m"),
                ("gdp_stn", None),
                ("h_p_r", [0.0, 0.0, 180.0]),
                ("length", 100.0),
                (
                    "u_t_m1",
                    ["311238.97:4281888.79:1548.1", "311288:4281879:1548.1"],
                ),
                ("x_y_z1", ["311238.97:4281888.79:0", "311288:4281879:0"]),
                ("x_y_z2", ["311337.03:4281869.21:0", "311288:4281879:0"]),
            ]
        )
        with self.subTest("zyx_rx"):
            self.assertDictEqual(
                zyx_rx,
                self.header._comp_dict["zyx"]["rx"].to_dict(single=True),
            )

        zyx_ch = OrderedDict(
            [
                ("a_d_card_s_n", ["c6c58cb0", "5ee2ee6b"]),
                ("azimuth", ["101.3", "11.3"]),
                ("c_res", ["0", "0"]),
                ("cmp", ["ey", "hx"]),
                ("gdp_box", ["17", "17"]),
                ("incl", ["0", "0"]),
                ("number", ["22", "2374"]),
                ("stn", ["22", "22"]),
            ]
        )

        with self.subTest("zyx_ch"):
            self.assertDictEqual(
                zyx_ch,
                self.header._comp_dict["zyx"]["ch"].to_dict(single=True),
            )

    def test_zyy(self):
        zyy_rx = OrderedDict(
            [
                ("center", "311288:4281879:1548.1 m"),
                ("gdp_stn", None),
                ("h_p_r", [0.0, 0.0, 180.0]),
                ("length", 100.0),
                (
                    "u_t_m1",
                    ["311238.97:4281888.79:1548.1", "311288:4281879:1548.1"],
                ),
                ("x_y_z1", ["311238.97:4281888.79:0", "311288:4281879:0"]),
                ("x_y_z2", ["311337.03:4281869.21:0", "311288:4281879:0"]),
            ]
        )
        with self.subTest("zyy_rx"):
            self.assertDictEqual(
                zyy_rx,
                self.header._comp_dict["zyy"]["rx"].to_dict(single=True),
            )

        zyy_ch = OrderedDict(
            [
                ("a_d_card_s_n", ["c6c58cb0", "2ee08e36"]),
                ("azimuth", ["101.3", "101.3"]),
                ("c_res", ["0", "0"]),
                ("cmp", ["ey", "hy"]),
                ("gdp_box", ["17", "17"]),
                ("incl", ["0", "0"]),
                ("number", ["22", "287"]),
                ("stn", ["22", "22"]),
            ]
        )

        with self.subTest("zyy_ch"):
            self.assertDictEqual(
                zyy_ch,
                self.header._comp_dict["zyy"]["ch"].to_dict(single=True),
            )

    def test_tzx(self):
        tzx_rx = OrderedDict(
            [
                ("center", "311288:4281879:774.05 m"),
                ("gdp_stn", None),
                ("h_p_r", [0.0, 0.0, 180.0]),
                ("length", 0.0),
                ("u_t_m1", ["311288:4281879:1548.1", "311288:4281879:1548.1"]),
                ("x_y_z1", ["311288:4281879:0", "311288:4281879:0"]),
                ("x_y_z2", ["311288:4281879:0", "311288:4281879:0"]),
            ]
        )
        with self.subTest("tzx_rx"):
            self.assertDictEqual(
                tzx_rx,
                self.header._comp_dict["tzx"]["rx"].to_dict(single=True),
            )

        tzx_ch = OrderedDict(
            [
                ("a_d_card_s_n", ["2ac72b6b", "5ee2ee6b"]),
                ("azimuth", ["0", "11.3"]),
                ("c_res", ["0", "0"]),
                ("cmp", ["hz", "hx"]),
                ("gdp_box", ["17", "17"]),
                ("incl", ["90", "0"]),
                ("number", ["2524", "2374"]),
                ("stn", ["22", "22"]),
            ]
        )

        with self.subTest("tzx_ch"):
            self.assertDictEqual(
                tzx_ch,
                self.header._comp_dict["tzx"]["ch"].to_dict(single=True),
            )

    def test_tzy(self):
        tzy_rx = OrderedDict(
            [
                ("center", "311288:4281879:774.05 m"),
                ("gdp_stn", None),
                ("h_p_r", [0.0, 0.0, 180.0]),
                ("length", 0.0),
                ("u_t_m1", ["311288:4281879:1548.1", "311288:4281879:1548.1"]),
                ("x_y_z1", ["311288:4281879:0", "311288:4281879:0"]),
                ("x_y_z2", ["311288:4281879:0", "311288:4281879:0"]),
            ]
        )
        with self.subTest("tzy_rx"):
            self.assertDictEqual(
                tzy_rx,
                self.header._comp_dict["tzy"]["rx"].to_dict(single=True),
            )

        tzy_ch = OrderedDict(
            [
                ("a_d_card_s_n", ["2ac72b6b", "2ee08e36"]),
                ("azimuth", ["0", "101.3"]),
                ("c_res", ["0", "0"]),
                ("cmp", ["hz", "hy"]),
                ("gdp_box", ["17", "17"]),
                ("incl", ["90", "0"]),
                ("number", ["2524", "287"]),
                ("stn", ["22", "22"]),
            ]
        )

        with self.subTest("tzy_ch"):
            self.assertDictEqual(
                tzy_ch,
                self.header._comp_dict["tzy"]["ch"].to_dict(single=True),
            )

    def test_latitude(self):
        self.assertAlmostEqual(38.6653467, self.header.latitude)

    def test_longitude(self):
        self.assertAlmostEqual(-113.1690717, self.header.longitude)

    def test_elevation(self):
        self.assertAlmostEqual(1548.1, self.header.elevation)

    def test_has_channel(self):
        for ch in ["zxx", "zxy", "zyx", "zyy", "tzx", "tzy"]:
            with self.subTest(msg=ch):
                self.assertTrue(self.header._has_channel(ch))

    def test_center_location(self):
        self.assertListEqual([311288.0, 4281879.0, 1548.1], self.header.center_location)

    def test_easting(self):
        self.assertEqual(311288.0, self.header.easting)

    def test_northing(self):
        self.assertEqual(4281879.0, self.header.northing)

    def test_datum(self):
        self.assertEqual("WGS84", self.header.datum)

    def test_utm_zone(self):
        self.assertEqual("12", self.header.utm_zone)

    def test_station(self):
        self.assertEqual("22", self.header.station)

    def test_instrument_id(self):
        self.assertEqual("17", self.header.instrument_id)

    def test_instrument_type(self):
        self.assertEqual("ZEN", self.header.instrument_type)

    def test_firmware(self):
        self.assertEqual("4457", self.header.firmware)

    def start_time(self):
        self.assertEqual("2022-05-16T23:46:18+00:00", self.header.start_time)


class TestAVG(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.avg = ZongeMTAvg(fn=TF_AVG_TIPPER, z_positive="up")
        self.avg.read()

    def test_z(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.avg.z.shape, (51, 2, 2))

        with self.subTest("type"):
            self.assertEqual(self.avg.z.dtype.type, np.complex128)

        with self.subTest("non zero"):
            self.assertTrue(self.avg.z.all() != 0)

    def test_z_err(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.avg.z_err.shape, (51, 2, 2))

        with self.subTest("type"):
            self.assertEqual(self.avg.z_err.dtype.type, np.float64)

        with self.subTest("non zero"):
            self.assertTrue(self.avg.z_err.all() != 0)

    def test_t(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.avg.t.shape, (51, 1, 2))

        with self.subTest("type"):
            self.assertEqual(self.avg.t.dtype.type, np.complex128)

        with self.subTest("non zero"):
            self.assertTrue(self.avg.t.all() != 0)

    def test_t_err(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.avg.t_err.shape, (51, 1, 2))

        with self.subTest("type"):
            self.assertEqual(self.avg.t_err.dtype.type, np.float64)

        with self.subTest("non zero"):
            self.assertTrue(self.avg.t_err.all() != 0)

    def test_frequency(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.avg.frequency.shape, (51,))

    def test_z_first_element(self):
        z1 = np.array(
            [
                [-10.16752339 - 2.70034593j, 0.21016642 + 0.49228452j],
                [52.05528553 + 4.76589728j, -0.42514998 - 1.2095569j],
            ]
        )

        self.assertTrue(np.isclose(z1, self.avg.z[0]).all())

    def test_z_final_element(self):
        zf = np.array(
            [
                [51.80694503 - 42.43686378j, 116.01781236 + 128.3445648j],
                [-1051.1278249 + 1808.8705608j, -112.92397163 + 35.82342154j],
            ]
        )

        self.assertTrue(np.isclose(zf, self.avg.z[-1]).all())

    def test_t_first_element(self):
        t1 = np.array([[923.7823987 - 524.50678723j, -22.74427485 - 18.94823397j]])

        self.assertTrue(np.isclose(t1, self.avg.t[0]).all())

    def test_t_last_element(self):
        t1 = np.array([[3.71315818 + 10.6661564j, -0.30581038 + 0.60563024j]])

        self.assertTrue(np.isclose(t1, self.avg.t[-1]).all())

    def test_z_err_first_element(self):
        z1 = np.array([[13.50078836, 0.69379092], [67.73395417, 1.66174935]])

        self.assertTrue(np.isclose(z1, self.avg.z_err[0]).all())

    def test_z_err_final_element(self):
        zf = np.array([[22.00814395, 9.4763284], [362.35893807, 22.16312252]])

        self.assertTrue(np.isclose(zf, self.avg.z_err[-1]).all())

    def test_t_err_first_element(self):
        t1 = np.array([[1062.3, 29.603]])

        self.assertTrue(np.isclose(t1, self.avg.t_err[0]).all())

    def test_t_err_last_element(self):
        t1 = np.array([[11.294, 0.67846]])

        self.assertTrue(np.isclose(t1, self.avg.t_err[-1]).all())


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
