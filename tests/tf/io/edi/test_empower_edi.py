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
from mt_metadata import TF_EDI_EMPOWER

# =============================================================================
# CGG
# =============================================================================
class TestEMPOWEREDI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_EMPOWER)
        self.maxDiff = None

    def test_header(self):
        head = OrderedDict(
            [
                ("acqdate", "1980-01-01T00:00:00+00:00"),
                ("coordinate_system", "geographic"),
                ("dataid", "701_merged_wrcal"),
                ("datum", "WGS84"),
                ("elevation", 2489.0),
                ("empty", 1e32),
                ("fileby", "EMTF FCU"),
                ("latitude", 40.64811111111111),
                ("longitude", -106.21241666666667),
                ("stdvers", "SEG 1.0"),
                ("units", "millivolts_per_kilometer_per_nanotesla"),
            ]
        )

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("Declination Model"):
            self.assertEqual(self.edi_obj.Header.declination.model, "WMM")
        with self.subTest("Declination value"):
            self.assertEqual(self.edi_obj.Header.declination.value, 0.0)

    def test_info(self):
        info_list = [
            "unique_id = {88290cfe-9200-4cc2-a0dd-5ed7cd7f95ea}",
            "duration = 24h 47m 13s",
            "comb_filter = 60 HZ",
            "fine_robust = NONE",
            "totoal_rejected_crosspowers = 0.0000%",
        ]

        self.assertListEqual(info_list, self.edi_obj.Info.info_list)

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 90.0),
                ("chtype", "EX"),
                ("id", 1004.001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", -48.8),
                ("y2", 46.5),
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
                ("x", -50.6),
                ("x2", 48.5),
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
                ("x", 8.5),
                ("y", 8.5),
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
                ("x", -8.5),
                ("y", 8.5),
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
                ("x", 21.2),
                ("y", -21.2),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hz.to_dict(single=True)
        )

    def test_measurement(self):
        m_list = [
            "MAXCHAN=7",
            "MAXRUN=999",
            "MAXMEAS=9999",
            "UNITS=M",
            "REFTYPE=CART",
        ]

        self.assertListEqual(
            m_list, self.edi_obj.Measurement.measurement_list[0 : len(m_list)]
        )

        with self.subTest("reflat"):
            self.assertAlmostEqual(
                40.64811111111111, self.edi_obj.Measurement.reflat, 5
            )

        with self.subTest("reflon"):
            self.assertAlmostEqual(
                -106.21241666666667, self.edi_obj.Measurement.reflon, 5
            )

        with self.subTest("reflong"):
            self.assertAlmostEqual(
                -106.21241666666667, self.edi_obj.Measurement.reflong, 5
            )

        with self.subTest("refelev"):
            self.assertAlmostEqual(2489.0, self.edi_obj.Measurement.refelev, 2)

    def test_data_section(self):
        d_list = [
            'SECTID="701_merged_wrcal"',
            "NFREQ=98",
            "HX= 1001.001",
            "HY= 1002.001",
            "HZ= 1003.001",
            "EX= 1004.001",
            "EY= 1005.001",
        ]

        self.assertListEqual(d_list, self.edi_obj.Data.data_list)

    def test_impedance(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.z.shape, (98, 2, 2))

        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.z_err.shape, (98, 2, 2))

        with self.subTest("first element"):
            self.assertAlmostEqual(
                self.edi_obj.z[0, 0, 0], (19.91471 + 63.25052j)
            )

        with self.subTest("last element"):
            self.assertAlmostEqual(
                self.edi_obj.z[-1, 1, 1], (-0.005189691 - 0.0085249j)
            )
        with self.subTest("first element error"):
            self.assertAlmostEqual(
                self.edi_obj.z_err[0, 0, 0], 1.1270665463937788
            )

        with self.subTest("last element error"):
            self.assertAlmostEqual(
                self.edi_obj.z_err[-1, 1, 1], 0.00031013205251956787
            )

    def test_tipper(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.t.shape, (98, 1, 2))
        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.t_err.shape, (98, 1, 2))

        with self.subTest("first element"):
            self.assertAlmostEqual(
                self.edi_obj.t[0, 0, 0], (0.01175011 - 0.006787284j)
            )

        with self.subTest("last element"):
            self.assertAlmostEqual(
                self.edi_obj.t[-1, 0, 1], (0.2252638 + 0.1047829j)
            )
        with self.subTest("first element error"):
            self.assertAlmostEqual(
                self.edi_obj.t_err[0, 0, 0], 0.0006966629744718747
            )

        with self.subTest("last element error"):
            self.assertAlmostEqual(
                self.edi_obj.t_err[-1, 0, 1], 0.01090868461364614
            )

    def test_rotation_angle(self):
        with self.subTest("all zeros"):
            self.assertTrue((self.edi_obj.rotation_angle == 0).all())

        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.rotation_angle.shape, (98,))


class TestEMpowerTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf_obj = TF(TF_EDI_EMPOWER)
        self.tf_obj.read()

        self.edi_obj = self.tf_obj.to_edi()
        self.maxDiff = None

    def test_header(self):
        head = OrderedDict(
            [
                ("acqdate", "1980-01-01T00:00:00+00:00"),
                ("coordinate_system", "geographic"),
                ("dataid", "701_merged_wrcal"),
                ("datum", "WGS84"),
                ("elevation", 2489.0),
                ("empty", 1e32),
                ("fileby", "EMTF FCU"),
                ("latitude", 40.64811111111111),
                ("longitude", -106.21241666666667),
                ("stdvers", "SEG 1.0"),
                ("units", None),
            ]
        )

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("Declination Model"):
            self.assertEqual(self.edi_obj.Header.declination.model, "WMM")
        with self.subTest("Declination value"):
            self.assertEqual(self.edi_obj.Header.declination.value, 0.0)

    def test_info(self):
        info_list = [
            "701_merged_wrcala.channels_recorded_auxiliary = []",
            "701_merged_wrcala.channels_recorded_electric = ['ex', 'ey']",
            "701_merged_wrcala.channels_recorded_magnetic = ['hx', 'hy', 'hz']",
            "701_merged_wrcala.data_logger.model = mtu-5c",
            "701_merged_wrcala.data_logger.timing_system.drift = 0.0",
            "701_merged_wrcala.data_logger.timing_system.type = GPS",
            "701_merged_wrcala.data_logger.timing_system.uncertainty = 0.0",
            "701_merged_wrcala.data_type = BBMT",
            "701_merged_wrcala.ex.ac.end = 2.5",
            "701_merged_wrcala.ex.channel_id = 1004.001",
            "701_merged_wrcala.ex.channel_number = 0",
            "701_merged_wrcala.ex.comments = saturation=0.0870754",
            "701_merged_wrcala.ex.component = ex",
            "701_merged_wrcala.ex.contact_resistance.end = 4222.68",
            "701_merged_wrcala.ex.contact_resistance.start = 1558.69",
            "701_merged_wrcala.ex.dc.end = 0.0537872",
            "701_merged_wrcala.ex.dipole_length = 95.3",
            "701_merged_wrcala.ex.measurement_azimuth = 90.0",
            "701_merged_wrcala.ex.measurement_tilt = 0.0",
            "701_merged_wrcala.ex.negative.type = electric",
            "701_merged_wrcala.ex.positive.type = electric",
            "701_merged_wrcala.ex.translated_azimuth = 90.0",
            "701_merged_wrcala.ex.type = electric",
            "701_merged_wrcala.ey.ac.end = 2.5",
            "701_merged_wrcala.ey.channel_id = 1005.001",
            "701_merged_wrcala.ey.channel_number = 0",
            "701_merged_wrcala.ey.comments = saturation=0.0379904",
            "701_merged_wrcala.ey.component = ey",
            "701_merged_wrcala.ey.contact_resistance.end = 2230.26",
            "701_merged_wrcala.ey.contact_resistance.start = 2199.7",
            "701_merged_wrcala.ey.dc.end = 0.0120163",
            "701_merged_wrcala.ey.dipole_length = 99.1",
            "701_merged_wrcala.ey.measurement_azimuth = 0.0",
            "701_merged_wrcala.ey.measurement_tilt = 0.0",
            "701_merged_wrcala.ey.negative.type = electric",
            "701_merged_wrcala.ey.positive.type = electric",
            "701_merged_wrcala.ey.translated_azimuth = 0.0",
            "701_merged_wrcala.ey.type = electric",
            "701_merged_wrcala.hx.channel_id = 1001.001",
            "701_merged_wrcala.hx.channel_number = 0",
            "701_merged_wrcala.hx.comments = cal_name=57507_646504d8.scal,saturation=0.000280165",
            "701_merged_wrcala.hx.component = hx",
            "701_merged_wrcala.hx.measurement_azimuth = 0.0",
            "701_merged_wrcala.hx.measurement_tilt = 0.0",
            "701_merged_wrcala.hx.sensor.id = 57507",
            "701_merged_wrcala.hx.sensor.model = mtc-155",
            "701_merged_wrcala.hx.sensor.type = magnetic",
            "701_merged_wrcala.hx.type = magnetic",
            "701_merged_wrcala.hy.channel_id = 1002.001",
            "701_merged_wrcala.hy.channel_number = 0",
            "701_merged_wrcala.hy.comments = cal_name=57513_646504d8.scal,saturation=5.60331e-5",
            "701_merged_wrcala.hy.component = hy",
            "701_merged_wrcala.hy.measurement_azimuth = 90.0",
            "701_merged_wrcala.hy.measurement_tilt = 0.0",
            "701_merged_wrcala.hy.sensor.id = 57513",
            "701_merged_wrcala.hy.sensor.model = mtc-155",
            "701_merged_wrcala.hy.sensor.type = magnetic",
            "701_merged_wrcala.hy.translated_azimuth = 90.0",
            "701_merged_wrcala.hy.type = magnetic",
            "701_merged_wrcala.hz.channel_id = 1003.001",
            "701_merged_wrcala.hz.channel_number = 0",
            "701_merged_wrcala.hz.comments = cal_name=53408_646504d8.scal,saturation=0",
            "701_merged_wrcala.hz.component = hz",
            "701_merged_wrcala.hz.measurement_azimuth = 0.0",
            "701_merged_wrcala.hz.measurement_tilt = 0.0",
            "701_merged_wrcala.hz.sensor.id = 53408",
            "701_merged_wrcala.hz.sensor.model = mtc-185",
            "701_merged_wrcala.hz.sensor.type = magnetic",
            "701_merged_wrcala.hz.type = magnetic",
            "701_merged_wrcala.id = 701_merged_wrcala",
            "701_merged_wrcala.sample_rate = 0.0",
            "comb_filter = 60 HZ",
            "duration = 24h 47m 13s",
            "fine_robust = NONE",
            "provenance.creation_time = 2023-05-30T00:00:00+00:00",
            "provenance.software.name = EMTF FCU",
            "provenance.software.version = 4.0",
            "provenance.submitter.author = EMTF FCU",
            "provenance.submitter.name = EMTF FCU",
            "totoal_rejected_crosspowers = 0.0000%",
            "transfer_function.coordinate_system = geopgraphic",
            "transfer_function.data_quality.rating.value = 0",
            "transfer_function.id = 701_merged_wrcal",
            "transfer_function.processed_date = 2023-05-30",
            "transfer_function.remote_references = []",
            "transfer_function.runs_processed = ['701_merged_wrcala']",
            "transfer_function.software.name = empower v2.9.0.7",
            "unique_id = {88290cfe-9200-4cc2-a0dd-5ed7cd7f95ea}",
        ]

        self.assertListEqual(info_list, self.edi_obj.Info.info_list)

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", "1004.001"),
                ("azm", 90.0),
                ("chtype", "ex"),
                ("id", 1004.001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", -48.8),
                ("y2", 46.5),
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
                ("x", -50.6),
                ("x2", 48.5),
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
                ("x", 8.5),
                ("y", 8.5),
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
                ("x", -8.5),
                ("y", 8.5),
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
                ("x", 21.2),
                ("y", -21.2),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hz.to_dict(single=True)
        )

    def test_measurement(self):
        m_dict = OrderedDict(
            [
                ("maxchan", 5),
                ("maxmeas", 999),
                ("maxrun", 999),
                ("refelev", 2489.0),
                ("reflat", 40.648111),
                ("refloc", "701_merged_wrcal"),
                ("reflon", -106.212417),
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
                ("nchan", 5),
                ("nfreq", 98),
                ("rrhx", "0"),
                ("rrhy", "0"),
                ("sectid", "701_merged_wrcal"),
            ]
        )

        self.assertDictEqual(d_list, self.edi_obj.Data.to_dict(single=True))

    def test_impedance(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.z.shape, (98, 2, 2))

        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.z_err.shape, (98, 2, 2))

        with self.subTest("first element"):
            self.assertAlmostEqual(
                self.edi_obj.z[0, 0, 0], (19.91471 + 63.25052j)
            )

        with self.subTest("last element"):
            self.assertAlmostEqual(
                self.edi_obj.z[-1, 1, 1], (-0.005189691 - 0.0085249j)
            )
        with self.subTest("first element error"):
            self.assertAlmostEqual(
                self.edi_obj.z_err[0, 0, 0], 1.1270665463937788
            )

        with self.subTest("last element error"):
            self.assertAlmostEqual(
                self.edi_obj.z_err[-1, 1, 1], 0.00031013205251956787
            )

    def test_tipper(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.t.shape, (98, 1, 2))
        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.t_err.shape, (98, 1, 2))

        with self.subTest("first element"):
            self.assertAlmostEqual(
                self.edi_obj.t[0, 0, 0], (0.01175011 - 0.006787284j)
            )

        with self.subTest("last element"):
            self.assertAlmostEqual(
                self.edi_obj.t[-1, 0, 1], (0.2252638 + 0.1047829j)
            )
        with self.subTest("first element error"):
            self.assertAlmostEqual(
                self.edi_obj.t_err[0, 0, 0], 0.0006966629744718747
            )

        with self.subTest("last element error"):
            self.assertAlmostEqual(
                self.edi_obj.t_err[-1, 0, 1], 0.01090868461364614
            )

    def test_rotation_angle(self):
        with self.subTest("all zeros"):
            self.assertTrue((self.edi_obj.rotation_angle == 0).all())

        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.rotation_angle.shape, (98,))


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
