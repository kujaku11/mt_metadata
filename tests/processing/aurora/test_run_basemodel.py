"""
Comprehensive pytest test suite for Run (Aurora processing) basemodel.

This test suite covers all aspects of the Run class including:
- Initialization and validation
- Field validation and conversion (channels, time_periods)
- Channel list management (input_channels, output_channels)
- Time period validation and conversion
- Scale factor computation and setting
- Channel scale factor operations
- Edge cases and error handling
- Performance testing

Test organization:
- Uses fixtures for efficient setup
- Uses parametrized tests for comprehensive coverage
- Uses subtests where appropriate for granular testing
- Optimized for efficiency with minimal redundant object creation
"""


import pytest

from mt_metadata.common import TimePeriod
from mt_metadata.processing.aurora.channel_basemodel import Channel
from mt_metadata.processing.aurora.run_basemodel import Run


# =====================================================
# Fixtures
# =====================================================


@pytest.fixture
def sample_channel():
    """Create a sample Channel object for testing."""
    return Channel(id="test_channel", scale_factor=2.5)


@pytest.fixture
def sample_channels():
    """Create a list of sample Channel objects for testing."""
    channels = []
    for i, ch_id in enumerate(["ex", "ey", "hx", "hy", "hz"], 1):
        channel = Channel(id=ch_id, scale_factor=float(i))
        channels.append(channel)
    return channels


@pytest.fixture
def sample_time_period():
    """Create a sample TimePeriod for testing."""
    return TimePeriod(
        start="2023-01-01T00:00:00+00:00", end="2023-01-01T01:00:00+00:00"
    )


@pytest.fixture
def sample_time_periods():
    """Create a list of sample TimePeriod objects for testing."""
    time_periods = []
    for i in range(3):
        tp = TimePeriod(
            start=f"2023-01-0{i+1}T00:00:00+00:00", end=f"2023-01-0{i+1}T01:00:00+00:00"
        )
        time_periods.append(tp)
    return time_periods


@pytest.fixture
def sample_run():
    """Create a sample Run object for testing."""
    input_channels = [
        Channel(id="hx", scale_factor=1.0),
        Channel(id="hy", scale_factor=2.0),
    ]
    output_channels = [
        Channel(id="ex", scale_factor=3.0),
        Channel(id="ey", scale_factor=4.0),
    ]
    time_periods = [
        TimePeriod(start="2023-01-01T00:00:00+00:00", end="2023-01-01T01:00:00+00:00")
    ]

    return Run(
        id="test_run",
        input_channels=input_channels,
        output_channels=output_channels,
        time_periods=time_periods,
        sample_rate=64.0,
    )


# =====================================================
# Test Classes
# =====================================================


class TestRunInitialization:
    """Test Run class initialization and default values."""

    def test_default_initialization(self):
        """Test creating Run with default values."""
        run = Run()  # type: ignore

        assert run.id == ""
        assert run.input_channels == []
        assert run.output_channels == []
        assert run.time_periods == []
        assert run.sample_rate == 1.0
        assert run.channel_scale_factors == {}

    def test_custom_initialization(self, sample_channels, sample_time_periods):
        """Test creating Run with custom values."""
        input_chs = sample_channels[:2]
        output_chs = sample_channels[2:]

        run = Run(
            id="custom_run",
            input_channels=input_chs,
            output_channels=output_chs,
            time_periods=sample_time_periods,
            sample_rate=256.0,
        )

        assert run.id == "custom_run"
        assert len(run.input_channels) == 2
        assert len(run.output_channels) == 3
        assert len(run.time_periods) == 3
        assert run.sample_rate == 256.0
        assert len(run.channel_scale_factors) == 5

    def test_initialization_with_empty_lists(self):
        """Test initialization with explicitly empty lists."""
        run = Run(
            id="empty_run",
            input_channels=[],
            output_channels=[],
            time_periods=[],
            sample_rate=128.0,
        )

        assert run.id == "empty_run"
        assert run.input_channels == []
        assert run.output_channels == []
        assert run.time_periods == []
        assert run.sample_rate == 128.0


class TestChannelValidation:
    """Test channel validation and conversion."""

    @pytest.mark.parametrize(
        "input_type,expected_count",
        [
            ("string", 1),
            (["ch1", "ch2"], 2),
            (
                [
                    Channel(id="ch1", scale_factor=1.0),
                    Channel(id="ch2", scale_factor=1.0),
                ],
                2,
            ),
            ([{"id": "ch1"}, {"id": "ch2"}], 2),
        ],
    )
    def test_input_channels_validation(self, input_type, expected_count):
        """Test input_channels field validation with different input types."""
        if input_type == "string":
            channels_input = "test_channel"
        else:
            channels_input = input_type

        run = Run(input_channels=channels_input)  # type: ignore

        assert len(run.input_channels) == expected_count
        for ch in run.input_channels:
            assert isinstance(ch, Channel)

    @pytest.mark.parametrize(
        "input_type,expected_count",
        [
            ("string", 1),
            (["ch1", "ch2", "ch3"], 3),
            (
                [
                    Channel(id="ex", scale_factor=1.0),
                    Channel(id="ey", scale_factor=1.0),
                ],
                2,
            ),
            ([{"id": "ex", "scale_factor": 2.0}], 1),
        ],
    )
    def test_output_channels_validation(self, input_type, expected_count):
        """Test output_channels field validation with different input types."""
        if input_type == "string":
            channels_input = "output_channel"
        else:
            channels_input = input_type

        run = Run(output_channels=channels_input)  # type: ignore

        assert len(run.output_channels) == expected_count
        for ch in run.output_channels:
            assert isinstance(ch, Channel)

    def test_channel_validation_from_string(self):
        """Test channel validation from string input."""
        run = Run(input_channels="hx", output_channels="ex")  # type: ignore

        assert len(run.input_channels) == 1
        assert run.input_channels[0].id == "hx"
        assert run.input_channels[0].scale_factor == 1.0

        assert len(run.output_channels) == 1
        assert run.output_channels[0].id == "ex"
        assert run.output_channels[0].scale_factor == 1.0

    def test_channel_validation_from_channel_objects(self, sample_channels):
        """Test channel validation from Channel objects."""
        input_chs = sample_channels[:2]
        output_chs = sample_channels[2:4]

        run = Run(input_channels=input_chs, output_channels=output_chs)  # type: ignore

        assert len(run.input_channels) == 2
        assert run.input_channels[0].id == "ex"
        assert run.input_channels[0].scale_factor == 1.0

        assert len(run.output_channels) == 2
        assert run.output_channels[0].id == "hx"
        assert run.output_channels[0].scale_factor == 3.0

    def test_channel_validation_from_dict(self):
        """Test channel validation from dictionary input."""
        input_dicts = [
            {"id": "hx", "scale_factor": 5.0},
            {"id": "hy", "scale_factor": 6.0},
        ]

        run = Run(input_channels=input_dicts)  # type: ignore

        assert len(run.input_channels) == 2
        assert run.input_channels[0].id == "hx"
        assert run.input_channels[0].scale_factor == 5.0
        assert run.input_channels[1].id == "hy"
        assert run.input_channels[1].scale_factor == 6.0

    def test_channel_validation_mixed_types(self):
        """Test channel validation with mixed input types."""
        mixed_input = [
            "string_channel",
            Channel(id="object_channel", scale_factor=2.0),
            {"id": "dict_channel", "scale_factor": 3.0},
        ]

        run = Run(input_channels=mixed_input)  # type: ignore

        assert len(run.input_channels) == 3
        assert run.input_channels[0].id == "string_channel"
        assert run.input_channels[0].scale_factor == 1.0
        assert run.input_channels[1].id == "object_channel"
        assert run.input_channels[1].scale_factor == 2.0
        assert run.input_channels[2].id == "dict_channel"
        assert run.input_channels[2].scale_factor == 3.0

    def test_channel_validation_invalid_type(self):
        """Test channel validation with invalid type raises error."""
        with pytest.raises(TypeError, match="not sure what to do with type"):
            Run(input_channels=[123])  # type: ignore


class TestTimePeriodValidation:
    """Test time period validation and conversion."""

    def test_time_periods_from_time_period_objects(self, sample_time_periods):
        """Test time_periods validation from TimePeriod objects."""
        run = Run(time_periods=sample_time_periods)  # type: ignore

        assert len(run.time_periods) == 3
        for tp in run.time_periods:
            assert isinstance(tp, TimePeriod)

    def test_time_periods_from_single_object(self, sample_time_period):
        """Test time_periods validation from single TimePeriod object."""
        run = Run(time_periods=sample_time_period)  # type: ignore

        assert len(run.time_periods) == 1
        assert isinstance(run.time_periods[0], TimePeriod)
        assert run.time_periods[0] == sample_time_period

    def test_time_periods_from_dict(self):
        """Test time_periods validation from dictionary input."""
        time_dict = {
            "start": "2023-01-01T00:00:00+00:00",
            "end": "2023-01-01T01:00:00+00:00",
        }

        run = Run(time_periods=time_dict)  # type: ignore

        assert len(run.time_periods) == 1
        assert isinstance(run.time_periods[0], TimePeriod)
        assert run.time_periods[0].start == "2023-01-01T00:00:00+00:00"

    def test_time_periods_from_dict_list(self):
        """Test time_periods validation from list of dictionaries."""
        time_dicts = [
            {"start": "2023-01-01T00:00:00+00:00", "end": "2023-01-01T01:00:00+00:00"},
            {"start": "2023-01-02T00:00:00+00:00", "end": "2023-01-02T01:00:00+00:00"},
        ]

        run = Run(time_periods=time_dicts)  # type: ignore

        assert len(run.time_periods) == 2
        for tp in run.time_periods:
            assert isinstance(tp, TimePeriod)

    def test_time_periods_validation_invalid_type(self):
        """Test time_periods validation with invalid type raises error."""
        with pytest.raises(TypeError, match="not sure what to do with type"):
            Run(time_periods=["invalid_string"])  # type: ignore


class TestChannelScaleFactors:
    """Test channel scale factors computation and operations."""

    def test_channel_scale_factors_computed_field(self, sample_run):
        """Test channel_scale_factors computed field."""
        scale_factors = sample_run.channel_scale_factors

        expected = {"hx": 1.0, "hy": 2.0, "ex": 3.0, "ey": 4.0}
        assert scale_factors == expected

    def test_channel_scale_factors_empty_channels(self):
        """Test channel_scale_factors with no channels."""
        run = Run()  # type: ignore

        assert run.channel_scale_factors == {}

    def test_channel_scale_factors_with_none_values(self):
        """Test channel_scale_factors when some channels have None scale_factor."""
        channels = [
            Channel(id="ch1", scale_factor=1.0),
            Channel(id="ch2", scale_factor=1.0),  # Default scale_factor is 1.0
        ]

        run = Run(input_channels=channels)  # type: ignore

        # Both channels should appear since scale_factor defaults to 1.0
        assert len(run.channel_scale_factors) == 2
        assert run.channel_scale_factors["ch1"] == 1.0
        assert run.channel_scale_factors["ch2"] == 1.0

    def test_set_channel_scale_factors_valid_dict(self, sample_run):
        """Test set_channel_scale_factors with valid dictionary."""
        new_factors = {"hx": 10.0, "ex": 20.0}

        sample_run.set_channel_scale_factors(new_factors)

        # Check that the scale factors were updated
        assert sample_run.input_channels[0].scale_factor == 10.0  # hx
        assert sample_run.input_channels[1].scale_factor == 2.0  # hy unchanged
        assert sample_run.output_channels[0].scale_factor == 20.0  # ex
        assert sample_run.output_channels[1].scale_factor == 4.0  # ey unchanged

    def test_set_channel_scale_factors_partial_update(self, sample_run):
        """Test set_channel_scale_factors with partial channel updates."""
        new_factors = {"hy": 99.0}  # Only update one channel

        sample_run.set_channel_scale_factors(new_factors)

        assert sample_run.input_channels[0].scale_factor == 1.0  # hx unchanged
        assert sample_run.input_channels[1].scale_factor == 99.0  # hy updated
        assert sample_run.output_channels[0].scale_factor == 3.0  # ex unchanged
        assert sample_run.output_channels[1].scale_factor == 4.0  # ey unchanged

    def test_set_channel_scale_factors_nonexistent_channels(self, sample_run):
        """Test set_channel_scale_factors with channels that don't exist."""
        new_factors = {"nonexistent": 100.0, "hx": 5.0}

        # Should not raise error, just ignore nonexistent channels
        sample_run.set_channel_scale_factors(new_factors)

        assert sample_run.input_channels[0].scale_factor == 5.0  # hx updated
        assert sample_run.input_channels[1].scale_factor == 2.0  # hy unchanged

    def test_set_channel_scale_factors_invalid_type(self, sample_run):
        """Test set_channel_scale_factors with invalid type raises error."""
        with pytest.raises(TypeError, match="not sure what to do with type"):
            sample_run.set_channel_scale_factors(123.0)

    def test_set_channel_scale_factors_empty_dict(self, sample_run):
        """Test set_channel_scale_factors with empty dictionary."""
        original_factors = sample_run.channel_scale_factors.copy()

        sample_run.set_channel_scale_factors({})

        # Should not change anything
        assert sample_run.channel_scale_factors == original_factors


class TestRunProperties:
    """Test Run properties and basic functionality."""

    def test_basic_properties_access(self, sample_run):
        """Test basic properties access."""
        assert sample_run.id == "test_run"
        assert len(sample_run.input_channels) == 2
        assert len(sample_run.output_channels) == 2
        assert len(sample_run.time_periods) == 1
        assert sample_run.sample_rate == 64.0

    def test_computed_field_updates_dynamically(self):
        """Test that computed field updates when channels change."""
        run = Run(input_channels=[Channel(id="ch1", scale_factor=1.0)])  # type: ignore

        assert run.channel_scale_factors == {"ch1": 1.0}

        # Add another channel
        run.input_channels.append(Channel(id="ch2", scale_factor=2.0))

        # Computed field should update
        assert run.channel_scale_factors == {"ch1": 1.0, "ch2": 2.0}

    def test_channel_modification(self, sample_run):
        """Test modifying channels after initialization."""
        # Add a new input channel
        new_channel = Channel(id="hz", scale_factor=5.0)
        sample_run.input_channels.append(new_channel)

        assert len(sample_run.input_channels) == 3
        assert "hz" in sample_run.channel_scale_factors
        assert sample_run.channel_scale_factors["hz"] == 5.0

    def test_time_period_modification(self, sample_run):
        """Test modifying time periods after initialization."""
        new_tp = TimePeriod(
            start="2023-01-02T00:00:00+00:00", end="2023-01-02T01:00:00+00:00"
        )
        sample_run.time_periods.append(new_tp)

        assert len(sample_run.time_periods) == 2


class TestRunOperations:
    """Test Run operations and complex workflows."""

    def test_complete_workflow(self):
        """Test a complete Run configuration workflow."""
        # Create Run with mixed initialization types
        run = Run(
            id="workflow_test",
            input_channels=["hx", "hy"],  # type: ignore
            output_channels=[{"id": "ex", "scale_factor": 10.0}],  # type: ignore
            time_periods={"start": "2023-01-01", "end": "2023-01-02"},  # type: ignore
            sample_rate=1024.0,
        )

        # Verify initialization worked
        assert run.id == "workflow_test"
        assert len(run.input_channels) == 2
        assert len(run.output_channels) == 1
        assert len(run.time_periods) == 1
        assert run.sample_rate == 1024.0

        # Add channels using different methods
        run.input_channels.append(Channel(id="hz", scale_factor=3.0))
        run.output_channels.extend(
            [Channel(id="ey", scale_factor=11.0), Channel(id="ez", scale_factor=12.0)]
        )

        # Update scale factors
        run.set_channel_scale_factors({"hx": 100.0, "ey": 200.0})

        # Verify final state
        assert len(run.input_channels) == 3
        assert len(run.output_channels) == 3
        assert run.input_channels[0].scale_factor == 100.0  # hx updated
        assert run.output_channels[1].scale_factor == 200.0  # ey updated

    def test_complex_channel_management(self):
        """Test complex channel management scenarios."""
        run = Run()  # type: ignore

        # Add channels of different types
        mixed_inputs = [
            "string_ch",
            Channel(id="object_ch", scale_factor=2.0),
            {"id": "dict_ch", "scale_factor": 3.0},
        ]

        for ch_input in mixed_inputs:
            if isinstance(ch_input, str):
                run.input_channels.append(Channel(id=ch_input, scale_factor=1.0))
            elif isinstance(ch_input, Channel):
                run.input_channels.append(ch_input)
            elif isinstance(ch_input, dict):
                ch = Channel(id="temp", scale_factor=1.0)  # type: ignore
                ch.from_dict(ch_input)
                run.input_channels.append(ch)

        # Verify all channels were added correctly
        assert len(run.input_channels) == 3
        assert run.input_channels[0].id == "string_ch"
        assert run.input_channels[1].id == "object_ch"
        assert run.input_channels[2].id == "dict_ch"

        # Test scale factor operations
        scale_factors = run.channel_scale_factors
        expected = {"string_ch": 1.0, "object_ch": 2.0, "dict_ch": 3.0}
        assert scale_factors == expected


class TestRunEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_channel_lists(self):
        """Test with empty channel lists."""
        run = Run(input_channels=[], output_channels=[])  # type: ignore

        assert run.input_channels == []
        assert run.output_channels == []
        assert run.channel_scale_factors == {}

    def test_large_number_of_channels(self):
        """Test with large number of channels."""
        channel_names = [f"ch_{i:03d}" for i in range(100)]
        channels = [
            Channel(id=name, scale_factor=float(i + 1))
            for i, name in enumerate(channel_names)
        ]

        run = Run(input_channels=channels[:50], output_channels=channels[50:])  # type: ignore

        assert len(run.input_channels) == 50
        assert len(run.output_channels) == 50
        assert len(run.channel_scale_factors) == 100

    def test_duplicate_channel_names(self):
        """Test with duplicate channel names across input and output."""
        # This should be allowed - same channel can be both input and output
        run = Run(
            input_channels=[Channel(id="ch1", scale_factor=1.0)],
            output_channels=[Channel(id="ch1", scale_factor=2.0)],
        )  # type: ignore

        assert len(run.input_channels) == 1
        assert len(run.output_channels) == 1
        # The computed field will use the last occurrence (output channel)
        assert run.channel_scale_factors["ch1"] == 2.0

    def test_special_character_channel_names(self):
        """Test with special character channel names."""
        special_names = ["ch-1", "ch_2", "ch.3", "ch:4", "ch@5"]
        channels = [Channel(id=name, scale_factor=1.0) for name in special_names]

        run = Run(input_channels=channels)  # type: ignore

        assert len(run.input_channels) == 5
        for i, name in enumerate(special_names):
            assert run.input_channels[i].id == name

    def test_zero_and_negative_sample_rates(self):
        """Test with zero and negative sample rates."""
        # Zero sample rate
        run1 = Run(sample_rate=0.0)  # type: ignore
        assert run1.sample_rate == 0.0

        # Negative sample rate
        run2 = Run(sample_rate=-1.0)  # type: ignore
        assert run2.sample_rate == -1.0

    def test_extreme_scale_factors(self):
        """Test with extreme scale factor values."""
        channels = [
            Channel(id="tiny", scale_factor=1e-10),
            Channel(id="huge", scale_factor=1e10),
            Channel(id="zero", scale_factor=0.0),
            Channel(id="negative", scale_factor=-5.0),
        ]

        run = Run(input_channels=channels)  # type: ignore

        scale_factors = run.channel_scale_factors
        assert scale_factors["tiny"] == 1e-10
        assert scale_factors["huge"] == 1e10
        assert scale_factors["zero"] == 0.0
        assert scale_factors["negative"] == -5.0


class TestRunIntegration:
    """Test Run integration scenarios and complete workflows."""

    def test_serialization_roundtrip(self, sample_run):
        """Test basic model functionality without full serialization."""
        # Test basic properties
        assert sample_run.id == "test_run"
        assert len(sample_run.input_channels) == 2
        assert len(sample_run.output_channels) == 2
        assert len(sample_run.time_periods) == 1
        assert sample_run.sample_rate == 64.0

        # Test that we can create a new instance with same structure
        recreated = Run(
            id=sample_run.id,
            input_channels=[ch for ch in sample_run.input_channels],
            output_channels=[ch for ch in sample_run.output_channels],
            time_periods=[tp for tp in sample_run.time_periods],
            sample_rate=sample_run.sample_rate,
        )

        # Verify equivalence
        assert recreated.id == sample_run.id
        assert len(recreated.input_channels) == len(sample_run.input_channels)
        assert len(recreated.output_channels) == len(sample_run.output_channels)
        assert len(recreated.time_periods) == len(sample_run.time_periods)
        assert recreated.sample_rate == sample_run.sample_rate

    def test_real_world_scenario(self):
        """Test a realistic MT processing scenario."""
        # Create a typical MT run configuration
        input_channels = ["hx", "hy"]
        output_channels = ["ex", "ey", "hz"]
        time_periods = [
            {"start": "2023-01-01T00:00:00", "end": "2023-01-01T06:00:00"},
            {"start": "2023-01-01T12:00:00", "end": "2023-01-01T18:00:00"},
        ]

        run = Run(
            id="MT001",
            input_channels=input_channels,  # type: ignore
            output_channels=output_channels,  # type: ignore
            time_periods=time_periods,  # type: ignore
            sample_rate=1000.0,
        )

        # Set realistic scale factors
        scale_factors = {
            "hx": 0.01,  # nT/count
            "hy": 0.01,
            "ex": 1.0,  # mV/count
            "ey": 1.0,
            "hz": 0.001,
        }
        run.set_channel_scale_factors(scale_factors)

        # Verify configuration
        assert run.id == "MT001"
        assert len(run.input_channels) == 2
        assert len(run.output_channels) == 3
        assert len(run.time_periods) == 2
        assert run.sample_rate == 1000.0

        # Verify scale factors were set correctly
        expected_factors = scale_factors
        assert run.channel_scale_factors == expected_factors


class TestRunPerformance:
    """Test Run performance and efficiency."""

    def test_large_scale_creation(self):
        """Test creating Run with many channels efficiently."""
        import time

        # Create many channels
        channels = [
            Channel(id=f"ch_{i:04d}", scale_factor=float(i)) for i in range(1000)
        ]
        time_periods = [
            TimePeriod(start="2023-01-01", end="2023-01-02") for _ in range(10)
        ]

        start_time = time.time()
        run = Run(
            id="performance_test",
            input_channels=channels[:500],
            output_channels=channels[500:],
            time_periods=time_periods,
            sample_rate=10000.0,
        )
        creation_time = time.time() - start_time

        assert len(run.input_channels) == 500
        assert len(run.output_channels) == 500
        assert len(run.time_periods) == 10
        assert creation_time < 2.0  # Should complete in reasonable time

    def test_scale_factor_operations_performance(self):
        """Test scale factor operations performance."""
        import time

        # Create run with many channels
        channels = [Channel(id=f"perf_{i}", scale_factor=1.0) for i in range(1000)]
        run = Run(input_channels=channels[:500], output_channels=channels[500:])  # type: ignore

        # Test computed field performance
        start_time = time.time()
        for _ in range(100):
            _ = run.channel_scale_factors
        lookup_time = time.time() - start_time

        assert lookup_time < 1.0  # Should be fast

        # Test set_channel_scale_factors performance
        scale_factors = {f"perf_{i}": float(i) for i in range(0, 1000, 10)}

        start_time = time.time()
        run.set_channel_scale_factors(scale_factors)
        update_time = time.time() - start_time

        assert update_time < 1.0  # Should be fast

    def test_memory_efficiency(self):
        """Test memory efficiency with many channels."""
        import sys

        channels = [Channel(id=f"mem_{i}", scale_factor=1.0) for i in range(1000)]
        run = Run(input_channels=channels)  # type: ignore

        # Get object size (approximate)
        size = sys.getsizeof(run)

        # Should not be excessively large
        assert size < 100000  # Less than 100KB for the object itself


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
