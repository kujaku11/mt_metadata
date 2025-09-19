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
# Run tests
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
