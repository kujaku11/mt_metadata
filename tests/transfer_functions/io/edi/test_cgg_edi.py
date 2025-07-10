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

from mt_metadata import TF_EDI_CGG
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io import edi
from mt_metadata.utils.mttime import MTime


# =============================================================================
# CGG
# =============================================================================
class TestCGGEDI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.edi_obj = edi.EDI(fn=TF_EDI_CGG)
        cls.maxDiff = None

    def test_header(self):
        head = {
            "ACQBY": "GSC_CGG",
            "COORDINATE_SYSTEM": "geographic",
            "DATAID": "TEST01".lower(),
            "DATUM": "WGS 84",
            "ELEV": 175.270,
            "EMPTY": 1.000000e32,
            "FILEBY": "",
            "LAT": -30.930285,
            "LOC": "Australia",
            "LON": 127.22923,
        }

        for key, value in head.items():
            with self.subTest(key):
                if key == "ELEV":
                    key = "elevation"
                elif key == "LAT":
                    key = "latitude"
                elif key == "LON":
                    key = "longitude"
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("acquire date"):
            self.assertEqual(self.edi_obj.Header.acqdate, MTime(time_stamp="06/05/14"))

        with self.subTest("units"):
            self.assertNotEqual(
                self.edi_obj.Header.units,
                "milliVolt per kilometer per nanoTesla",
            )

    def test_info(self):
        info_list = [
            ">INFO\n",
            "    maxinfo=31\n",
            "    /*\n",
            "    site info\n",
            "    run.acquired_by.author=Somebody\n",
            "    run.data_logger.id=222\n",
            "    run.ex.measurement_azimuth=0.0\n",
            "    run.ex.dipole_length=100.0\n",
            "    run.ey.dipole_length=100.0\n",
            "    run.ex.contact_resistance.start=44479800\n",
            "    run.ey.contact_resistance.start=41693800\n",
            "    h_site=E_SITE\n",
            "    run.hx.measurement_azimuth=0.0\n",
            "    run.hx.sensor.id=MFS06e-246\n",
            "    run.hy.sensor.id=MFS06e-249\n",
            "    run.hz.sensor.id=MFS06e-249\n",
            "    run.hx.h_field_max.start=169869\n",
            "    run.hy.h_field_max.start=164154\n",
            "    run.hz.h_field_max.start=2653\n",
            "    processing parameters\n",
            "    transfer_function.software.name=L13ss\n",
            "    transfer_function.processing_parameters=[ndec=1, nfft=128, ntype=1, rrtype=None, removelargelines=true, rotmaxe=false]\n",
            "    */\n",
        ]

        self.assertListEqual(info_list, self.edi_obj.Info.write_info())

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
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
            ch, self.edi_obj.Measurement.measurements["ex"].to_dict(single=True)
        )

    def test_measurement_ey(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
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
            ch, self.edi_obj.Measurement.measurements["ey"].to_dict(single=True)
        )

    def test_measurement_hx(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
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
            ch, self.edi_obj.Measurement.measurements["hx"].to_dict(single=True)
        )

    def test_measurement_hy(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
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
            ch, self.edi_obj.Measurement.measurements["hy"].to_dict(single=True)
        )

    def test_measurement_hz(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
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
            ch, self.edi_obj.Measurement.measurements["hz"].to_dict(single=True)
        )

    def test_measurement_rrhx(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
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
            ch, self.edi_obj.Measurement.measurements["rrhx"].to_dict(single=True)
        )

    def test_measurement_rrhy(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
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
            ch, self.edi_obj.Measurement.measurements["rrhy"].to_dict(single=True)
        )

    def test_measurement(self):
        m_list = [
            '    REFLOC="TEST01"\n',
            "    REFLAT=-30:55:49.026000\n",
            "    REFLON=127:13:45.228000\n",
            "    REFELEV=175.27\n",
            "    REFTYPE=cartesian\n",
            "    UNITS=meter\n",
        ]

        self.assertListEqual(
            m_list, self.edi_obj.Measurement.write_measurement()[4 : 4 + len(m_list)]
        )

        with self.subTest("reflat"):
            self.assertAlmostEqual(-30.930285, self.edi_obj.Measurement.reflat, 5)

        with self.subTest("reflon"):
            self.assertAlmostEqual(127.22923, self.edi_obj.Measurement.reflon, 5)

        with self.subTest("reflong"):
            self.assertAlmostEqual(127.22923, self.edi_obj.Measurement.reflon, 5)

        with self.subTest("refelev"):
            self.assertAlmostEqual(175.27, self.edi_obj.Measurement.refelev, 2)

    # def test_data_section(self):
    #     d_list = ["NFREQ=73"]

    #     self.assertListEqual(d_list, self.edi_obj.Data.get)

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
    def setUpClass(cls):
        cls.tf_obj = TF(TF_EDI_CGG)
        cls.tf_obj.read()

        cls.edi_obj = cls.tf_obj.to_edi()
        cls.maxDiff = None

    def test_header(self):
        head = {
            "ACQBY": "GSC_CGG",
            "COORDINATE_SYSTEM": "geographic",
            "DATAID": "test01",
            "DATUM": "WGS 84",
            "ELEV": 175.270,
            "EMPTY": 1.000000e32,
            "FILEBY": "",
            "LAT": -30.930285,
            "LOC": "Australia",
            "LON": 127.22923,
        }

        for key, value in head.items():
            with self.subTest(key):
                if key == "ELEV":
                    key = "elevation"
                elif key == "LAT":
                    key = "latitude"
                elif key == "LON":
                    key = "longitude"

                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("acquire date"):
            self.assertEqual(self.edi_obj.Header.acqdate, MTime(time_stamp="06/05/14"))

        with self.subTest("units"):
            self.assertEqual(
                self.edi_obj.Header.units,
                "milliVolt per kilometer per nanoTesla",
            )

    def test_info(self):
        info_list = [
            ">INFO\n",
            "    survey.acquired_by.author=GSC_CGG\n",
            "    survey.datum=WGS 84\n",
            "    survey.geographic_name=Australia\n",
            "    survey.id=0\n",
            "    survey.project=EGC\n",
            "    survey.release_license=CC-BY-4.0\n",
            "    transfer_function.coordinate_system=geographic\n",
            "    transfer_function.id=test01\n",
            "    transfer_function.processed_date=2014-10-07T00:00:00+00:00\n",
            "    transfer_function.processing_parameters.ndec=1\n",
            "    transfer_function.processing_parameters.nfft=128\n",
            "    transfer_function.processing_parameters.ntype=1\n",
            "    transfer_function.processing_parameters.rrtype=None\n",
            "    transfer_function.processing_parameters.removelargelines=true\n",
            "    transfer_function.processing_parameters.rotmaxe=false\n",
            "    transfer_function.remote_references=[]\n",
            "    transfer_function.runs_processed=[test01a]\n",
            "    transfer_function.sign_convention=+\n",
            "    transfer_function.software.name=L13ss\n",
            "    transfer_function.units=milliVolt per kilometer per nanoTesla\n",
            "    provenance.creation_time=2014-10-07T00:00:00+00:00\n",
            "    provenance.software.version=Antlr3.Runtime:3.5.0.2;ContourEngine:1.0.41.8272;CoordinateSystemService:1.4.0.8439;DocumentCommon:1.4.0.8465;Fluent:2.1.0.0;GeoApi:1.7.0.0;hasp_net_windows:7.0.1.36183;Launcher:1.4.0.8471;MapDocument:1.4.0.8469;MTDocument:1.4.0.8459;MTDocumentDataProvider:1.4.0.8467;MTInversionCommon:1.4.0.8371;Ookii.Dialogs.Wpf:1.0.0.0;PlotElement:1.4.0.8466;PluginHost:1.4.0.8440;ProjNet:1.2.5085.21309;ShellEngine:1.4.0.8380;System.Windows.Interactivity:4.0.0.0;Utils:1.4.0.8449;Xceed.Wpf.AvalonDock:2.0.0.0;Xceed.Wpf.AvalonDock.Themes.Aero:2.0.0.0;Xceed.Wpf.Toolkit:1.9.0.0;\n",
            "    test01a.acquired_by.author=Somebody\n",
            "    test01a.channels_recorded_auxiliary=[rrhx, rrhy]\n",
            "    test01a.channels_recorded_electric=[ex, ey]\n",
            "    test01a.channels_recorded_magnetic=[hx, hy, hz]\n",
            "    test01a.data_logger.id=222\n",
            "    test01a.data_logger.power_source.voltage.end=0.0\n",
            "    test01a.data_logger.power_source.voltage.start=0.0\n",
            "    test01a.data_logger.timing_system.drift=0.0\n",
            "    test01a.data_logger.timing_system.type=GPS\n",
            "    test01a.data_logger.timing_system.uncertainty=0.0\n",
            "    test01a.data_type=BBMT\n",
            "    test01a.id=test01a\n",
            "    test01a.sample_rate=0.0\n",
            "    test01a.time_period.start=2014-06-05T00:00:00+00:00\n",
            "    test01a.hx.channel_id=1001.001\n",
            "    test01a.hx.channel_number=0\n",
            "    test01a.hx.component=hx\n",
            "    test01a.hx.h_field_max.end=0.0\n",
            "    test01a.hx.h_field_max.start=0.0\n",
            "    test01a.hx.h_field_min.end=0.0\n",
            "    test01a.hx.h_field_min.start=0.0\n",
            "    test01a.hx.location.datum=WGS 84\n",
            "    test01a.hx.measurement_azimuth=0.0\n",
            "    test01a.hx.measurement_tilt=0.0\n",
            "    test01a.hx.sensor.id=MFS06e-246\n",
            "    test01a.hx.sensor.type=magnetic\n",
            "    test01a.hx.type=magnetic\n",
            "    test01a.hy.channel_id=1002.001\n",
            "    test01a.hy.channel_number=0\n",
            "    test01a.hy.component=hy\n",
            "    test01a.hy.h_field_max.end=0.0\n",
            "    test01a.hy.h_field_max.start=0.0\n",
            "    test01a.hy.h_field_min.end=0.0\n",
            "    test01a.hy.h_field_min.start=0.0\n",
            "    test01a.hy.location.datum=WGS 84\n",
            "    test01a.hy.measurement_azimuth=90.0\n",
            "    test01a.hy.measurement_tilt=0.0\n",
            "    test01a.hy.sensor.id=MFS06e-249\n",
            "    test01a.hy.sensor.type=magnetic\n",
            "    test01a.hy.translated_azimuth=90.0\n",
            "    test01a.hy.type=magnetic\n",
            "    test01a.hz.channel_id=1003.001\n",
            "    test01a.hz.channel_number=0\n",
            "    test01a.hz.component=hz\n",
            "    test01a.hz.h_field_max.end=0.0\n",
            "    test01a.hz.h_field_max.start=0.0\n",
            "    test01a.hz.h_field_min.end=0.0\n",
            "    test01a.hz.h_field_min.start=0.0\n",
            "    test01a.hz.location.datum=WGS 84\n",
            "    test01a.hz.measurement_azimuth=0.0\n",
            "    test01a.hz.measurement_tilt=0.0\n",
            "    test01a.hz.sensor.id=MFS06e-249\n",
            "    test01a.hz.sensor.type=magnetic\n",
            "    test01a.hz.type=magnetic\n",
            "    test01a.ex.ac.end=0.0\n",
            "    test01a.ex.ac.start=0.0\n",
            "    test01a.ex.channel_id=1004.001\n",
            "    test01a.ex.channel_number=0\n",
            "    test01a.ex.component=ex\n",
            "    test01a.ex.contact_resistance.end=0.0\n",
            "    test01a.ex.contact_resistance.start=44479800.0\n",
            "    test01a.ex.dc.end=0.0\n",
            "    test01a.ex.dc.start=0.0\n",
            "    test01a.ex.dipole_length=100.0\n",
            "    test01a.ex.measurement_azimuth=0.0\n",
            "    test01a.ex.measurement_tilt=0.0\n",
            "    test01a.ex.negative.datum=WGS 84\n",
            "    test01a.ex.negative.type=electric\n",
            "    test01a.ex.positive.datum=WGS 84\n",
            "    test01a.ex.positive.type=electric\n",
            "    test01a.ex.type=electric\n",
            "    test01a.ey.ac.end=0.0\n",
            "    test01a.ey.ac.start=0.0\n",
            "    test01a.ey.channel_id=1005.001\n",
            "    test01a.ey.channel_number=0\n",
            "    test01a.ey.component=ey\n",
            "    test01a.ey.contact_resistance.end=0.0\n",
            "    test01a.ey.contact_resistance.start=41693800.0\n",
            "    test01a.ey.dc.end=0.0\n",
            "    test01a.ey.dc.start=0.0\n",
            "    test01a.ey.dipole_length=100.0\n",
            "    test01a.ey.measurement_azimuth=0.0\n",
            "    test01a.ey.measurement_tilt=0.0\n",
            "    test01a.ey.negative.datum=WGS 84\n",
            "    test01a.ey.negative.type=electric\n",
            "    test01a.ey.positive.datum=WGS 84\n",
            "    test01a.ey.positive.type=electric\n",
            "    test01a.ey.type=electric\n",
            "    test01a.rrhx.channel_id=1006.001\n",
            "    test01a.rrhx.channel_number=0\n",
            "    test01a.rrhx.component=rrhx\n",
            "    test01a.rrhx.location.datum=WGS 84\n",
            "    test01a.rrhx.measurement_azimuth=0.0\n",
            "    test01a.rrhx.measurement_tilt=0.0\n",
            "    test01a.rrhx.sensor.type=magnetic\n",
            "    test01a.rrhx.type=auxiliary\n",
            "    test01a.rrhy.channel_id=1007.001\n",
            "    test01a.rrhy.channel_number=0\n",
            "    test01a.rrhy.component=rrhy\n",
            "    test01a.rrhy.location.datum=WGS 84\n",
            "    test01a.rrhy.measurement_azimuth=90.0\n",
            "    test01a.rrhy.measurement_tilt=0.0\n",
            "    test01a.rrhy.sensor.type=magnetic\n",
            "    test01a.rrhy.translated_azimuth=90.0\n",
            "    test01a.rrhy.type=auxiliary\n",
        ]

        self.assertListEqual(info_list, self.edi_obj.Info.write_info())

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
            ch, self.edi_obj.Measurement.measurements["ex"].to_dict(single=True)
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
            ch, self.edi_obj.Measurement.measurements["ey"].to_dict(single=True)
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
            ch, self.edi_obj.Measurement.measurements["hx"].to_dict(single=True)
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
            ch, self.edi_obj.Measurement.measurements["hy"].to_dict(single=True)
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
            ch, self.edi_obj.Measurement.measurements["hz"].to_dict(single=True)
        )

    def test_measurement(self):
        m_dict = OrderedDict(
            [
                ("maxchan", 7),
                ("maxmeas", 7),
                ("maxrun", 999),
                ("refelev", 175.27),
                ("reflat", -30.930285),
                ("refloc", "test01"),
                ("reflon", 127.22923),
                ("reftype", "cartesian"),
                ("units", "meter"),
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
                    self.assertEqual(value, getattr(self.edi_obj.Measurement, key))

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
                ("sectid", "test01"),
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
