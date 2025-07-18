# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

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
        head = {
            "ACQBY": "Quantec Consulting",
            "COORDINATE_SYSTEM": "geographic",
            "DATAID": "SAGE_2005_og",
            "DATUM": "WGS 84",
            "ELEV": 0,
            "EMPTY": 1e32,
            "FILEBY": "Quantec Consulting",
            "LAT": 35.55,
            "LON": -106.28333333333333,
        }

        for key, value in head.items():
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


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__])
