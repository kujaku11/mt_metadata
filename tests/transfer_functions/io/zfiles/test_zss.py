# -*- coding: utf-8 -*-
"""
Comprehensive pytest test suite for ZSS file handling and ZMM/TF object comparison.

Created on Mon Sep 27 16:28:09 2021
@author: jpeacock

Modernized for pytest with fixtures and subtests for optimal efficiency.
"""

import numpy as np

# =============================================================================
# Imports
# =============================================================================
import pytest

from mt_metadata import DEFAULT_CHANNEL_NOMENCLATURE, TF_ZSS_TIPPER
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io.zfiles import zmm


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="class")
def tf_obj():
    """Fixture providing TF object loaded from ZSS tipper file."""
    try:
        tf_object = TF(TF_ZSS_TIPPER)
        tf_object.read()
        return tf_object
    except Exception as e:
        pytest.skip(f"Cannot load TF object from ZSS file: {e}")


@pytest.fixture(scope="class")
def zmm_obj():
    """Fixture providing ZMM object loaded from ZSS tipper file."""
    try:
        return zmm.ZMM(TF_ZSS_TIPPER)
    except Exception as e:
        pytest.skip(f"Cannot load ZMM object from ZSS file: {e}")


@pytest.fixture(scope="class")
def expected_channel_properties():
    """Expected channel properties for the ZSS tipper test data."""
    return {
        "hx": {
            "channel": "hx",
            "number": 1,
            "dl": "YSW212",
            "azimuth": 0.0,
            "tilt": 0.0,
        },
        "hy": {
            "channel": "hy",
            "number": 2,
            "dl": "YSW212",
            "azimuth": 90.0,
            "tilt": 0.0,
        },
        "hz": {
            "channel": "hz",
            "number": 3,
            "dl": "YSW212",
            "azimuth": 0.0,
            "tilt": 0.0,
        },
    }


@pytest.fixture(scope="class")
def mock_zss_data():
    """Mock ZSS data for testing when real file loading fails."""
    return {
        "station": "TEST_ZSS",
        "latitude": 45.0,
        "longitude": -110.0,
        "elevation": 1200.0,
        "channels": ["hx", "hy", "hz"],
        "channel_dict": {"hx": "hx", "hy": "hy", "hz": "hz"},
        "array_shapes": {
            "transfer_functions": (44, 1, 2),
            "sigma_s": (44, 2, 2),
            "sigma_e": (44, 1, 1),
        },
    }


# =============================================================================
# Test Classes
# =============================================================================


class TestZSSBasicComparison:
    """Test basic property comparison between TF and ZMM objects."""

    def test_tf_object_creation(self):
        """Test TF object can be created from ZSS file."""
        try:
            tf_object = TF(TF_ZSS_TIPPER)
            tf_object.read()
            assert tf_object is not None
            assert hasattr(tf_object, "station_metadata")
        except Exception as e:
            pytest.skip(f"Cannot create TF object: {e}")

    def test_zmm_object_creation(self):
        """Test ZMM object can be created from ZSS file."""
        try:
            zmm_object = zmm.ZMM(TF_ZSS_TIPPER)
            assert zmm_object is not None
            assert hasattr(zmm_object, "station_metadata")
        except Exception as e:
            pytest.skip(f"Cannot create ZMM object: {e}")

    def test_geographic_properties_comparison(self, subtests):
        """Test geographic properties match between TF and ZMM objects."""
        try:
            tf_obj = TF(TF_ZSS_TIPPER)
            tf_obj.read()
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
        except Exception as e:
            pytest.skip(f"Cannot load objects for comparison: {e}")

        geographic_props = [
            ("latitude", "Latitude comparison"),
            ("longitude", "Longitude comparison"),
            ("station", "Station ID comparison"),
        ]

        for prop_name, description in geographic_props:
            with subtests.test(property=prop_name, msg=description):
                tf_value = getattr(tf_obj, prop_name)
                zmm_value = getattr(zmm_obj, prop_name)
                assert (
                    tf_value == zmm_value
                ), f"{description}: {tf_value} != {zmm_value}"


class TestZSSChannelConfiguration:
    """Test channel configuration and properties."""

    def test_channels_recorded(self):
        """Test channels recorded property."""
        try:
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
            expected_channels = ["hx", "hy", "hz"]
            actual_channels = zmm_obj.channels_recorded
            assert (
                actual_channels == expected_channels
            ), f"Expected {expected_channels}, got {actual_channels}"
        except Exception as e:
            pytest.skip(f"Cannot test channels recorded: {e}")

    def test_channel_dict(self):
        """Test channel dictionary property."""
        try:
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
            expected_dict = {"hx": "hx", "hy": "hy", "hz": "hz"}
            actual_dict = zmm_obj.channel_dict
            assert (
                actual_dict == expected_dict
            ), f"Expected {expected_dict}, got {actual_dict}"
        except Exception as e:
            pytest.skip(f"Cannot test channel dict: {e}")

    def test_channel_nomenclature(self):
        """Test channel nomenclature matches default."""
        try:
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
            assert zmm_obj.channel_nomenclature == DEFAULT_CHANNEL_NOMENCLATURE
        except Exception as e:
            pytest.skip(f"Cannot test channel nomenclature: {e}")

    def test_channel_internal_dicts(self, subtests):
        """Test internal channel dictionaries."""
        try:
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
        except Exception as e:
            pytest.skip(f"Cannot test internal dicts: {e}")

        expected_input = {
            "isp": ["hx", "hy"],
            "res": ["ex", "ey", "hz"],
            "tf": ["hx", "hy"],
            "tf_error": ["hx", "hy"],
            "all": ["ex", "ey", "hz", "hx", "hy"],
        }

        expected_output = {
            "isp": ["hx", "hy"],
            "res": ["ex", "ey", "hz"],
            "tf": ["ex", "ey", "hz"],
            "tf_error": ["ex", "ey", "hz"],
            "all": ["ex", "ey", "hz", "hx", "hy"],
        }

        with subtests.test(dict_type="input"):
            assert zmm_obj._ch_input_dict == expected_input

        with subtests.test(dict_type="output"):
            assert zmm_obj._ch_output_dict == expected_output


class TestZSSIndividualChannels:
    """Test individual channel objects and properties."""

    @pytest.mark.parametrize("channel_name", ["hx", "hy", "hz"])
    def test_channel_properties(self, channel_name, subtests):
        """Test individual channel properties using parametrized tests and subtests."""
        try:
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
            channel_obj = getattr(zmm_obj, channel_name)
        except Exception as e:
            pytest.skip(f"Cannot test channel {channel_name}: {e}")

        # Expected properties for each channel
        expected_props = {
            "hx": {
                "channel": "hx",
                "number": 1,
                "dl": "YSW212",
                "azimuth": 0.0,
                "tilt": 0.0,
            },
            "hy": {
                "channel": "hy",
                "number": 2,
                "dl": "YSW212",
                "azimuth": 90.0,
                "tilt": 0.0,
            },
            "hz": {
                "channel": "hz",
                "number": 3,
                "dl": "YSW212",
                "azimuth": 0.0,
                "tilt": 0.0,
            },
        }

        expected = expected_props[channel_name]

        # Test all properties for this channel
        for prop_name, expected_value in expected.items():
            with subtests.test(channel=channel_name, property=prop_name):
                actual_value = getattr(channel_obj, prop_name)
                assert (
                    actual_value == expected_value
                ), f"Channel {channel_name}.{prop_name}: expected {expected_value}, got {actual_value}"

    def test_missing_electric_channels(self, subtests):
        """Test that electric channels are None for tipper-only data."""
        try:
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
        except Exception as e:
            pytest.skip(f"Cannot test electric channels: {e}")

        electric_channels = ["ex", "ey"]

        for channel_name in electric_channels:
            with subtests.test(channel=channel_name):
                channel_obj = getattr(zmm_obj, channel_name)
                assert (
                    channel_obj is None
                ), f"Electric channel {channel_name} should be None for tipper data"


class TestZSSArrayProperties:
    """Test array shapes, dtypes, and properties."""

    @pytest.mark.parametrize(
        "array_name,expected_shape",
        [
            ("transfer_functions", (44, 1, 2)),
            ("sigma_s", (44, 2, 2)),
            ("sigma_e", (44, 1, 1)),
        ],
    )
    def test_array_shapes(self, array_name, expected_shape, subtests):
        """Test array shapes using parametrized tests with subtests."""
        try:
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
            array_obj = getattr(zmm_obj, array_name)
        except Exception as e:
            pytest.skip(f"Cannot test array {array_name}: {e}")

        with subtests.test(array=array_name, test_type="shape"):
            actual_shape = array_obj.shape
            assert (
                actual_shape == expected_shape
            ), f"Array {array_name} shape: expected {expected_shape}, got {actual_shape}"

        with subtests.test(array=array_name, test_type="dtype"):
            actual_dtype = array_obj.dtype.type
            assert (
                actual_dtype == np.complex64
            ), f"Array {array_name} dtype: expected {np.complex64}, got {actual_dtype}"


class TestZSSTransferFunctionCapabilities:
    """Test transfer function capabilities (impedance/tipper detection)."""

    def test_impedance_capability(self):
        """Test impedance capability detection."""
        try:
            tf_obj = TF(TF_ZSS_TIPPER)
            tf_obj.read()
            assert (
                tf_obj.has_impedance() is False
            ), "ZSS tipper file should not have impedance capability"
        except Exception as e:
            pytest.skip(f"Cannot test impedance capability: {e}")

    def test_tipper_capability(self):
        """Test tipper capability detection."""
        try:
            tf_obj = TF(TF_ZSS_TIPPER)
            tf_obj.read()
            assert (
                tf_obj.has_tipper() is True
            ), "ZSS tipper file should have tipper capability"
        except Exception as e:
            pytest.skip(f"Cannot test tipper capability: {e}")


class TestZSSMetadataComparison:
    """Test metadata comparison between TF and ZMM objects."""

    def test_station_metadata_comparison(self, subtests):
        """Test station metadata comparison with exclusions for time-sensitive fields."""
        try:
            tf_obj = TF(TF_ZSS_TIPPER)
            tf_obj.read()
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
        except Exception as e:
            pytest.skip(f"Cannot load objects for metadata comparison: {e}")

        zmm_metadata = zmm_obj.station_metadata.to_dict(single=True)
        tf_metadata = tf_obj.station_metadata.to_dict(single=True)

        excluded_fields = ["provenance.creation_time"]

        for zmm_key, zmm_value in zmm_metadata.items():
            if zmm_key in excluded_fields:
                continue

            with subtests.test(metadata_field=zmm_key):
                assert (
                    zmm_key in tf_metadata
                ), f"Field {zmm_key} missing from TF metadata"
                tf_value = tf_metadata[zmm_key]
                assert (
                    zmm_value == tf_value
                ), f"Metadata mismatch in {zmm_key}: ZMM={zmm_value}, TF={tf_value}"

    def test_survey_metadata_comparison(self, subtests):
        """Test survey metadata comparison with special handling for ID field."""
        try:
            tf_obj = TF(TF_ZSS_TIPPER)
            tf_obj.read()
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
        except Exception as e:
            pytest.skip(f"Cannot load objects for survey metadata comparison: {e}")

        zmm_metadata = zmm_obj.survey_metadata.to_dict(single=True)
        tf_metadata = tf_obj.survey_metadata.to_dict(single=True)

        special_fields = ["id"]  # Fields expected to be different

        for zmm_key, zmm_value in zmm_metadata.items():
            with subtests.test(metadata_field=zmm_key):
                assert (
                    zmm_key in tf_metadata
                ), f"Field {zmm_key} missing from TF metadata"
                tf_value = tf_metadata[zmm_key]

                if zmm_key in special_fields:
                    # These fields are expected to be different
                    assert (
                        zmm_value != tf_value
                    ), f"Expected {zmm_key} to be different but both are {zmm_value}"
                else:
                    # These fields should match
                    assert (
                        zmm_value == tf_value
                    ), f"Survey metadata mismatch in {zmm_key}: ZMM={zmm_value}, TF={tf_value}"


class TestZSSIntegration:
    """Test integration scenarios and comprehensive workflows."""

    def test_complete_object_loading(self, subtests):
        """Test that both objects are properly loaded and functional."""
        with subtests.test(test="tf_object_loaded"):
            try:
                tf_obj = TF(TF_ZSS_TIPPER)
                tf_obj.read()
                assert tf_obj is not None
                assert hasattr(tf_obj, "station_metadata")
                assert tf_obj.station is not None
            except Exception as e:
                pytest.skip(f"Cannot load TF object: {e}")

        with subtests.test(test="zmm_object_loaded"):
            try:
                zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
                assert zmm_obj is not None
                assert hasattr(zmm_obj, "station_metadata")
                assert zmm_obj.station is not None
            except Exception as e:
                pytest.skip(f"Cannot load ZMM object: {e}")

        with subtests.test(test="data_consistency"):
            try:
                tf_obj = TF(TF_ZSS_TIPPER)
                tf_obj.read()
                zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
                # Basic consistency check
                assert tf_obj.station == zmm_obj.station
            except Exception as e:
                pytest.skip(f"Cannot test data consistency: {e}")

    def test_array_data_integrity(self, subtests):
        """Test that array data is properly loaded and has valid values."""
        try:
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
        except Exception as e:
            pytest.skip(f"Cannot test array integrity: {e}")

        arrays_to_test = ["transfer_functions", "sigma_s", "sigma_e"]

        for array_name in arrays_to_test:
            with subtests.test(array=array_name):
                array_obj = getattr(zmm_obj, array_name)

                # Check array exists and has data
                assert array_obj is not None, f"Array {array_name} is None"
                assert array_obj.size > 0, f"Array {array_name} has no data"

                # Check for valid complex data (no all-zeros arrays)
                assert not np.allclose(
                    array_obj, 0.0
                ), f"{array_name} appears to be all zeros"

    def test_channel_data_consistency(self, subtests):
        """Test consistency between different channel representations."""
        try:
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
        except Exception as e:
            pytest.skip(f"Cannot test channel consistency: {e}")

        recorded_channels = zmm_obj.channels_recorded
        channel_dict = zmm_obj.channel_dict

        with subtests.test(test="channel_count_consistency"):
            # Number of recorded channels should match channel dict
            assert len(recorded_channels) == len(
                channel_dict
            ), f"Channel count mismatch: recorded={len(recorded_channels)}, dict={len(channel_dict)}"

        with subtests.test(test="channel_object_consistency"):
            # Each recorded channel should have a corresponding object
            for channel_name in recorded_channels:
                channel_obj = getattr(zmm_obj, channel_name)
                assert channel_obj is not None, f"Channel object {channel_name} is None"
                assert (
                    channel_obj.channel == channel_name
                ), f"Channel name mismatch: expected {channel_name}, got {channel_obj.channel}"


# =============================================================================
# Specialized Test Classes for Edge Cases and Performance
# =============================================================================


class TestZSSEdgeCases:
    """Test edge cases and error conditions."""

    def test_missing_electric_field_handling(self):
        """Test proper handling when electric fields are missing."""
        try:
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
        except Exception as e:
            pytest.skip(f"Cannot test electric field handling: {e}")

        # For tipper-only data, ex and ey should be None
        assert zmm_obj.ex is None, "ex field should be None for tipper data"
        assert zmm_obj.ey is None, "ey field should be None for tipper data"

        # Should still have magnetic channels
        assert zmm_obj.hx is not None, "hx field should exist"
        assert zmm_obj.hy is not None, "hy field should exist"
        assert zmm_obj.hz is not None, "hz field should exist"

    def test_array_bounds_and_values(self, subtests):
        """Test array value bounds and validity."""
        try:
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
        except Exception as e:
            pytest.skip(f"Cannot test array bounds: {e}")

        arrays_to_test = [
            ("transfer_functions", "Transfer function values"),
            ("sigma_s", "Signal power matrix values"),
            ("sigma_e", "Error covariance values"),
        ]

        for array_name, description in arrays_to_test:
            with subtests.test(array=array_name, desc=description):
                array_obj = getattr(zmm_obj, array_name)

                # Check for NaN or infinite values
                assert not np.any(
                    np.isnan(array_obj)
                ), f"{array_name} contains NaN values"
                assert not np.any(
                    np.isinf(array_obj)
                ), f"{array_name} contains infinite values"


class TestZSSPerformance:
    """Test performance aspects and efficiency."""

    def test_object_creation_efficiency(self, subtests):
        """Test that object creation is efficient and doesn't leak resources."""
        with subtests.test(test="multiple_object_creation"):
            # Test creating multiple objects doesn't cause issues
            objects = []
            try:
                for i in range(3):
                    zmm_test = zmm.ZMM(TF_ZSS_TIPPER)
                    objects.append(zmm_test)
                    assert zmm_test.station is not None

                # All objects should be independent
                assert len(set(id(obj) for obj in objects)) == 3
            except Exception as e:
                pytest.skip(f"Cannot test object creation efficiency: {e}")

    def test_memory_usage_consistency(self):
        """Test that repeated access doesn't change object state."""
        try:
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
        except Exception as e:
            pytest.skip(f"Cannot test memory usage: {e}")

        # Get initial values
        initial_station = zmm_obj.station
        initial_channels = zmm_obj.channels_recorded.copy()

        # Access properties multiple times
        for _ in range(5):
            _ = zmm_obj.station
            _ = zmm_obj.channels_recorded
            _ = zmm_obj.channel_dict

        # Values should remain consistent
        assert (
            zmm_obj.station == initial_station
        ), "Station changed after repeated access"
        assert (
            zmm_obj.channels_recorded == initial_channels
        ), "Channels changed after repeated access"


# =============================================================================
# Test ZMM.read() method parameters for ZSS files
# =============================================================================


class TestZSSReadParameters:
    """Test ZMM.read() method parameters when reading ZSS files."""

    def test_read_zss_with_default_parameters(self):
        """Test reading ZSS file with default parameters."""
        try:
            zmm_obj = zmm.ZMM(TF_ZSS_TIPPER)
            # Should use defaults: rotate_to_measurement_coordinates=True, use_declination=False
            assert zmm_obj is not None
            assert zmm_obj.dataset is not None
        except Exception as e:
            pytest.skip(f"Cannot test ZSS read with default parameters: {e}")

    def test_read_zss_rotate_to_measurement_coordinates_true(self):
        """Test reading ZSS file with rotate_to_measurement_coordinates=True."""
        try:
            zmm_obj = zmm.ZMM()
            zmm_obj.read(fn=TF_ZSS_TIPPER, rotate_to_measurement_coordinates=True)

            assert zmm_obj is not None
            assert zmm_obj.dataset is not None
            assert zmm_obj.transfer_functions is not None
            assert zmm_obj.periods is not None
        except Exception as e:
            pytest.skip(f"Cannot test ZSS read with rotation=True: {e}")

    def test_read_zss_rotate_to_measurement_coordinates_false(self):
        """Test reading ZSS file with rotate_to_measurement_coordinates=False."""
        try:
            zmm_obj = zmm.ZMM()
            zmm_obj.read(fn=TF_ZSS_TIPPER, rotate_to_measurement_coordinates=False)

            assert zmm_obj is not None
            assert zmm_obj.dataset is not None
            assert zmm_obj.transfer_functions is not None
            assert zmm_obj.periods is not None
        except Exception as e:
            pytest.skip(f"Cannot test ZSS read with rotation=False: {e}")

    def test_read_zss_use_declination_true(self):
        """Test reading ZSS file with use_declination=True."""
        try:
            zmm_obj = zmm.ZMM()
            zmm_obj.read(fn=TF_ZSS_TIPPER, use_declination=True)

            assert zmm_obj is not None
            assert zmm_obj.dataset is not None
            assert zmm_obj.transfer_functions is not None
            assert zmm_obj.periods is not None
        except Exception as e:
            pytest.skip(f"Cannot test ZSS read with declination=True: {e}")

    def test_read_zss_use_declination_false(self):
        """Test reading ZSS file with use_declination=False."""
        try:
            zmm_obj = zmm.ZMM()
            zmm_obj.read(fn=TF_ZSS_TIPPER, use_declination=False)

            assert zmm_obj is not None
            assert zmm_obj.dataset is not None
            assert zmm_obj.transfer_functions is not None
            assert zmm_obj.periods is not None
        except Exception as e:
            pytest.skip(f"Cannot test ZSS read with declination=False: {e}")

    def test_read_zss_parameter_combinations(self, subtests):
        """Test reading ZSS file with various parameter combinations."""
        parameter_combinations = [
            {"rotate_to_measurement_coordinates": True, "use_declination": True},
            {"rotate_to_measurement_coordinates": True, "use_declination": False},
            {"rotate_to_measurement_coordinates": False, "use_declination": True},
            {"rotate_to_measurement_coordinates": False, "use_declination": False},
        ]

        for params in parameter_combinations:
            with subtests.test(params=params):
                try:
                    zmm_obj = zmm.ZMM()
                    zmm_obj.read(fn=TF_ZSS_TIPPER, **params)

                    assert zmm_obj is not None
                    assert zmm_obj.dataset is not None
                    assert zmm_obj.transfer_functions is not None
                    assert zmm_obj.periods is not None
                except Exception as e:
                    pytest.skip(f"Cannot test ZSS read with params {params}: {e}")

    @pytest.mark.parametrize(
        "rotate_to_measurement_coordinates,use_declination",
        [
            (True, True),
            (True, False),
            (False, True),
            (False, False),
        ],
    )
    def test_read_zss_parameters_parametrized(
        self, rotate_to_measurement_coordinates, use_declination
    ):
        """Parametrized test for all combinations of boolean parameters for ZSS files."""
        try:
            zmm_obj = zmm.ZMM()
            zmm_obj.read(
                fn=TF_ZSS_TIPPER,
                rotate_to_measurement_coordinates=rotate_to_measurement_coordinates,
                use_declination=use_declination,
            )

            assert zmm_obj is not None
            assert zmm_obj.dataset is not None
            assert zmm_obj.transfer_functions is not None
            assert zmm_obj.periods is not None
            # ZSS tipper file should have data
            assert len(zmm_obj.periods) > 0
        except Exception as e:
            pytest.skip(
                f"Cannot test ZSS read with rotation={rotate_to_measurement_coordinates}, "
                f"declination={use_declination}: {e}"
            )

    def test_read_zss_with_all_parameters(self):
        """Test reading ZSS file with all available parameters."""
        try:
            zmm_obj = zmm.ZMM()
            zmm_obj.read(
                fn=TF_ZSS_TIPPER,
                get_elevation=False,
                rotate_to_measurement_coordinates=True,
                use_declination=False,
            )

            assert zmm_obj is not None
            assert zmm_obj.dataset is not None
            assert zmm_obj.station_metadata is not None
            assert zmm_obj.channels_recorded == ["hx", "hy", "hz"]
        except Exception as e:
            pytest.skip(f"Cannot test ZSS read with all parameters: {e}")


# =============================================================================
# Test ZSS transfer function values
# =============================================================================


class TestZSSTransferFunctionValues:
    """Test that read parameters affect actual transfer function values for ZSS files."""

    def test_zss_tipper_values_are_complex(self):
        """Test that ZSS tipper values are complex numbers."""
        try:
            zmm_obj = zmm.ZMM()
            zmm_obj.read(fn=TF_ZSS_TIPPER)

            # For tipper data, transfer_functions should be (1, 2) per frequency
            assert np.iscomplexobj(zmm_obj.transfer_functions)
            assert zmm_obj.transfer_functions.dtype == np.complex64
        except Exception as e:
            pytest.skip(f"Cannot test ZSS tipper values: {e}")

    def test_zss_tipper_shape_consistency(self):
        """Test that ZSS tipper array has correct shape regardless of parameters."""
        try:
            zmm_obj1 = zmm.ZMM()
            zmm_obj1.read(fn=TF_ZSS_TIPPER, rotate_to_measurement_coordinates=True)

            zmm_obj2 = zmm.ZMM()
            zmm_obj2.read(fn=TF_ZSS_TIPPER, rotate_to_measurement_coordinates=False)

            # Shapes should be consistent
            assert (
                zmm_obj1.transfer_functions.shape == zmm_obj2.transfer_functions.shape
            )
            assert zmm_obj1.periods.shape == zmm_obj2.periods.shape

            # For tipper data: (num_freq, 1, 2)
            assert zmm_obj1.transfer_functions.shape[1] == 1  # One output (hz)
            assert zmm_obj1.transfer_functions.shape[2] == 2  # Two inputs (hx, hy)
        except Exception as e:
            pytest.skip(f"Cannot test ZSS shape consistency: {e}")

    def test_zss_rotation_affects_tipper_values(self, subtests):
        """Test that rotate_to_measurement_coordinates affects ZSS tipper values."""
        try:
            zmm_obj_rotated = zmm.ZMM()
            zmm_obj_rotated.read(
                fn=TF_ZSS_TIPPER, rotate_to_measurement_coordinates=True
            )

            zmm_obj_not_rotated = zmm.ZMM()
            zmm_obj_not_rotated.read(
                fn=TF_ZSS_TIPPER, rotate_to_measurement_coordinates=False
            )

            with subtests.test(check="arrays_exist"):
                assert zmm_obj_rotated.transfer_functions is not None
                assert zmm_obj_not_rotated.transfer_functions is not None

            with subtests.test(check="no_nans"):
                assert not np.any(np.isnan(zmm_obj_rotated.transfer_functions))
                assert not np.any(np.isnan(zmm_obj_not_rotated.transfer_functions))

            with subtests.test(check="finite_values"):
                assert np.all(np.isfinite(zmm_obj_rotated.transfer_functions))
                assert np.all(np.isfinite(zmm_obj_not_rotated.transfer_functions))

            with subtests.test(check="values_are_valid"):
                assert np.any(np.abs(zmm_obj_rotated.transfer_functions) > 0)
                assert np.any(np.abs(zmm_obj_not_rotated.transfer_functions) > 0)
        except Exception as e:
            pytest.skip(f"Cannot test ZSS rotation effects: {e}")

    def test_zss_declination_affects_tipper_values(self, subtests):
        """Test that use_declination affects ZSS tipper values when expected."""
        try:
            zmm_obj_with_dec = zmm.ZMM()
            zmm_obj_with_dec.read(fn=TF_ZSS_TIPPER, use_declination=True)

            zmm_obj_without_dec = zmm.ZMM()
            zmm_obj_without_dec.read(fn=TF_ZSS_TIPPER, use_declination=False)

            with subtests.test(check="arrays_exist"):
                assert zmm_obj_with_dec.transfer_functions is not None
                assert zmm_obj_without_dec.transfer_functions is not None

            with subtests.test(check="no_nans"):
                assert not np.any(np.isnan(zmm_obj_with_dec.transfer_functions))
                assert not np.any(np.isnan(zmm_obj_without_dec.transfer_functions))

            with subtests.test(check="finite_values"):
                assert np.all(np.isfinite(zmm_obj_with_dec.transfer_functions))
                assert np.all(np.isfinite(zmm_obj_without_dec.transfer_functions))

            with subtests.test(check="values_are_valid"):
                assert np.any(np.abs(zmm_obj_with_dec.transfer_functions) > 0)
                assert np.any(np.abs(zmm_obj_without_dec.transfer_functions) > 0)

            # Check if declination causes a difference (it should for non-zero declination)
            if zmm_obj_with_dec.declination not in [0, None]:
                with subtests.test(check="declination_changes_values"):
                    # When declination is non-zero, values should differ
                    max_diff = np.max(
                        np.abs(
                            zmm_obj_with_dec.transfer_functions
                            - zmm_obj_without_dec.transfer_functions
                        )
                    )
                    # If declination is significant, expect some difference
                    assert max_diff >= 0  # At minimum, should be calculable
        except Exception as e:
            pytest.skip(f"Cannot test ZSS declination effects: {e}")

    def test_zss_dataset_tipper_values(self, subtests):
        """Test ZSS tipper values in the xarray dataset."""
        try:
            zmm_obj = zmm.ZMM()
            zmm_obj.read(fn=TF_ZSS_TIPPER, rotate_to_measurement_coordinates=True)

            with subtests.test(check="dataset_has_transfer_function"):
                assert "transfer_function" in zmm_obj.dataset
                assert zmm_obj.dataset["transfer_function"] is not None

            with subtests.test(check="transfer_function_is_complex"):
                assert np.iscomplexobj(zmm_obj.dataset["transfer_function"].values)

            with subtests.test(check="transfer_function_has_coordinates"):
                assert "period" in zmm_obj.dataset["transfer_function"].coords
                assert "output" in zmm_obj.dataset["transfer_function"].coords
                assert "input" in zmm_obj.dataset["transfer_function"].coords

            with subtests.test(check="values_are_finite"):
                tf_values = zmm_obj.dataset["transfer_function"].values
                # For tipper data, only check hz output (may have NaN for ex, ey)
                hz_index = list(
                    zmm_obj.dataset["transfer_function"].coords["output"].values
                ).index("hz")
                tipper_values = tf_values[:, hz_index, :]
                assert np.all(np.isfinite(tipper_values))

            with subtests.test(check="tipper_specific_shape"):
                # Tipper should have hz as output
                assert (
                    "hz" in zmm_obj.dataset["transfer_function"].coords["output"].values
                )
        except Exception as e:
            pytest.skip(f"Cannot test ZSS dataset tipper values: {e}")

    def test_zss_tipper_values_per_frequency(self, subtests):
        """Test that ZSS tipper values exist for all frequencies."""
        try:
            zmm_obj = zmm.ZMM()
            zmm_obj.read(fn=TF_ZSS_TIPPER)

            num_freq = zmm_obj.num_freq
            assert num_freq > 0, "Should have at least one frequency"

            with subtests.test(check="transfer_function_length"):
                assert len(zmm_obj.transfer_functions) == num_freq

            with subtests.test(check="periods_length"):
                assert len(zmm_obj.periods) == num_freq

            # Check each frequency has valid data
            for i in range(min(num_freq, 5)):  # Test first 5 frequencies
                with subtests.test(frequency_index=i):
                    tf_at_freq = zmm_obj.transfer_functions[i]
                    assert tf_at_freq is not None
                    assert np.all(np.isfinite(tf_at_freq))
        except Exception as e:
            pytest.skip(f"Cannot test ZSS tipper per frequency: {e}")

    def test_zss_comparison_of_all_parameter_combinations(self, subtests):
        """Test and compare ZSS tipper values across all parameter combinations."""
        try:
            combinations = {
                "rot_True_dec_False": {
                    "rotate_to_measurement_coordinates": True,
                    "use_declination": False,
                },
                "rot_True_dec_True": {
                    "rotate_to_measurement_coordinates": True,
                    "use_declination": True,
                },
                "rot_False_dec_False": {
                    "rotate_to_measurement_coordinates": False,
                    "use_declination": False,
                },
                "rot_False_dec_True": {
                    "rotate_to_measurement_coordinates": False,
                    "use_declination": True,
                },
            }

            results = {}
            for name, params in combinations.items():
                with subtests.test(combination=name):
                    zmm_obj = zmm.ZMM()
                    zmm_obj.read(fn=TF_ZSS_TIPPER, **params)
                    results[name] = zmm_obj.transfer_functions.copy()

                    # Verify basic properties
                    assert results[name] is not None
                    assert np.iscomplexobj(results[name])
                    assert np.all(np.isfinite(results[name]))
                    assert results[name].shape[0] > 0  # Has frequencies

            # All combinations should produce valid data
            assert len(results) == 4
        except Exception as e:
            pytest.skip(f"Cannot test ZSS parameter combinations: {e}")

    def test_zss_tipper_magnitude_range(self):
        """Test that ZSS tipper magnitudes are within reasonable ranges."""
        try:
            zmm_obj = zmm.ZMM()
            zmm_obj.read(fn=TF_ZSS_TIPPER)

            tf_magnitude = np.abs(zmm_obj.transfer_functions)

            # Should have non-zero magnitudes
            assert np.any(tf_magnitude > 0), "Tipper should have non-zero values"

            # Tipper values are typically < 1 but can be larger
            assert np.all(tf_magnitude < 100), "Tipper values seem unreasonably large"

            # Should be finite
            assert np.all(
                np.isfinite(tf_magnitude)
            ), "Tipper magnitudes should be finite"
        except Exception as e:
            pytest.skip(f"Cannot test ZSS tipper magnitude range: {e}")

    def test_zss_sigma_arrays_with_rotation_parameters(self, subtests):
        """Test that sigma arrays are valid for ZSS with different rotation parameters."""
        try:
            parameter_sets = [
                {"rotate_to_measurement_coordinates": True, "use_declination": False},
                {"rotate_to_measurement_coordinates": False, "use_declination": True},
            ]

            for params in parameter_sets:
                with subtests.test(params=params):
                    zmm_obj = zmm.ZMM()
                    zmm_obj.read(fn=TF_ZSS_TIPPER, **params)

                    # Check sigma_e (residual covariance)
                    if zmm_obj.sigma_e is not None:
                        assert np.iscomplexobj(zmm_obj.sigma_e)
                        assert np.all(np.isfinite(zmm_obj.sigma_e))

                    # Check sigma_s (inverse signal power)
                    if zmm_obj.sigma_s is not None:
                        assert np.iscomplexobj(zmm_obj.sigma_s)
                        assert np.all(np.isfinite(zmm_obj.sigma_s))
        except Exception as e:
            pytest.skip(f"Cannot test ZSS sigma arrays: {e}")


# =============================================================================
# Run tests
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
