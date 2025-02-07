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
from mt_metadata.transfer_functions.io import edi
from mt_metadata.transfer_functions import TF
from mt_metadata.utils.mttime import MTime
from mt_metadata import TF_EDI_CGG


# =============================================================================
# CGG
# =============================================================================
class TestCGGEDI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_CGG)
        self.maxDiff = None

    def test_header(self):
        head = {
            "ACQBY": "GSC_CGG",
            "COORDINATE_SYSTEM": "geographic",
            "DATAID": "TEST01",
            "DATUM": "WGS84",
            "ELEV": 175.270,
            "EMPTY": 1.000000e32,
            "FILEBY": None,
            "LAT": -30.930285,
            "LOC": "Australia",
            "LON": 127.22923,
        }

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("acquire date"):
            self.assertEqual(self.edi_obj.Header._acqdate, MTime("06/05/14"))

        with self.subTest("units"):
            self.assertNotEqual(
                self.edi_obj.Header.units,
                "millivolts_per_kilometer_per_nanotesla",
            )

    def test_info(self):
        info_list = sorted(
            [
                "SITE INFO:",
                "H_SITE=E_SITE",
                "PROCESSING PARAMETERS:",
            ]
        )

        self.assertListEqual(info_list, self.edi_obj.Info.info_list)

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "EX"),
                ("id", 1004.001),
                ("x", 0.0),
                ("x2", 0.0),
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
                ("azm", 0.0),
                ("chtype", "EY"),
                ("id", 1005.001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", 0.0),
                ("y2", 0.0),
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
                ("id", 1001.001),
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
                ("id", 1002.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hy.to_dict(single=True)
        )

    def test_measurement_hz(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "HZ"),
                ("dip", 0.0),
                ("id", 1003.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hz.to_dict(single=True)
        )

    def test_measurement_rrhx(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "RRHX"),
                ("dip", 0.0),
                ("id", 1006.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_rrhx.to_dict(single=True)
        )

    def test_measurement_rrhy(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 90.0),
                ("chtype", "RRHY"),
                ("dip", 0.0),
                ("id", 1007.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_rrhy.to_dict(single=True)
        )

    def test_measurement(self):
        m_list = [
            'REFLOC="TEST01"',
            "REFLAT=-30:55:49.026",
            "REFLONG=+127:13:45.228",
            "REFELEV=175.27",
            "UNITS=M",
        ]

        self.assertListEqual(
            m_list, self.edi_obj.Measurement.measurement_list[0 : len(m_list)]
        )

        with self.subTest("reflat"):
            self.assertAlmostEqual(
                -30.930285, self.edi_obj.Measurement.reflat, 5
            )

        with self.subTest("reflon"):
            self.assertAlmostEqual(
                127.22923, self.edi_obj.Measurement.reflon, 5
            )

        with self.subTest("reflong"):
            self.assertAlmostEqual(
                127.22923, self.edi_obj.Measurement.reflong, 5
            )

        with self.subTest("refelev"):
            self.assertAlmostEqual(175.27, self.edi_obj.Measurement.refelev, 2)

    def test_data_section(self):
        d_list = ["NFREQ=73"]

        self.assertListEqual(d_list, self.edi_obj.Data.data_list)

    def test_impedance(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.z.shape, (73, 2, 2))

        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.z_err.shape, (73, 2, 2))

        with self.subTest("has zero"):
            self.assertEqual(self.edi_obj.z[0, 0, 0], 0 + 0j)

        with self.subTest("not zero"):
            self.assertNotEqual(self.edi_obj.z[1, 0, 0], 0 + 0j)

    def test_tipper(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.t.shape, (73, 1, 2))
        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.t_err.shape, (73, 1, 2))

    def test_rotation_angle(self):
        with self.subTest("all zeros"):
            self.assertTrue((self.edi_obj.rotation_angle == 0).all())

        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.rotation_angle.shape, (73,))


class TestCGGTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf_obj = TF(TF_EDI_CGG)
        self.tf_obj.read()

        self.edi_obj = self.tf_obj.to_edi()
        self.maxDiff = None

    def test_header(self):
        head = {
            "ACQBY": "GSC_CGG",
            "COORDINATE_SYSTEM": "geographic",
            "DATAID": "TEST01",
            "DATUM": "WGS84",
            "ELEV": 175.270,
            "EMPTY": 1.000000e32,
            "FILEBY": None,
            "LAT": -30.930285,
            "LOC": "Australia",
            "LON": 127.22923,
        }

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("acquire date"):
            self.assertEqual(self.edi_obj.Header._acqdate, MTime("06/05/14"))

        with self.subTest("units"):
            self.assertNotEqual(
                self.edi_obj.Header.units,
                "millivolts_per_kilometer_per_nanotesla",
            )

    def test_info(self):
        info_list = [
            "H_SITE=E_SITE",
            "PROCESSING PARAMETERS:",
            "SITE INFO:",
            "TEST01a.acquired_by.author = Somebody",
            "TEST01a.channels_recorded_auxiliary = []",
            "TEST01a.channels_recorded_electric = ['ex', 'ey']",
            "TEST01a.channels_recorded_magnetic = ['hx', 'hy', 'hz', 'rrhx', 'rrhy']",
            "TEST01a.data_logger.id = 222",
            "TEST01a.data_logger.timing_system.drift = 0.0",
            "TEST01a.data_logger.timing_system.type = GPS",
            "TEST01a.data_logger.timing_system.uncertainty = 0.0",
            "TEST01a.data_type = BBMT",
            "TEST01a.ex.channel_id = 1004.001",
            "TEST01a.ex.channel_number = 0",
            "TEST01a.ex.component = ex",
            "TEST01a.ex.contact_resistance.start = 44479800.0",
            "TEST01a.ex.dipole_length = 100.0",
            "TEST01a.ex.measurement_azimuth = 0.0",
            "TEST01a.ex.measurement_tilt = 0.0",
            "TEST01a.ex.negative.type = electric",
            "TEST01a.ex.positive.type = electric",
            "TEST01a.ex.translated_azimuth = 0.0",
            "TEST01a.ex.type = electric",
            "TEST01a.ey.channel_id = 1005.001",
            "TEST01a.ey.channel_number = 0",
            "TEST01a.ey.component = ey",
            "TEST01a.ey.contact_resistance.start = 41693800.0",
            "TEST01a.ey.dipole_length = 100.0",
            "TEST01a.ey.measurement_azimuth = 0.0",
            "TEST01a.ey.measurement_tilt = 0.0",
            "TEST01a.ey.negative.type = electric",
            "TEST01a.ey.positive.type = electric",
            "TEST01a.ey.translated_azimuth = 0.0",
            "TEST01a.ey.type = electric",
            "TEST01a.hx.channel_id = 1001.001",
            "TEST01a.hx.channel_number = 0",
            "TEST01a.hx.component = hx",
            "TEST01a.hx.h_field_max.start = 169869.0",
            "TEST01a.hx.measurement_azimuth = 0.0",
            "TEST01a.hx.measurement_tilt = 0.0",
            "TEST01a.hx.sensor.id = MFS06e-246",
            "TEST01a.hx.sensor.type = magnetic",
            "TEST01a.hx.type = magnetic",
            "TEST01a.hy.channel_id = 1002.001",
            "TEST01a.hy.channel_number = 0",
            "TEST01a.hy.component = hy",
            "TEST01a.hy.h_field_max.start = 164154.0",
            "TEST01a.hy.measurement_azimuth = 90.0",
            "TEST01a.hy.measurement_tilt = 0.0",
            "TEST01a.hy.sensor.id = MFS06e-249",
            "TEST01a.hy.sensor.type = magnetic",
            "TEST01a.hy.translated_azimuth = 90.0",
            "TEST01a.hy.type = magnetic",
            "TEST01a.hz.channel_id = 1003.001",
            "TEST01a.hz.channel_number = 0",
            "TEST01a.hz.component = hz",
            "TEST01a.hz.h_field_max.start = 2653.0",
            "TEST01a.hz.measurement_azimuth = 0.0",
            "TEST01a.hz.measurement_tilt = 0.0",
            "TEST01a.hz.sensor.id = MFS06e-249",
            "TEST01a.hz.sensor.type = magnetic",
            "TEST01a.hz.type = magnetic",
            "TEST01a.id = TEST01a",
            "TEST01a.rrhx.channel_id = 1006.001",
            "TEST01a.rrhx.channel_number = 0",
            "TEST01a.rrhx.component = rrhx",
            "TEST01a.rrhx.measurement_azimuth = 0.0",
            "TEST01a.rrhx.measurement_tilt = 0.0",
            "TEST01a.rrhx.sensor.type = magnetic",
            "TEST01a.rrhx.translated_azimuth = 0.0",
            "TEST01a.rrhx.type = magnetic",
            "TEST01a.rrhy.channel_id = 1007.001",
            "TEST01a.rrhy.channel_number = 0",
            "TEST01a.rrhy.component = rrhy",
            "TEST01a.rrhy.measurement_azimuth = 90.0",
            "TEST01a.rrhy.measurement_tilt = 0.0",
            "TEST01a.rrhy.sensor.type = magnetic",
            "TEST01a.rrhy.translated_azimuth = 90.0",
            "TEST01a.rrhy.type = magnetic",
            "TEST01a.sample_rate = 0.0",
            "TEST01a.time_period.start = 2014-06-05T00:00:00+00:00",
            "provenance.archive.author = none",
            "provenance.creation_time = 2014-10-07T00:00:00+00:00",
            "provenance.creator.author = none",
            "provenance.software.version = Antlr3.Runtime:3.5.0.2;ContourEngine:1.0.41.8272;CoordinateSystemService:1.4.0.8439;DocumentCommon:1.4.0.8465;Fluent:2.1.0.0;GeoApi:1.7.0.0;hasp_net_windows:7.0.1.36183;Launcher:1.4.0.8471;MapDocument:1.4.0.8469;MTDocument:1.4.0.8459;MTDocumentDataProvider:1.4.0.8467;MTInversionCommon:1.4.0.8371;Ookii.Dialogs.Wpf:1.0.0.0;PlotElement:1.4.0.8466;PluginHost:1.4.0.8440;ProjNet:1.2.5085.21309;ShellEngine:1.4.0.8380;System.Windows.Interactivity:4.0.0.0;Utils:1.4.0.8449;Xceed.Wpf.AvalonDock:2.0.0.0;Xceed.Wpf.AvalonDock.Themes.Aero:2.0.0.0;Xceed.Wpf.Toolkit:1.9.0.0;",
            "survey.acquired_by.author = GSC_CGG",
            "survey.datum = WGS84",
            "survey.geographic_name = Australia",
            "survey.id = 0",
            "survey.project = EGC",
            "survey.release_license = CC0-1.0",
            "transfer_function.coordinate_system = geopgraphic",
            "transfer_function.data_quality.rating.value = 0",
            "transfer_function.id = TEST01",
            "transfer_function.processed_date = 2014-10-07",
            "transfer_function.processing_parameters.processing_parameters = [NDec = 1, NFFT = 128, Ntype = 1, RRType = None, RemoveLargeLines = true, RotMaxE = false]",
            "transfer_function.remote_references = []",
            "transfer_function.runs_processed = ['TEST01a']",
            "transfer_function.sign_convention = +",
            "transfer_function.software.name = L13ss",
        ]

        self.assertListEqual(info_list, self.edi_obj.Info.info_list)

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", "1004.001"),
                ("azm", 0.0),
                ("chtype", "ex"),
                ("id", 1004.001),
                ("x", 0.0),
                ("x2", 0.0),
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
                ("acqchan", "1005.001"),
                ("azm", 0.0),
                ("chtype", "ey"),
                ("id", 1005.001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", 0.0),
                ("y2", 0.0),
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
                ("acqchan", "1001.001"),
                ("azm", 0.0),
                ("chtype", "hx"),
                ("dip", 0.0),
                ("id", 1001.001),
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
                ("acqchan", "1002.001"),
                ("azm", 90.0),
                ("chtype", "hy"),
                ("dip", 0.0),
                ("id", 1002.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hy.to_dict(single=True)
        )

    def test_measurement_hz(self):
        ch = OrderedDict(
            [
                ("acqchan", "1003.001"),
                ("azm", 0.0),
                ("chtype", "hz"),
                ("dip", 0.0),
                ("id", 1003.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hz.to_dict(single=True)
        )

    def test_measurement(self):
        m_dict = OrderedDict(
            [
                ("maxchan", 7),
                ("maxmeas", 999),
                ("maxrun", 999),
                ("refelev", 175.27),
                ("reflat", -30.930285),
                ("refloc", "TEST01"),
                ("reflon", 127.22923),
                ("reftype", "cartesian"),
                ("units", "m"),
            ]
        )

        for key, value in m_dict.items():
            if key in ["reflat", "reflon", "refelev"]:
                with self.subTest(key):
                    self.assertAlmostEqual(
                        value, getattr(self.edi_obj.Measurement, key), 5
                    )
            else:
                with self.subTest(key):
                    self.assertEqual(
                        value, getattr(self.edi_obj.Measurement, key)
                    )

    def test_data_section(self):
        d_list = OrderedDict(
            [
                ("ex", "1004.001"),
                ("ey", "1005.001"),
                ("hx", "1001.001"),
                ("hy", "1002.001"),
                ("hz", "1003.001"),
                ("maxblocks", 999),
                ("nchan", 7),
                ("nfreq", 73),
                ("rrhx", "1006.001"),
                ("rrhy", "1007.001"),
                ("sectid", "TEST01"),
            ]
        )

        self.assertDictEqual(d_list, self.edi_obj.Data.to_dict(single=True))

    def test_impedance(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.z.shape, (73, 2, 2))

        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.z_err.shape, (73, 2, 2))

        with self.subTest("has zero"):
            self.assertEqual(self.edi_obj.z[0, 0, 0], 0 + 0j)

        with self.subTest("not zero"):
            self.assertNotEqual(self.edi_obj.z[1, 0, 0], 0 + 0j)

    def test_tipper(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.t.shape, (73, 1, 2))
        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.t_err.shape, (73, 1, 2))

    def test_rotation_angle(self):
        with self.subTest("all zeros"):
            self.assertTrue((self.edi_obj.rotation_angle == 0).all())

        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.rotation_angle.shape, (73,))

    def test_set_rotation_angle_to_tf(self):
        a = self.tf_obj.to_edi()
        a.rotation_angle[:] = 13

        tf = TF()
        tf.from_edi(a)

        self.assertTrue((tf._rotation_angle == a.rotation_angle).all())


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
