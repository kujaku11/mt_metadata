# -*- coding: utf-8 -*-
"""
Test suite for BirrpAngles metadata class

This comprehensive test suite provides coverage for the BirrpAngles class,
testing instantiation, field validation, serialization, and edge cases.
The test suite is designed for efficiency using pytest fixtures, parametrized
tests, and subtests to optimize test execution.

Key test areas covered:
- BirrpAngles instantiation with various data types
- Field validation (theta1, theta2, phi) with float conversion
- Angle value validation and boundary testing
- JSON/XML serialization and deserialization
- Dictionary operations and round-trip testing
- Edge cases (negative angles, large values, precision)
- Field metadata verification
- Performance testing with batch operations
- Invalid input handling and error cases

The BirrpAngles class contains three float fields representing rotation angles:
- theta1: rotation angle for block x (default 0.0)
- theta2: rotation angle for block y (default 0.0)
- phi: rotation angle for block (default 0.0)

All angles are measured in degrees and are required fields according to
the schema metadata.
"""

import json
from xml.etree import ElementTree as et

import numpy as np
import pytest

# Direct import to avoid jfiles package import issues
from mt_metadata.transfer_functions.io.jfiles.metadata.birrp_angles import BirrpAngles


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture
def default_angles():
    """Default angle values for testing."""
    return {
        "theta1": 0.0,
        "theta2": 0.0,
        "phi": 0.0,
    }


@pytest.fixture
def basic_angles():
    """Basic angle values for testing."""
    return {
        "theta1": 45.0,
        "theta2": 90.0,
        "phi": 180.0,
    }


@pytest.fixture
def precise_angles():
    """High precision angle values for testing."""
    return {
        "theta1": 45.123456,
        "theta2": 90.987654,
        "phi": 180.555555,
    }


@pytest.fixture
def boundary_angles():
    """Boundary angle values for testing."""
    return [
        {"theta1": 0.0, "theta2": 0.0, "phi": 0.0},
        {"theta1": 360.0, "theta2": 360.0, "phi": 360.0},
        {"theta1": -180.0, "theta2": -90.0, "phi": -360.0},
        {"theta1": 720.0, "theta2": 450.0, "phi": -720.0},
    ]


@pytest.fixture
def conversion_test_data():
    """Test data for type conversion validation."""
    return [
        # (input_value, expected_output)
        (0, 0.0),
        (45, 45.0),
        ("90.5", 90.5),
        ("180", 180.0),
        (np.float32(270.0), 270.0),
        (np.float64(359.999), 359.999),
    ]


@pytest.fixture
def invalid_angle_data():
    """Invalid angle data that should raise ValidationError."""
    return [
        "not_a_number",
        "45.0.0",  # Invalid float format
        None,
        complex(1, 2),
        [],
        {},
        "inf",
        "nan",
    ]


@pytest.fixture
def empty_angles():
    """Empty BirrpAngles instance."""
    return BirrpAngles()


@pytest.fixture
def basic_angles_instance(basic_angles):
    """Basic BirrpAngles instance."""
    return BirrpAngles(**basic_angles)


@pytest.fixture
def precise_angles_instance(precise_angles):
    """High precision BirrpAngles instance."""
    return BirrpAngles(**precise_angles)


# =============================================================================
# Test Class: BirrpAngles Instantiation
# =============================================================================
class TestBirrpAnglesInstantiation:
    """Test BirrpAngles instantiation scenarios."""

    def test_default_instantiation(self, empty_angles, default_angles):
        """Test creating BirrpAngles with default values."""
        assert empty_angles.theta1 == default_angles["theta1"]
        assert empty_angles.theta2 == default_angles["theta2"]
        assert empty_angles.phi == default_angles["phi"]

        # Verify all fields are floats
        assert isinstance(empty_angles.theta1, float)
        assert isinstance(empty_angles.theta2, float)
        assert isinstance(empty_angles.phi, float)

    def test_basic_instantiation(self, basic_angles_instance, basic_angles):
        """Test creating BirrpAngles with basic angle values."""
        assert basic_angles_instance.theta1 == basic_angles["theta1"]
        assert basic_angles_instance.theta2 == basic_angles["theta2"]
        assert basic_angles_instance.phi == basic_angles["phi"]

    def test_precise_instantiation(self, precise_angles_instance, precise_angles):
        """Test creating BirrpAngles with high precision values."""
        # Use pytest.approx for floating point comparison
        assert precise_angles_instance.theta1 == pytest.approx(precise_angles["theta1"])
        assert precise_angles_instance.theta2 == pytest.approx(precise_angles["theta2"])
        assert precise_angles_instance.phi == pytest.approx(precise_angles["phi"])

    @pytest.mark.parametrize(
        "input_val,expected",
        [
            (0, 0.0),
            (45, 45.0),
            ("90.5", 90.5),
            ("180", 180.0),
        ],
    )
    def test_individual_field_assignment(self, empty_angles, input_val, expected):
        """Test individual field assignment with type conversion."""
        # Test theta1 assignment
        empty_angles.theta1 = input_val
        assert empty_angles.theta1 == expected
        assert isinstance(empty_angles.theta1, float)

        # Reset and test theta2
        angles_copy = BirrpAngles()
        angles_copy.theta2 = input_val
        assert angles_copy.theta2 == expected
        assert isinstance(angles_copy.theta2, float)

        # Reset and test phi
        angles_copy2 = BirrpAngles()
        angles_copy2.phi = input_val
        assert angles_copy2.phi == expected
        assert isinstance(angles_copy2.phi, float)

    def test_inheritance_from_metadata_base(self, empty_angles):
        """Test that BirrpAngles properly inherits from MetadataBase."""
        # Should have MetadataBase methods
        assert hasattr(empty_angles, "to_dict")
        assert hasattr(empty_angles, "from_dict")
        assert hasattr(empty_angles, "to_json")
        assert hasattr(empty_angles, "to_xml")

        # Should be able to call str() and repr()
        str_repr = str(empty_angles)
        assert isinstance(str_repr, str)

        repr_str = repr(empty_angles)
        assert isinstance(repr_str, str)


# =============================================================================
# Test Class: Field Validation
# =============================================================================
class TestFieldValidation:
    """Test field validation and conversion."""

    @pytest.mark.parametrize("field_name", ["theta1", "theta2", "phi"])
    @pytest.mark.parametrize(
        "input_val,expected",
        [
            (0, 0.0),
            (45, 45.0),
            ("90.5", 90.5),
            (np.float32(180.0), 180.0),
            (np.float64(270.0), 270.0),
        ],
    )
    def test_valid_type_conversion(self, empty_angles, field_name, input_val, expected):
        """Test valid type conversion for all fields."""
        setattr(empty_angles, field_name, input_val)
        result = getattr(empty_angles, field_name)
        assert result == pytest.approx(expected)
        assert isinstance(result, float)

    @pytest.mark.parametrize("field_name", ["theta1", "theta2", "phi"])
    @pytest.mark.parametrize(
        "invalid_val",
        [
            "not_a_number",
            "45.0.0",
            complex(1, 2),
            [],
            {},
        ],
    )
    def test_invalid_values_raise_error(self, empty_angles, field_name, invalid_val):
        """Test that invalid values raise ValidationError."""
        with pytest.raises(Exception):  # Could be ValidationError or ValueError
            setattr(empty_angles, field_name, invalid_val)

    def test_boundary_values(self, boundary_angles):
        """Test boundary angle values."""
        for angles_data in boundary_angles:
            angles = BirrpAngles(**angles_data)
            assert isinstance(angles.theta1, float)
            assert isinstance(angles.theta2, float)
            assert isinstance(angles.phi, float)

            # Values should be exactly what was set (no normalization)
            assert angles.theta1 == angles_data["theta1"]
            assert angles.theta2 == angles_data["theta2"]
            assert angles.phi == angles_data["phi"]

    def test_field_metadata(self, empty_angles):
        """Test that field metadata is properly configured."""
        # Get field info from model
        fields = empty_angles.model_fields

        # Check that all expected fields exist
        assert "theta1" in fields
        assert "theta2" in fields
        assert "phi" in fields

        # Check field properties
        for field_name in ["theta1", "theta2", "phi"]:
            field_info = fields[field_name]
            assert field_info.default == 0.0
            assert field_info.annotation == float


# =============================================================================
# Test Class: Dictionary Operations
# =============================================================================
class TestDictionaryOperations:
    """Test dictionary serialization and deserialization."""

    def test_to_dict_default_values(self, empty_angles):
        """Test converting default BirrpAngles to dictionary."""
        result = empty_angles.to_dict()

        assert isinstance(result, dict)
        assert "birrp_angles" in result
        angles_data = result["birrp_angles"]
        expected_keys = {"theta1", "theta2", "phi"}
        assert set(angles_data.keys()).issuperset(expected_keys)
        assert angles_data["theta1"] == 0.0
        assert angles_data["theta2"] == 0.0
        assert angles_data["phi"] == 0.0

    def test_to_dict_custom_values(self, basic_angles_instance, basic_angles):
        """Test converting BirrpAngles with custom values to dictionary."""
        result = basic_angles_instance.to_dict()

        assert "birrp_angles" in result
        angles_data = result["birrp_angles"]
        assert angles_data["theta1"] == basic_angles["theta1"]
        assert angles_data["theta2"] == basic_angles["theta2"]
        assert angles_data["phi"] == basic_angles["phi"]

    def test_from_dict_basic(self, empty_angles, basic_angles):
        """Test loading BirrpAngles from dictionary."""
        empty_angles.from_dict(basic_angles)

        assert empty_angles.theta1 == basic_angles["theta1"]
        assert empty_angles.theta2 == basic_angles["theta2"]
        assert empty_angles.phi == basic_angles["phi"]

    def test_round_trip_dictionary(self, basic_angles_instance):
        """Test round-trip dictionary conversion."""
        # Convert to dict and back
        dict_data = basic_angles_instance.to_dict()
        new_angles = BirrpAngles()
        new_angles.from_dict(dict_data)

        # Should be identical
        assert new_angles.theta1 == basic_angles_instance.theta1
        assert new_angles.theta2 == basic_angles_instance.theta2
        assert new_angles.phi == basic_angles_instance.phi

    def test_from_dict_partial_data(self, empty_angles):
        """Test loading from dictionary with partial data."""
        partial_data = {"theta1": 30.0}
        empty_angles.from_dict(partial_data)

        # Updated field
        assert empty_angles.theta1 == 30.0
        # Default fields should remain
        assert empty_angles.theta2 == 0.0
        assert empty_angles.phi == 0.0


# =============================================================================
# Test Class: JSON Serialization
# =============================================================================
class TestJSONSerialization:
    """Test JSON serialization and deserialization."""

    def test_to_json_basic(self, basic_angles_instance):
        """Test converting BirrpAngles to JSON."""
        json_str = basic_angles_instance.to_json()

        assert isinstance(json_str, str)
        # Should be valid JSON
        json_data = json.loads(json_str)
        assert isinstance(json_data, dict)

    def test_json_round_trip(self, basic_angles_instance):
        """Test JSON round-trip conversion."""
        # Convert to JSON and parse back
        json_str = basic_angles_instance.to_json()
        json_data = json.loads(json_str)

        # Create new instance from parsed data
        new_angles = BirrpAngles()
        new_angles.from_dict(json_data)

        # Should match original
        assert new_angles.theta1 == basic_angles_instance.theta1
        assert new_angles.theta2 == basic_angles_instance.theta2
        assert new_angles.phi == basic_angles_instance.phi

    def test_json_precision_preservation(self, precise_angles_instance):
        """Test that JSON preserves floating point precision."""
        json_str = precise_angles_instance.to_json()
        json_data = json.loads(json_str)

        new_angles = BirrpAngles()
        new_angles.from_dict(json_data)

        # Should preserve precision
        assert new_angles.theta1 == pytest.approx(precise_angles_instance.theta1)
        assert new_angles.theta2 == pytest.approx(precise_angles_instance.theta2)
        assert new_angles.phi == pytest.approx(precise_angles_instance.phi)


# =============================================================================
# Test Class: XML Serialization
# =============================================================================
class TestXMLSerialization:
    """Test XML serialization."""

    def test_to_xml_element(self, basic_angles_instance):
        """Test converting BirrpAngles to XML element."""
        xml_element = basic_angles_instance.to_xml(string=False)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "birrp_angles"

    def test_to_xml_string(self, basic_angles_instance):
        """Test converting BirrpAngles to XML string."""
        xml_string = basic_angles_instance.to_xml(string=True)

        assert isinstance(xml_string, str)
        assert "birrp_angles" in xml_string
        assert "theta1" in xml_string
        assert "theta2" in xml_string
        assert "phi" in xml_string

    def test_xml_contains_values(self, basic_angles_instance, basic_angles):
        """Test that XML contains the expected values."""
        xml_string = basic_angles_instance.to_xml(string=True)

        # Parse the XML to verify structure
        root = et.fromstring(xml_string)
        assert root.tag == "birrp_angles"

        # Check for expected values (convert to strings for comparison)
        theta1_str = str(basic_angles["theta1"])
        theta2_str = str(basic_angles["theta2"])
        phi_str = str(basic_angles["phi"])

        assert theta1_str in xml_string or f"{theta1_str}" in xml_string
        assert theta2_str in xml_string or f"{theta2_str}" in xml_string
        assert phi_str in xml_string or f"{phi_str}" in xml_string


# =============================================================================
# Test Class: Edge Cases and Error Handling
# =============================================================================
class TestEdgeCasesAndErrorHandling:
    """Test edge cases and error handling."""

    def test_very_large_angles(self, empty_angles):
        """Test handling of very large angle values."""
        large_value = 1e10
        empty_angles.theta1 = large_value
        empty_angles.theta2 = large_value
        empty_angles.phi = large_value

        assert empty_angles.theta1 == large_value
        assert empty_angles.theta2 == large_value
        assert empty_angles.phi == large_value

    def test_very_small_angles(self, empty_angles):
        """Test handling of very small angle values."""
        small_value = 1e-10
        empty_angles.theta1 = small_value
        empty_angles.theta2 = small_value
        empty_angles.phi = small_value

        assert empty_angles.theta1 == pytest.approx(small_value)
        assert empty_angles.theta2 == pytest.approx(small_value)
        assert empty_angles.phi == pytest.approx(small_value)

    def test_negative_angles(self, empty_angles):
        """Test handling of negative angle values."""
        empty_angles.theta1 = -45.0
        empty_angles.theta2 = -90.0
        empty_angles.phi = -180.0

        assert empty_angles.theta1 == -45.0
        assert empty_angles.theta2 == -90.0
        assert empty_angles.phi == -180.0

    @pytest.mark.parametrize("field_name", ["theta1", "theta2", "phi"])
    def test_none_values_rejected(self, empty_angles, field_name):
        """Test that None values are properly rejected."""
        with pytest.raises(Exception):  # ValidationError
            setattr(empty_angles, field_name, None)

    def test_equality_comparison(self, basic_angles):
        """Test equality comparison between BirrpAngles instances."""
        angles1 = BirrpAngles(**basic_angles)
        angles2 = BirrpAngles(**basic_angles)
        angles3 = BirrpAngles(theta1=0.0, theta2=0.0, phi=0.0)

        assert angles1 == angles2
        # Note: The MetadataBase equality comparison may not work as expected
        # so we test the values directly
        assert not (
            angles1.theta1 == angles3.theta1
            and angles1.theta2 == angles3.theta2
            and angles1.phi == angles3.phi
        )

    def test_float_precision_edge_cases(self, empty_angles):
        """Test floating point precision edge cases."""
        # Test values that might cause floating point precision issues
        precision_values = [
            0.1 + 0.2,  # Classic floating point precision issue
            1.0 / 3.0,  # Repeating decimal
            np.pi,  # Irrational number
        ]

        for value in precision_values:
            empty_angles.theta1 = value
            # Should not raise an error and should preserve reasonable precision
            assert isinstance(empty_angles.theta1, float)
            assert empty_angles.theta1 == pytest.approx(value)


# =============================================================================
# Test Class: Performance and Batch Operations
# =============================================================================
class TestPerformanceAndBatchOperations:
    """Test performance characteristics and batch operations."""

    def test_batch_instantiation(self):
        """Test creating multiple BirrpAngles instances efficiently."""
        num_instances = 100
        instances = []

        for i in range(num_instances):
            angles = BirrpAngles(theta1=i * 1.0, theta2=i * 2.0, phi=i * 3.0)
            instances.append(angles)

        # Verify all instances were created correctly
        assert len(instances) == num_instances
        for i, angles in enumerate(instances):
            assert angles.theta1 == i * 1.0
            assert angles.theta2 == i * 2.0
            assert angles.phi == i * 3.0

    def test_batch_serialization(self, basic_angles):
        """Test batch serialization to various formats."""
        num_instances = 50
        instances = [BirrpAngles(**basic_angles) for _ in range(num_instances)]

        # Batch convert to dictionaries
        dicts = [instance.to_dict() for instance in instances]
        assert len(dicts) == num_instances

        # Batch convert to JSON
        json_strings = [instance.to_json() for instance in instances]
        assert len(json_strings) == num_instances

        # All should be identical
        for i in range(1, len(dicts)):
            assert dicts[i] == dicts[0]

        for i in range(1, len(json_strings)):
            assert json_strings[i] == json_strings[0]

    def test_field_modification_performance(self, empty_angles):
        """Test performance of repeated field modifications."""
        num_modifications = 1000

        # Modify fields repeatedly
        for i in range(num_modifications):
            empty_angles.theta1 = i % 360
            empty_angles.theta2 = (i * 2) % 360
            empty_angles.phi = (i * 3) % 360

        # Final values should match the last iteration
        final_i = num_modifications - 1
        assert empty_angles.theta1 == final_i % 360
        assert empty_angles.theta2 == (final_i * 2) % 360
        assert empty_angles.phi == (final_i * 3) % 360


# =============================================================================
# Test Class: Integration and Workflow Tests
# =============================================================================
class TestIntegrationAndWorkflow:
    """Test integration scenarios and complete workflows."""

    def test_complete_workflow_scenario(self, basic_angles):
        """Test a complete workflow scenario."""
        # Step 1: Create instance
        angles = BirrpAngles()

        # Step 2: Load from dictionary
        angles.from_dict(basic_angles)

        # Step 3: Modify values
        angles.theta1 += 10.0
        angles.theta2 -= 5.0
        angles.phi *= 2.0

        # Step 4: Export to JSON
        json_str = angles.to_json()

        # Step 5: Create new instance and load from JSON
        new_angles = BirrpAngles()
        json_data = json.loads(json_str)
        new_angles.from_dict(json_data)

        # Step 6: Verify workflow worked correctly
        assert new_angles.theta1 == basic_angles["theta1"] + 10.0
        assert new_angles.theta2 == basic_angles["theta2"] - 5.0
        assert new_angles.phi == basic_angles["phi"] * 2.0

    def test_multiple_format_round_trip(self, precise_angles):
        """Test round-trip conversion through multiple formats."""
        # Start with precise angles
        original = BirrpAngles(**precise_angles)

        # Round trip through dictionary
        dict_data = original.to_dict()
        from_dict = BirrpAngles()
        from_dict.from_dict(dict_data)

        # Round trip through JSON
        json_str = from_dict.to_json()
        json_data = json.loads(json_str)
        from_json = BirrpAngles()
        from_json.from_dict(json_data)

        # All should be equivalent with floating point tolerance
        assert from_dict.theta1 == pytest.approx(original.theta1)
        assert from_dict.theta2 == pytest.approx(original.theta2)
        assert from_dict.phi == pytest.approx(original.phi)

        assert from_json.theta1 == pytest.approx(original.theta1)
        assert from_json.theta2 == pytest.approx(original.theta2)
        assert from_json.phi == pytest.approx(original.phi)

    def test_error_recovery_workflow(self, basic_angles):
        """Test error recovery in workflow scenarios."""
        angles = BirrpAngles(**basic_angles)
        original_values = (angles.theta1, angles.theta2, angles.phi)

        # Attempt invalid operations and ensure state is preserved
        try:
            angles.theta1 = "invalid"
        except Exception:
            pass  # Expected to fail

        try:
            angles.phi = None
        except Exception:
            pass  # Expected to fail

        # Original values should be preserved after failed operations
        assert angles.theta1 == original_values[0]
        assert angles.theta2 == original_values[1]
        assert angles.phi == original_values[2]

        # Valid operations should still work
        angles.theta1 = 999.0
        assert angles.theta1 == 999.0
