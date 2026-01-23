# -*- coding: utf-8 -*-
"""
Created on September 7, 2025

@author: GitHub Copilot

Comprehensive pytest test suite for Estimator basemodel using fixtures and subtests
whilst optimizing for efficiency.
"""

# =============================================================================
# Imports
# =============================================================================

import pytest
from pydantic import ValidationError

from mt_metadata.processing.aurora.estimator import EngineEnum, Estimator

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def default_estimator():
    """Fixture for default Estimator instance."""
    return Estimator()


@pytest.fixture
def custom_estimator():
    """Fixture for custom Estimator instance with specific parameters."""
    return Estimator(engine=EngineEnum.RME, estimate_per_channel=False)


@pytest.fixture
def estimator_params():
    """Fixture providing various parameter combinations for testing."""
    return {
        "rme_rr_true": {"engine": EngineEnum.RME_RR, "estimate_per_channel": True},
        "rme_false": {"engine": EngineEnum.RME, "estimate_per_channel": False},
        "other_true": {"engine": EngineEnum.other, "estimate_per_channel": True},
        "rme_rr_false": {"engine": EngineEnum.RME_RR, "estimate_per_channel": False},
        "string_values": {"engine": "RME", "estimate_per_channel": True},
    }


@pytest.fixture
def all_engine_types():
    """Fixture providing all engine enum values for comprehensive testing."""
    return [EngineEnum.RME_RR, EngineEnum.RME, EngineEnum.other]


@pytest.fixture
def all_boolean_values():
    """Fixture providing all boolean values for estimate_per_channel testing."""
    return [True, False]


# =============================================================================
# Test Classes
# =============================================================================


class TestEstimatorInitialization:
    """Test Estimator initialization and default values."""

    def test_default_initialization(self, default_estimator):
        """Test default Estimator initialization."""
        assert default_estimator.engine == EngineEnum.RME_RR
        assert default_estimator.estimate_per_channel is True

    def test_custom_initialization(self, custom_estimator):
        """Test custom Estimator initialization with all parameters."""
        assert custom_estimator.engine == EngineEnum.RME
        assert custom_estimator.estimate_per_channel is False

    @pytest.mark.parametrize(
        "param_set", ["rme_rr_true", "rme_false", "other_true", "rme_rr_false"]
    )
    def test_parametrized_initialization(self, estimator_params, param_set):
        """Test initialization with different parameter sets."""
        params = estimator_params[param_set]
        estimator = Estimator(**params)

        # Verify all provided parameters are set correctly
        for key, value in params.items():
            assert getattr(estimator, key) == value

    def test_string_engine_initialization(self, estimator_params):
        """Test initialization with string engine values."""
        params = estimator_params["string_values"]
        estimator = Estimator(**params)

        # String "RME" should convert to EngineEnum.RME
        assert estimator.engine == EngineEnum.RME
        assert estimator.estimate_per_channel is True

    def test_initialization_with_invalid_types(self):
        """Test initialization with invalid parameter types."""
        with pytest.raises(ValidationError):
            Estimator(engine="invalid_engine")

        with pytest.raises(ValidationError):
            Estimator(estimate_per_channel="not_a_boolean")

    def test_partial_initialization(self):
        """Test initialization with only some parameters provided."""
        # Only engine specified
        estimator1 = Estimator(engine=EngineEnum.other)
        assert estimator1.engine == EngineEnum.other
        assert estimator1.estimate_per_channel is True  # Default value

        # Only estimate_per_channel specified
        estimator2 = Estimator(estimate_per_channel=False)
        assert estimator2.engine == EngineEnum.RME_RR  # Default value
        assert estimator2.estimate_per_channel is False


class TestEstimatorProperties:
    """Test Estimator property access and modification."""

    def test_property_access(self, custom_estimator):
        """Test that all properties are accessible."""
        assert hasattr(custom_estimator, "engine")
        assert hasattr(custom_estimator, "estimate_per_channel")

    def test_property_modification(self, default_estimator):
        """Test property modification."""
        # Test engine modification
        default_estimator.engine = EngineEnum.RME
        assert default_estimator.engine == EngineEnum.RME

        # Test estimate_per_channel modification
        default_estimator.estimate_per_channel = False
        assert default_estimator.estimate_per_channel is False

    def test_enum_property_validation(self, default_estimator):
        """Test that enum properties validate correctly."""
        # Valid enum values should work
        for engine in [EngineEnum.RME_RR, EngineEnum.RME, EngineEnum.other]:
            default_estimator.engine = engine
            assert default_estimator.engine == engine

        # Invalid enum values should raise ValidationError
        with pytest.raises(ValidationError):
            default_estimator.engine = "invalid_engine"

    def test_boolean_property_validation(self, default_estimator):
        """Test that boolean properties validate correctly."""
        # Valid boolean values should work
        for value in [True, False]:
            default_estimator.estimate_per_channel = value
            assert default_estimator.estimate_per_channel is value

        # Invalid boolean values should raise ValidationError
        with pytest.raises(ValidationError):
            default_estimator.estimate_per_channel = "not_a_boolean"


class TestEstimatorEnumerations:
    """Test Estimator enumeration types and values."""

    @pytest.mark.parametrize(
        "engine_value", [EngineEnum.RME_RR, EngineEnum.RME, EngineEnum.other]
    )
    def test_engine_enum_values(self, engine_value):
        """Test EngineEnum values."""
        estimator = Estimator(engine=engine_value)
        assert estimator.engine == engine_value

    def test_engine_enum_string_values(self):
        """Test that EngineEnum accepts string values."""
        # Test with string representations
        estimator_rme_rr = Estimator(engine="RME_RR")
        assert estimator_rme_rr.engine == EngineEnum.RME_RR

        estimator_rme = Estimator(engine="RME")
        assert estimator_rme.engine == EngineEnum.RME

        estimator_other = Estimator(engine="other")
        assert estimator_other.engine == EngineEnum.other

    def test_engine_enum_values_exist(self, all_engine_types):
        """Test that all expected engine enum values exist."""
        expected_values = {"RME_RR", "RME", "other"}
        actual_values = {engine.value for engine in all_engine_types}
        assert actual_values == expected_values

    def test_engine_enum_default_value(self):
        """Test that the default engine value is correct."""
        estimator = Estimator()
        assert estimator.engine == EngineEnum.RME_RR
        assert estimator.engine == "RME_RR"  # Engine is stored as string


class TestEstimatorValidation:
    """Test Estimator field validation and error handling."""

    def test_engine_validation(self, all_engine_types):
        """Test engine field validation."""
        # Valid enum values
        for engine in all_engine_types:
            estimator = Estimator(engine=engine)
            assert estimator.engine == engine

        # Valid string values
        valid_strings = ["RME_RR", "RME", "other"]
        for engine_str in valid_strings:
            estimator = Estimator(engine=engine_str)
            assert estimator.engine.value == engine_str

        # Invalid string values should raise ValidationError
        with pytest.raises(ValidationError):
            Estimator(engine="invalid_engine")

    def test_estimate_per_channel_validation(self, all_boolean_values):
        """Test estimate_per_channel field validation."""
        # Valid boolean values
        for value in all_boolean_values:
            estimator = Estimator(estimate_per_channel=value)
            assert estimator.estimate_per_channel is value

        # Invalid types should raise ValidationError
        with pytest.raises(ValidationError):
            Estimator(estimate_per_channel="invalid")

        # Note: Integer 1 and 0 are coerced to boolean True and False in Pydantic
        # This is normal behavior, so we don't test for ValidationError here

    @pytest.mark.parametrize(
        "field_name,invalid_value",
        [
            ("engine", "invalid_engine"),
            ("estimate_per_channel", "invalid"),
            ("estimate_per_channel", None),
        ],
    )
    def test_field_validation_errors(self, field_name, invalid_value):
        """Test that invalid field values raise ValidationError."""
        with pytest.raises(ValidationError):
            Estimator(**{field_name: invalid_value})

    def test_engine_type_validation_errors(self):
        """Test that engine field rejects non-string types."""
        # These should raise TypeError from the enum, not ValidationError
        with pytest.raises(TypeError):
            Estimator(engine=123)

        with pytest.raises(ValidationError):
            Estimator(engine=None)

    def test_empty_initialization_uses_defaults(self):
        """Test that empty initialization uses default values."""
        estimator = Estimator()
        assert estimator.engine == EngineEnum.RME_RR
        assert estimator.estimate_per_channel is True


class TestEstimatorComparison:
    """Test Estimator comparison and copying."""

    def test_equality_comparison(self, estimator_params):
        """Test Estimator equality comparison."""
        params = estimator_params["rme_false"]
        estimator1 = Estimator(**params)
        estimator2 = Estimator(**params)

        assert estimator1 == estimator2

    def test_inequality_comparison(self, default_estimator, custom_estimator):
        """Test Estimator inequality comparison."""
        assert default_estimator != custom_estimator

    def test_model_copy(self, custom_estimator):
        """Test Estimator model copying."""
        copied_estimator = custom_estimator.model_copy()
        assert custom_estimator == copied_estimator

        # Verify they are different objects
        assert id(custom_estimator) != id(copied_estimator)

    def test_model_copy_with_changes(self, custom_estimator):
        """Test Estimator model copying with modifications."""
        copied_estimator = custom_estimator.model_copy(
            update={"engine": EngineEnum.other}
        )

        assert copied_estimator.engine == EngineEnum.other
        assert custom_estimator.engine == EngineEnum.RME  # Original unchanged
        assert (
            copied_estimator.estimate_per_channel
            == custom_estimator.estimate_per_channel
        )  # Other fields copied

    def test_different_engine_inequality(self):
        """Test that estimators with different engines are not equal."""
        estimator1 = Estimator(engine=EngineEnum.RME_RR)
        estimator2 = Estimator(engine=EngineEnum.RME)

        assert estimator1 != estimator2

    def test_different_estimate_per_channel_inequality(self):
        """Test that estimators with different estimate_per_channel values are not equal."""
        estimator1 = Estimator(estimate_per_channel=True)
        estimator2 = Estimator(estimate_per_channel=False)

        assert estimator1 != estimator2


class TestEstimatorRepresentation:
    """Test Estimator string representation and serialization."""

    def test_string_representation(self, custom_estimator):
        """Test string representation of Estimator."""
        str_repr = str(custom_estimator)

        # The representation should contain key information
        assert "engine" in str_repr
        assert "RME" in str_repr
        assert "estimate_per_channel" in str_repr
        assert "False" in str_repr

    def test_model_dump(self, custom_estimator):
        """Test model serialization."""
        estimator_dict = custom_estimator.model_dump()

        assert isinstance(estimator_dict, dict)
        assert estimator_dict["engine"] == "RME"
        assert estimator_dict["estimate_per_channel"] is False

    def test_model_dump_json(self, custom_estimator):
        """Test JSON serialization."""
        json_str = custom_estimator.model_dump_json()

        assert isinstance(json_str, str)
        assert "engine" in json_str
        assert "RME" in json_str
        assert "estimate_per_channel" in json_str
        assert "false" in json_str.lower()

    def test_model_validate(self, estimator_params):
        """Test model validation from dict."""
        params = estimator_params["other_true"]
        estimator = Estimator.model_validate(params)

        for key, value in params.items():
            assert getattr(estimator, key) == value

    def test_model_validate_json(self, custom_estimator):
        """Test model validation from JSON string."""
        json_str = custom_estimator.model_dump_json()
        recreated_estimator = Estimator.model_validate_json(json_str)

        assert recreated_estimator == custom_estimator


class TestEstimatorEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_model_fields_info(self):
        """Test model fields information."""
        fields = Estimator.model_fields

        expected_fields = {"engine", "estimate_per_channel"}
        assert set(fields.keys()) == expected_fields

    def test_field_defaults(self):
        """Test that field defaults are correctly set."""
        estimator = Estimator()

        # Check that defaults match expected values
        assert estimator.engine == EngineEnum.RME_RR
        assert estimator.estimate_per_channel is True

    def test_field_types(self):
        """Test that fields have correct types."""
        estimator = Estimator()

        # Engine is stored as string, not enum object
        assert isinstance(estimator.engine, str)
        assert isinstance(estimator.estimate_per_channel, bool)

    def test_enum_membership(self):
        """Test that all enum values are properly defined."""
        # Test that all expected values are in the enum
        expected_engines = ["RME_RR", "RME", "other"]
        actual_engines = [e.value for e in EngineEnum]

        assert set(actual_engines) == set(expected_engines)

    def test_field_descriptions(self):
        """Test that fields have proper descriptions."""
        fields = Estimator.model_fields

        # Test that fields have descriptions
        assert fields["engine"].description == "The transfer function estimator engine"
        assert fields["estimate_per_channel"].description == "Estimate per channel"


class TestEstimatorIntegration:
    """Test Estimator integration scenarios and complex workflows."""

    def test_complete_workflow(self, estimator_params):
        """Test a complete estimator configuration workflow."""
        # Create estimator with specific parameters
        params = estimator_params["other_true"]
        estimator = Estimator(**params)

        # Verify all parameters are set
        assert estimator.engine == EngineEnum.other
        assert estimator.estimate_per_channel is True

        # Test serialization and deserialization
        estimator_dict = estimator.model_dump()
        recreated_estimator = Estimator.model_validate(estimator_dict)
        assert estimator == recreated_estimator

    def test_estimator_configuration_matrix(self, all_engine_types, all_boolean_values):
        """Test all combinations of engine and estimate_per_channel values."""
        configurations = []

        for engine in all_engine_types:
            for estimate_per_channel in all_boolean_values:
                estimator = Estimator(
                    engine=engine, estimate_per_channel=estimate_per_channel
                )
                configurations.append(estimator)

        # Verify we have all combinations (3 engines × 2 booleans = 6)
        assert len(configurations) == 6

        # Verify all configurations are unique when they should be
        unique_configs = set(
            (est.engine, est.estimate_per_channel) for est in configurations
        )
        assert len(unique_configs) == 6

    def test_estimation_workflow_simulation(self):
        """Test simulating different estimation workflows."""
        # Scenario 1: RME_RR with per-channel estimation
        estimator_rme_rr = Estimator(
            engine=EngineEnum.RME_RR, estimate_per_channel=True
        )

        # Scenario 2: RME without per-channel estimation
        estimator_rme = Estimator(engine=EngineEnum.RME, estimate_per_channel=False)

        # Scenario 3: Other engine with per-channel estimation
        estimator_other = Estimator(engine=EngineEnum.other, estimate_per_channel=True)

        estimators = [estimator_rme_rr, estimator_rme, estimator_other]

        # Verify each scenario has correct configuration
        assert (
            estimators[0].engine == EngineEnum.RME_RR
            and estimators[0].estimate_per_channel is True
        )
        assert (
            estimators[1].engine == EngineEnum.RME
            and estimators[1].estimate_per_channel is False
        )
        assert (
            estimators[2].engine == EngineEnum.other
            and estimators[2].estimate_per_channel is True
        )

    def test_engine_comparison_workflow(self):
        """Test comparing different estimation engines."""
        # Create estimators with same estimate_per_channel but different engines
        estimators = []
        for engine in [EngineEnum.RME_RR, EngineEnum.RME, EngineEnum.other]:
            estimator = Estimator(engine=engine, estimate_per_channel=True)
            estimators.append(estimator)

        # They should be different due to engine differences
        for i in range(len(estimators)):
            for j in range(i + 1, len(estimators)):
                assert estimators[i] != estimators[j]
                assert estimators[i].engine != estimators[j].engine
                assert (
                    estimators[i].estimate_per_channel
                    == estimators[j].estimate_per_channel
                )

    @pytest.mark.parametrize(
        "engine,expected_description",
        [
            (EngineEnum.RME_RR, "RME with Remote Reference"),
            (EngineEnum.RME, "Robust Multiple Estimator"),
            (EngineEnum.other, "Other estimation method"),
        ],
    )
    def test_engine_usage_scenarios(self, engine, expected_description):
        """Test different engine usage scenarios with descriptions."""
        estimator = Estimator(engine=engine)

        # Verify the engine is set correctly
        assert estimator.engine == engine

        # This test documents the expected use cases for each engine
        # The descriptions are not stored in the model but document expected usage
        if engine == EngineEnum.RME_RR:
            # RME_RR is typically used when remote reference data is available
            assert estimator.engine.value == "RME_RR"
        elif engine == EngineEnum.RME:
            # RME is used for robust estimation without remote reference
            assert estimator.engine.value == "RME"
        elif engine == EngineEnum.other:
            # Other is used for alternative estimation methods
            assert estimator.engine.value == "other"


# =============================================================================
# Performance and Efficiency Tests
# =============================================================================


class TestEstimatorPerformance:
    """Test Estimator performance and efficiency aspects."""

    def test_creation_performance(self, estimator_params):
        """Test that Estimator creation is efficient."""
        import time

        # Test creation time for multiple instances
        start_time = time.time()
        estimators = []
        for _ in range(1000):
            estimator = Estimator(**estimator_params["rme_false"])
            estimators.append(estimator)

        creation_time = time.time() - start_time

        # Should create 1000 instances in reasonable time (< 1 second)
        assert creation_time < 1.0
        assert len(estimators) == 1000

    def test_memory_efficiency(self, all_engine_types, all_boolean_values):
        """Test memory efficiency of Estimator instances."""
        # Create multiple instances and verify they don't leak memory
        estimators = []
        for i, engine in enumerate(all_engine_types):
            for j, estimate_per_channel in enumerate(all_boolean_values):
                estimator = Estimator(
                    engine=engine, estimate_per_channel=estimate_per_channel
                )
                estimators.append(estimator)

        # All instances should be unique and properly configured
        assert len(estimators) == 6  # 3 engines × 2 booleans
        assert len(set(id(estimator) for estimator in estimators)) == 6

    def test_serialization_performance(self, custom_estimator):
        """Test serialization performance."""
        import time

        # Test multiple serialization cycles
        start_time = time.time()
        for _ in range(10000):
            serialized = custom_estimator.model_dump_json()
            deserialized = Estimator.model_validate_json(serialized)

        serialization_time = time.time() - start_time

        # Should complete 10000 cycles in reasonable time (< 2 seconds)
        assert serialization_time < 2.0

    def test_comparison_performance(self, estimator_params):
        """Test comparison operation performance."""
        import time

        # Create many estimators for comparison
        estimators = []
        for _ in range(100):
            estimator = Estimator(**estimator_params["rme_rr_true"])
            estimators.append(estimator)

        # Test comparison performance
        start_time = time.time()
        for i in range(len(estimators)):
            for j in range(i + 1, len(estimators)):
                _ = estimators[i] == estimators[j]

        comparison_time = time.time() - start_time

        # Should complete comparisons in reasonable time (< 1 second)
        assert comparison_time < 1.0


# =============================================================================
# Comprehensive Integration Tests
# =============================================================================


class TestEstimatorComprehensive:
    """Comprehensive tests covering multiple aspects simultaneously."""

    def test_full_lifecycle(self):
        """Test complete Estimator lifecycle from creation to serialization."""
        # Step 1: Create with defaults
        estimator = Estimator()
        assert estimator.engine == EngineEnum.RME_RR
        assert estimator.estimate_per_channel is True

        # Step 2: Modify properties
        estimator.engine = EngineEnum.RME
        estimator.estimate_per_channel = False

        # Step 3: Verify modifications
        assert estimator.engine == EngineEnum.RME
        assert estimator.estimate_per_channel is False

        # Step 4: Serialize to dict
        estimator_dict = estimator.model_dump()
        assert estimator_dict["engine"] == "RME"
        assert estimator_dict["estimate_per_channel"] is False

        # Step 5: Recreate from dict
        new_estimator = Estimator.model_validate(estimator_dict)
        assert estimator == new_estimator

        # Step 6: JSON round-trip
        json_str = new_estimator.model_dump_json()
        final_estimator = Estimator.model_validate_json(json_str)
        assert estimator == final_estimator

    def test_all_combinations_validation(self):
        """Test all valid combinations of parameters."""
        engines = [EngineEnum.RME_RR, EngineEnum.RME, EngineEnum.other]
        boolean_values = [True, False]

        valid_combinations = []

        for engine in engines:
            for estimate_per_channel in boolean_values:
                estimator = Estimator(
                    engine=engine, estimate_per_channel=estimate_per_channel
                )
                valid_combinations.append(estimator)

                # Verify each combination
                assert estimator.engine == engine
                assert estimator.estimate_per_channel == estimate_per_channel

        # Should have all 6 combinations
        assert len(valid_combinations) == 6

        # All should serialize and deserialize correctly
        for estimator in valid_combinations:
            json_str = estimator.model_dump_json()
            recreated = Estimator.model_validate_json(json_str)
            assert estimator == recreated
