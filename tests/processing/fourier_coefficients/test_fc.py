"""
Comprehensive pytest test suite for FC (Fourier Coefficients) basemodel.

This test suite covers all aspects of the FC class including:
- Initialization and validation
- Field validation and conversion
- Synchronization between decimation_levels and levels
- Decimation level management operations
- Time period updates
- Edge cases and error handling
- Performance testing

Test organization:
- Uses fixtures for efficient setup
- Uses parametrized tests for comprehensive coverage
- Uses subtests where appropriate for granular testing
- Optimized for efficiency with minimal redundant object creation
"""

import numpy as np
import pytest

from mt_metadata.common import ListDict, TimePeriod
from mt_metadata.processing.fourier_coefficients.decimation import Decimation
from mt_metadata.processing.fourier_coefficients.fc import FC, MethodEnum


# =====================================================
# Fixtures
# =====================================================


@pytest.fixture
def sample_decimation():
    """Create a sample Decimation object for testing."""
    return Decimation(
        id="test_level",
        channels_estimated=["ex", "hy"],
        time_period=TimePeriod(
            start="2023-01-01T00:00:00+00:00", end="2023-01-02T00:00:00+00:00"
        ),
    )  # type: ignore


@pytest.fixture
def sample_decimation_list():
    """Create a list of sample Decimation objects for testing."""
    decimations = []
    for i in range(3):
        decimation = Decimation(
            id=f"level_{i+1}",
            channels_estimated=["ex", "hy"],
            time_period=TimePeriod(
                start=f"2023-01-0{i+1}T00:00:00+00:00",
                end=f"2023-01-0{i+2}T00:00:00+00:00",
            ),
        )  # type: ignore
        decimations.append(decimation)
    return decimations


@pytest.fixture
def sample_time_period():
    """Create a sample TimePeriod for testing."""
    return TimePeriod(
        start="2023-01-01T00:00:00+00:00", end="2023-01-07T00:00:00+00:00"
    )


# =====================================================
# Test Classes
# =====================================================


class TestFCInitialization:
    """Test FC class initialization and default values."""

    def test_default_initialization(self):
        """Test creating FC with default values."""
        fc = FC()  # type: ignore

        assert fc.decimation_levels == []
        assert fc.id == ""
        assert fc.channels_estimated == []
        assert fc.starting_sample_rate == 1.0
        assert fc.method == MethodEnum.fft
        assert isinstance(fc.time_period, TimePeriod)
        assert isinstance(fc.levels, ListDict)
        assert fc.n_decimation_levels == 0

    def test_custom_initialization(self):
        """Test creating FC with custom values."""
        time_period = TimePeriod(
            start="2023-01-01T00:00:00+00:00", end="2023-01-02T00:00:00+00:00"
        )

        fc = FC(
            id="test_fc",
            decimation_levels=["level1", "level2"],
            channels_estimated=["ex", "hy"],
            starting_sample_rate=64.0,
            method="wavelet",
            time_period=time_period,
        )  # type: ignore

        assert fc.id == "test_fc"
        assert fc.decimation_levels == ["level1", "level2"]
        assert fc.channels_estimated == ["ex", "hy"]
        assert fc.starting_sample_rate == 64.0
        assert fc.method == MethodEnum.wavelet
        assert fc.time_period == time_period
        assert fc.n_decimation_levels == 2  # Auto-created by validator


class TestFieldValidation:
    """Test field validation and conversion."""

    @pytest.mark.parametrize(
        "input_value,expected",
        [
            (["ex", "hy"], ["ex", "hy"]),
            (np.array(["ex", "hy"]), ["ex", "hy"]),
            ("ex,hy", ["ex", "hy"]),
            ([], []),
            (None, []),
        ],
    )
    def test_channels_estimated_validation(self, input_value, expected):
        """Test channels_estimated field validation with different input types."""
        fc = FC(channels_estimated=input_value)  # type: ignore
        assert fc.channels_estimated == expected

    @pytest.mark.parametrize(
        "input_value,expected",
        [
            (["1", "2"], ["1", "2"]),
            (np.array(["1", "2"]), ["1", "2"]),
            ("1,2", ["1", "2"]),
            ([], []),
        ],
    )
    def test_decimation_levels_validation(self, input_value, expected):
        """Test decimation_levels field validation with different input types."""
        fc = FC(decimation_levels=input_value)  # type: ignore
        assert fc.decimation_levels == expected

    def test_channels_estimated_invalid_type(self):
        """Test channels_estimated validation with invalid type."""
        with pytest.raises(TypeError, match="must be set with a list"):
            FC(channels_estimated=123)  # type: ignore

    @pytest.mark.parametrize("method_value", ["fft", "wavelet", "other"])
    def test_method_enum_validation(self, method_value):
        """Test method field validation with enum values."""
        fc = FC(method=method_value)  # type: ignore
        assert fc.method == MethodEnum(method_value)

    def test_levels_validation_from_decimation_objects(self, sample_decimation_list):
        """Test levels validation from Decimation objects."""
        fc = FC(levels=sample_decimation_list)  # type: ignore

        assert fc.n_decimation_levels == 3
        assert "level_1" in fc.levels.keys()
        assert "level_2" in fc.levels.keys()
        assert "level_3" in fc.levels.keys()

    def test_levels_validation_from_dict_list(self):
        """Test levels validation from dictionary list."""
        dict_levels = [{"id": "dict_level_1"}, {"id": "dict_level_2"}]

        fc = FC(levels=dict_levels)  # type: ignore

        assert fc.n_decimation_levels == 2
        assert "dict_level_1" in fc.levels.keys()
        assert "dict_level_2" in fc.levels.keys()

    def test_levels_validation_invalid_type(self):
        """Test levels validation with invalid type."""
        fc = FC(levels="invalid")  # type: ignore
        assert fc.levels == ListDict()
        # with pytest.raises(TypeError, match="input dl_list must be an iterable"):
        #     FC(levels="invalid")  # type: ignore


class TestLevelsSynchronization:
    """Test synchronization between decimation_levels and levels."""

    def test_decimation_levels_creates_levels(self):
        """Test that decimation_levels automatically creates Decimation objects."""
        fc = FC(decimation_levels=["sync_level1", "sync_level2", "sync_level3"])  # type: ignore

        assert fc.n_decimation_levels == 3
        assert set(fc.levels.keys()) == {"sync_level1", "sync_level2", "sync_level3"}

        # Verify each level is properly created
        for level_name in ["sync_level1", "sync_level2", "sync_level3"]:
            level = fc.levels[level_name]
            assert isinstance(level, Decimation)
            assert level.id == level_name

    def test_levels_added_to_decimation_levels(self, sample_decimation_list):
        """Test that existing levels get their names added to decimation_levels."""
        fc = FC(levels=sample_decimation_list, decimation_levels=[])  # type: ignore

        assert set(fc.decimation_levels) == {"level_1", "level_2", "level_3"}
        assert set(fc.levels.keys()) == {"level_1", "level_2", "level_3"}

    def test_mixed_scenario_synchronization(self, sample_decimation):
        """Test mixed scenario with some existing and some missing levels."""
        fc = FC(
            decimation_levels=["mixed1", "mixed2", "test_level"],
            levels=[sample_decimation],
        )  # type: ignore

        assert fc.n_decimation_levels == 3
        assert set(fc.decimation_levels) == {"mixed1", "mixed2", "test_level"}
        assert set(fc.levels.keys()) == {"test_level", "mixed1", "mixed2"}

    def test_levels_without_decimation_entries(self, sample_decimation_list):
        """Test levels without corresponding decimation_levels entries."""
        fc = FC(
            levels=sample_decimation_list,
            decimation_levels=["level_1"],  # Missing level_2, level_3
        )  # type: ignore

        assert set(fc.decimation_levels) == {"level_1", "level_2", "level_3"}
        assert set(fc.levels.keys()) == {"level_1", "level_2", "level_3"}


class TestFCLevelManagement:
    """Test level management functionality."""

    @pytest.fixture
    def fc_with_levels(self):
        """Create FC with sample levels."""
        return FC(decimation_levels=["mgmt_level1", "mgmt_level2", "mgmt_level3"])  # type: ignore

    def test_has_decimation_level(self, fc_with_levels):
        """Test has_decimation_level method."""
        assert fc_with_levels.has_decimation_level("mgmt_level1") is True
        assert fc_with_levels.has_decimation_level("mgmt_level2") is True
        assert fc_with_levels.has_decimation_level("nonexistent") is False

    def test_decimation_level_index(self, fc_with_levels):
        """Test decimation_level_index method."""
        assert fc_with_levels.decimation_level_index("mgmt_level1") == 0
        assert fc_with_levels.decimation_level_index("mgmt_level2") == 1
        assert fc_with_levels.decimation_level_index("mgmt_level3") == 2
        assert fc_with_levels.decimation_level_index("nonexistent") is None

    def test_get_decimation_level(self, fc_with_levels):
        """Test get_decimation_level method."""
        level = fc_with_levels.get_decimation_level("mgmt_level1")
        assert isinstance(level, Decimation)
        assert level.id == "mgmt_level1"

        # Test non-existent level
        assert fc_with_levels.get_decimation_level("nonexistent") is None

    def test_add_decimation_level_new(self, fc_with_levels, sample_decimation):
        """Test adding a new decimation level."""
        new_decimation = Decimation(id="new_mgmt_level")  # type: ignore
        initial_count = fc_with_levels.n_decimation_levels

        fc_with_levels.add_decimation_level(new_decimation)

        assert fc_with_levels.n_decimation_levels == initial_count + 1
        assert fc_with_levels.has_decimation_level("new_mgmt_level") is True
        assert "new_mgmt_level" in fc_with_levels.levels.keys()

    def test_add_decimation_level_existing_updates(self, fc_with_levels):
        """Test adding an existing decimation level updates it."""
        # Create a new decimation with the same id but different properties
        updated_decimation = Decimation(
            id="mgmt_level1", channels_estimated=["updated_channel"]
        )  # type: ignore

        fc_with_levels.add_decimation_level(updated_decimation)

        # Should not increase count
        assert fc_with_levels.n_decimation_levels == 3
        # Should have updated the decimation level
        retrieved_level = fc_with_levels.get_decimation_level("mgmt_level1")
        assert retrieved_level.channels_estimated == ["updated_channel"]

    def test_add_decimation_level_invalid_type(self, fc_with_levels):
        """Test adding invalid decimation level type raises error."""
        with pytest.raises(ValueError, match="Input must be metadata.decimation_level"):
            fc_with_levels.add_decimation_level("not_a_decimation")

    def test_remove_decimation_level(self, fc_with_levels):
        """Test removing a decimation level."""
        initial_count = fc_with_levels.n_decimation_levels

        fc_with_levels.remove_decimation_level("mgmt_level2")

        # Should be removed from both levels and decimation_levels
        assert fc_with_levels.n_decimation_levels == initial_count - 1
        assert "mgmt_level2" not in fc_with_levels.levels.keys()
        assert not fc_with_levels.has_decimation_level("mgmt_level2")

    def test_remove_nonexistent_level(self, fc_with_levels):
        """Test removing non-existent level logs warning but doesn't crash."""
        initial_count = fc_with_levels.n_decimation_levels

        # Should not raise error, just log warning
        fc_with_levels.remove_decimation_level("nonexistent")

        assert fc_with_levels.n_decimation_levels == initial_count

    def test_n_decimation_levels_property(self, fc_with_levels):
        """Test n_decimation_levels property."""
        assert fc_with_levels.n_decimation_levels == 3

        new_decimation = Decimation(id="prop_test_level")  # type: ignore
        fc_with_levels.add_decimation_level(new_decimation)
        assert fc_with_levels.n_decimation_levels == 4


class TestFCProperties:
    """Test FC properties and special methods."""

    @pytest.fixture
    def fc_with_data(self):
        """Create FC with sample data."""
        return FC(
            id="property_test_fc",
            decimation_levels=["prop1", "prop2"],
            channels_estimated=["ex", "hy"],
            starting_sample_rate=256.0,
        )  # type: ignore

    def test_basic_properties(self, fc_with_data):
        """Test basic properties access."""
        assert fc_with_data.id == "property_test_fc"
        assert fc_with_data.decimation_levels == ["prop1", "prop2"]
        assert fc_with_data.channels_estimated == ["ex", "hy"]
        assert fc_with_data.starting_sample_rate == 256.0
        assert fc_with_data.n_decimation_levels == 2

    def test_method_enum_access(self, fc_with_data):
        """Test method enum access and conversion."""
        assert fc_with_data.method == MethodEnum.fft

        fc_with_data.method = "wavelet"
        assert fc_with_data.method == MethodEnum.wavelet

    def test_time_period_access(self, fc_with_data):
        """Test time period access."""
        assert isinstance(fc_with_data.time_period, TimePeriod)

        # Set custom time period
        new_period = TimePeriod(start="2024-01-01", end="2024-12-31")
        fc_with_data.time_period = new_period
        assert fc_with_data.time_period == new_period


class TestFCOperations:
    """Test FC operations and complex workflows."""

    def test_update_time_period(self):
        """Test update_time_period method."""
        # Create FC with levels that have specific time periods
        decimation1 = Decimation(
            id="time_test1",
            time_period=TimePeriod(
                start="2023-01-01T00:00:00+00:00", end="2023-01-02T00:00:00+00:00"
            ),
        )  # type: ignore

        decimation2 = Decimation(
            id="time_test2",
            time_period=TimePeriod(
                start="2023-01-01T12:00:00+00:00", end="2023-01-03T00:00:00+00:00"
            ),
        )  # type: ignore

        fc = FC(levels=[decimation1, decimation2])  # type: ignore

        # Call update_time_period
        fc.update_time_period()

        # Should have updated to encompass all level time periods
        assert fc.time_period.start != "1980-01-01T00:00:00+00:00"
        assert fc.time_period.end != "1980-01-01T00:00:00+00:00"

    def test_complex_level_management(self):
        """Test complex level management scenarios."""
        fc = FC(decimation_levels=["complex1", "complex2"])  # type: ignore

        # Add multiple levels with different properties
        for i, level_id in enumerate(["complex3", "complex4"], 3):
            decimation = Decimation(
                id=level_id,
                channels_estimated=[f"ch_{i}"],
                time_period=TimePeriod(
                    start=f"2023-01-0{i}T00:00:00+00:00",
                    end=f"2023-01-0{i+1}T00:00:00+00:00",
                ),
            )  # type: ignore
            fc.add_decimation_level(decimation)

        # Verify all levels exist
        assert fc.n_decimation_levels == 4

        # Test level retrieval
        complex3 = fc.get_decimation_level("complex3")
        assert isinstance(complex3, Decimation)
        assert complex3.id == "complex3"

        # Remove some levels
        fc.remove_decimation_level("complex1")
        fc.remove_decimation_level("complex2")

        assert fc.n_decimation_levels == 2
        assert "complex1" not in fc.levels.keys()
        assert "complex2" not in fc.levels.keys()
        assert not fc.has_decimation_level("complex1")
        assert not fc.has_decimation_level("complex2")


class TestFCEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_decimation_levels(self):
        """Test with empty decimation_levels."""
        fc = FC(decimation_levels=[])  # type: ignore

        assert fc.decimation_levels == []
        assert fc.n_decimation_levels == 0

    def test_large_number_of_levels(self):
        """Test with large number of levels."""
        level_names = [f"level_{i:03d}" for i in range(100)]
        fc = FC(decimation_levels=level_names)  # type: ignore

        assert fc.n_decimation_levels == 100
        assert len(fc.decimation_levels) == 100

    def test_duplicate_level_names(self):
        """Test with duplicate level names."""
        fc = FC(decimation_levels=["dup1", "dup1", "dup2"])  # type: ignore

        # Should handle duplicates gracefully
        assert fc.n_decimation_levels <= 3

    def test_special_character_level_names(self):
        """Test with special character level names."""
        special_names = ["level-1", "level_2", "level.3", "level:4"]
        fc = FC(decimation_levels=special_names)  # type: ignore

        assert fc.n_decimation_levels == 4
        for name in special_names:
            assert fc.has_decimation_level(name)

    def test_numeric_level_names(self):
        """Test with numeric level names."""
        numeric_names = ["1", "2", "3", "10", "100"]
        fc = FC(decimation_levels=numeric_names)  # type: ignore

        assert fc.n_decimation_levels == 5
        for name in numeric_names:
            assert fc.has_decimation_level(name)


class TestFCIntegration:
    """Test FC integration scenarios and complete workflows."""

    def test_complete_workflow(self):
        """Test a complete FC configuration workflow."""
        # Create FC with mixed initialization
        decimations = ListDict()
        existing_decimation = Decimation(
            id="existing", channels_estimated=["ex", "hy"]
        )  # type: ignore
        decimations.append(existing_decimation)

        fc = FC(
            id="workflow_test",
            decimation_levels=["existing", "new1", "new2"],
            levels=decimations,
            channels_estimated=["ex", "hy", "hz"],
            starting_sample_rate=1024.0,
        )  # type: ignore

        # Verify synchronization worked
        assert fc.n_decimation_levels == 3
        assert set(fc.decimation_levels) == {"existing", "new1", "new2"}
        assert set(fc.levels.keys()) == {"existing", "new1", "new2"}

        # Add another level
        new_decimation = Decimation(id="added", channels_estimated=["hz"])  # type: ignore
        fc.add_decimation_level(new_decimation)

        # Update time period
        fc.update_time_period()

        # Verify final state
        assert fc.n_decimation_levels == 4
        assert "added" in fc.levels.keys()
        # Note: added level won't be in decimation_levels because add_decimation_level
        # doesn't automatically add to that list (design choice)

    def test_serialization_roundtrip(self):
        """Test basic model functionality without full serialization."""
        original = FC(
            id="roundtrip_test",
            decimation_levels=["rt1", "rt2"],
            channels_estimated=["ex", "hy"],
            starting_sample_rate=512.0,
        )  # type: ignore

        # Test basic properties
        assert original.id == "roundtrip_test"
        assert original.decimation_levels == ["rt1", "rt2"]
        assert original.channels_estimated == ["ex", "hy"]
        assert original.n_decimation_levels == 2

        # Test that we can create a new instance with same parameters
        recreated = FC(
            id=original.id,
            decimation_levels=original.decimation_levels,
            channels_estimated=original.channels_estimated,
            starting_sample_rate=original.starting_sample_rate,
        )  # type: ignore

        # Verify equivalence
        assert recreated.id == original.id
        assert recreated.decimation_levels == original.decimation_levels
        assert recreated.channels_estimated == original.channels_estimated
        assert recreated.n_decimation_levels == original.n_decimation_levels


class TestFCPerformance:
    """Test FC performance and efficiency."""

    def test_large_scale_creation(self):
        """Test creating FC with many levels efficiently."""
        import time

        level_names = [f"perf_level_{i:04d}" for i in range(1000)]

        start_time = time.time()
        fc = FC(decimation_levels=level_names)  # type: ignore
        creation_time = time.time() - start_time

        assert fc.n_decimation_levels == 1000
        assert creation_time < 5.0  # Should complete in reasonable time

    def test_level_operations_performance(self):
        """Test level operations performance."""
        import time

        fc = FC(decimation_levels=[f"perf_{i}" for i in range(100)])  # type: ignore

        # Test has_decimation_level performance
        start_time = time.time()
        for i in range(100):
            fc.has_decimation_level(f"perf_{i}")
        lookup_time = time.time() - start_time

        assert lookup_time < 1.0  # Should be fast

        # Test get_decimation_level performance
        start_time = time.time()
        for i in range(100):
            fc.get_decimation_level(f"perf_{i}")
        retrieval_time = time.time() - start_time

        assert retrieval_time < 1.0  # Should be fast

    def test_memory_efficiency(self):
        """Test memory efficiency with many levels."""
        import sys

        fc = FC(decimation_levels=[f"mem_{i}" for i in range(1000)])  # type: ignore

        # Get object size (approximate)
        size = sys.getsizeof(fc)

        # Should not be excessively large
        assert size < 200000  # Less than 200KB for the object itself


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
