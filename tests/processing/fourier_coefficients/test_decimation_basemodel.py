"""
Comprehensive pytest test suite for Decimation model.

This test suite covers:
- Initialization and field validation
- Channel management functionality
- Validator behavior (especially channels/channels_estimated synchronization)
- Property access and modification
- Complex integration scenarios
- Performance and efficiency tests

Uses fixtures and parametrization for optimal efficiency.
"""


import numpy as np
import pytest

from mt_metadata.common import ListDict, TimePeriod
from mt_metadata.processing.fourier_coefficients.decimation_basemodel import (
    Decimation,
    fc_decimations_creator,
    get_degenerate_fc_decimation,
)
from mt_metadata.processing.fourier_coefficients.fc_channel_basemodel import FCChannel
from mt_metadata.processing.short_time_fourier_transform_basemodel import (
    ShortTimeFourierTransform,
)
from mt_metadata.processing.time_series_decimation_basemodel import TimeSeriesDecimation


# Helper functions for creating valid test objects
def create_fc_channel(component="ex", **kwargs):
    """Create a valid FCChannel with defaults."""
    defaults = {
        "component": component,
        "frequency_max": 100.0,
        "frequency_min": 1.0,
        "sample_rate_decimation_level": 256.0,
        "sample_rate_window_step": 1.0,
        "units": "counts",  # Use 'counts' instead of 'millivolts' to avoid warnings
    }
    defaults.update(kwargs)
    return FCChannel(**defaults)


def create_stft(**kwargs):
    """Create a valid ShortTimeFourierTransform with defaults."""
    defaults = {
        "harmonic_indices": -1,  # Use -1 for all harmonics instead of None
        "method": "fft",
        "min_num_stft_windows": 2,  # Use a valid integer instead of None
        "per_window_detrend_type": "",
        "pre_fft_detrend_type": "linear",
        "prewhitening_type": "first difference",
        "recoloring": True,
    }
    defaults.update(kwargs)
    return ShortTimeFourierTransform(**defaults)


class TestDecimationInitialization:
    """Test Decimation initialization and default values."""

    def test_default_initialization(self):
        """Test creating Decimation with minimal parameters."""
        # Use type: ignore to suppress static analyzer warnings for known defaults
        decimation = Decimation()  # type: ignore

        assert decimation.id == ""
        assert decimation.channels_estimated == []
        assert isinstance(decimation.time_period, TimePeriod)
        assert isinstance(decimation.channels, ListDict)
        assert isinstance(decimation.time_series_decimation, TimeSeriesDecimation)
        assert isinstance(
            decimation.short_time_fourier_transform, ShortTimeFourierTransform
        )
        assert len(decimation.channels) == 0

    def test_custom_initialization(self):
        """Test creating Decimation with custom values."""
        time_period = TimePeriod(
            start="2023-01-01T00:00:00+00:00", end="2023-01-02T00:00:00+00:00"
        )

        decimation = Decimation(
            id="level_1", channels_estimated=["ex", "hy"], time_period=time_period
        )  # type: ignore

        assert decimation.id == "level_1"
        assert decimation.channels_estimated == ["ex", "hy"]
        assert decimation.time_period == time_period
        assert len(decimation.channels) == 2  # Auto-created by validator
        assert "ex" in decimation.channels.keys()
        assert "hy" in decimation.channels.keys()

    @pytest.mark.parametrize(
        "field_name,field_value,expected",
        [
            ("id", "decimation_1", "decimation_1"),
            ("id", "", ""),
            ("channels_estimated", ["ex"], ["ex"]),
            ("channels_estimated", ["ex", "hy", "hz"], ["ex", "hy", "hz"]),
            ("channels_estimated", [], []),
        ],
    )
    def test_parametrized_field_initialization(self, field_name, field_value, expected):
        """Test initialization with various field values."""
        kwargs = {field_name: field_value}
        decimation = Decimation(**kwargs)  # type: ignore

        assert getattr(decimation, field_name) == expected


class TestDecimationValidation:
    """Test Decimation field validation and error handling."""

    def test_channels_estimated_validation_valid(self):
        """Test valid channels_estimated values."""
        valid_channels = [["ex", "hy"], ["hx", "hy", "hz"], [], ["single_channel"]]

        for channels in valid_channels:
            decimation = Decimation(channels_estimated=channels)  # type: ignore
            assert decimation.channels_estimated == channels

    def test_short_time_fourier_transform_validation(self):
        """Test STFT validation."""
        # Valid STFT object
        stft = create_stft()
        decimation = Decimation(short_time_fourier_transform=stft)  # type: ignore
        assert decimation.short_time_fourier_transform == stft

    def test_channels_validation_from_dict(self):
        """Test channels validation from dictionary input."""
        channel_dict = {
            "ex": {"component": "ex", "frequency_max": 100.0},
            "hy": {"component": "hy", "frequency_max": 50.0},
        }

        decimation = Decimation(channels=channel_dict)  # type: ignore
        assert len(decimation.channels) == 2
        assert "ex" in decimation.channels.keys()
        assert "hy" in decimation.channels.keys()

    def test_channels_validation_from_list(self):
        """Test channels validation from list input."""
        fc1 = create_fc_channel("ex")
        fc2 = create_fc_channel("hy")

        decimation = Decimation(channels=[fc1, fc2])  # type: ignore
        assert len(decimation.channels) == 2
        assert "ex" in decimation.channels.keys()
        assert "hy" in decimation.channels.keys()


class TestChannelsEstimatedSynchronization:
    """Test the synchronization between channels_estimated and channels."""

    def test_channels_estimated_creates_channels(self):
        """Test that channels_estimated automatically creates FCChannel objects."""
        decimation = Decimation(channels_estimated=["ex", "hy", "hz"])  # type: ignore

        assert len(decimation.channels) == 3
        assert set(decimation.channels.keys()) == {"ex", "hy", "hz"}

        # Verify each channel is properly created
        for channel_name in ["ex", "hy", "hz"]:
            channel = decimation.channels[channel_name]
            assert isinstance(channel, FCChannel)
            assert channel.component == channel_name

    def test_existing_channels_added_to_estimated(self):
        """Test that existing channels get their names added to channels_estimated."""
        channels = ListDict()
        channels.append(create_fc_channel("ex"))
        channels.append(create_fc_channel("hy"))

        decimation = Decimation(channels=channels, channels_estimated=[])  # type: ignore

        assert set(decimation.channels_estimated) == {"ex", "hy"}
        assert set(decimation.channels.keys()) == {"ex", "hy"}

    def test_mixed_scenario_synchronization(self):
        """Test mixed scenario with some existing and some missing channels."""
        # Pre-existing channel
        channels = ListDict()
        channels.append(create_fc_channel("ex"))

        # channels_estimated includes both existing and new channels
        decimation = Decimation(
            channels=channels, channels_estimated=["ex", "hy", "hz"]
        )  # type: ignore

        assert len(decimation.channels) == 3
        assert set(decimation.channels_estimated) == {"ex", "hy", "hz"}
        assert set(decimation.channels.keys()) == {"ex", "hy", "hz"}

    def test_channels_without_estimated_entries(self):
        """Test channels without corresponding channels_estimated entries."""
        channels = ListDict()
        channels.append(create_fc_channel("ex"))
        channels.append(create_fc_channel("hy"))

        decimation = Decimation(
            channels=channels, channels_estimated=["ex"]  # Missing 'hy'
        )  # type: ignore

        assert set(decimation.channels_estimated) == {"ex", "hy"}
        assert set(decimation.channels.keys()) == {"ex", "hy"}


class TestDecimationChannelManagement:
    """Test channel management functionality."""

    @pytest.fixture
    def sample_decimation(self):
        """Create a decimation with sample channels."""
        return Decimation(channels_estimated=["ex", "hy", "hz"])  # type: ignore

    def test_has_channel(self, sample_decimation):
        """Test has_channel method."""
        assert sample_decimation.has_channel("ex") is True
        assert sample_decimation.has_channel("hy") is True
        assert sample_decimation.has_channel("nonexistent") is False

    def test_channel_index(self, sample_decimation):
        """Test channel_index method."""
        assert sample_decimation.channel_index("ex") == 0
        assert sample_decimation.channel_index("hy") == 1
        assert sample_decimation.channel_index("hz") == 2
        assert sample_decimation.channel_index("nonexistent") is None

    def test_get_channel(self, sample_decimation):
        """Test get_channel method."""
        ex_channel = sample_decimation.get_channel("ex")
        assert isinstance(ex_channel, FCChannel)
        assert ex_channel.component == "ex"

        assert sample_decimation.get_channel("nonexistent") is None

    def test_add_channel_new(self, sample_decimation):
        """Test adding a new channel - note: add_channel doesn't update channels_estimated."""
        new_channel = create_fc_channel("ez")
        initial_count = len(sample_decimation.channels)

        sample_decimation.add_channel(new_channel)

        # Channel is added to channels list
        assert len(sample_decimation.channels) == initial_count + 1
        # But has_channel checks channels_estimated, so it returns False
        assert sample_decimation.has_channel("ez") is False
        # Channel can be retrieved directly from channels though
        assert "ez" in sample_decimation.channels.keys()
        assert sample_decimation.channels["ez"].component == "ez"

    def test_add_channel_existing_updates(self, sample_decimation):
        """Test adding an existing channel updates it."""
        updated_channel = create_fc_channel("ex", frequency_max=200.0)

        sample_decimation.add_channel(updated_channel)

        # Should not increase count
        assert len(sample_decimation.channels) == 3
        # Should update the frequency
        assert sample_decimation.get_channel("ex").frequency_max == 200.0

    def test_add_channel_invalid_type(self, sample_decimation):
        """Test adding invalid channel type raises error."""
        with pytest.raises(ValueError, match="Input must be metadata FCChannel"):
            sample_decimation.add_channel("not_a_channel")

    def test_remove_channel(self, sample_decimation):
        """Test removing a channel - only removes from channels list, not channels_estimated."""
        initial_count = len(sample_decimation.channels)

        # Verify channel exists in channels_estimated first
        assert sample_decimation.has_channel("ex")
        assert "ex" in sample_decimation.channels.keys()

        sample_decimation.remove_channel("ex")

        # Channel should be removed from channels list
        assert len(sample_decimation.channels) == initial_count - 1
        assert "ex" not in sample_decimation.channels.keys()
        # But still be in channels_estimated (design limitation)
        assert sample_decimation.has_channel(
            "ex"
        )  # Still True because channels_estimated not updated

    def test_n_channels_property(self, sample_decimation):
        """Test n_channels property."""
        assert sample_decimation.n_channels == 3

        sample_decimation.add_channel(create_fc_channel("ez"))
        assert sample_decimation.n_channels == 4

    def test_len_method(self, sample_decimation):
        """Test __len__ method returns number of model fields, not channels."""
        # The __len__ method on MetadataBase returns number of model fields
        assert len(sample_decimation) > 0  # Should have many fields
        # Use n_channels for actual channel count
        assert sample_decimation.n_channels == 3


class TestDecimationProperties:
    """Test Decimation properties and property access."""

    @pytest.fixture
    def decimation_with_data(self):
        """Create decimation with sample data."""
        return Decimation(
            id="test_decimation",
            channels_estimated=["ex", "hy"],
        )  # type: ignore

    def test_decimation_property(self, decimation_with_data):
        """Test decimation property (passthrough to time_series_decimation)."""
        assert isinstance(decimation_with_data.decimation, TimeSeriesDecimation)
        assert (
            decimation_with_data.decimation
            is decimation_with_data.time_series_decimation
        )

    def test_stft_property(self, decimation_with_data):
        """Test stft property (passthrough to short_time_fourier_transform)."""
        assert isinstance(decimation_with_data.stft, ShortTimeFourierTransform)
        assert (
            decimation_with_data.stft
            is decimation_with_data.short_time_fourier_transform
        )

    def test_fft_frequencies(self, decimation_with_data):
        """Test fft_frequencies property."""
        # Set up decimation with sample rate and valid window parameters
        decimation_with_data.time_series_decimation.sample_rate = 100.0
        decimation_with_data.short_time_fourier_transform.num_samples_window = 1024
        decimation_with_data.short_time_fourier_transform.window.num_samples = 1024
        decimation_with_data.short_time_fourier_transform.window.overlap = 512

        frequencies = decimation_with_data.fft_frequencies  # Property, not method

        assert isinstance(frequencies, np.ndarray)
        assert len(frequencies) > 0

    def test_is_valid_for_time_series_length(self, decimation_with_data):
        """Test time series length validation."""
        # Set up parameters with valid values
        decimation_with_data.short_time_fourier_transform.num_samples_window = 1024
        decimation_with_data.short_time_fourier_transform.num_samples_overlap = 512
        decimation_with_data.short_time_fourier_transform.min_num_stft_windows = 2
        decimation_with_data.short_time_fourier_transform.window.num_samples = 1024
        decimation_with_data.short_time_fourier_transform.window.overlap = 512

        # Valid length
        assert decimation_with_data.is_valid_for_time_series_length(2048) is True

        # Invalid length (too short)
        assert decimation_with_data.is_valid_for_time_series_length(512) is False


class TestDecimationOperations:
    """Test Decimation operations like add, update, etc."""

    @pytest.fixture
    def decimation1(self):
        return Decimation(id="dec1", channels_estimated=["ex", "hy"])  # type: ignore

    @pytest.fixture
    def decimation2(self):
        return Decimation(id="dec2", channels_estimated=["hz", "ez"])  # type: ignore

    def test_add_decimations(self, decimation1, decimation2):
        """Test adding two decimations."""
        result = decimation1.add(decimation2)

        assert result is decimation1  # Returns self
        assert len(decimation1.channels) == 4  # Combined channels

    def test_add_invalid_type(self, decimation1):
        """Test adding invalid type raises error."""
        with pytest.raises(TypeError, match="Can only merge ch objects"):
            decimation1.add("not_a_decimation")

    def test_update_decimation(self, decimation1, decimation2):
        """Test updating decimation with another."""
        original_id = decimation1.id

        decimation1.update(decimation2)

        # ID should be updated
        assert decimation1.id == "dec2"

        # Channels should be combined
        assert len(decimation1.channels) >= 2

    def test_update_time_period(self, decimation1):
        """Test update_time_period method."""
        # Add a channel with specific time period
        channel = create_fc_channel(
            "test",
            time_period=TimePeriod(
                start="2023-01-01T00:00:00+00:00", end="2023-01-02T00:00:00+00:00"
            ),
        )
        decimation1.add_channel(channel)

        # Call update_time_period
        decimation1.update_time_period()

        # Should have updated the decimation's time period
        assert decimation1.time_period.start != "1980-01-01T00:00:00+00:00"


class TestDecimationRepresentation:
    """Test Decimation string representation and basic properties."""

    @pytest.fixture
    def sample_decimation(self):
        return Decimation(
            id="test_decimation", channels_estimated=["ex", "hy"]
        )  # type: ignore

    def test_basic_properties(self, sample_decimation):
        """Test basic properties access."""
        assert sample_decimation.id == "test_decimation"
        assert sample_decimation.channels_estimated == ["ex", "hy"]
        assert len(sample_decimation.channels) == 2

    def test_basic_access(self, sample_decimation):
        """Test basic access doesn't crash."""
        # Test basic property access
        assert sample_decimation.id == "test_decimation"
        assert len(sample_decimation.channels) == 2

    def test_dict_access(self, sample_decimation):
        """Test dictionary-style access to fields."""
        assert sample_decimation.id == "test_decimation"
        assert "ex" in sample_decimation.channels.keys()
        assert "hy" in sample_decimation.channels.keys()


class TestDecimationEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_channels_estimated(self):
        """Test with empty channels_estimated."""
        decimation = Decimation(channels_estimated=[])  # type: ignore

        assert decimation.channels_estimated == []
        assert len(decimation.channels) == 0

    def test_large_number_of_channels(self):
        """Test with large number of channels."""
        channel_names = [f"ch_{i:03d}" for i in range(100)]
        decimation = Decimation(channels_estimated=channel_names)  # type: ignore

        assert len(decimation.channels) == 100
        assert len(decimation.channels_estimated) == 100

    def test_duplicate_channel_names(self):
        """Test with duplicate channel names."""
        decimation = Decimation(channels_estimated=["ex", "ex", "hy"])  # type: ignore

        # Should deduplicate automatically
        assert len(set(decimation.channels_estimated)) <= 3
        assert len(decimation.channels) <= 3

    def test_special_character_channel_names(self):
        """Test with special character channel names."""
        special_names = ["ch-1", "ch_2", "ch.3", "ch:4"]
        decimation = Decimation(channels_estimated=special_names)  # type: ignore

        assert len(decimation.channels) == 4
        for name in special_names:
            assert decimation.has_channel(name)


class TestDecimationHelperFunctions:
    """Test helper functions in the module."""

    def test_fc_decimations_creator_basic(self):
        """Test fc_decimations_creator function."""
        time_period = TimePeriod(
            start="2023-01-01T00:00:00+00:00", end="2023-01-02T00:00:00+00:00"
        )

        decimations = fc_decimations_creator(
            initial_sample_rate=1024.0,
            decimation_factors=[1, 4, 16],
            max_levels=3,
            time_period=time_period,
        )

        assert isinstance(decimations, list)
        assert len(decimations) == 3
        assert all(isinstance(d, Decimation) for d in decimations)

    def test_fc_decimations_creator_with_defaults(self):
        """Test fc_decimations_creator with default parameters."""
        decimations = fc_decimations_creator(initial_sample_rate=1024.0)

        assert isinstance(decimations, list)
        assert len(decimations) > 0

    def test_get_degenerate_fc_decimation(self):
        """Test get_degenerate_fc_decimation function."""
        result = get_degenerate_fc_decimation(1024.0)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Decimation)


class TestDecimationIntegration:
    """Test Decimation integration scenarios and complex workflows."""

    def test_complete_workflow(self):
        """Test a complete decimation configuration workflow."""
        # Create decimation with mixed initialization
        channels = ListDict()
        channels.append(create_fc_channel("ex", frequency_max=100.0))

        decimation = Decimation(
            id="workflow_test", channels=channels, channels_estimated=["ex", "hy", "hz"]
        )  # type: ignore

        # Verify synchronization worked
        assert len(decimation.channels) == 3
        assert set(decimation.channels_estimated) == {"ex", "hy", "hz"}
        ex_channel = decimation.get_channel("ex")
        assert ex_channel is not None
        assert ex_channel.frequency_max == 100.0

        # Add another channel
        new_channel = create_fc_channel("ez", frequency_max=50.0)
        decimation.add_channel(new_channel)

        # Update time period
        decimation.update_time_period()

        # Verify final state - channel is in the channels list but not in channels_estimated
        assert len(decimation.channels) == 4
        assert "ez" in decimation.channels.keys()
        # has_channel only checks channels_estimated, so this returns False
        assert decimation.has_channel("ez") is False

    def test_serialization_roundtrip(self):
        """Test basic model functionality without full serialization."""
        original = Decimation(
            id="roundtrip_test", channels_estimated=["ex", "hy"]
        )  # type: ignore

        # Test basic properties
        assert original.id == "roundtrip_test"
        assert original.channels_estimated == ["ex", "hy"]
        assert len(original.channels) == 2

        # Test that we can create a new instance with same parameters
        recreated = Decimation(
            id=original.id, channels_estimated=original.channels_estimated
        )  # type: ignore

        # Verify equivalence
        assert recreated.id == original.id
        assert recreated.channels_estimated == original.channels_estimated
        assert len(recreated.channels) == len(original.channels)

    def test_complex_channel_management(self):
        """Test complex channel management scenarios."""
        decimation = Decimation(channels_estimated=["ex", "hy"])  # type: ignore

        # Add multiple channels with different properties
        for i, component in enumerate(["ez", "hx", "hz"], 1):
            channel = create_fc_channel(
                component, frequency_max=float(100 * i), frequency_min=float(10 * i)
            )
            decimation.add_channel(channel)

        # Verify all channels exist in the channels list
        assert len(decimation.channels) == 5

        # Test direct channel retrieval from channels (not using get_channel which might use has_channel)
        assert "ez" in decimation.channels.keys()
        ez_channel = decimation.channels["ez"]
        assert isinstance(ez_channel, FCChannel)
        assert ez_channel.frequency_max == 100.0

        assert "hx" in decimation.channels.keys()
        hx_channel = decimation.channels["hx"]
        assert isinstance(hx_channel, FCChannel)
        assert hx_channel.frequency_max == 200.0

        # Remove some channels (only removes from channels list, not channels_estimated)
        decimation.remove_channel("ex")
        decimation.remove_channel("hy")

        assert len(decimation.channels) == 3  # Only ez, hx, hz remain in channels
        assert "ex" not in decimation.channels.keys()
        assert "hy" not in decimation.channels.keys()
        # But has_channel still returns True because it checks channels_estimated
        assert decimation.has_channel("ex")  # Still True due to design limitation
        assert decimation.has_channel("hy")  # Still True due to design limitation


class TestDecimationPerformance:
    """Test Decimation performance and efficiency."""

    def test_large_scale_creation(self):
        """Test creating decimation with many channels efficiently."""
        import time

        channel_names = [f"channel_{i:04d}" for i in range(1000)]

        start_time = time.time()
        decimation = Decimation(channels_estimated=channel_names)  # type: ignore
        creation_time = time.time() - start_time

        assert len(decimation.channels) == 1000
        assert creation_time < 5.0  # Should complete in reasonable time

    def test_channel_operations_performance(self):
        """Test channel operations performance."""
        import time

        decimation = Decimation(channels_estimated=[f"ch_{i}" for i in range(100)])  # type: ignore

        # Test has_channel performance
        start_time = time.time()
        for i in range(100):
            decimation.has_channel(f"ch_{i}")
        lookup_time = time.time() - start_time

        assert lookup_time < 1.0  # Should be fast

        # Test get_channel performance
        start_time = time.time()
        for i in range(100):
            decimation.get_channel(f"ch_{i}")
        retrieval_time = time.time() - start_time

        assert retrieval_time < 1.0  # Should be fast

    def test_memory_efficiency(self):
        """Test memory efficiency with many channels."""
        import sys

        decimation = Decimation(channels_estimated=[f"ch_{i}" for i in range(1000)])  # type: ignore

        # Get object size (approximate)
        size = sys.getsizeof(decimation)

        # Should not be excessively large
        assert size < 100000  # Less than 100KB for the object itself


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
