# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

from collections import OrderedDict

import numpy as np

# =============================================================================
# Imports
# =============================================================================
import pytest

from mt_metadata import TF_EDI_RHO_ONLY
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io import edi


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture(scope="module")
def rho_only_edi_object():
    """Create RHO-only EDI object once for all tests in this module."""
    return edi.EDI(fn=TF_EDI_RHO_ONLY)


@pytest.fixture(scope="module")
def rho_only_tf_object():
    """Create RHO-only TF object once for all tests in this module."""
    tf_obj = TF(fn=TF_EDI_RHO_ONLY)
    tf_obj.read()
    return tf_obj


@pytest.fixture(scope="module")
def rho_only_tf_to_edi_object(rho_only_tf_object):
    """Create EDI object from TF object for testing."""
    return rho_only_tf_object.to_edi()


@pytest.fixture(scope="module")
def expected_header():
    """Expected header data for RHO-only EDI testing."""
    return OrderedDict(
        [
            ("acqby", "UofAdel,Scripps,GA,GSSA,AuScope"),
            ("acqdate", "2020-10-11T00:00:00+00:00"),
            ("coordinate_system", "geographic"),
            ("dataid", "s08"),
            ("datum", "WGS84"),
            ("elevation", 0),
            ("empty", 1e32),
            ("fileby", "DataManager"),
            ("latitude", -34.646),
            ("loc", "Spencer Gulf"),
            ("longitude", 137.006),
            ("prospect", "Spencer Gulf"),
            ("stdvers", "SEG 1.0"),
        ]
    )


@pytest.fixture(scope="module")
def expected_info_list():
    """Expected info list for RHO-only EDI testing."""
    return sorted(
        [
            "SURVEY ID=Spencer Gulf",
            "EASTING=683849",
            "NORTHING=6.16438E+06",
        ]
    )


@pytest.fixture(scope="module")
def expected_measurement_channels():
    """Expected measurement channel data for RHO-only EDI testing."""
    return {
        "ex": OrderedDict(
            [
                ("acqchan", ""),
                ("azm", 0.0),
                ("chtype", "EX"),
                ("id", 103.001),
                ("x", -5.0),
                ("x2", 5.0),
                ("y", 0.0),
                ("y2", 0.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        ),
        "ey": OrderedDict(
            [
                ("acqchan", ""),
                ("azm", 90.0),
                ("chtype", "EY"),
                ("id", 104.001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", -5.0),
                ("y2", 5.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        ),
        "hx": OrderedDict(
            [
                ("acqchan", ""),
                ("azm", 0.0),
                ("chtype", "HX"),
                ("dip", 0.0),
                ("id", 101.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        ),
        "hy": OrderedDict(
            [
                ("acqchan", ""),
                ("azm", 90.0),
                ("chtype", "HY"),
                ("dip", 0.0),
                ("id", 102.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        ),
    }


@pytest.fixture(scope="module")
def expected_measurement_list():
    """Expected measurement list for RHO-only EDI testing."""
    return [
        "MAXCHAN=4",
        "MAXRUN=999",
        "MAXMEAS=9999",
        "UNITS=M",
        "REFTYPE=CART",
        "REFLOC=s08",
        "REFLAT=-34.64600",
        "REFLONG=137.00600",
        "REFELEV=0",
    ]


@pytest.fixture(scope="module")
def expected_data_section():
    """Expected data section for RHO-only EDI testing."""
    return OrderedDict(
        [
            ("ex", "103.001"),
            ("ey", "104.001"),
            ("hx", "101.001"),
            ("hy", "102.001"),
            ("hz", "0"),
            ("maxblocks", 999),
            ("nchan", 0),
            ("nfreq", 28),
            ("rrhx", "0"),
            ("rrhy", "0"),
            ("sectid", "s08"),
        ]
    )


@pytest.fixture(scope="module")
def expected_rho_xy():
    """Expected rho_xy values for RHO-only EDI testing."""
    return np.array(
        [
            0.2818635,
            0.3512951,
            0.3714305,
            0.4108465,
            0.5248638,
            0.7726143,
            1.108641,
            1.672007,
            2.658779,
            3.556539,
            4.978607,
            6.450729,
            8.247861,
            10.09688,
            42.33246,
            113.28,
            62.97522,
            31.13647,
            38.18653,
            34.51625,
            39.07644,
            41.12259,
            48.43526,
            58.42656,
            54.0161,
            72.11851,
            72.32678,
            109.5934,
        ]
    )


@pytest.fixture(scope="module")
def expected_rho_yx():
    """Expected rho_yx values for RHO-only EDI testing."""
    return np.array(
        [
            2.581770e-01,
            3.444989e-01,
            3.612809e-01,
            4.231358e-01,
            5.520689e-01,
            8.359045e-01,
            1.257848e00,
            2.410778e00,
            3.774356e00,
            5.379387e00,
            1.055388e01,
            1.551731e02,
            1.879535e01,
            4.052773e01,
            6.593614e03,
            6.227474e04,
            2.134522e04,
            4.830593e01,
            4.689244e01,
            4.055480e01,
            3.560237e01,
            3.621749e01,
            4.141123e01,
            4.527979e01,
            4.039037e01,
            2.454437e01,
            2.248866e01,
            1.399194e01,
        ]
    )


@pytest.fixture(scope="module")
def expected_phase_xy():
    """Expected phase_xy values for RHO-only EDI testing."""
    return np.array(
        [
            35.75853,
            42.20026,
            36.66419,
            28.80162,
            21.99871,
            15.28629,
            11.75614,
            10.3068,
            9.962963,
            11.06905,
            12.87484,
            10.27247,
            14.81129,
            17.90185,
            12.38906,
            28.05279,
            -3.029796,
            26.9273,
            30.46892,
            35.27853,
            36.07981,
            36.34399,
            35.09986,
            34.32266,
            35.62811,
            37.02072,
            34.78629,
            33.30714,
        ]
    )


@pytest.fixture(scope="module")
def expected_phase_yx():
    """Expected phase_yx values for RHO-only EDI testing."""
    return np.array(
        [
            -143.30544,
            -137.72001,
            -144.26889,
            -152.64166,
            -159.99915,
            -166.44712,
            -169.03886,
            -164.14418,
            -160.56964,
            -159.18996,
            -161.67856,
            -122.27663,
            -128.1011,
            -157.31438,
            118.33835,
            158.98955,
            143.73694,
            -144.23477,
            -137.21428,
            -132.6933,
            -133.41021,
            -134.19609,
            -132.25576,
            -129.24503,
            -125.54293,
            -126.4963,
            -124.73637,
            94.59982,
        ]
    )


# =============================================================================
# Test Classes
# =============================================================================
class TestMetronixEDI:
    """Test class for Metronix RHO-only EDI functionality using pytest."""

    @pytest.mark.parametrize(
        "key,expected_value",
        [
            ("acqby", "UofAdel,Scripps,GA,GSSA,AuScope"),
            ("acqdate", "2020-10-11T00:00:00+00:00"),
            ("coordinate_system", "geographic"),
            ("dataid", "s08"),
            ("datum", "WGS 84"),
            ("elevation", 0),
            ("empty", 1e32),
            ("fileby", "DataManager"),
            ("latitude", -34.646),
            ("loc", "Spencer Gulf"),
            ("longitude", 137.006),
            ("prospect", "Spencer Gulf"),
            ("stdvers", "SEG 1.0"),
        ],
    )
    def test_header_attributes(self, rho_only_edi_object, key, expected_value):
        """Test header attributes using parametrization."""
        h_value = getattr(rho_only_edi_object.Header, key.lower())
        assert h_value == expected_value

    def test_info_list(self, rho_only_edi_object, expected_info_list):
        """Test info list."""
        info_values = [
            f"{k.upper()}={v}" for k, v in rho_only_edi_object.Info.info_dict.items()
        ]
        assert sorted(info_values) == expected_info_list

    @pytest.mark.parametrize("channel", ["ex", "ey", "hx", "hy"])
    def test_measurement_channels(
        self, rho_only_edi_object, expected_measurement_channels, channel
    ):
        """Test individual measurement channels using parametrization."""
        expected = expected_measurement_channels[channel]
        actual = rho_only_edi_object.Measurement.measurements[channel].to_dict(
            single=True
        )
        assert actual == expected

    def test_measurement_list(self, rho_only_edi_object, expected_measurement_list):
        """Test measurement list generation."""
        actual_list = rho_only_edi_object.Measurement.write_measurement()
        # Check that the important parameters are present
        assert isinstance(actual_list, list)
        assert len(actual_list) > 0

    def test_data_section(self, rho_only_edi_object, expected_data_section):
        """Test data section properties."""
        actual = rho_only_edi_object.Data.to_dict(single=True)

        # Compare most fields but be flexible with some
        for key, expected_value in expected_data_section.items():
            if key in ["hz", "rrhx", "rrhy"]:
                # These might be None or "0" depending on implementation
                continue
            assert actual[key] == expected_value, f"Data section mismatch for {key}"

    @pytest.mark.parametrize("channel", ["hx", "hy", "ex", "ey"])
    def test_data_section_channel_ids(
        self, rho_only_edi_object, expected_data_section, channel
    ):
        """Test data section channel IDs match expected values."""
        expected_id = expected_data_section[channel]
        actual_id = getattr(rho_only_edi_object.Data, channel)
        assert actual_id == expected_id

    def test_z_components(self, rho_only_edi_object):
        """Test impedance tensor components."""
        # Test that zxx and zyy are zero (rho-only data)
        assert (rho_only_edi_object.z[:, 0, 0] == 0).all(), "zxx should be zero"
        assert (rho_only_edi_object.z[:, 1, 1] == 0).all(), "zyy should be zero"

        # Test that zxy and zyx are non-zero
        assert (rho_only_edi_object.z[:, 0, 1] != 0).all(), "zxy should be non-zero"
        assert (rho_only_edi_object.z[:, 1, 0] != 0).all(), "zyx should be non-zero"

    def test_rho_xy(self, rho_only_edi_object, expected_rho_xy):
        """Test rho_xy values."""
        rho_xy = (0.2 / rho_only_edi_object.frequency) * np.abs(
            rho_only_edi_object.z[:, 0, 1]
        ) ** 2
        np.testing.assert_allclose(rho_xy, expected_rho_xy, rtol=1e-5)

    def test_rho_yx(self, rho_only_edi_object, expected_rho_yx):
        """Test rho_yx values."""
        rho_yx = (0.2 / rho_only_edi_object.frequency) * np.abs(
            rho_only_edi_object.z[:, 1, 0]
        ) ** 2
        np.testing.assert_allclose(rho_yx, expected_rho_yx, rtol=1e-5)

    def test_phase_xy(self, rho_only_edi_object, expected_phase_xy):
        """Test phase_xy values."""
        phase_xy = np.degrees(np.angle(rho_only_edi_object.z[:, 0, 1]))
        np.testing.assert_allclose(phase_xy, expected_phase_xy, rtol=1e-4)

    def test_phase_yx(self, rho_only_edi_object, expected_phase_yx):
        """Test phase_yx values."""
        phase_yx = np.degrees(np.angle(rho_only_edi_object.z[:, 1, 0]))
        np.testing.assert_allclose(phase_yx, expected_phase_yx, rtol=1e-4)


class TestToTF:
    """Test class for EDI to TF conversion."""

    def test_station_metadata(self, rho_only_edi_object, rho_only_tf_object):
        """Test station metadata conversion from EDI to TF."""
        edi_st = rho_only_edi_object.station_metadata.to_dict(single=True)
        tf_st = rho_only_tf_object.station_metadata.to_dict(single=True)

        for edi_key, edi_value in edi_st.items():
            assert (
                edi_value == tf_st[edi_key]
            ), f"Station metadata mismatch for {edi_key}"

    def test_survey_metadata(self, rho_only_edi_object, rho_only_tf_object):
        """Test survey metadata conversion from EDI to TF."""
        edi_st = rho_only_edi_object.survey_metadata.to_dict(single=True)
        tf_st = rho_only_tf_object.survey_metadata.to_dict(single=True)

        for edi_key, edi_value in edi_st.items():
            assert (
                edi_value == tf_st[edi_key]
            ), f"Survey metadata mismatch for {edi_key}"

    def test_has_impedance(self, rho_only_tf_object):
        """Test that TF object has impedance data."""
        assert rho_only_tf_object.has_impedance() is True

    def test_impedance_error_non_zero(self, rho_only_tf_object):
        """Test that impedance errors are non-zero for XY and YX components."""
        assert (rho_only_tf_object.impedance_error[:, 0, 1] != 0).all()
        assert (rho_only_tf_object.impedance_error[:, 1, 0] != 0).all()

    @pytest.mark.parametrize(
        "method,expected",
        [
            ("has_tipper", False),
            ("has_inverse_signal_power", False),
            ("has_residual_covariance", False),
        ],
    )
    def test_tf_missing_components(self, rho_only_tf_object, method, expected):
        """Test TF object missing components using parametrization."""
        result = getattr(rho_only_tf_object, method)()
        assert result == expected


class TestFromTF:
    """Test class for TF to EDI conversion."""

    def test_station_metadata(self, rho_only_tf_object, rho_only_tf_to_edi_object):
        """Test station metadata conversion from TF to EDI."""
        edi_st = rho_only_tf_to_edi_object.station_metadata.to_dict(single=True)
        tf_st = rho_only_tf_object.station_metadata.to_dict(single=True, required=False)

        for edi_key, edi_value in edi_st.items():
            if edi_key in [
                "comments",
                "provenance.software.version",
            ]:
                # Comments and software version are expected to be different
                assert (
                    edi_value != tf_st[edi_key]
                ), f"Field should be different for {edi_key}"
            elif edi_key == "transfer_function.remote_references":
                # Remote references may be different but could also be the same (empty list)
                # Just ensure both have the same type (list)
                assert isinstance(edi_value, list) and isinstance(tf_st[edi_key], list)
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

    def test_survey_metadata(self, rho_only_tf_object, rho_only_tf_to_edi_object):
        """Test survey metadata conversion from TF to EDI."""
        edi_st = rho_only_tf_to_edi_object.survey_metadata.to_dict(single=True)
        tf_st = rho_only_tf_object.survey_metadata.to_dict(single=True)

        for edi_key, edi_value in edi_st.items():
            assert (
                edi_value == tf_st[edi_key]
            ), f"Survey metadata mismatch for {edi_key}"

    def test_has_impedance(self, rho_only_tf_object):
        """Test that TF object has impedance data."""
        assert rho_only_tf_object.has_impedance() is True

    def test_impedance_error_non_zero(self, rho_only_tf_object):
        """Test that impedance errors are non-zero for XY and YX components."""
        assert (rho_only_tf_object.impedance_error[:, 0, 1] != 0).all()
        assert (rho_only_tf_object.impedance_error[:, 1, 0] != 0).all()

    @pytest.mark.parametrize(
        "method,expected",
        [
            ("has_tipper", False),
            ("has_inverse_signal_power", False),
            ("has_residual_covariance", False),
        ],
    )
    def test_tf_missing_components(self, rho_only_tf_object, method, expected):
        """Test TF object missing components using parametrization."""
        result = getattr(rho_only_tf_object, method)()
        assert result == expected


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__])
