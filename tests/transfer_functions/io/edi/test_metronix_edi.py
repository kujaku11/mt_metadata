# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

<<<<<<< HEAD
from collections import OrderedDict

# =============================================================================
# Imports
# =============================================================================
import pytest

from mt_metadata import TF_EDI_METRONIX
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io import edi
from mt_metadata.utils.mttime import MTime


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture(scope="module")
def metronix_edi_object():
    """Create Metronix EDI object once for all tests in this module."""
    return edi.EDI(fn=TF_EDI_METRONIX)


@pytest.fixture(scope="module")
def metronix_tf_object():
    """Create Metronix TF object once for all tests in this module."""
    tf_obj = TF(fn=TF_EDI_METRONIX)
    tf_obj.read()
    return tf_obj


@pytest.fixture(scope="module")
def metronix_tf_to_edi_object(metronix_tf_object):
    """Create EDI object from TF object for testing."""
    return metronix_tf_object.to_edi()


@pytest.fixture(scope="module")
def expected_header():
    """Expected header data for Metronix EDI testing."""
    return {
        "acqby": "Metronix",
        "country": "Germany",
        "dataid": "GEO858",
        "datum": "WGS 84",
        "elevation": 181.0,
        "fileby": "Metronix",
        "filedate": "2014-10-17",
        "latitude": 22.691378333333333,
        "longitude": 139.70504,
        "progdate": "2014-08-14",
        "progname": "mt_metadata",
        "progvers": "Version 14 AUG 2014 SVN 1277 MINGW64",
        "state": "LX",
        "stdvers": "SEG 1.0",
        "units": "milliVolt per kilometer per nanoTesla",
    }


@pytest.fixture(scope="module")
def expected_info():
    """Expected info dictionary for Metronix EDI testing."""
    return {"maxinfo": "1000"}


@pytest.fixture(scope="module")
def expected_measurement_channels():
    """Expected measurement channel data for Metronix EDI testing."""
    return {
        "ex": OrderedDict(
            [
                ("acqchan", ""),
=======
# =============================================================================
#
# =============================================================================
import unittest

from collections import OrderedDict
from mt_metadata.transfer_functions.io import edi
from mt_metadata.transfer_functions import TF
from mt_metadata.utils.mttime import MTime
from mt_metadata import TF_EDI_METRONIX

# =============================================================================
# Metronix
# =============================================================================
class TestMetronixEDI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_METRONIX)
        self.maxDiff = None

    def test_header(self):
        head = {
            "acqby": "Metronix",
            "country": "Germany",
            "dataid": "GEO858",
            "datum": "WGS84",
            "elevation": 181.0,
            "fileby": "Metronix",
            "filedate": "2014-10-17",
            "latitude": 22.691378333333333,
            "longitude": 139.70504,
            "progdate": "2014-08-14",
            "progname": "mt_metadata",
            "progvers": "Version 14 AUG 2014 SVN 1277 MINGW64",
            "state": "LX",
            "stdvers": "SEG 1.0",
            "units": "millivolts_per_kilometer_per_nanotesla",
        }

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("acquire date"):
            self.assertEqual(
                self.edi_obj.Header._acqdate, MTime("08/17/14 04:58")
            )

        with self.subTest("end date"):
            self.assertEqual(
                self.edi_obj.Header._enddate, MTime("08/17/14 20:03")
            )

    def test_info(self):
        info_list = []

        self.assertListEqual(info_list, self.edi_obj.Info.info_list)

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
>>>>>>> main
                ("azm", 0.0),
                ("chtype", "EX"),
                ("id", 1000.0001),
                ("x", -50.0),
                ("x2", 50.0),
                ("y", 0.0),
                ("y2", 0.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
<<<<<<< HEAD
        ),
        "ey": OrderedDict(
            [
                ("acqchan", ""),
=======
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_ex.to_dict(single=True)
        )

    def test_measurement_ey(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
>>>>>>> main
                ("azm", 90.0),
                ("chtype", "EY"),
                ("id", 1001.0001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", -50.0),
                ("y2", 50.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
<<<<<<< HEAD
        ),
        "hx": OrderedDict(
            [
                ("acqchan", ""),
=======
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_ey.to_dict(single=True)
        )

    def test_measurement_hx(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
>>>>>>> main
                ("azm", 0.0),
                ("chtype", "HX"),
                ("dip", 0.0),
                ("id", 1002.0001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
<<<<<<< HEAD
        ),
        "hy": OrderedDict(
            [
                ("acqchan", ""),
=======
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hx.to_dict(single=True)
        )

    def test_measurement_hy(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
>>>>>>> main
                ("azm", 0.0),
                ("chtype", "HY"),
                ("dip", 0.0),
                ("id", 1003.0001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
<<<<<<< HEAD
        ),
        "hz": OrderedDict(
            [
                ("acqchan", ""),
=======
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hy.to_dict(single=True)
        )

    def test_measurement_hz(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
>>>>>>> main
                ("azm", 0.0),
                ("chtype", "HZ"),
                ("dip", 0.0),
                ("id", 1004.0001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
<<<<<<< HEAD
        ),
    }


@pytest.fixture(scope="module")
def expected_measurement_output():
    """Expected measurement output for Metronix EDI testing."""
    return [
        "\n>=DEFINEMEAS\n",
        "    MAXCHAN=9\n",
        "    MAXRUN=999\n",
        "    MAXMEAS=1000\n",
        "    REFLOC=Braunschweig\n",
        "    REFLAT=22:41:28.962000\n",
        "    REFLON=139:42:18.144000\n",
        "    REFELEV=181.0\n",
        "    REFTYPE=CART\n",
        "    UNITS=m\n",
        "\n",
        ">EMEAS ID=1000.0001 CHTYPE=EX X=-50.00 Y=0.00 Z=0.00 X2=50.00 Y2=0.00 Z2=0.00 AZM=0.00 ACQCHAN=\n",
        ">EMEAS ID=1001.0001 CHTYPE=EY X=0.00 Y=-50.00 Z=0.00 X2=0.00 Y2=50.00 Z2=0.00 AZM=90.00 ACQCHAN=\n",
        ">HMEAS ID=1002.0001 CHTYPE=HX X=0.00 Y=0.00 Z=0.00 AZM=0.00 DIP=0.00 ACQCHAN=\n",
        ">HMEAS ID=1003.0001 CHTYPE=HY X=0.00 Y=0.00 Z=0.00 AZM=0.00 DIP=0.00 ACQCHAN=\n",
        ">HMEAS ID=1004.0001 CHTYPE=HZ X=0.00 Y=0.00 Z=0.00 AZM=0.00 DIP=0.00 ACQCHAN=\n",
    ]


@pytest.fixture(scope="module")
def expected_data_section_output():
    """Expected data section output for Metronix EDI testing."""
    return [
        "\n>=MTSECT\n",
        "    NFREQ=73\n",
        "    SECTID=GEO858\n",
        "    NCHAN=0\n",
        "    MAXBLOCKS=999\n",
        "    EX=1000.0001\n",
        "    EY=1001.0001\n",
        "    HX=1002.0001\n",
        "    HY=1003.0001\n",
        "    HZ=1004.0001\n",
        "\n",
    ]


# =============================================================================
# Test Classes
# =============================================================================
class TestMetronixEDI:
    """Test class for Metronix EDI functionality using pytest."""

    @pytest.mark.parametrize(
        "key,expected_value",
        [
            ("acqby", "Metronix"),
            ("country", "Germany"),
            ("dataid", "GEO858"),
            ("datum", "WGS 84"),
            ("elevation", 181.0),
            ("fileby", "Metronix"),
            ("filedate", "2014-10-17"),
            ("latitude", 22.691378333333333),
            ("longitude", 139.70504),
            ("progdate", "2014-08-14"),
            ("progname", "mt_metadata"),
            ("progvers", "Version 14 AUG 2014 SVN 1277 MINGW64"),
            ("state", "LX"),
            ("stdvers", "SEG 1.0"),
            ("units", "milliVolt per kilometer per nanoTesla"),
        ],
    )
    def test_header_attributes(self, metronix_edi_object, key, expected_value):
        """Test header attributes using parametrization."""
        h_value = getattr(metronix_edi_object.Header, key.lower())
        assert h_value == expected_value

    def test_header_dates(self, metronix_edi_object):
        """Test header date attributes."""
        assert metronix_edi_object.Header.acqdate == MTime(time_stamp="08/17/14 04:58")
        assert metronix_edi_object.Header.enddate == MTime(time_stamp="08/17/14 20:03")

    def test_info(self, metronix_edi_object, expected_info):
        """Test info dictionary."""
        assert metronix_edi_object.Info.info_dict == expected_info

    @pytest.mark.parametrize("channel", ["ex", "ey", "hx", "hy", "hz"])
    def test_measurement_channels(
        self, metronix_edi_object, expected_measurement_channels, channel
    ):
        """Test individual measurement channels using parametrization."""
        expected = expected_measurement_channels[channel]
        actual = metronix_edi_object.Measurement.measurements[channel].to_dict(
            single=True
        )
        assert actual == expected

    def test_measurement_output(self, metronix_edi_object, expected_measurement_output):
        """Test measurement write output."""
        actual_output = metronix_edi_object.Measurement.write_measurement()
        assert actual_output == expected_measurement_output

    @pytest.mark.parametrize(
        "attr,expected,precision",
        [
            ("reflat", 22.6913783, 5),
            ("reflon", 139.70504, 5),
            ("refelev", 181.0, 2),
        ],
    )
    def test_measurement_reference_values(
        self, metronix_edi_object, attr, expected, precision
    ):
        """Test measurement reference values with specified precision."""
        actual = getattr(metronix_edi_object.Measurement, attr)
        assert abs(actual - expected) < 10 ** (-precision)

    def test_data_section_output(
        self, metronix_edi_object, expected_data_section_output
    ):
        """Test data section write output."""
        actual_output = metronix_edi_object.Data.write_data()
        assert actual_output == expected_data_section_output

    @pytest.mark.parametrize(
        "channel,expected_id",
        [
            ("ex", "1000.0001"),
            ("ey", "1001.0001"),
            ("hx", "1002.0001"),
            ("hy", "1003.0001"),
            ("hz", "1004.0001"),
        ],
    )
    def test_data_section_channel_ids(self, metronix_edi_object, channel, expected_id):
        """Test data section channel IDs."""
        actual_id = getattr(metronix_edi_object.Data, channel)
        assert actual_id == expected_id


class TestToTF:
    """Test class for EDI to TF conversion."""

    def test_station_metadata(self, metronix_edi_object, metronix_tf_object):
        """Test station metadata conversion from EDI to TF."""
        edi_st = metronix_edi_object.station_metadata.to_dict(single=True)
        tf_st = metronix_tf_object.station_metadata.to_dict(single=True)

        for edi_key, edi_value in edi_st.items():
            assert (
                edi_value == tf_st[edi_key]
            ), f"Station metadata mismatch for {edi_key}"

    def test_survey_metadata(self, metronix_edi_object, metronix_tf_object):
        """Test survey metadata conversion from EDI to TF."""
        edi_st = metronix_edi_object.survey_metadata.to_dict(single=True)
        tf_st = metronix_tf_object.survey_metadata.to_dict(single=True)

        for edi_key, edi_value in edi_st.items():
            assert (
                edi_value == tf_st[edi_key]
            ), f"Survey metadata mismatch for {edi_key}"

    @pytest.mark.parametrize(
        "method,expected",
        [
            ("has_impedance", True),
            ("has_tipper", True),
            ("has_inverse_signal_power", False),
            ("has_residual_covariance", False),
        ],
    )
    def test_tf_properties(self, metronix_tf_object, method, expected):
        """Test TF object properties using parametrization."""
        result = getattr(metronix_tf_object, method)()
        assert result == expected


class TestFromTF:
    """Test class for TF to EDI conversion."""

    def test_station_metadata(self, metronix_tf_object, metronix_tf_to_edi_object):
        """Test station metadata conversion from TF to EDI."""
        edi_st = metronix_tf_to_edi_object.station_metadata.to_dict(single=True)
        tf_st = metronix_tf_object.station_metadata.to_dict(single=True, required=False)

        for edi_key, edi_value in edi_st.items():
            if edi_key in ["comments"]:
                # Comments are expected to be different
                assert (
                    edi_value != tf_st[edi_key]
                ), f"Comments should be different for {edi_key}"
            else:
                assert (
                    edi_value == tf_st[edi_key]
                ), f"Station metadata mismatch for {edi_key}"

    def test_survey_metadata(self, metronix_tf_object, metronix_tf_to_edi_object):
        """Test survey metadata conversion from TF to EDI."""
        edi_st = metronix_tf_to_edi_object.survey_metadata.to_dict(single=True)
        tf_st = metronix_tf_object.survey_metadata.to_dict(single=True)

        for edi_key, edi_value in edi_st.items():
            assert (
                edi_value == tf_st[edi_key]
            ), f"Survey metadata mismatch for {edi_key}"

    @pytest.mark.parametrize(
        "method,expected",
        [
            ("has_impedance", True),
            ("has_tipper", True),
            ("has_inverse_signal_power", False),
            ("has_residual_covariance", False),
        ],
    )
    def test_tf_properties(self, metronix_tf_object, method, expected):
        """Test TF object properties using parametrization."""
        result = getattr(metronix_tf_object, method)()
        assert result == expected
=======
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hz.to_dict(single=True)
        )

    def test_measurement(self):
        m_list = [
            "MAXCHAN=9",
            "MAXRUN=999",
            "MAXMEAS=1000",
            "REFTYPE=CART",
            "REFLOC=Braunschweig",
            "REFLAT=22:41:28.962",
            "REFLONG=139:42:18.144",
            "REFELEV=181",
        ]

        self.assertListEqual(
            m_list, self.edi_obj.Measurement.measurement_list[0 : len(m_list)]
        )

        with self.subTest("reflat"):
            self.assertAlmostEqual(
                22.6913783, self.edi_obj.Measurement.reflat, 5
            )

        with self.subTest("reflon"):
            self.assertAlmostEqual(
                139.70504, self.edi_obj.Measurement.reflon, 5
            )

        with self.subTest("reflong"):
            self.assertAlmostEqual(
                139.70504, self.edi_obj.Measurement.reflong, 5
            )

        with self.subTest("refelev"):
            self.assertAlmostEqual(181.0, self.edi_obj.Measurement.refelev, 2)

    def test_data_section(self):
        d_list = [
            "SECTID=GEO858",
            "NFREQ=73",
            "EX=1000.0001",
            "EY=1001.0001",
            "HX=1002.0001",
            "HY=1003.0001",
            "HZ=1004.0001",
        ]

        self.assertListEqual(d_list, self.edi_obj.Data.data_list)

        for ii, ch in enumerate(["ex", "ey", "hx", "hy", "hz"], 2):
            with self.subTest(ch):
                self.assertEqual(
                    d_list[ii].split("=")[1], getattr(self.edi_obj.Data, ch)
                )


class TestToTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi = edi.EDI(fn=TF_EDI_METRONIX)
        self.tf = TF(fn=TF_EDI_METRONIX)
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

    def test_has_tipper(self):
        self.assertTrue(self.tf.has_tipper())

    def test_has_isp(self):
        self.assertFalse(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertFalse(self.tf.has_residual_covariance())


class TestFromTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_EDI_METRONIX)
        self.tf.read()

        self.edi = self.tf.to_edi()
        self.maxDiff = None

    def test_station_metadata(self):
        edi_st = self.edi.station_metadata.to_dict(single=True)
        tf_st = self.tf.station_metadata.to_dict(single=True, required=False)
        for edi_key, edi_value in edi_st.items():
            if edi_key in ["comments", "transfer_function.remote_references"]:
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

    def test_has_tipper(self):
        self.assertTrue(self.tf.has_tipper())

    def test_has_isp(self):
        self.assertFalse(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertFalse(self.tf.has_residual_covariance())
>>>>>>> main


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
<<<<<<< HEAD
    pytest.main([__file__])
=======
    unittest.main()
>>>>>>> main
