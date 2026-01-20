"""
Test module for ChannelWeightSpec file loading functionality.
Converted to pytest with fixtures for improved maintainability and efficiency.
"""

import inspect
import json
import pathlib

import pytest

import mt_metadata
from mt_metadata.features.weights.channel_weight_spec import ChannelWeightSpec

# Path setup
init_file = inspect.getfile(mt_metadata)
MT_METADATA_PATH = pathlib.Path(init_file).parent.parent
TEST_PATH = MT_METADATA_PATH.joinpath("tests")
TEST_HELPERS_PATH = MT_METADATA_PATH.joinpath("mt_metadata", "features", "test_helpers")


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture(scope="session")
def channel_weight_specs_json_path():
    """Path to the example JSON file containing channel weight specs."""
    return TEST_HELPERS_PATH.joinpath("channel_weight_specs_example.json")


@pytest.fixture(scope="session")
def channel_weight_specs_data(channel_weight_specs_json_path):
    """Raw data loaded from the channel weight specs JSON file."""
    with open(channel_weight_specs_json_path, "r") as f:
        data = json.load(f)
    return data.get("channel_weight_specs", data)


@pytest.fixture
def channel_weight_spec_dicts(channel_weight_specs_data):
    """Individual channel weight spec dictionaries from the test data."""
    return channel_weight_specs_data


@pytest.fixture(params=range(3))  # Actual number of specs in test data
def single_channel_weight_spec_dict(channel_weight_specs_data, request):
    """Parametrized fixture providing individual channel weight spec dictionaries."""
    if request.param < len(channel_weight_specs_data):
        return channel_weight_specs_data[request.param]
    pytest.skip(
        f"Test data only contains {len(channel_weight_specs_data)} channel weight specs"
    )


@pytest.fixture
def loaded_channel_weight_spec(single_channel_weight_spec_dict):
    """A ChannelWeightSpec instance loaded from test data."""
    cws = ChannelWeightSpec()
    cws.from_dict(single_channel_weight_spec_dict)
    return cws


# ============================================================================
# TEST CLASSES
# ============================================================================


@pytest.mark.file_loading
class TestChannelWeightSpecFromFile:
    """Test cases for loading ChannelWeightSpec from JSON files."""

    def test_json_file_exists(self, channel_weight_specs_json_path):
        """Test that the example JSON file exists and is readable."""
        assert (
            channel_weight_specs_json_path.exists()
        ), f"JSON file not found: {channel_weight_specs_json_path}"
        assert (
            channel_weight_specs_json_path.is_file()
        ), f"Path is not a file: {channel_weight_specs_json_path}"

    def test_json_data_structure(self, channel_weight_specs_data):
        """Test that the JSON data has the expected structure."""
        assert isinstance(
            channel_weight_specs_data, list
        ), "Expected channel_weight_specs to be a list"
        assert (
            len(channel_weight_specs_data) >= 1
        ), "Expected at least one channel weight spec in test data"

        # Verify each item is a dictionary
        for i, spec_dict in enumerate(channel_weight_specs_data):
            assert isinstance(
                spec_dict, dict
            ), f"Channel weight spec {i} should be a dictionary"

    def test_load_channel_weight_spec_from_dict(self, single_channel_weight_spec_dict):
        """Test loading a single ChannelWeightSpec from dictionary data."""
        cws = ChannelWeightSpec()
        cws.from_dict(single_channel_weight_spec_dict)

        # Basic object validation
        assert isinstance(cws, ChannelWeightSpec)
        assert hasattr(cws, "feature_weight_specs")

    def test_loaded_channel_weight_spec_properties(self, loaded_channel_weight_spec):
        """Test properties of a loaded ChannelWeightSpec instance."""
        cws = loaded_channel_weight_spec

        # Verify basic properties
        assert isinstance(cws, ChannelWeightSpec)
        assert hasattr(cws, "feature_weight_specs")
        assert hasattr(cws, "output_channels")
        assert hasattr(cws, "combination_style")

    def test_feature_weight_specs_count(self, loaded_channel_weight_spec):
        """Test that loaded specs have the expected number of feature weight specs."""
        assert (
            len(loaded_channel_weight_spec.feature_weight_specs) >= 1
        ), "Expected at least one feature weight spec"

    def test_load_all_channel_weight_specs(self, channel_weight_spec_dicts):
        """Test loading all channel weight specs from the test file."""
        loaded_specs = []

        for cws_dict in channel_weight_spec_dicts:
            cws = ChannelWeightSpec()
            cws.from_dict(cws_dict)
            loaded_specs.append(cws)

            # Validate each loaded spec
            assert isinstance(cws, ChannelWeightSpec)
            assert hasattr(cws, "feature_weight_specs")
            assert len(cws.feature_weight_specs) >= 1

        assert len(loaded_specs) == len(
            channel_weight_spec_dicts
        ), "Should load same number of specs as in test data"

    @pytest.mark.parametrize(
        "expected_attributes",
        ["feature_weight_specs", "output_channels", "combination_style"],
    )
    def test_loaded_spec_has_attributes(
        self, loaded_channel_weight_spec, expected_attributes
    ):
        """Test that loaded specs have expected attributes."""
        assert hasattr(
            loaded_channel_weight_spec, expected_attributes
        ), f"ChannelWeightSpec should have attribute: {expected_attributes}"


@pytest.mark.file_loading
@pytest.mark.integration
class TestChannelWeightSpecFileIntegration:
    """Integration tests for ChannelWeightSpec file loading with validation."""

    def test_complete_file_loading_workflow(self, channel_weight_specs_json_path):
        """Test the complete workflow of loading specs from file."""
        # Load file
        with open(channel_weight_specs_json_path, "r") as f:
            data = json.load(f)

        # Extract specs
        channel_weight_specs = data.get("channel_weight_specs", data)
        assert len(channel_weight_specs) >= 1

        # Load each spec
        loaded_specs = []
        for cws_dict in channel_weight_specs:
            cws = ChannelWeightSpec()
            cws.from_dict(cws_dict)
            loaded_specs.append(cws)

        # Validate results
        assert len(loaded_specs) == len(channel_weight_specs)
        for spec in loaded_specs:
            assert isinstance(spec, ChannelWeightSpec)
            assert len(spec.feature_weight_specs) >= 1

    def test_json_content_validity(self, channel_weight_specs_data):
        """Test that the JSON content contains valid ChannelWeightSpec data."""
        for i, spec_dict in enumerate(channel_weight_specs_data):
            # Check for required top-level structure
            if "channel_weight_spec" in spec_dict:
                inner_spec = spec_dict["channel_weight_spec"]
                assert (
                    "feature_weight_specs" in inner_spec
                ), f"Spec {i} missing feature_weight_specs"
                assert isinstance(
                    inner_spec["feature_weight_specs"], list
                ), f"Spec {i} feature_weight_specs should be a list"
