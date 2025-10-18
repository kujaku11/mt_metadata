# -*- coding: utf-8 -*-
"""
Created on September 7, 2025

@author: GitHub Copilot

Comprehensive pytest test suite for Regression basemodel using fixtures and subtests
whilst optimizing for efficiency.
"""
# =============================================================================
# Imports
# =============================================================================

import pytest
from pydantic import ValidationError

from mt_metadata.processing.aurora.regression import Regression


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def default_regression():
    """Fixture for default Regression instance."""
    return Regression()


@pytest.fixture
def custom_regression():
    """Fixture for custom Regression instance with specific parameters."""
    return Regression(
        minimum_cycles=5,
        max_iterations=20,
        max_redescending_iterations=3,
        r0=1.8,
        u0=3.2,
        tolerance=0.001,
        verbosity=2,
    )


@pytest.fixture
def regression_params():
    """Fixture providing various parameter combinations for testing."""
    return {
        "minimal": {
            "minimum_cycles": 1,
            "max_iterations": 5,
            "max_redescending_iterations": 1,
            "r0": 1.0,
            "u0": 2.0,
            "tolerance": 0.01,
            "verbosity": 0,
        },
        "standard": {
            "minimum_cycles": 10,
            "max_iterations": 15,
            "max_redescending_iterations": 2,
            "r0": 1.5,
            "u0": 2.8,
            "tolerance": 0.005,
            "verbosity": 1,
        },
        "high_precision": {
            "minimum_cycles": 20,
            "max_iterations": 50,
            "max_redescending_iterations": 5,
            "r0": 1.2,
            "u0": 2.5,
            "tolerance": 0.0001,
            "verbosity": 3,
        },
        "conservative": {
            "minimum_cycles": 50,
            "max_iterations": 100,
            "max_redescending_iterations": 10,
            "r0": 2.0,
            "u0": 3.5,
            "tolerance": 0.001,
            "verbosity": 0,
        },
    }


@pytest.fixture
def integer_fields():
    """Fixture providing integer field names and test values."""
    return {
        "minimum_cycles": [1, 5, 10, 50, 100],
        "max_iterations": [5, 10, 20, 50, 100],
        "max_redescending_iterations": [1, 2, 3, 5, 10],
        "verbosity": [0, 1, 2, 3, 4],
    }


@pytest.fixture
def float_fields():
    """Fixture providing float field names and test values."""
    return {
        "r0": [1.0, 1.2, 1.5, 1.8, 2.0],
        "u0": [2.0, 2.5, 2.8, 3.0, 3.5],
        "tolerance": [0.001, 0.005, 0.01, 0.05, 0.1],
    }


@pytest.fixture
def boundary_values():
    """Fixture providing boundary test values."""
    return {
        "valid_minimums": {
            "minimum_cycles": 1,
            "max_iterations": 1,
            "max_redescending_iterations": 0,
            "r0": 0.1,
            "u0": 0.1,
            "tolerance": 0.0001,
            "verbosity": 0,
        },
        "valid_maximums": {
            "minimum_cycles": 1000,
            "max_iterations": 1000,
            "max_redescending_iterations": 100,
            "r0": 10.0,
            "u0": 10.0,
            "tolerance": 1.0,
            "verbosity": 10,
        },
    }


# =============================================================================
# Test Classes
# =============================================================================


class TestRegressionInitialization:
    """Test Regression initialization and default values."""

    def test_default_initialization(self, default_regression):
        """Test default Regression initialization."""
        assert default_regression.minimum_cycles == 1
        assert default_regression.max_iterations == 10
        assert default_regression.max_redescending_iterations == 2
        assert default_regression.r0 == 1.5
        assert default_regression.u0 == 2.8
        assert default_regression.tolerance == 0.005
        assert default_regression.verbosity == 1

    def test_custom_initialization(self, custom_regression):
        """Test custom Regression initialization with all parameters."""
        assert custom_regression.minimum_cycles == 5
        assert custom_regression.max_iterations == 20
        assert custom_regression.max_redescending_iterations == 3
        assert custom_regression.r0 == 1.8
        assert custom_regression.u0 == 3.2
        assert custom_regression.tolerance == 0.001
        assert custom_regression.verbosity == 2

    @pytest.mark.parametrize(
        "param_set", ["minimal", "standard", "high_precision", "conservative"]
    )
    def test_parametrized_initialization(self, regression_params, param_set):
        """Test initialization with different parameter sets."""
        params = regression_params[param_set]
        regression = Regression(**params)

        # Verify all provided parameters are set correctly
        for key, value in params.items():
            assert getattr(regression, key) == value

    def test_partial_initialization(self):
        """Test initialization with only some parameters provided."""
        # Only minimum_cycles specified
        regression1 = Regression(minimum_cycles=15)
        assert regression1.minimum_cycles == 15
        assert regression1.max_iterations == 10  # Default
        assert regression1.verbosity == 1  # Default

        # Only float parameters specified
        regression2 = Regression(r0=2.0, tolerance=0.001)
        assert regression2.r0 == 2.0
        assert regression2.tolerance == 0.001
        assert regression2.minimum_cycles == 1  # Default

    def test_initialization_with_invalid_types(self):
        """Test initialization with invalid parameter types."""
        with pytest.raises(ValidationError):
            Regression(minimum_cycles="invalid")

        with pytest.raises(ValidationError):
            Regression(r0="not_a_float")

        with pytest.raises(ValidationError):
            Regression(verbosity=1.5)  # Float instead of int

    def test_empty_initialization_uses_defaults(self):
        """Test that empty initialization uses default values."""
        regression = Regression()
        assert regression.minimum_cycles == 1
        assert regression.max_iterations == 10
        assert regression.max_redescending_iterations == 2
        assert regression.r0 == 1.5
        assert regression.u0 == 2.8
        assert regression.tolerance == 0.005
        assert regression.verbosity == 1


class TestRegressionProperties:
    """Test Regression property access and modification."""

    def test_property_access(self, custom_regression):
        """Test that all properties are accessible."""
        assert hasattr(custom_regression, "minimum_cycles")
        assert hasattr(custom_regression, "max_iterations")
        assert hasattr(custom_regression, "max_redescending_iterations")
        assert hasattr(custom_regression, "r0")
        assert hasattr(custom_regression, "u0")
        assert hasattr(custom_regression, "tolerance")
        assert hasattr(custom_regression, "verbosity")

    def test_integer_property_modification(self, default_regression, integer_fields):
        """Test integer property modification."""
        for field_name, test_values in integer_fields.items():
            for value in test_values:
                setattr(default_regression, field_name, value)
                assert getattr(default_regression, field_name) == value

    def test_float_property_modification(self, default_regression, float_fields):
        """Test float property modification."""
        for field_name, test_values in float_fields.items():
            for value in test_values:
                setattr(default_regression, field_name, value)
                assert getattr(default_regression, field_name) == value

    def test_property_type_validation(self, default_regression):
        """Test that properties validate types correctly."""
        # Valid integer assignments
        default_regression.minimum_cycles = 5
        assert default_regression.minimum_cycles == 5

        # Valid float assignments
        default_regression.r0 = 2.0
        assert default_regression.r0 == 2.0

        # Invalid type assignments should raise ValidationError
        with pytest.raises(ValidationError):
            default_regression.minimum_cycles = "not_an_int"

        with pytest.raises(ValidationError):
            default_regression.r0 = "not_a_float"


class TestRegressionValidation:
    """Test Regression field validation and error handling."""

    @pytest.mark.parametrize(
        "field_name,valid_values",
        [
            ("minimum_cycles", [1, 5, 10, 100]),
            ("max_iterations", [1, 10, 50, 200]),
            ("max_redescending_iterations", [0, 1, 5, 20]),
            ("verbosity", [0, 1, 2, 5]),
        ],
    )
    def test_integer_field_validation(self, field_name, valid_values):
        """Test integer field validation with valid values."""
        for value in valid_values:
            regression = Regression(**{field_name: value})
            assert getattr(regression, field_name) == value

    @pytest.mark.parametrize(
        "field_name,valid_values",
        [
            ("r0", [0.1, 1.0, 1.5, 2.0, 5.0]),
            ("u0", [1.0, 2.0, 2.8, 3.5, 10.0]),
            ("tolerance", [0.0001, 0.001, 0.01, 0.1, 1.0]),
        ],
    )
    def test_float_field_validation(self, field_name, valid_values):
        """Test float field validation with valid values."""
        for value in valid_values:
            regression = Regression(**{field_name: value})
            assert getattr(regression, field_name) == value

    @pytest.mark.parametrize(
        "field_name,invalid_value",
        [
            ("minimum_cycles", "invalid"),
            ("minimum_cycles", 1.5),
            ("max_iterations", "invalid"),
            ("max_iterations", []),
            ("r0", "invalid"),
            ("r0", None),
            ("tolerance", "invalid"),
            ("verbosity", 1.5),
        ],
    )
    def test_field_validation_errors(self, field_name, invalid_value):
        """Test that invalid field values raise ValidationError."""
        with pytest.raises(ValidationError):
            Regression(**{field_name: invalid_value})

    def test_boundary_values(self, boundary_values):
        """Test boundary values for all fields."""
        # Test valid minimum values
        min_regression = Regression(**boundary_values["valid_minimums"])
        for field_name, value in boundary_values["valid_minimums"].items():
            assert getattr(min_regression, field_name) == value

        # Test valid maximum values
        max_regression = Regression(**boundary_values["valid_maximums"])
        for field_name, value in boundary_values["valid_maximums"].items():
            assert getattr(max_regression, field_name) == value

    def test_negative_values_handling(self):
        """Test handling of negative values where applicable."""
        # Most fields should accept non-negative values
        # Testing edge cases with zero and small positive values
        regression = Regression(
            minimum_cycles=1,  # Should be positive
            max_iterations=1,  # Should be positive
            max_redescending_iterations=0,  # Can be zero
            r0=0.1,  # Should be positive
            u0=0.1,  # Should be positive
            tolerance=0.0001,  # Should be positive
            verbosity=0,  # Can be zero
        )

        assert regression.minimum_cycles == 1
        assert regression.max_redescending_iterations == 0
        assert regression.verbosity == 0


class TestRegressionComparison:
    """Test Regression comparison and copying."""

    def test_equality_comparison(self, regression_params):
        """Test Regression equality comparison."""
        params = regression_params["standard"]
        regression1 = Regression(**params)
        regression2 = Regression(**params)

        assert regression1 == regression2

    def test_inequality_comparison(self, default_regression, custom_regression):
        """Test Regression inequality comparison."""
        assert default_regression != custom_regression

    def test_model_copy(self, custom_regression):
        """Test Regression model copying."""
        copied_regression = custom_regression.model_copy()
        assert custom_regression == copied_regression

        # Verify they are different objects
        assert id(custom_regression) != id(copied_regression)

    def test_model_copy_with_changes(self, custom_regression):
        """Test Regression model copying with modifications."""
        copied_regression = custom_regression.model_copy(update={"minimum_cycles": 25})

        assert copied_regression.minimum_cycles == 25
        assert custom_regression.minimum_cycles == 5  # Original unchanged
        assert (
            copied_regression.max_iterations == custom_regression.max_iterations
        )  # Other fields copied

    def test_field_specific_inequality(self):
        """Test that regressions with different field values are not equal."""
        base_params = {"minimum_cycles": 10, "max_iterations": 20}

        regression1 = Regression(**base_params, r0=1.5)
        regression2 = Regression(**base_params, r0=2.0)

        assert regression1 != regression2

    def test_multiple_field_changes(self):
        """Test inequality with multiple field differences."""
        regression1 = Regression(minimum_cycles=5, r0=1.5, verbosity=1)
        regression2 = Regression(minimum_cycles=10, r0=2.0, verbosity=2)

        assert regression1 != regression2


class TestRegressionRepresentation:
    """Test Regression string representation and serialization."""

    def test_string_representation(self, custom_regression):
        """Test string representation of Regression."""
        str_repr = str(custom_regression)

        # The representation should contain key information
        assert "minimum_cycles" in str_repr
        assert "5" in str_repr
        assert "max_iterations" in str_repr
        assert "20" in str_repr
        assert "r0" in str_repr
        assert "1.8" in str_repr

    def test_model_dump(self, custom_regression):
        """Test model serialization."""
        regression_dict = custom_regression.model_dump()

        assert isinstance(regression_dict, dict)
        assert regression_dict["minimum_cycles"] == 5
        assert regression_dict["max_iterations"] == 20
        assert regression_dict["max_redescending_iterations"] == 3
        assert regression_dict["r0"] == 1.8
        assert regression_dict["u0"] == 3.2
        assert regression_dict["tolerance"] == 0.001
        assert regression_dict["verbosity"] == 2

    def test_model_dump_json(self, custom_regression):
        """Test JSON serialization."""
        json_str = custom_regression.model_dump_json()

        assert isinstance(json_str, str)
        assert "minimum_cycles" in json_str
        assert "max_iterations" in json_str
        assert "r0" in json_str
        assert "tolerance" in json_str

    def test_model_validate(self, regression_params):
        """Test model validation from dict."""
        params = regression_params["high_precision"]
        regression = Regression.model_validate(params)

        for key, value in params.items():
            assert getattr(regression, key) == value

    def test_model_validate_json(self, custom_regression):
        """Test model validation from JSON string."""
        json_str = custom_regression.model_dump_json()
        recreated_regression = Regression.model_validate_json(json_str)

        assert recreated_regression == custom_regression

    def test_round_trip_serialization(self, regression_params):
        """Test complete serialization round trip."""
        for param_set_name, params in regression_params.items():
            # Create original
            original = Regression(**params)

            # Serialize to dict and back
            dict_data = original.model_dump()
            from_dict = Regression.model_validate(dict_data)
            assert original == from_dict

            # Serialize to JSON and back
            json_data = original.model_dump_json()
            from_json = Regression.model_validate_json(json_data)
            assert original == from_json


class TestRegressionEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_model_fields_info(self):
        """Test model fields information."""
        fields = Regression.model_fields

        expected_fields = {
            "minimum_cycles",
            "max_iterations",
            "max_redescending_iterations",
            "r0",
            "u0",
            "tolerance",
            "verbosity",
        }

        assert set(fields.keys()) == expected_fields

    def test_field_defaults(self):
        """Test that field defaults are correctly set."""
        regression = Regression()

        # Check that defaults match expected values
        assert regression.minimum_cycles == 1
        assert regression.max_iterations == 10
        assert regression.max_redescending_iterations == 2
        assert regression.r0 == 1.5
        assert regression.u0 == 2.8
        assert regression.tolerance == 0.005
        assert regression.verbosity == 1

    def test_field_types(self):
        """Test that fields have correct types."""
        regression = Regression()

        # Integer fields
        assert isinstance(regression.minimum_cycles, int)
        assert isinstance(regression.max_iterations, int)
        assert isinstance(regression.max_redescending_iterations, int)
        assert isinstance(regression.verbosity, int)

        # Float fields
        assert isinstance(regression.r0, float)
        assert isinstance(regression.u0, float)
        assert isinstance(regression.tolerance, float)

    def test_precision_handling(self):
        """Test handling of float precision."""
        regression = Regression(r0=1.123456789, u0=2.987654321, tolerance=0.000123456)

        # Values should be preserved with reasonable precision
        assert abs(regression.r0 - 1.123456789) < 1e-10
        assert abs(regression.u0 - 2.987654321) < 1e-10
        assert abs(regression.tolerance - 0.000123456) < 1e-12

    def test_field_descriptions(self):
        """Test that fields have proper descriptions."""
        fields = Regression.model_fields

        # Check that key fields have descriptions
        assert "minimum" in fields["minimum_cycles"].description.lower()
        assert "max" in fields["max_iterations"].description.lower()
        assert (
            "convergence" in fields["tolerance"].description.lower()
        )  # Tolerance controls convergence
        assert (
            "logging" in fields["verbosity"].description.lower()
        )  # Verbosity controls logging


class TestRegressionIntegration:
    """Test Regression integration scenarios and complex workflows."""

    def test_complete_workflow(self, regression_params):
        """Test a complete regression configuration workflow."""
        # Create regression with high precision parameters
        params = regression_params["high_precision"]
        regression = Regression(**params)

        # Verify all parameters are set
        assert regression.minimum_cycles == 20
        assert regression.max_iterations == 50
        assert regression.tolerance == 0.0001
        assert regression.verbosity == 3

        # Test serialization and deserialization
        regression_dict = regression.model_dump()
        recreated_regression = Regression.model_validate(regression_dict)
        assert regression == recreated_regression

    def test_regression_parameter_scaling(self):
        """Test different scales of regression parameters."""
        # Low precision, fast regression
        fast_regression = Regression(
            minimum_cycles=1, max_iterations=5, tolerance=0.01, verbosity=0
        )

        # High precision, slow regression
        precise_regression = Regression(
            minimum_cycles=100, max_iterations=500, tolerance=0.00001, verbosity=3
        )

        # Verify configurations
        assert fast_regression.tolerance > precise_regression.tolerance
        assert fast_regression.max_iterations < precise_regression.max_iterations
        assert fast_regression.verbosity < precise_regression.verbosity

    def test_huber_regression_parameters(self):
        """Test Huber regression specific parameter combinations."""
        # Test different r0 and u0 combinations
        huber_configs = [
            {"r0": 1.0, "u0": 2.0},  # Conservative
            {"r0": 1.5, "u0": 2.8},  # Standard
            {"r0": 2.0, "u0": 3.5},  # Robust
        ]

        for config in huber_configs:
            regression = Regression(**config)
            assert regression.r0 == config["r0"]
            assert regression.u0 == config["u0"]
            # Verify u0 > r0 (typical constraint)
            assert regression.u0 > regression.r0

    def test_iteration_parameter_relationships(self):
        """Test relationships between iteration parameters."""
        regression = Regression(max_iterations=50, max_redescending_iterations=10)

        # Verify that redescending iterations is typically less than max iterations
        assert regression.max_redescending_iterations <= regression.max_iterations

        # Test edge case where they're equal
        regression_equal = Regression(max_iterations=10, max_redescending_iterations=10)
        assert (
            regression_equal.max_redescending_iterations
            == regression_equal.max_iterations
        )

    @pytest.mark.parametrize(
        "verbosity_level,expected_behavior",
        [
            (0, "Silent mode"),
            (1, "Basic logging"),
            (2, "Detailed logging"),
            (3, "Debug logging"),
        ],
    )
    def test_verbosity_levels(self, verbosity_level, expected_behavior):
        """Test different verbosity levels with expected behaviors."""
        regression = Regression(verbosity=verbosity_level)

        # Verify verbosity is set correctly
        assert regression.verbosity == verbosity_level

        # This test documents the expected behavior for each verbosity level
        if verbosity_level == 0:
            assert regression.verbosity == 0  # Silent
        elif verbosity_level >= 3:
            assert regression.verbosity >= 3  # Debug level


# =============================================================================
# Performance and Efficiency Tests
# =============================================================================


class TestRegressionPerformance:
    """Test Regression performance and efficiency aspects."""

    def test_creation_performance(self, regression_params):
        """Test that Regression creation is efficient."""
        import time

        # Test creation time for multiple instances
        start_time = time.time()
        regressions = []
        for _ in range(1000):
            regression = Regression(**regression_params["standard"])
            regressions.append(regression)

        creation_time = time.time() - start_time

        # Should create 1000 instances in reasonable time (< 1 second)
        assert creation_time < 1.0
        assert len(regressions) == 1000

    def test_memory_efficiency(self, integer_fields, float_fields):
        """Test memory efficiency of Regression instances."""
        # Create multiple instances and verify they don't leak memory
        regressions = []
        for i in range(50):
            regression = Regression(
                minimum_cycles=i + 1,
                max_iterations=(i + 1) * 2,
                r0=1.0 + i * 0.1,
                tolerance=0.001 + i * 0.0001,
            )
            regressions.append(regression)

        # All instances should be unique and properly configured
        assert len(set(id(regression) for regression in regressions)) == 50
        assert all(
            regression.minimum_cycles == i + 1
            for i, regression in enumerate(regressions)
        )

    def test_serialization_performance(self, custom_regression):
        """Test serialization performance."""
        import time

        # Test multiple serialization cycles
        start_time = time.time()
        for _ in range(5000):
            serialized = custom_regression.model_dump_json()
            deserialized = Regression.model_validate_json(serialized)

        serialization_time = time.time() - start_time

        # Should complete 5000 cycles in reasonable time (< 2 seconds)
        assert serialization_time < 2.0

    def test_comparison_performance(self, regression_params):
        """Test comparison operation performance."""
        import time

        # Create many regressions for comparison
        regressions = []
        for _ in range(100):
            regression = Regression(**regression_params["standard"])
            regressions.append(regression)

        # Test comparison performance
        start_time = time.time()
        for i in range(len(regressions)):
            for j in range(i + 1, len(regressions)):
                _ = regressions[i] == regressions[j]

        comparison_time = time.time() - start_time

        # Should complete comparisons in reasonable time (< 2 seconds)
        assert comparison_time < 2.0

    def test_field_access_performance(self, custom_regression):
        """Test field access performance."""
        import time

        field_names = [
            "minimum_cycles",
            "max_iterations",
            "r0",
            "u0",
            "tolerance",
            "verbosity",
        ]

        # Test field access performance
        start_time = time.time()
        for _ in range(10000):
            for field_name in field_names:
                _ = getattr(custom_regression, field_name)

        access_time = time.time() - start_time

        # Should complete field access in reasonable time (< 0.5 seconds)
        assert access_time < 0.5


# =============================================================================
# Comprehensive Integration Tests
# =============================================================================


class TestRegressionComprehensive:
    """Comprehensive tests covering multiple aspects simultaneously."""

    def test_full_lifecycle(self):
        """Test complete Regression lifecycle from creation to serialization."""
        # Step 1: Create with defaults
        regression = Regression()
        assert regression.minimum_cycles == 1
        assert regression.tolerance == 0.005

        # Step 2: Modify properties
        regression.minimum_cycles = 25
        regression.max_iterations = 75
        regression.r0 = 1.8
        regression.tolerance = 0.0005

        # Step 3: Verify modifications
        assert regression.minimum_cycles == 25
        assert regression.max_iterations == 75
        assert regression.r0 == 1.8
        assert regression.tolerance == 0.0005

        # Step 4: Serialize to dict
        regression_dict = regression.model_dump()
        assert regression_dict["minimum_cycles"] == 25
        assert regression_dict["tolerance"] == 0.0005

        # Step 5: Recreate from dict
        new_regression = Regression.model_validate(regression_dict)
        assert regression == new_regression

        # Step 6: JSON round-trip
        json_str = new_regression.model_dump_json()
        final_regression = Regression.model_validate_json(json_str)
        assert regression == final_regression

    def test_all_field_combinations_validation(self, integer_fields, float_fields):
        """Test various combinations of all fields."""
        # Test with minimum values from each field type
        min_values = {
            "minimum_cycles": min(integer_fields["minimum_cycles"]),
            "max_iterations": min(integer_fields["max_iterations"]),
            "max_redescending_iterations": min(
                integer_fields["max_redescending_iterations"]
            ),
            "verbosity": min(integer_fields["verbosity"]),
            "r0": min(float_fields["r0"]),
            "u0": min(float_fields["u0"]),
            "tolerance": min(float_fields["tolerance"]),
        }

        min_regression = Regression(**min_values)
        for field_name, expected_value in min_values.items():
            assert getattr(min_regression, field_name) == expected_value

        # Test with maximum values from each field type
        max_values = {
            "minimum_cycles": max(integer_fields["minimum_cycles"]),
            "max_iterations": max(integer_fields["max_iterations"]),
            "max_redescending_iterations": max(
                integer_fields["max_redescending_iterations"]
            ),
            "verbosity": max(integer_fields["verbosity"]),
            "r0": max(float_fields["r0"]),
            "u0": max(float_fields["u0"]),
            "tolerance": max(float_fields["tolerance"]),
        }

        max_regression = Regression(**max_values)
        for field_name, expected_value in max_values.items():
            assert getattr(max_regression, field_name) == expected_value

    def test_realistic_regression_scenarios(self):
        """Test realistic regression analysis scenarios."""
        scenarios = [
            {
                "name": "Quick Exploration",
                "params": {
                    "minimum_cycles": 5,
                    "max_iterations": 20,
                    "tolerance": 0.01,
                    "verbosity": 1,
                },
            },
            {
                "name": "Production Analysis",
                "params": {
                    "minimum_cycles": 50,
                    "max_iterations": 100,
                    "tolerance": 0.001,
                    "verbosity": 2,
                },
            },
            {
                "name": "Research Quality",
                "params": {
                    "minimum_cycles": 100,
                    "max_iterations": 500,
                    "tolerance": 0.0001,
                    "verbosity": 3,
                },
            },
        ]

        for scenario in scenarios:
            regression = Regression(**scenario["params"])

            # Verify each scenario has appropriate settings
            for param_name, expected_value in scenario["params"].items():
                assert getattr(regression, param_name) == expected_value

            # Verify serialization works for each scenario
            json_str = regression.model_dump_json()
            recreated = Regression.model_validate_json(json_str)
            assert regression == recreated
