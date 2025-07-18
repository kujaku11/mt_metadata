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

from mt_metadata import TF_EDI_QUANTEC
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io import edi


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture(scope="module")
def quantec_edi_object():
    """Create Quantec EDI object once for all tests in this module."""
    return edi.EDI(fn=TF_EDI_QUANTEC)


@pytest.fixture(scope="module")
def quantec_tf_object():
    """Create Quantec TF object once for all tests in this module."""
    tf_obj = TF(fn=TF_EDI_QUANTEC)
    tf_obj.read()
    return tf_obj


@pytest.fixture(scope="module")
def quantec_tf_to_edi_object(quantec_tf_object):
    """Create EDI object from TF object for testing."""
    return quantec_tf_object.to_edi()


@pytest.fixture(scope="module")
def expected_header():
    """Expected header data for Quantec EDI testing."""
    return {
        "acqby": "Quantec Geoscience",
        "acqdate": "2014-11-15T00:00:00+00:00",
        "coordinate_system": "geographic",
        "country": "Australia",
        "county": "Boulia",
        "dataid": "TEST_01",
        "datum": "WGS84",
        "elevation": 122.0,
        "enddate": "2014-11-15T00:00:00+00:00",
        "fileby": "Quantec Geoscience",
        "filedate": "2014-11-17",
        "latitude": -23.051133333333333,
        "longitude": 139.46753333333334,
        "progdate": "2012-10-10",
        "progname": "mt_metadata",
        "progvers": "MTeditor_v1d",
        "state": "Queensland",
        "stdvers": "1.0",
    }


@pytest.fixture(scope="module")
def expected_measurement_channels():
    """Expected measurement channel data for Quantec EDI testing."""
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
from mt_metadata import TF_EDI_QUANTEC

# =============================================================================
# Quantec
# =============================================================================
class TestQuantecEDI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_QUANTEC)

    def test_header(self):
        head = {
            "acqby": "Quantec Geoscience",
            "acqdate": "2014-11-15T00:00:00+00:00",
            "coordinate_system": "geographic",
            "country": "Australia",
            "county": "Boulia",
            "dataid": "TEST_01",
            "datum": "WGS84",
            "elevation": 122.0,
            "enddate": "2014-11-15T00:00:00+00:00",
            "fileby": "Quantec Geoscience",
            "filedate": "2014-11-17",
            "latitude": -23.051133333333333,
            "longitude": 139.46753333333334,
            "progdate": "2012-10-10",
            "progname": "mt_metadata",
            "progvers": "MTeditor_v1d",
            "state": "Queensland",
            "stdvers": "1.0",
        }

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

    def test_info(self):
        info_list = ["MAXLINES=1000"]

        self.assertListEqual(info_list, self.edi_obj.Info.info_list)

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
>>>>>>> main
                ("azm", 0.0),
                ("chtype", "EX"),
                ("id", 14.001),
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
                ("id", 15.001),
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
                ("id", 11.001),
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
                ("azm", 90.0),
                ("chtype", "HY"),
                ("dip", 0.0),
                ("id", 12.001),
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
                ("id", 13.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
<<<<<<< HEAD
        ),
    }


@pytest.fixture(scope="module")
def expected_measurement_list():
    """Expected measurement list for Quantec EDI testing."""
    return [
        "MAXCHAN=7",
        "MAXRUN=999",
        "MAXMEAS=99999",
        "UNITS=M",
        "REFLAT=-23:03:4.08",
        "REFLONG=139:28:3.12",
        "REFELEV=122",
    ]


@pytest.fixture(scope="module")
def expected_data_section():
    """Expected data section for Quantec EDI testing."""
    return OrderedDict(
        [
            ("ex", "14.001"),
            ("ey", "15.001"),
            ("hx", "11.001"),
            ("hy", "12.001"),
            ("hz", "13.001"),
            ("maxblocks", 999),
            ("nchan", 7),
            ("nfreq", 41),
            ("rrhx", None),
            ("rrhy", None),
            ("sectid", "TEST_01"),
        ]
    )


# =============================================================================
# Test Classes
# =============================================================================
class TestQuantecEDI:
    """Test class for Quantec EDI functionality using pytest."""

    @pytest.mark.parametrize(
        "key,expected_value",
        [
            ("acqby", "Quantec Geoscience"),
            ("acqdate", "2014-11-15T00:00:00+00:00"),
            ("coordinate_system", "geographic"),
            ("country", "Australia"),
            ("county", "Boulia"),
            ("dataid", "TEST_01"),
            ("datum", "WGS 84"),
            ("elevation", 122.0),
            ("enddate", "2014-11-15T00:00:00+00:00"),
            ("fileby", "Quantec Geoscience"),
            ("filedate", "2014-11-17"),
            ("latitude", -23.051133333333333),
            ("longitude", 139.46753333333334),
            ("progdate", "2012-10-10"),
            ("progname", "mt_metadata"),
            ("progvers", "MTeditor_v1d"),
            ("state", "Queensland"),
            ("stdvers", "1.0"),
        ],
    )
    def test_header_attributes(self, quantec_edi_object, key, expected_value):
        """Test header attributes using parametrization."""
        h_value = getattr(quantec_edi_object.Header, key.lower())
        assert h_value == expected_value

    def test_info(self, quantec_edi_object):
        """Test info dictionary."""
        expected_info_dict = {}  # Quantec appears to have no specific info
        assert quantec_edi_object.Info.info_dict == expected_info_dict

    @pytest.mark.parametrize("channel", ["ex", "ey", "hx", "hy", "hz"])
    def test_measurement_channels(
        self, quantec_edi_object, expected_measurement_channels, channel
    ):
        """Test individual measurement channels using parametrization."""
        expected = expected_measurement_channels[channel]
        actual = quantec_edi_object.Measurement.measurements[channel].to_dict(
            single=True
        )
        assert actual == expected

    def test_measurement_no_rrhx(self, quantec_edi_object):
        """Test that rrhx attribute doesn't exist."""
        assert not hasattr(quantec_edi_object.Measurement, "rrhx")

    def test_measurement_no_rrhy(self, quantec_edi_object):
        """Test that rrhy attribute doesn't exist."""
        assert not hasattr(quantec_edi_object.Measurement, "rrhy")

    def test_measurement_output(self, quantec_edi_object):
        """Test measurement write output."""
        actual_output = quantec_edi_object.Measurement.write_measurement()
        # Just check that it returns a list
        assert isinstance(actual_output, list)

    @pytest.mark.parametrize(
        "attr,expected,precision",
        [
            ("reflat", -23.05113, 5),
            ("reflon", 139.46753, 5),
            ("refelev", 122.0, 2),
        ],
    )
    def test_measurement_reference_values(
        self, quantec_edi_object, attr, expected, precision
    ):
        """Test measurement reference values with specified precision."""
        actual = getattr(quantec_edi_object.Measurement, attr)
        assert abs(actual - expected) < 10 ** (-precision)

    def test_data_section(self, quantec_edi_object, expected_data_section):
        """Test data section properties."""
        assert quantec_edi_object.Data.to_dict(single=True) == expected_data_section

    @pytest.mark.parametrize("channel", ["hx", "hy", "hz", "ex", "ey"])
    def test_data_section_channel_ids(
        self, quantec_edi_object, expected_data_section, channel
    ):
        """Test data section channel IDs match expected values."""
        expected_id = expected_data_section[channel]
        actual_id = getattr(quantec_edi_object.Data, channel)
        assert actual_id == expected_id

    def test_data_section_rrhx_rrhy(self, quantec_edi_object):
        """Test that rrhx and rrhy are None for Quantec data."""
        assert quantec_edi_object.Data.rrhx is None
        assert quantec_edi_object.Data.rrhy is None


class TestToTF:
    """Test class for EDI to TF conversion."""

    def test_station_metadata(self, quantec_edi_object, quantec_tf_object):
        """Test station metadata conversion from EDI to TF."""
        edi_st = quantec_edi_object.station_metadata.to_dict(single=True)
        tf_st = quantec_tf_object.station_metadata.to_dict(single=True)

        for edi_key, edi_value in edi_st.items():
            assert (
                edi_value == tf_st[edi_key]
            ), f"Station metadata mismatch for {edi_key}"

    def test_survey_metadata(self, quantec_edi_object, quantec_tf_object):
        """Test survey metadata conversion from EDI to TF."""
        edi_st = quantec_edi_object.survey_metadata.to_dict(single=True)
        tf_st = quantec_tf_object.survey_metadata.to_dict(single=True)

        for edi_key, edi_value in edi_st.items():
            assert (
                edi_value == tf_st[edi_key]
            ), f"Survey metadata mismatch for {edi_key}"

    @pytest.mark.parametrize(
        "method,expected",
        [
            ("has_impedance", True),
            ("has_tipper", True),
            ("has_inverse_signal_power", True),
            ("has_residual_covariance", True),
        ],
    )
    def test_tf_properties(self, quantec_tf_object, method, expected):
        """Test TF object properties using parametrization."""
        result = getattr(quantec_tf_object, method)()
        assert result == expected

    def test_impedance_error_non_zero(self, quantec_tf_object):
        """Test that impedance errors are non-zero."""
        assert (quantec_tf_object.impedance_error.data != 0).all()


class TestFromTF:
    """Test class for TF to EDI conversion."""

    def test_station_metadata(self, quantec_tf_object, quantec_tf_to_edi_object):
        """Test station metadata conversion from TF to EDI."""
        edi_st = quantec_tf_to_edi_object.station_metadata.to_dict(single=True)
        tf_st = quantec_tf_object.station_metadata.to_dict(single=True, required=False)

        for edi_key, edi_value in edi_st.items():
            if edi_key in [
                "comments",
            ]:
                # These fields are expected to be different
                assert (
                    edi_value != tf_st[edi_key]
                ), f"Field {edi_key} should be different"
            else:
                assert (
                    edi_value == tf_st[edi_key]
                ), f"Station metadata mismatch for {edi_key}"

    def test_survey_metadata(self, quantec_tf_object, quantec_tf_to_edi_object):
        """Test survey metadata conversion from TF to EDI."""
        edi_st = quantec_tf_to_edi_object.survey_metadata.to_dict(single=True)
        tf_st = quantec_tf_object.survey_metadata.to_dict(single=True)

        for edi_key, edi_value in edi_st.items():
            assert (
                edi_value == tf_st[edi_key]
            ), f"Survey metadata mismatch for {edi_key}"

    @pytest.mark.parametrize(
        "method,expected",
        [
            ("has_impedance", True),
            ("has_tipper", True),
            ("has_inverse_signal_power", True),
            ("has_residual_covariance", True),
        ],
    )
    def test_tf_properties(self, quantec_tf_object, method, expected):
        """Test TF object properties using parametrization."""
        result = getattr(quantec_tf_object, method)()
        assert result == expected

    def test_impedance_error_non_zero(self, quantec_tf_object):
        """Test that impedance errors are non-zero."""
        assert (quantec_tf_object.impedance_error.data != 0).all()
=======
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hz.to_dict(single=True)
        )

    def test_measurement_rrhx(self):
        self.assertFalse(hasattr(self.edi_obj.Measurement, "rrhx"))

    def test_measurement_rrhy(self):
        self.assertFalse(hasattr(self.edi_obj.Measurement, "rrhy"))

    def test_measurement(self):
        m_list = [
            "MAXCHAN=7",
            "MAXRUN=999",
            "MAXMEAS=99999",
            "UNITS=M",
            "REFLAT=-23:03:4.08",
            "REFLONG=139:28:3.12",
            "REFELEV=122",
        ]

        self.assertListEqual(
            m_list, self.edi_obj.Measurement.measurement_list[0 : len(m_list)]
        )

        with self.subTest("reflat"):
            self.assertAlmostEqual(
                -23.05113, self.edi_obj.Measurement.reflat, 5
            )

        with self.subTest("reflon"):
            self.assertAlmostEqual(
                139.46753, self.edi_obj.Measurement.reflon, 5
            )

        with self.subTest("refelev"):
            self.assertAlmostEqual(122.0, self.edi_obj.Measurement.refelev, 2)

    def test_data_section(self):
        d_list = OrderedDict(
            [
                ("ex", "14.001"),
                ("ey", "15.001"),
                ("hx", "11.001"),
                ("hy", "12.001"),
                ("hz", "13.001"),
                ("maxblocks", 999),
                ("nchan", 7),
                ("nfreq", 41),
                ("rrhx", "0"),
                ("rrhy", "0"),
                ("sectid", "TEST_01"),
            ]
        )

        self.assertDictEqual(d_list, self.edi_obj.Data.to_dict(single=True))

        for ch in ["hx", "hy", "hz", "ex", "ey", "rrhx", "rrhy"]:
            with self.subTest(ch):
                self.assertEqual(d_list[ch], getattr(self.edi_obj.Data, ch))


class TestToTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi = edi.EDI(fn=TF_EDI_QUANTEC)
        self.tf = TF(fn=TF_EDI_QUANTEC)
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
        self.assertTrue((self.tf.impedance_error.data != 0).all())

    def test_has_tipper(self):
        self.assertTrue(self.tf.has_tipper())

    def test_has_isp(self):
        self.assertTrue(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertTrue(self.tf.has_residual_covariance())


class TestFromTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_EDI_QUANTEC)
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
        self.assertTrue((self.tf.impedance_error.data != 0).all())

    def test_has_tipper(self):
        self.assertTrue(self.tf.has_tipper())

    def test_has_isp(self):
        self.assertTrue(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertTrue(self.tf.has_residual_covariance())
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
