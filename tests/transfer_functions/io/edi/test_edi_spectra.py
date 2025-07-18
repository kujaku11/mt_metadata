# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

<<<<<<< HEAD
from collections import OrderedDict

import numpy as np

# =============================================================================
#
# =============================================================================
import pytest

from mt_metadata import TF_EDI_SPECTRA, TF_EDI_SPECTRA_OUT
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io.edi import EDI
from mt_metadata.utils.mttime import MTime


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture(scope="module")
def edi_spectra():
    """Fixture to create EDI spectra object once per module."""
    return EDI(fn=TF_EDI_SPECTRA)


@pytest.fixture(scope="module")
def edi_z():
    """Fixture to create EDI Z object once per module."""
    return EDI(fn=TF_EDI_SPECTRA_OUT)


@pytest.fixture(scope="module")
def tf_spectra():
    """Fixture to create TF spectra object once per module."""
    tf = TF(fn=TF_EDI_SPECTRA)
    tf.read()
    return tf


@pytest.fixture(scope="module")
def tf_to_edi(tf_spectra):
    """Fixture to create EDI from TF object once per module."""
    return tf_spectra.to_edi()


# =============================================================================
# Spectra EDI Tests
# =============================================================================
class TestSpectraEDI:
    """Test Spectra EDI file parsing."""

    def test_header(self, edi_spectra):
        """Test header values."""
=======
# =============================================================================
#
# =============================================================================
import unittest
import numpy as np

from collections import OrderedDict
from mt_metadata.transfer_functions.io.edi import EDI
from mt_metadata.utils.mttime import MTime
from mt_metadata import TF_EDI_SPECTRA, TF_EDI_SPECTRA_OUT
from mt_metadata.transfer_functions import TF


# =============================================================================
# CGG
# =============================================================================
class TestSpectraEDI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi_spectra = EDI(fn=TF_EDI_SPECTRA)
        self.edi_z = EDI(fn=TF_EDI_SPECTRA_OUT)
        self.maxDiff = None

    def test_header(self):
>>>>>>> main
        head = {
            "ACQBY": "Quantec Consulting",
            "COORDINATE_SYSTEM": "geographic",
            "DATAID": "SAGE_2005_og",
<<<<<<< HEAD
            "DATUM": "WGS 84",
=======
            "DATUM": "WGS84",
>>>>>>> main
            "ELEV": 0,
            "EMPTY": 1e32,
            "FILEBY": "Quantec Consulting",
            "LAT": 35.55,
            "LON": -106.28333333333333,
        }

        for key, value in head.items():
<<<<<<< HEAD
            if key == "LAT":
                key = "LATITUDE"
            elif key == "LON":
                key = "LONGITUDE"
            elif key == "ELEV":
                key = "ELEVATION"
            h_value = getattr(edi_spectra.Header, key.lower())
            assert (
                h_value == value
            ), f"Header {key} mismatch: expected {value}, got {h_value}"

    def test_header_acquire_date(self, edi_spectra):
        """Test acquire date."""
        assert edi_spectra.Header.acqdate == MTime(time_stamp="2004-07-03")

    def test_header_units(self, edi_spectra):
        """Test units."""
        assert edi_spectra.Header.units != "millivolt per kilometer per nanotesla"

    def test_info(self, edi_spectra):
        """Test info section."""
        info_list = [">INFO\n"]
        assert info_list == edi_spectra.Info.write_info()

    @pytest.mark.parametrize(
        "channel,expected",
        [
            (
                "ex",
                OrderedDict(
                    [
                        ("acqchan", ""),
                        ("azm", 106.97549946792975),
                        ("chtype", "EX"),
                        ("id", 14.001),
                        ("x", 4872.0),
                        ("x2", 4843.0),
                        ("y", -3577.0),
                        ("y2", -3482.0),
                        ("z", 0.0),
                        ("z2", 0.0),
                    ]
                ),
            ),
            (
                "ey",
                OrderedDict(
                    [
                        ("acqchan", ""),
                        ("azm", -163.19130837379313),
                        ("chtype", "EY"),
                        ("id", 15.001),
                        ("x", 4906.0),
                        ("x2", 4810.0),
                        ("y", -3515.0),
                        ("y2", -3544.0),
                        ("z", 0.0),
                        ("z2", 0.0),
                    ]
                ),
            ),
            (
                "hx",
                OrderedDict(
                    [
                        ("acqchan", ""),
                        ("azm", 107.0),
                        ("chtype", "HX"),
                        ("dip", 0.0),
                        ("id", 11.001),
                        ("x", 4858.0),
                        ("y", -3530.0),
                        ("z", 0.0),
                    ]
                ),
            ),
            (
                "hy",
                OrderedDict(
                    [
                        ("acqchan", ""),
                        ("azm", -163.0),
                        ("chtype", "HY"),
                        ("dip", 0.0),
                        ("id", 12.001),
                        ("x", 4858.0),
                        ("y", -3530.0),
                        ("z", 0.0),
                    ]
                ),
            ),
            (
                "hz",
                OrderedDict(
                    [
                        ("acqchan", ""),
                        ("azm", 0.0),
                        ("chtype", "HZ"),
                        ("dip", 0.0),
                        ("id", 13.001),
                        ("x", 4858.0),
                        ("y", -3530.0),
                        ("z", 0.0),
                    ]
                ),
            ),
        ],
    )
    def test_measurement_channels(self, edi_spectra, channel, expected):
        """Test measurement channels using parametrize for efficiency."""
        assert expected == edi_spectra.Measurement.measurements[channel].to_dict(
            single=True
        )

    @pytest.mark.parametrize(
        "channel,edi_obj",
        [
            ("rrhx", "edi_spectra"),
            ("rrhx", "edi_z"),
            ("rrhy", "edi_spectra"),
            ("rrhy", "edi_z"),
        ],
    )
    def test_measurement_missing_channels(self, request, channel, edi_obj):
        """Test that certain channels are not present."""
        edi = request.getfixturevalue(edi_obj)
        assert channel not in edi.Measurement.measurements.keys()

    def test_measurement_metadata(self, edi_spectra):
        """Test measurement metadata."""
        m_list = [
            "\n>=DEFINEMEAS\n",
            "    MAXCHAN=7\n",
            "    MAXRUN=999\n",
            "    MAXMEAS=99999\n",
            "    REFLAT=35:33:0.000000\n",
            "    REFLON=-106:17:0.000000\n",
            "    REFELEV=0\n",
            "    REFTYPE=cartesian\n",
            "    UNITS=meter\n",
        ]

        assert m_list == edi_spectra.Measurement.write_measurement()[0 : len(m_list)]

    @pytest.mark.parametrize(
        "attr,expected,precision",
        [
            ("reflat", 35.55, 2),
            ("reflon", -106.2833, 4),
            ("refelev", 0.0, 2),
        ],
    )
    def test_measurement_coordinates(self, edi_spectra, attr, expected, precision):
        """Test measurement coordinates with different precisions."""
        actual = getattr(edi_spectra.Measurement, attr)
        assert abs(actual - expected) < 10 ** (
            -precision
        ), f"{attr} mismatch: expected {expected}, got {actual}"

    def test_data_section(self, edi_spectra):
        """Test data section."""
        d_list = [
            "\n>=MTSECT\n",
            "    NFREQ=33\n",
            "    SECTID=Ex\n",
            "    NCHAN=7\n",
            "    MAXBLOCKS=999\n",
            "    HX=11.001\n",
            "    HY=12.001\n",
            "    HZ=13.001\n",
            "    EX=14.001\n",
            "    EY=15.001\n",
        ]

        assert d_list == edi_spectra.Data.write_data()[0 : len(d_list)]

    @pytest.mark.parametrize("array_type", ["z", "z_err", "t", "t_err"])
    def test_array_comparison(self, edi_spectra, edi_z, array_type):
        """Test that arrays match between spectra and z files."""
        spectra_array = getattr(edi_spectra, array_type)
        z_array = getattr(edi_z, array_type)
        assert np.isclose(
            spectra_array, z_array
        ).all(), f"{array_type} arrays do not match"


# =============================================================================
# TF to EDI Tests
# =============================================================================
class TestToTF:
    """Test TF object functionality."""

    @pytest.mark.parametrize("metadata_type", ["station_metadata", "survey_metadata"])
    def test_metadata_comparison(self, edi_spectra, tf_spectra, metadata_type):
        """Test metadata comparison between EDI and TF objects."""
        edi_metadata = getattr(edi_spectra, metadata_type).to_dict(single=True)
        tf_metadata = getattr(tf_spectra, metadata_type).to_dict(single=True)

        for key, value in edi_metadata.items():
            assert (
                value == tf_metadata[key]
            ), f"{metadata_type}.{key} mismatch: expected {value}, got {tf_metadata[key]}"

    @pytest.mark.parametrize(
        "method,expected",
        [
            ("has_impedance", True),
            ("has_tipper", True),
            ("has_inverse_signal_power", True),
            ("has_residual_covariance", True),
        ],
    )
    def test_tf_capabilities(self, tf_spectra, method, expected):
        """Test TF object capabilities."""
        result = getattr(tf_spectra, method)()
        assert result == expected, f"{method} returned {result}, expected {expected}"


# =============================================================================
# TF from EDI Tests
# =============================================================================
class TestFromTF:
    """Test EDI creation from TF object."""

    def test_station_metadata(self, tf_to_edi, tf_spectra):
        """Test station metadata comparison with special handling for comments."""
        edi_st = tf_to_edi.station_metadata.to_dict(single=True)
        tf_st = tf_spectra.station_metadata.to_dict(single=True)

        for key, value in edi_st.items():
            if key == "comments":
                # Comments are expected to be different
                assert (
                    value != tf_st[key]
                ), f"Comments should be different but both are: {value}"
            else:
                assert (
                    value == tf_st[key]
                ), f"station_metadata.{key} mismatch: expected {value}, got {tf_st[key]}"

    def test_survey_metadata(self, tf_to_edi, tf_spectra):
        """Test survey metadata comparison."""
        edi_st = tf_to_edi.survey_metadata.to_dict(single=True)
        tf_st = tf_spectra.survey_metadata.to_dict(single=True)

        for key, value in edi_st.items():
            assert (
                value == tf_st[key]
            ), f"survey_metadata.{key} mismatch: expected {value}, got {tf_st[key]}"

    @pytest.mark.parametrize(
        "method,expected",
        [
            ("has_impedance", True),
            ("has_tipper", True),
            ("has_inverse_signal_power", True),
            ("has_residual_covariance", True),
        ],
    )
    def test_tf_capabilities(self, tf_spectra, method, expected):
        """Test TF object capabilities."""
        result = getattr(tf_spectra, method)()
        assert result == expected, f"{method} returned {result}, expected {expected}"
=======
            with self.subTest(key):
                h_value = getattr(self.edi_spectra.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("acquire date"):
            self.assertEqual(
                self.edi_spectra.Header._acqdate, MTime("2004-07-03")
            )

        with self.subTest("units"):
            self.assertNotEqual(
                self.edi_spectra.Header.units,
                "millivolts_per_kilometer_per_nanotesla",
            )

    def test_info(self):
        info_list = ["MAXLINES=1000"]

        self.assertListEqual(info_list, self.edi_spectra.Info.info_list)

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 106.97549946792975),
                ("chtype", "EX"),
                ("id", 14.001),
                ("x", 4872.0),
                ("x2", 4843.0),
                ("y", -3577.0),
                ("y2", -3482.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_spectra.Measurement.meas_ex.to_dict(single=True)
        )

    def test_measurement_ey(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", -163.19130837379313),
                ("chtype", "EY"),
                ("id", 15.001),
                ("x", 4906.0),
                ("x2", 4810.0),
                ("y", -3515.0),
                ("y2", -3544.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_spectra.Measurement.meas_ey.to_dict(single=True)
        )

    def test_measurement_hx(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 107.0),
                ("chtype", "HX"),
                ("dip", 0.0),
                ("id", 11.001),
                ("x", 4858.0),
                ("y", -3530.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_spectra.Measurement.meas_hx.to_dict(single=True)
        )

    def test_measurement_hy(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", -163.0),
                ("chtype", "HY"),
                ("dip", 0.0),
                ("id", 12.001),
                ("x", 4858.0),
                ("y", -3530.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_spectra.Measurement.meas_hy.to_dict(single=True)
        )

    def test_measurement_hz(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "HZ"),
                ("dip", 0.0),
                ("id", 13.001),
                ("x", 4858.0),
                ("y", -3530.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_spectra.Measurement.meas_hz.to_dict(single=True)
        )

    def test_measurement_rrhx(self):
        with self.subTest("spectra"):
            self.assertFalse(hasattr(self.edi_spectra.Measurement, "rrhx"))
        with self.subTest("z"):
            self.assertFalse(hasattr(self.edi_z.Measurement, "rrhx"))

        with self.subTest("spectra"):
            self.assertFalse(hasattr(self.edi_spectra.Measurement, "rrhy"))
        with self.subTest("z"):
            self.assertFalse(hasattr(self.edi_z.Measurement, "rrhy"))

    def test_measurement(self):
        m_list = [
            "MAXCHAN=7",
            "MAXRUN=999",
            "MAXMEAS=99999",
            "UNITS=M",
            "REFLAT=35:33:00",
            "REFLONG=-106:17:00",
        ]

        self.assertListEqual(
            m_list,
            self.edi_spectra.Measurement.measurement_list[0 : len(m_list)],
        )

        with self.subTest("reflat"):
            self.assertAlmostEqual(
                35.55, self.edi_spectra.Measurement.reflat, 2
            )

        with self.subTest("reflon"):
            self.assertAlmostEqual(
                -106.2833, self.edi_spectra.Measurement.reflon, 4
            )

        with self.subTest("reflong"):
            self.assertAlmostEqual(
                -106.2833, self.edi_spectra.Measurement.reflong, 4
            )

        with self.subTest("refelev"):
            self.assertAlmostEqual(
                0.0, self.edi_spectra.Measurement.refelev, 2
            )

    def test_data_section(self):
        d_list = [
            "SECTID=Ex",
            "NCHAN=7",
            "NFREQ=33",
            "MAXBLKS=100",
            "//7",
            "11.001    12.001    13.001    14.001    15.001    11.001    12.001",
        ]

        self.assertListEqual(d_list, self.edi_spectra.Data.data_list)

    def test_z(self):
        self.assertTrue(np.isclose(self.edi_spectra.z, self.edi_z.z).all())

    def test_z_err(self):
        self.assertTrue(
            np.isclose(self.edi_spectra.z_err, self.edi_z.z_err).all()
        )

    def test_t(self):
        self.assertTrue(np.isclose(self.edi_spectra.t, self.edi_z.t).all())

    def test_t_err(self):
        self.assertTrue(
            np.isclose(self.edi_spectra.t_err, self.edi_z.t_err).all()
        )


class TestToTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi = EDI(fn=TF_EDI_SPECTRA)
        self.tf = TF(fn=TF_EDI_SPECTRA)
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
        self.assertTrue(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertTrue(self.tf.has_residual_covariance())


class TestFromTF(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_EDI_SPECTRA)
        self.tf.read()

        self.edi = self.tf.to_edi()
        self.maxDiff = None

    def test_station_metadata(self):
        edi_st = self.edi.station_metadata.to_dict(single=True)
        tf_st = self.tf.station_metadata.to_dict(single=True)
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
        self.assertTrue(self.tf.has_inverse_signal_power())

    def test_has_residual_covariance(self):
        self.assertTrue(self.tf.has_residual_covariance())


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
>>>>>>> main
