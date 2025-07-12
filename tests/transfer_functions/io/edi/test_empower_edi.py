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

from mt_metadata import TF_EDI_EMPOWER
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io import edi


# =============================================================================
# CGG
# =============================================================================
class TestEMPOWEREDI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.edi_obj = edi.EDI(fn=TF_EDI_EMPOWER)
        cls.maxDiff = None

    def test_header(self):
        head = OrderedDict(
            [
                ("acqdate", "1980-01-01T00:00:00+00:00"),
                ("coordinate_system", "geographic"),
                ("dataid", "701_merged_wrcal"),
                ("datum", "WGS 84"),
                ("elevation", 2489.0),
                ("empty", 1e32),
                ("fileby", "EMTF FCU"),
                ("latitude", 40.64811111111111),
                ("longitude", -106.21241666666667),
                ("stdvers", "SEG 1.0"),
                ("units", "milliVolt per kilometer per nanoTesla"),
            ]
        )

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("Declination Model"):
            self.assertEqual(self.edi_obj.Header.declination.model, "IGRF")
        with self.subTest("Declination value"):
            self.assertEqual(self.edi_obj.Header.declination.value, 0.0)

    def test_info(self):
        info_list = [
            ">INFO\n",
            "    maxinfo=999\n",
            "    project\n",
            "    survey\n",
            "    survey.time_period.start_date=2023\n",
            "    processedby\n",
            "    transfer_function.software.name=EMpower v2.9.0.7\n",
            "    processingtag\n",
            "    station.geographic_name=Near Steamboat Springs, US (Mountain Standard Time)\n",
            "    runlist\n",
            "    remoteref\n",
            "    remotesite\n",
            "    signconvention\n",
            "    unique id={88290cfe-9200-4cc2-a0dd-5ed7cd7f95ea}\n",
            "    process date=2023-05-30 16:22\n",
            "    duration=24h 47m 13s\n",
            "    station.location.declination.value=0°\n",
            "    coordinates=40° 38' 53.2\", -106° 12' 44.7\"\n",
            "    gps (min - max)=8 - 13\n",
            "    temperature (min - max)=18° - 48°\n",
            "    comb filter=60 HZ\n",
            "    fine robust=NONE\n",
            "    editing_workbench.totoal rejected crosspowers=0.0000%\n",
            "    run.id=10526_2023-05-19-170246\n",
            "    run.data_logger.model=MTU-5C\n",
            "    run.geographic_name=701 Walden South\n",
            "    run.acquired_by.author\n",
            "    run.measurement_azimuth=0\n",
            "    run.ex.component=E1\n",
            "    run.ex.dipole_length=95.3\n",
            "    run.ex.ac.end=2.5\n",
            "    run.ex.dc.end=0.0537872\n",
            "    run.ex.contact_resistance.start=1558.69\n",
            "    run.ex.contact_resistance.end=4222.68\n",
            "    run.ex.comments=[saturation=0.0870754%, min value=-1.25, max value=1.25]\n",
            "    run.ey.component=E2\n",
            "    run.ey.dipole_length=99.1\n",
            "    run.ey.ac.end=2.5\n",
            "    run.ey.dc.end=0.0120163\n",
            "    run.ey.contact_resistance.start=2199.7\n",
            "    run.ey.contact_resistance.end=2230.26\n",
            "    run.ey.comments=[saturation=0.0379904%, min value=-1.25, max value=1.25]\n",
            "    run.ey.id=10526_2023-05-19-170246\n",
            "    run.ey.data_logger.model=MTU-5C\n",
            "    run.ey.geographic_name=701 Walden South\n",
            "    run.ey.acquired_by.author\n",
            "    run.ey.measurement_azimuth=0\n",
            "    run.hx.component=H1\n",
            "    run.hx.sensor.model=MTC-155\n",
            "    run.hx.ac.end=0.00976562\n",
            "    run.hx.dc.end=-0.0160217\n",
            "    run.hx.comments=[cal name=57507_646504D8.scal, saturation=0.000280165 %, min value=-0.00488281, max value=0.00488281]\n",
            "    run.hx.sensor.id=57507\n",
            "    run.hy.component=H2\n",
            "    run.hy.sensor.model=MTC-155\n",
            "    run.hy.ac.end=0.00913765\n",
            "    run.hy.dc.end=-0.00793457\n",
            "    run.hy.comments=[cal name=57513_646504D8.scal, saturation=5.60331e-5 %, min value=-0.00488281, max value=0.00425484]\n",
            "    run.hy.sensor.id=57513\n",
            "    run.hz.component=H3\n",
            "    run.hz.sensor.model=MTC-185\n",
            "    run.hz.ac.end=0.000317973\n",
            "    run.hz.dc.end=-0.0448608\n",
            "    run.hz.comments=[cal name=53408_646504D8.scal, saturation=0 %, min value=-0.000170265, max value=0.000147708]\n",
            "    run.hz.sensor.id=53408\n",
            "    transfer_function.remote_references.hz.id=10647_2023-05-18-202538\n",
            "    transfer_function.remote_references.hz.data_logger.model=MTU-5C\n",
            "    transfer_function.remote_references.hz.geographic_name=706 Red Canyon\n",
            "    transfer_function.remote_references.hz.acquired_by.author\n",
            "    transfer_function.remote_references.hz.measurement_azimuth=0\n",
            "    transfer_function.remote_references.rrhx.component=H1\n",
            "    transfer_function.remote_references.rrhx.sensor.model=MTC-155\n",
            "    transfer_function.remote_references.rrhx.ac.end=0.00976562\n",
            "    transfer_function.remote_references.rrhx.dc.end=0.0205994\n",
            "    transfer_function.remote_references.rrhx.comments=[cal name=57454_6466657B.scal, saturation=0.00229736 %, min value=-0.00488281, max value=0.00488281]\n",
            "    transfer_function.remote_references.rrhx.sensor.id=57454\n",
            "    transfer_function.remote_references.rrhy.component=H2\n",
            "    transfer_function.remote_references.rrhy.sensor.model=MTC-155\n",
            "    transfer_function.remote_references.rrhy.ac.end=0.00976562\n",
            "    transfer_function.remote_references.rrhy.dc.end=0.00549316\n",
            "    transfer_function.remote_references.rrhy.comments=[cal name=57458_6466657B.scal, saturation=0.00207322 %, min value=-0.00488281, max value=0.00488281]\n",
            "    transfer_function.remote_references.rrhy.sensor.id=57458\n",
        ]

        self.assertListEqual(info_list, self.edi_obj.Info.write_info())

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
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
            ch, self.edi_obj.Measurement.measurements["ex"].to_dict(single=True)
        )

    def test_measurement_ey(self):
        ch = OrderedDict(
            [
                ("acqchan", ""),
                ("azm", 90.0),
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
                ("x", 8.5),
                ("y", 8.5),
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
                ("x", -8.5),
                ("y", 8.5),
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
                ("x", 21.2),
                ("y", -21.2),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.measurements["hz"].to_dict(single=True)
        )

    def test_measurement(self):
        m_list = [
            "\n>=DEFINEMEAS\n",
            "    MAXCHAN=7\n",
            "    MAXRUN=999\n",
            "    MAXMEAS=9999\n",
            "    REFLAT=40:38:53.200000\n",
            "    REFLON=-106:12:44.700000\n",
            "    REFELEV=2489.0\n",
            "    REFTYPE=CART\n",
            "    UNITS=meter\n",
            "\n",
            ">HMEAS ID=1001.001 CHTYPE=HX X=8.50 Y=8.50 Z=0.00 AZM=0.00 DIP=0.00 ACQCHAN=\n",
            ">HMEAS ID=1002.001 CHTYPE=HY X=-8.50 Y=8.50 Z=0.00 AZM=90.00 DIP=0.00 ACQCHAN=\n",
            ">HMEAS ID=1003.001 CHTYPE=HZ X=21.20 Y=-21.20 Z=0.00 AZM=0.00 DIP=0.00 ACQCHAN=\n",
            ">EMEAS ID=1004.001 CHTYPE=EX X=0.00 Y=-48.80 Z=0.00 X2=0.00 Y2=46.50 Z2=0.00 AZM=90.00 ACQCHAN=\n",
            ">EMEAS ID=1005.001 CHTYPE=EY X=-50.60 Y=0.00 Z=0.00 X2=48.50 Y2=0.00 Z2=0.00 AZM=90.00 ACQCHAN=\n",
        ]

        self.assertListEqual(m_list, self.edi_obj.Measurement.write_measurement())

        with self.subTest("reflat"):
            self.assertAlmostEqual(
                40.64811111111111, self.edi_obj.Measurement.reflat, 5
            )

        with self.subTest("reflon"):
            self.assertAlmostEqual(
                -106.21241666666667, self.edi_obj.Measurement.reflon, 5
            )

        with self.subTest("refelev"):
            self.assertAlmostEqual(2489.0, self.edi_obj.Measurement.refelev, 2)

    def test_data_section(self):
        d_list = [
            "\n>=MTSECT\n",
            "    NFREQ=98\n",
            "    SECTID=701_merged_wrcal\n",
            "    NCHAN=0\n",
            "    MAXBLOCKS=999\n",
            "    HX=1001.001\n",
            "    HY=1002.001\n",
            "    HZ=1003.001\n",
            "    EX=1004.001\n",
            "    EY=1005.001\n",
            "\n",
        ]

        self.assertListEqual(d_list, self.edi_obj.Data.write_data())

    def test_impedance(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.z.shape, (98, 2, 2))

        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.z_err.shape, (98, 2, 2))

        with self.subTest("first element"):
            self.assertAlmostEqual(self.edi_obj.z[0, 0, 0], (19.91471 + 63.25052j))

        with self.subTest("last element"):
            self.assertAlmostEqual(
                self.edi_obj.z[-1, 1, 1], (-0.005189691 - 0.0085249j)
            )
        with self.subTest("first element error"):
            self.assertAlmostEqual(self.edi_obj.z_err[0, 0, 0], 1.1270665463937788)

        with self.subTest("last element error"):
            self.assertAlmostEqual(self.edi_obj.z_err[-1, 1, 1], 0.00031013205251956787)

    def test_tipper(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.t.shape, (98, 1, 2))
        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.t_err.shape, (98, 1, 2))

        with self.subTest("first element"):
            self.assertAlmostEqual(self.edi_obj.t[0, 0, 0], (0.01175011 - 0.006787284j))

        with self.subTest("last element"):
            self.assertAlmostEqual(self.edi_obj.t[-1, 0, 1], (0.2252638 + 0.1047829j))
        with self.subTest("first element error"):
            self.assertAlmostEqual(self.edi_obj.t_err[0, 0, 0], 0.0006966629744718747)

        with self.subTest("last element error"):
            self.assertAlmostEqual(self.edi_obj.t_err[-1, 0, 1], 0.01090868461364614)

    def test_rotation_angle(self):
        with self.subTest("all zeros"):
            self.assertTrue((self.edi_obj.rotation_angle == 0).all())

        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.rotation_angle.shape, (98,))


class TestEMpowerTF(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tf_obj = TF(TF_EDI_EMPOWER)
        cls.tf_obj.read()

        cls.edi_obj = cls.tf_obj.to_edi()
        cls.maxDiff = None

    def test_header(self):
        head = OrderedDict(
            [
                ("acqdate", "1980-01-01T00:00:00+00:00"),
                ("coordinate_system", "geographic"),
                ("dataid", "701_merged_wrcal"),
                ("datum", "WGS 84"),
                ("elevation", 2489.0),
                ("empty", 1e32),
                ("fileby", "EMTF FCU"),
                ("latitude", 40.64811111111111),
                ("longitude", -106.21241666666667),
                ("stdvers", "SEG 1.0"),
                ("units", "milliVolt per kilometer per nanoTesla"),
            ]
        )

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("Declination Model"):
            self.assertEqual(self.edi_obj.Header.declination.model, "IGRF")
        with self.subTest("Declination value"):
            self.assertEqual(self.edi_obj.Header.declination.value, 0.0)

    def test_info(self):
        info_list = {
            "survey.datum": "WGS 84",
            "survey.id": "0",
            "survey.release_license": "CC-BY-4.0",
            "transfer_function.coordinate_system": "geographic",
            "transfer_function.id": "701_merged_wrcal",
            "transfer_function.processed_date": "2023-05-30T00:00:00+00:00",
            "transfer_function.remote_references": ["706 Red Canyon"],
            "transfer_function.runs_processed": ["701_merged_wrcala"],
            "transfer_function.sign_convention": "+",
            "transfer_function.software.name": "EMpower v2.9.0.7",
            "transfer_function.units": "milliVolt per kilometer per nanoTesla",
            "provenance.creation_time": "2023-05-30T00:00:00+00:00",
            "provenance.software.name": "EMTF FCU",
            "provenance.software.version": "4.0",
            "provenance.submitter.author": "EMTF FCU",
            "701_merged_wrcala.channels_recorded_auxiliary": [],
            "701_merged_wrcala.channels_recorded_electric": ["e1", "e2", "ex", "ey"],
            "701_merged_wrcala.channels_recorded_magnetic": ["hx", "hy", "hz"],
            "701_merged_wrcala.data_logger.model": "MTU-5C",
            "701_merged_wrcala.data_logger.power_source.voltage.end": 0.0,
            "701_merged_wrcala.data_logger.power_source.voltage.start": 0.0,
            "701_merged_wrcala.data_logger.timing_system.drift": 0.0,
            "701_merged_wrcala.data_logger.timing_system.type": "GPS",
            "701_merged_wrcala.data_logger.timing_system.uncertainty": 0.0,
            "701_merged_wrcala.data_type": "BBMT",
            "701_merged_wrcala.id": "701_merged_wrcala",
            "701_merged_wrcala.sample_rate": 0.0,
            "701_merged_wrcala.hx.channel_id": "1001.001",
            "701_merged_wrcala.hx.channel_number": 0,
            "701_merged_wrcala.hx.component": "hx",
            "701_merged_wrcala.hx.h_field_max.end": 0.0,
            "701_merged_wrcala.hx.h_field_max.start": 0.0,
            "701_merged_wrcala.hx.h_field_min.end": 0.0,
            "701_merged_wrcala.hx.h_field_min.start": 0.0,
            "701_merged_wrcala.hx.location.datum": "WGS 84",
            "701_merged_wrcala.hx.measurement_azimuth": 0.0,
            "701_merged_wrcala.hx.measurement_tilt": 0.0,
            "701_merged_wrcala.hx.sensor.model": "MTC-155",
            "701_merged_wrcala.hx.sensor.type": "magnetic",
            "701_merged_wrcala.hx.type": "magnetic",
            "701_merged_wrcala.hy.channel_id": "1002.001",
            "701_merged_wrcala.hy.channel_number": 0,
            "701_merged_wrcala.hy.component": "hy",
            "701_merged_wrcala.hy.h_field_max.end": 0.0,
            "701_merged_wrcala.hy.h_field_max.start": 0.0,
            "701_merged_wrcala.hy.h_field_min.end": 0.0,
            "701_merged_wrcala.hy.h_field_min.start": 0.0,
            "701_merged_wrcala.hy.location.datum": "WGS 84",
            "701_merged_wrcala.hy.measurement_azimuth": 90.0,
            "701_merged_wrcala.hy.measurement_tilt": 0.0,
            "701_merged_wrcala.hy.sensor.model": "MTC-155",
            "701_merged_wrcala.hy.sensor.type": "magnetic",
            "701_merged_wrcala.hy.translated_azimuth": 90.0,
            "701_merged_wrcala.hy.type": "magnetic",
            "701_merged_wrcala.hz.channel_id": "1003.001",
            "701_merged_wrcala.hz.channel_number": 0,
            "701_merged_wrcala.hz.component": "hz",
            "701_merged_wrcala.hz.h_field_max.end": 0.0,
            "701_merged_wrcala.hz.h_field_max.start": 0.0,
            "701_merged_wrcala.hz.h_field_min.end": 0.0,
            "701_merged_wrcala.hz.h_field_min.start": 0.0,
            "701_merged_wrcala.hz.location.datum": "WGS 84",
            "701_merged_wrcala.hz.measurement_azimuth": 0.0,
            "701_merged_wrcala.hz.measurement_tilt": 0.0,
            "701_merged_wrcala.hz.sensor.model": "MTC-185",
            "701_merged_wrcala.hz.sensor.type": "magnetic",
            "701_merged_wrcala.hz.type": "magnetic",
            "701_merged_wrcala.ex.ac.end": 0.0,
            "701_merged_wrcala.ex.ac.start": 0.0,
            "701_merged_wrcala.ex.channel_number": 0,
            "701_merged_wrcala.ex.component": "ex",
            "701_merged_wrcala.ex.contact_resistance.end": 0.0,
            "701_merged_wrcala.ex.contact_resistance.start": 0.0,
            "701_merged_wrcala.ex.dc.end": 0.0,
            "701_merged_wrcala.ex.dc.start": 0.0,
            "701_merged_wrcala.ex.dipole_length": 0.0,
            "701_merged_wrcala.ex.measurement_azimuth": 0.0,
            "701_merged_wrcala.ex.measurement_tilt": 0.0,
            "701_merged_wrcala.ex.negative.datum": "WGS 84",
            "701_merged_wrcala.ex.positive.datum": "WGS 84",
            "701_merged_wrcala.ex.type": "electric",
            "701_merged_wrcala.ey.ac.end": 0.0,
            "701_merged_wrcala.ey.ac.start": 0.0,
            "701_merged_wrcala.ey.channel_number": 0,
            "701_merged_wrcala.ey.component": "ey",
            "701_merged_wrcala.ey.contact_resistance.end": 0.0,
            "701_merged_wrcala.ey.contact_resistance.start": 0.0,
            "701_merged_wrcala.ey.dc.end": 0.0,
            "701_merged_wrcala.ey.dc.start": 0.0,
            "701_merged_wrcala.ey.dipole_length": 0.0,
            "701_merged_wrcala.ey.measurement_azimuth": 0.0,
            "701_merged_wrcala.ey.measurement_tilt": 0.0,
            "701_merged_wrcala.ey.negative.datum": "WGS 84",
            "701_merged_wrcala.ey.positive.datum": "WGS 84",
            "701_merged_wrcala.ey.type": "electric",
            "701_merged_wrcala.e1.ac.end": 2.5,
            "701_merged_wrcala.e1.ac.start": 0.0,
            "701_merged_wrcala.e1.channel_id": "1004.001",
            "701_merged_wrcala.e1.channel_number": 0,
            "701_merged_wrcala.e1.comments": "saturation=0.0870754%,min value=-1.25,max value=1.25",
            "701_merged_wrcala.e1.component": "e1",
            "701_merged_wrcala.e1.contact_resistance.end": 4222.68,
            "701_merged_wrcala.e1.contact_resistance.start": 1558.69,
            "701_merged_wrcala.e1.dc.end": 0.0537872,
            "701_merged_wrcala.e1.dc.start": 0.0,
            "701_merged_wrcala.e1.dipole_length": 95.3,
            "701_merged_wrcala.e1.measurement_azimuth": 90.0,
            "701_merged_wrcala.e1.measurement_tilt": 0.0,
            "701_merged_wrcala.e1.negative.datum": "WGS 84",
            "701_merged_wrcala.e1.negative.type": "electric",
            "701_merged_wrcala.e1.positive.datum": "WGS 84",
            "701_merged_wrcala.e1.positive.type": "electric",
            "701_merged_wrcala.e1.translated_azimuth": 90.0,
            "701_merged_wrcala.e1.type": "electric",
            "701_merged_wrcala.e2.ac.end": 2.5,
            "701_merged_wrcala.e2.ac.start": 0.0,
            "701_merged_wrcala.e2.channel_id": "1005.001",
            "701_merged_wrcala.e2.channel_number": 0,
            "701_merged_wrcala.e2.comments": "saturation=0.0379904%,min value=-1.25,max value=1.25",
            "701_merged_wrcala.e2.component": "e2",
            "701_merged_wrcala.e2.contact_resistance.end": 2230.26,
            "701_merged_wrcala.e2.contact_resistance.start": 2199.7,
            "701_merged_wrcala.e2.dc.end": 0.0120163,
            "701_merged_wrcala.e2.dc.start": 0.0,
            "701_merged_wrcala.e2.dipole_length": 99.1,
            "701_merged_wrcala.e2.measurement_azimuth": 0.0,
            "701_merged_wrcala.e2.measurement_tilt": 0.0,
            "701_merged_wrcala.e2.negative.datum": "WGS 84",
            "701_merged_wrcala.e2.negative.type": "electric",
            "701_merged_wrcala.e2.positive.datum": "WGS 84",
            "701_merged_wrcala.e2.positive.type": "electric",
            "701_merged_wrcala.e2.translated_azimuth": 0.0,
            "701_merged_wrcala.e2.type": "electric",
        }

        self.assertDictEqual(info_list, self.edi_obj.Info.info_dict)

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

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_ex.to_dict(single=True))

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

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_ey.to_dict(single=True))

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

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_hx.to_dict(single=True))

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

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_hy.to_dict(single=True))

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

        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_hz.to_dict(single=True))

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
            self.assertAlmostEqual(self.edi_obj.z[0, 0, 0], (19.91471 + 63.25052j))

        with self.subTest("last element"):
            self.assertAlmostEqual(
                self.edi_obj.z[-1, 1, 1], (-0.005189691 - 0.0085249j)
            )
        with self.subTest("first element error"):
            self.assertAlmostEqual(self.edi_obj.z_err[0, 0, 0], 1.1270665463937788)

        with self.subTest("last element error"):
            self.assertAlmostEqual(self.edi_obj.z_err[-1, 1, 1], 0.00031013205251956787)

    def test_tipper(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.t.shape, (98, 1, 2))
        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.t_err.shape, (98, 1, 2))

        with self.subTest("first element"):
            self.assertAlmostEqual(self.edi_obj.t[0, 0, 0], (0.01175011 - 0.006787284j))

        with self.subTest("last element"):
            self.assertAlmostEqual(self.edi_obj.t[-1, 0, 1], (0.2252638 + 0.1047829j))
        with self.subTest("first element error"):
            self.assertAlmostEqual(self.edi_obj.t_err[0, 0, 0], 0.0006966629744718747)

        with self.subTest("last element error"):
            self.assertAlmostEqual(self.edi_obj.t_err[-1, 0, 1], 0.01090868461364614)

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
