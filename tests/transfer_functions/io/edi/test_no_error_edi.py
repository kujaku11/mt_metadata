# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

from collections import OrderedDict

# =============================================================================
# Imports
# =============================================================================
import pytest

from mt_metadata import TF_EDI_NO_ERROR
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io import edi


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture(scope="module")
def no_error_edi_object():
    """Create No Error EDI object once for all tests in this module."""
    return edi.EDI(fn=TF_EDI_NO_ERROR)


@pytest.fixture(scope="module")
def no_error_tf_object():
    """Create No Error TF object once for all tests in this module."""
    tf_obj = TF(fn=TF_EDI_NO_ERROR)
    tf_obj.read()
    return tf_obj


@pytest.fixture(scope="module")
def no_error_tf_to_edi_object(no_error_tf_object):
    """Create EDI object from TF object for testing."""
    return no_error_tf_object.to_edi()


@pytest.fixture(scope="module")
def expected_header():
    """Expected header data for No Error EDI testing."""
    return OrderedDict(
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


@pytest.fixture(scope="module")
def expected_info():
    """Expected info dictionary for No Error EDI testing."""
    return {"maxinfo": "500"}


@pytest.fixture(scope="module")
def expected_measurement_channels():
    """Expected measurement channel data for No Error EDI testing."""
    return {
        "ex": OrderedDict(
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
        ),
        "ey": OrderedDict(
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
        ),
        "hx": OrderedDict(
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
        ),
        "hy": OrderedDict(
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
        ),
        "hz": OrderedDict(
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
        ),
    }


@pytest.fixture(scope="module")
def expected_measurement_output():
    """Expected measurement output for No Error EDI testing."""
    return [
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


@pytest.fixture(scope="module")
def expected_data_section_output():
    """Expected data section output for No Error EDI testing."""
    return [
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


# =============================================================================
# Test Classes
# =============================================================================
class TestNoErrorEDI:
    """Test class for No Error EDI functionality using pytest."""

    @pytest.mark.parametrize(
        "key,expected_value",
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
        ],
    )
    def test_header_attributes(self, no_error_edi_object, key, expected_value):
        """Test header attributes using parametrization."""
        h_value = no_error_edi_object.Header.get_attr_from_name(key)
        assert h_value == expected_value

    def test_info(self, no_error_edi_object, expected_info):
        """Test info dictionary."""
        assert no_error_edi_object.Info.info_dict == expected_info

    @pytest.mark.parametrize("channel", ["ex", "ey", "hx", "hy", "hz"])
    def test_measurement_channels(
        self, no_error_edi_object, expected_measurement_channels, channel
    ):
        """Test individual measurement channels using parametrization."""
        expected = expected_measurement_channels[channel]
        actual = no_error_edi_object.Measurement.measurements[channel].to_dict(
            single=True
        )
        assert actual == expected

    def test_measurement_output(self, no_error_edi_object, expected_measurement_output):
        """Test measurement write output."""
        actual_output = no_error_edi_object.Measurement.write_measurement()
        assert actual_output == expected_measurement_output

    @pytest.mark.parametrize(
        "attr,expected,precision",
        [
            ("reflat", 0, 5),
            ("reflon", 0, 5),
            ("refelev", 0, 2),
        ],
    )
    def test_measurement_reference_values(
        self, no_error_edi_object, attr, expected, precision
    ):
        """Test measurement reference values with specified precision."""
        actual = getattr(no_error_edi_object.Measurement, attr)
        assert abs(actual - expected) < 10 ** (-precision)

    def test_data_section_output(
        self, no_error_edi_object, expected_data_section_output
    ):
        """Test data section write output."""
        actual_output = no_error_edi_object.Data.write_data()
        assert actual_output == expected_data_section_output

    @pytest.mark.parametrize(
        "array_name,expected_shape",
        [
            ("z", (47, 2, 2)),
            ("z_err", (47, 2, 2)),
        ],
    )
    def test_impedance_shapes(self, no_error_edi_object, array_name, expected_shape):
        """Test impedance array shapes."""
        array = getattr(no_error_edi_object, array_name)
        assert array.shape == expected_shape

    def test_impedance_values(self, no_error_edi_object):
        """Test specific impedance values."""
        # Test that error at first element is zero
        assert no_error_edi_object.z_err[0, 0, 0] == 0

        # Test that impedance value is not zero
        assert no_error_edi_object.z[1, 0, 0] != 0 + 0j

    @pytest.mark.parametrize(
        "array_name,expected_shape",
        [
            ("t", (47, 1, 2)),
            ("t_err", (47, 1, 2)),
        ],
    )
    def test_tipper_shapes(self, no_error_edi_object, array_name, expected_shape):
        """Test tipper array shapes."""
        array = getattr(no_error_edi_object, array_name)
        assert array.shape == expected_shape

    def test_tipper_values(self, no_error_edi_object):
        """Test specific tipper values."""
        # Test that error at first element is zero
        assert no_error_edi_object.t_err[0, 0, 0] == 0

    def test_rotation_angle(self, no_error_edi_object):
        """Test rotation angle properties."""
        rotation_angle = no_error_edi_object.rotation_angle

        # Test that all values are zero
        assert (rotation_angle == 0).all()

        # Test shape
        assert rotation_angle.shape == (47,)


class TestToTF:
    """Test class for EDI to TF conversion."""

    def test_station_metadata(self, no_error_edi_object, no_error_tf_object):
        """Test station metadata conversion from EDI to TF."""
        edi_st = no_error_edi_object.station_metadata.to_dict(single=True)
        tf_st = no_error_tf_object.station_metadata.to_dict(single=True)

        for edi_key, edi_value in edi_st.items():
            assert (
                edi_value == tf_st[edi_key]
            ), f"Station metadata mismatch for {edi_key}"

    def test_survey_metadata(self, no_error_edi_object, no_error_tf_object):
        """Test survey metadata conversion from EDI to TF."""
        edi_st = no_error_edi_object.survey_metadata.to_dict(single=True)
        tf_st = no_error_tf_object.survey_metadata.to_dict(single=True)

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
    def test_tf_properties(self, no_error_tf_object, method, expected):
        """Test TF object properties using parametrization."""
        result = getattr(no_error_tf_object, method)()
        assert result == expected

    def test_impedance_error_zeros(self, no_error_tf_object):
        """Test that impedance errors are zero."""
        assert (no_error_tf_object.impedance_error.data[:, 0, 0] == 0).all()


class TestFromTF:
    """Test class for TF to EDI conversion."""

    def test_station_metadata(self, no_error_tf_object, no_error_tf_to_edi_object):
        """Test station metadata conversion from TF to EDI."""
        edi_st = no_error_tf_to_edi_object.station_metadata.to_dict(single=True)
        tf_st = no_error_tf_object.station_metadata.to_dict(single=True, required=False)

        for edi_key, edi_value in edi_st.items():
            if edi_key in ["comments"]:
                # Comments are expected to be different
                assert (
                    edi_value != tf_st[edi_key]
                ), f"Comments should be different for {edi_key}"
            elif edi_key in ["location.x", "location.y", "location.z"]:
                # Location coordinates: None in TF becomes 0.0 in EDI
                tf_value = tf_st[edi_key]
                if tf_value is None:
                    assert (
                        edi_value == 0.0
                    ), f"Location coordinate {edi_key}: expected 0.0 for None TF value, got {edi_value}"
                else:
                    assert (
                        edi_value == tf_value
                    ), f"Location coordinate {edi_key} mismatch: EDI={edi_value} vs TF={tf_value}"
            else:
                assert (
                    edi_value == tf_st[edi_key]
                ), f"Station metadata mismatch for {edi_key}"

    def test_survey_metadata(self, no_error_tf_object, no_error_tf_to_edi_object):
        """Test survey metadata conversion from TF to EDI."""
        edi_st = no_error_tf_to_edi_object.survey_metadata.to_dict(single=True)
        tf_st = no_error_tf_object.survey_metadata.to_dict(single=True)

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
    def test_tf_properties(self, no_error_tf_object, method, expected):
        """Test TF object properties using parametrization."""
        result = getattr(no_error_tf_object, method)()
        assert result == expected

    def test_impedance_error_zeros(self, no_error_tf_object):
        """Test that impedance errors are zero."""
        assert (no_error_tf_object.impedance_error.data[:, 0, 0] == 0).all()


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__])
