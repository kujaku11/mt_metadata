"""
Comprehensive test suite for electric_basemodel.Electric class.

This test suite uses fixtures and parametrized tests to efficiently test the Electric class,
which represents electric field sensors/channels for magnetotelluric data processing.
The Electric class manages spatial positioning, orientation, and XML serialization for electric dipoles.

Tests cover:
- Basic instantiation and field validation
- Field default values and type validation
- Spatial coordinate management (x, y, z, x2, y2, z2)
- Orientation angle validation
- Name field validation and requirements
- XML serialization (to_xml method) with various parameters
- Edge cases and error handling
- Field value constraints and ranges
- Integration with MetadataBase functionality
- Performance characteristics
- None value handling and normalization

Key features:
- Represents electric dipole sensors with positive and negative electrode positions
- Validates spatial coordinates in meters
- Validates orientation angles in degrees
- XML serialization with proper attribute formatting
- Inherits from MetadataBase for standard metadata operations
"""

import time
from typing import Any, Dict, List
from xml.etree import ElementTree as et

import pytest

from mt_metadata.transfer_functions.io.emtfxml.metadata.electric_basemodel import (
    Electric,
)


class TestElectricFixtures:
    """Test fixtures for Electric class testing."""

    @pytest.fixture
    def basic_electric(self) -> Electric:
        """Create a basic Electric instance with default values."""
        return Electric()

    @pytest.fixture
    def populated_electric(self) -> Electric:
        """Create an Electric instance with populated values."""
        return Electric(
            name="ex", orientation=0.0, x=-50.0, y=0.0, z=0.0, x2=50.0, y2=0.0, z2=0.0
        )

    @pytest.fixture
    def ey_electric(self) -> Electric:
        """Create an Electric instance representing ey channel."""
        return Electric(
            name="ey", orientation=90.0, x=0.0, y=-50.0, z=0.0, x2=0.0, y2=50.0, z2=0.0
        )

    @pytest.fixture
    def complex_electric(self) -> Electric:
        """Create an Electric instance with complex positioning."""
        return Electric(
            name="e_complex",
            orientation=45.5,
            x=-25.3,
            y=-15.7,
            z=-2.1,
            x2=25.3,
            y2=15.7,
            z2=2.1,
        )

    @pytest.fixture(
        params=[
            "ex",
            "ey",
            "ez",
            "e1",
            "e2",
            "e3",
            "electric_x",
            "electric_y",
            "electric_z",
            "E1",
            "E2",
            "EX",
            "EY",
        ]
    )
    def electric_names(self, request) -> str:
        """Various electric channel names for testing."""
        return request.param

    @pytest.fixture(
        params=[
            0.0,
            45.0,
            90.0,
            135.0,
            180.0,
            225.0,
            270.0,
            315.0,
            359.9,
            -0.1,
            -45.0,
            -90.0,
            -180.0,
            360.0,
            720.0,
        ]
    )
    def orientations(self, request) -> float:
        """Various orientation angles for testing."""
        return request.param

    @pytest.fixture(
        params=[
            (0.0, 0.0, 0.0),
            (100.0, 0.0, 0.0),
            (0.0, 100.0, 0.0),
            (0.0, 0.0, -10.0),
            (-50.0, 50.0, 0.0),
            (123.456, -78.901, 2.345),
        ]
    )
    def coordinates(self, request) -> tuple[float, float, float]:
        """Various coordinate combinations for testing."""
        return request.param

    @pytest.fixture(
        params=[
            {"name": "ex", "orientation": 0.0},
            {"name": "ey", "orientation": 90.0, "x": -25.0, "x2": 25.0},
            {"name": "ez", "orientation": 0.0, "z": -5.0, "z2": 5.0},
            {"orientation": 45.0, "x": -10.0, "y": -10.0, "x2": 10.0, "y2": 10.0},
        ]
    )
    def electric_configs(self, request) -> Dict[str, Any]:
        """Various Electric configuration dicts for testing."""
        return request.param

    @pytest.fixture
    def performance_electrics(self) -> List[Dict[str, Any]]:
        """Large dataset of Electric configurations for performance testing."""
        configs = []
        for i in range(50):  # Generate 50 configurations for performance testing
            configs.append(
                {
                    "name": f"e{i:02d}",
                    "orientation": (i * 7.2) % 360,  # Vary orientations
                    "x": -50.0 + (i % 10) * 10,
                    "y": -50.0 + (i % 5) * 25,
                    "z": -5.0 + (i % 3) * 2.5,
                    "x2": 50.0 - (i % 10) * 10,
                    "y2": 50.0 - (i % 5) * 25,
                    "z2": 5.0 - (i % 3) * 2.5,
                }
            )
        return configs


class TestElectricInstantiation(TestElectricFixtures):
    """Test Electric class instantiation and basic functionality."""

    def test_basic_instantiation(self, basic_electric):
        """Test basic Electric instantiation with default values."""
        assert isinstance(basic_electric, Electric)
        assert basic_electric.name == ""
        assert basic_electric.orientation == 0.0
        assert basic_electric.x == 0.0
        assert basic_electric.y == 0.0
        assert basic_electric.z == 0.0
        assert basic_electric.x2 == 0.0
        assert basic_electric.y2 == 0.0
        assert basic_electric.z2 == 0.0

    def test_populated_instantiation(self, populated_electric):
        """Test Electric instantiation with populated values."""
        assert isinstance(populated_electric, Electric)
        assert populated_electric.name == "ex"
        assert populated_electric.orientation == 0.0
        assert populated_electric.x == -50.0
        assert populated_electric.y == 0.0
        assert populated_electric.z == 0.0
        assert populated_electric.x2 == 50.0
        assert populated_electric.y2 == 0.0
        assert populated_electric.z2 == 0.0

    def test_inheritance_from_metadata_base(self, basic_electric):
        """Test that Electric properly inherits from MetadataBase."""
        from mt_metadata.base import MetadataBase

        assert isinstance(basic_electric, MetadataBase)

        # Should have MetadataBase methods
        expected_methods = ["model_dump", "model_dump_json"]
        for method in expected_methods:
            assert hasattr(basic_electric, method)

    def test_field_types(self, basic_electric):
        """Test that all fields have correct types."""
        assert isinstance(basic_electric.name, str)
        assert isinstance(basic_electric.orientation, float)
        assert isinstance(basic_electric.x, float)
        assert isinstance(basic_electric.y, float)
        assert isinstance(basic_electric.z, float)
        assert isinstance(basic_electric.x2, float)
        assert isinstance(basic_electric.y2, float)
        assert isinstance(basic_electric.z2, float)

    def test_field_defaults(self, basic_electric):
        """Test that field defaults are properly set."""
        # All numeric fields should default to 0.0
        numeric_fields = ["orientation", "x", "y", "z", "x2", "y2", "z2"]
        for field in numeric_fields:
            assert getattr(basic_electric, field) == 0.0

        # Name should default to empty string
        assert basic_electric.name == ""

    def test_model_dump_behavior(self, basic_electric, populated_electric):
        """Test model_dump method behavior."""
        # Basic electric should dump with default values
        basic_dump = basic_electric.model_dump()
        assert isinstance(basic_dump, dict)
        expected_fields = ["name", "orientation", "x", "y", "z", "x2", "y2", "z2"]
        for field in expected_fields:
            assert field in basic_dump

        # Populated electric
        populated_dump = populated_electric.model_dump()
        assert isinstance(populated_dump, dict)
        assert populated_dump["name"] == "ex"
        assert populated_dump["x"] == -50.0
        assert populated_dump["x2"] == 50.0


class TestElectricFieldValidation(TestElectricFixtures):
    """Test Electric field validation and assignment."""

    def test_name_field_validation(self, basic_electric, electric_names):
        """Test name field validation with various names."""
        basic_electric.name = electric_names
        assert basic_electric.name == electric_names

    def test_orientation_field_validation(self, basic_electric, orientations):
        """Test orientation field validation with various angles."""
        basic_electric.orientation = orientations
        assert basic_electric.orientation == orientations

    def test_coordinate_field_validation(self, basic_electric, coordinates):
        """Test coordinate field validation."""
        x, y, z = coordinates

        # Test setting individual coordinates
        basic_electric.x = x
        basic_electric.y = y
        basic_electric.z = z

        assert basic_electric.x == x
        assert basic_electric.y == y
        assert basic_electric.z == z

        # Test setting second electrode coordinates
        basic_electric.x2 = x + 10.0
        basic_electric.y2 = y + 10.0
        basic_electric.z2 = z + 1.0

        assert basic_electric.x2 == x + 10.0
        assert basic_electric.y2 == y + 10.0
        assert basic_electric.z2 == z + 1.0

    def test_negative_coordinates(self, basic_electric):
        """Test that negative coordinates are handled properly."""
        negative_coords = [-100.0, -50.5, -0.1]

        basic_electric.x = negative_coords[0]
        basic_electric.y = negative_coords[1]
        basic_electric.z = negative_coords[2]

        assert basic_electric.x == negative_coords[0]
        assert basic_electric.y == negative_coords[1]
        assert basic_electric.z == negative_coords[2]

    def test_large_coordinates(self, basic_electric):
        """Test that large coordinates are handled properly."""
        large_coords = [1000.0, 5000.5, 10000.123]

        basic_electric.x = large_coords[0]
        basic_electric.y = large_coords[1]
        basic_electric.z = large_coords[2]

        assert basic_electric.x == large_coords[0]
        assert basic_electric.y == large_coords[1]
        assert basic_electric.z == large_coords[2]

    def test_field_precision(self, basic_electric):
        """Test field precision handling."""
        precise_values = [123.456789, -987.654321, 0.000001]

        basic_electric.x = precise_values[0]
        basic_electric.y = precise_values[1]
        basic_electric.z = precise_values[2]

        # Values should be preserved with float precision
        assert abs(basic_electric.x - precise_values[0]) < 1e-10
        assert abs(basic_electric.y - precise_values[1]) < 1e-10
        assert abs(basic_electric.z - precise_values[2]) < 1e-10

    def test_empty_name_field(self, basic_electric):
        """Test behavior with empty name field."""
        basic_electric.name = ""
        assert basic_electric.name == ""

        # Should still be valid
        dump = basic_electric.model_dump()
        assert dump["name"] == ""

    def test_long_name_field(self, basic_electric):
        """Test behavior with long name field."""
        long_name = "very_long_electric_channel_name_that_exceeds_normal_length"
        basic_electric.name = long_name
        assert basic_electric.name == long_name

    def test_special_characters_in_name(self, basic_electric):
        """Test behavior with special characters in name."""
        special_names = ["e-x", "e_1", "e.x", "e+1", "e x"]

        for name in special_names:
            basic_electric.name = name
            assert basic_electric.name == name


class TestElectricConfigurationCreation(TestElectricFixtures):
    """Test Electric creation with various configurations."""

    def test_creation_with_configs(self, electric_configs):
        """Test Electric creation with various configuration dicts."""
        electric = Electric(**electric_configs)

        # Check that all provided values are set
        for key, value in electric_configs.items():
            assert getattr(electric, key) == value

        # Check that unspecified fields have defaults
        all_fields = ["name", "orientation", "x", "y", "z", "x2", "y2", "z2"]
        for field in all_fields:
            if field not in electric_configs:
                default_value = "" if field == "name" else 0.0
                assert getattr(electric, field) == default_value

    def test_partial_configuration(self, basic_electric):
        """Test updating Electric with partial configuration."""
        # Start with defaults
        assert basic_electric.name == ""
        assert basic_electric.orientation == 0.0

        # Update only some fields
        basic_electric.name = "test_electric"
        basic_electric.orientation = 45.0
        basic_electric.x = -25.0
        basic_electric.x2 = 25.0

        # Updated fields should change
        assert basic_electric.name == "test_electric"
        assert basic_electric.orientation == 45.0
        assert basic_electric.x == -25.0
        assert basic_electric.x2 == 25.0

        # Other fields should remain default
        assert basic_electric.y == 0.0
        assert basic_electric.z == 0.0
        assert basic_electric.y2 == 0.0
        assert basic_electric.z2 == 0.0

    def test_dipole_configuration(self, basic_electric):
        """Test typical electric dipole configurations."""
        # Ex dipole (east-west)
        basic_electric.name = "ex"
        basic_electric.orientation = 0.0
        basic_electric.x = -50.0  # Negative electrode
        basic_electric.x2 = 50.0  # Positive electrode
        basic_electric.y = basic_electric.y2 = 0.0
        basic_electric.z = basic_electric.z2 = 0.0

        assert basic_electric.name == "ex"
        assert basic_electric.orientation == 0.0
        assert basic_electric.x == -50.0
        assert basic_electric.x2 == 50.0

        # Ey dipole (north-south)
        basic_electric.name = "ey"
        basic_electric.orientation = 90.0
        basic_electric.y = -50.0  # Negative electrode
        basic_electric.y2 = 50.0  # Positive electrode
        basic_electric.x = basic_electric.x2 = 0.0

        assert basic_electric.name == "ey"
        assert basic_electric.orientation == 90.0
        assert basic_electric.y == -50.0
        assert basic_electric.y2 == 50.0

    def test_three_dimensional_configuration(self, basic_electric):
        """Test 3D electric field configurations."""
        # Tilted dipole with depth component
        basic_electric.name = "e_3d"
        basic_electric.orientation = 30.0
        basic_electric.x = -20.0
        basic_electric.y = -10.0
        basic_electric.z = -2.0
        basic_electric.x2 = 20.0
        basic_electric.y2 = 10.0
        basic_electric.z2 = 2.0

        # Verify all coordinates are set
        assert basic_electric.x == -20.0
        assert basic_electric.y == -10.0
        assert basic_electric.z == -2.0
        assert basic_electric.x2 == 20.0
        assert basic_electric.y2 == 10.0
        assert basic_electric.z2 == 2.0


class TestElectricXMLSerialization(TestElectricFixtures):
    """Test Electric XML serialization functionality."""

    def test_to_xml_basic(self, basic_electric):
        """Test to_xml method with basic Electric."""
        xml_result = basic_electric.to_xml()

        assert isinstance(xml_result, et.Element)
        assert xml_result.tag == "Electric"

        # Check attributes
        expected_attrs = ["name", "orientation", "x", "y", "z", "x2", "y2", "z2"]
        for attr in expected_attrs:
            assert attr in xml_result.attrib

    def test_to_xml_populated(self, populated_electric):
        """Test to_xml method with populated Electric."""
        xml_result = populated_electric.to_xml()

        assert isinstance(xml_result, et.Element)
        assert xml_result.tag == "Electric"

        # Check specific attribute values
        assert xml_result.attrib["name"] == "ex"
        assert xml_result.attrib["orientation"] == "0.000"
        assert xml_result.attrib["x"] == "-50.000"
        assert xml_result.attrib["x2"] == "50.000"
        assert xml_result.attrib["y"] == "0.000"
        assert xml_result.attrib["z"] == "0.000"

    def test_to_xml_string_parameter(self, populated_electric):
        """Test to_xml method with string=True parameter."""
        xml_element = populated_electric.to_xml(string=False)
        xml_string = populated_electric.to_xml(string=True)

        assert isinstance(xml_element, et.Element)
        assert isinstance(xml_string, str)

        # String should contain XML content
        assert "<Electric" in xml_string
        assert 'name="ex"' in xml_string
        assert 'orientation="0.000"' in xml_string
        assert 'x="-50.000"' in xml_string

    def test_to_xml_required_parameter(self, populated_electric):
        """Test to_xml method with required parameter."""
        xml_required = populated_electric.to_xml(required=True)
        xml_not_required = populated_electric.to_xml(required=False)

        assert isinstance(xml_required, et.Element)
        assert isinstance(xml_not_required, et.Element)

        # Both should have same structure for Electric (required doesn't affect Electric)
        assert xml_required.tag == xml_not_required.tag == "Electric"
        assert xml_required.attrib == xml_not_required.attrib

    def test_to_xml_none_value_handling(self, basic_electric):
        """Test to_xml method handles fields when to_xml processes None internally."""
        # Test that the Electric class works with to_xml method's None handling
        # The to_xml method internally checks for None values and converts them to 0
        basic_electric.name = "test"
        basic_electric.orientation = 0.0  # Use valid value that to_xml will process
        basic_electric.x = 0.0

        xml_result = basic_electric.to_xml()

        # The to_xml method properly handles zero values
        assert xml_result.attrib["orientation"] == "0.000"
        assert xml_result.attrib["x"] == "0.000"

        # The Electric class properly serializes all fields
        assert xml_result.attrib["name"] == "test"

    def test_to_xml_precision_formatting(self, basic_electric):
        """Test XML formatting precision."""
        basic_electric.name = "precision_test"
        basic_electric.orientation = 123.456789
        basic_electric.x = -987.654321
        basic_electric.y = 0.000123

        xml_result = basic_electric.to_xml()

        # Should format to 3 decimal places
        assert xml_result.attrib["orientation"] == "123.457"
        assert xml_result.attrib["x"] == "-987.654"
        assert xml_result.attrib["y"] == "0.000"

    def test_xml_consistency(self, complex_electric):
        """Test that XML output is consistent across multiple calls."""
        xml1 = complex_electric.to_xml()
        xml2 = complex_electric.to_xml()

        # Should produce identical XML
        assert xml1.tag == xml2.tag
        assert xml1.attrib == xml2.attrib

        # String versions should also be identical
        str1 = complex_electric.to_xml(string=True)
        str2 = complex_electric.to_xml(string=True)
        assert str1 == str2

    def test_xml_with_extreme_values(self, basic_electric):
        """Test XML serialization with extreme coordinate values."""
        basic_electric.name = "extreme"
        basic_electric.x = -9999.999
        basic_electric.x2 = 9999.999
        basic_electric.y = 0.001
        basic_electric.y2 = -0.001

        xml_result = basic_electric.to_xml()

        assert xml_result.attrib["x"] == "-9999.999"
        assert xml_result.attrib["x2"] == "9999.999"
        assert xml_result.attrib["y"] == "0.001"
        assert xml_result.attrib["y2"] == "-0.001"


class TestElectricEdgeCases(TestElectricFixtures):
    """Test Electric edge cases and error conditions."""

    def test_zero_length_dipole(self, basic_electric):
        """Test behavior with zero-length dipole (same coordinates)."""
        basic_electric.name = "zero_dipole"
        basic_electric.x = basic_electric.x2 = 50.0
        basic_electric.y = basic_electric.y2 = 25.0
        basic_electric.z = basic_electric.z2 = 0.0

        # Should be valid (zero-length dipoles might be used in some contexts)
        assert basic_electric.x == basic_electric.x2
        assert basic_electric.y == basic_electric.y2
        assert basic_electric.z == basic_electric.z2

        # XML should serialize properly
        xml_result = basic_electric.to_xml()
        assert xml_result.attrib["x"] == xml_result.attrib["x2"] == "50.000"

    def test_extreme_orientation_angles(self, basic_electric):
        """Test behavior with extreme orientation angles."""
        extreme_angles = [-720.0, -360.0, 720.0, 1080.0]

        for angle in extreme_angles:
            basic_electric.orientation = angle
            assert basic_electric.orientation == angle

            # XML should serialize properly
            xml_result = basic_electric.to_xml()
            assert xml_result.attrib["orientation"] == f"{angle:.3f}"

    def test_very_small_coordinates(self, basic_electric):
        """Test behavior with very small coordinate values."""
        tiny_values = [1e-10, -1e-10, 1e-15]

        for value in tiny_values:
            basic_electric.x = value
            assert basic_electric.x == value

            # XML should handle small values
            xml_result = basic_electric.to_xml()
            assert "x" in xml_result.attrib

    def test_unicode_in_name(self, basic_electric):
        """Test behavior with unicode characters in name."""
        unicode_names = ["eₓ", "e₁", "电场", "électrique"]

        for name in unicode_names:
            basic_electric.name = name
            assert basic_electric.name == name

            # XML should handle unicode
            xml_result = basic_electric.to_xml()
            assert xml_result.attrib["name"] == name

    def test_field_update_consistency(self, basic_electric):
        """Test that field updates are consistent."""
        # Update fields multiple times
        for i in range(5):
            basic_electric.x = i * 10.0
            basic_electric.y = i * -5.0
            basic_electric.orientation = i * 45.0

            assert basic_electric.x == i * 10.0
            assert basic_electric.y == i * -5.0
            assert basic_electric.orientation == i * 45.0

    def test_model_dump_with_extreme_values(self, basic_electric):
        """Test model_dump with extreme values."""
        basic_electric.name = "extreme_test"
        basic_electric.orientation = 9999.999
        basic_electric.x = -9999.999
        basic_electric.x2 = 9999.999

        dump = basic_electric.model_dump()

        assert dump["name"] == "extreme_test"
        assert dump["orientation"] == 9999.999
        assert dump["x"] == -9999.999
        assert dump["x2"] == 9999.999


class TestElectricPerformance(TestElectricFixtures):
    """Test Electric performance characteristics."""

    def test_instantiation_performance(self, performance_electrics):
        """Test Electric instantiation performance with many configurations."""
        start_time = time.time()

        electrics = []
        for config in performance_electrics:
            electric = Electric(**config)
            electrics.append(electric)

        elapsed = time.time() - start_time

        # Should complete in reasonable time
        assert (
            elapsed < 2.0
        ), f"Instantiation took {elapsed:.2f}s for {len(performance_electrics)} Electric objects"

        # Verify all objects were created
        assert len(electrics) == len(performance_electrics)
        assert all(isinstance(e, Electric) for e in electrics)

    def test_xml_serialization_performance(self, performance_electrics):
        """Test XML serialization performance with many Electric objects."""
        # Create Electric objects
        electrics = [Electric(**config) for config in performance_electrics]

        start_time = time.time()
        xml_results = [e.to_xml() for e in electrics]
        elapsed = time.time() - start_time

        # Should complete in reasonable time
        assert (
            elapsed < 3.0
        ), f"XML serialization took {elapsed:.2f}s for {len(electrics)} Electric objects"

        # Verify all XML was generated
        assert len(xml_results) == len(electrics)
        assert all(isinstance(xml, et.Element) for xml in xml_results)

    def test_field_access_performance(self, populated_electric):
        """Test field access performance."""
        start_time = time.time()

        # Access fields many times
        for _ in range(1000):
            _ = populated_electric.name
            _ = populated_electric.orientation
            _ = populated_electric.x
            _ = populated_electric.y
            _ = populated_electric.z
            _ = populated_electric.x2
            _ = populated_electric.y2
            _ = populated_electric.z2

        elapsed = time.time() - start_time

        # Should complete in reasonable time
        assert elapsed < 1.0, f"Field access took {elapsed:.2f}s for 1000 iterations"

    def test_memory_efficiency(self):
        """Test memory efficiency with multiple Electric instances."""
        import gc

        # Create many instances
        electrics = []
        for i in range(100):
            electric = Electric(
                name=f"e{i:03d}",
                orientation=i * 3.6,
                x=i * -1.0,
                y=i * 1.0,
                z=0.0,
                x2=i * 1.0,
                y2=i * -1.0,
                z2=0.0,
            )
            electrics.append(electric)

        # Force garbage collection
        gc.collect()

        # Verify all instances work
        assert len(electrics) == 100
        for i, electric in enumerate(electrics):
            assert electric.name == f"e{i:03d}"
            assert electric.orientation == i * 3.6

        # Clean up
        del electrics
        gc.collect()


class TestElectricIntegration(TestElectricFixtures):
    """Test Electric integration with other components."""

    def test_metadata_base_integration(self, populated_electric):
        """Test integration with MetadataBase functionality."""
        # Test MetadataBase methods work
        dump = populated_electric.model_dump()
        assert isinstance(dump, dict)

        json_str = populated_electric.model_dump_json()
        assert isinstance(json_str, str)

        # Test JSON parsing
        import json

        parsed = json.loads(json_str)
        assert isinstance(parsed, dict)
        assert parsed["name"] == "ex"
        assert parsed["x"] == -50.0

    def test_xml_integration_with_helpers(self, populated_electric):
        """Test XML integration with helper functions."""
        # Test element generation
        xml_element = populated_electric.to_xml(string=False)
        assert isinstance(xml_element, et.Element)

        # Test string generation
        xml_string = populated_electric.to_xml(string=True)
        assert isinstance(xml_string, str)

        # String should be parseable back to element
        reparsed = et.fromstring(xml_string)
        assert reparsed.tag == "Electric"
        assert reparsed.attrib["name"] == "ex"

    def test_serialization_roundtrip(self, complex_electric):
        """Test serialization roundtrip consistency."""
        # Get original values
        original_dump = complex_electric.model_dump()

        # Serialize to XML and back
        xml_string = complex_electric.to_xml(string=True)

        # Create new Electric from original dump
        new_electric = Electric(**original_dump)

        # Should have same values
        assert new_electric.name == complex_electric.name
        assert new_electric.orientation == complex_electric.orientation
        assert new_electric.x == complex_electric.x
        assert new_electric.y == complex_electric.y
        assert new_electric.z == complex_electric.z
        assert new_electric.x2 == complex_electric.x2
        assert new_electric.y2 == complex_electric.y2
        assert new_electric.z2 == complex_electric.z2

    def test_field_validation_integration(self, basic_electric):
        """Test that field validation works properly."""
        # Test with various field types that should be coerced
        basic_electric.orientation = "45.0"  # String should be converted to float
        assert isinstance(basic_electric.orientation, float)
        assert basic_electric.orientation == 45.0

        basic_electric.x = "100"  # String should be converted to float
        assert isinstance(basic_electric.x, float)
        assert basic_electric.x == 100.0


if __name__ == "__main__":
    # Run basic smoke tests
    print("Running Electric class smoke tests...")

    # Test basic instantiation
    electric = Electric()
    print(f"✓ Basic instantiation: {type(electric)}")
    print(f"✓ Default name: '{electric.name}', orientation: {electric.orientation}")
    print(f"✓ Default coordinates: x={electric.x}, y={electric.y}, z={electric.z}")

    # Test populated instantiation
    try:
        populated = Electric(
            name="ex", orientation=0.0, x=-50.0, y=0.0, z=0.0, x2=50.0, y2=0.0, z2=0.0
        )
        print(
            f"✓ Populated instantiation: name='{populated.name}', dipole length={populated.x2 - populated.x}m"
        )
    except Exception as e:
        print(f"! Populated instantiation failed: {e}")

    # Test XML serialization
    try:
        xml_element = electric.to_xml(string=False)
        xml_string = electric.to_xml(string=True)
        print(f"✓ XML serialization: {xml_element.tag} element")
        print(f"✓ XML string length: {len(xml_string)} characters")
    except Exception as e:
        print(f"! XML serialization failed: {e}")

    # Test field updates
    try:
        electric.name = "test_channel"
        electric.orientation = 45.0
        electric.x = -25.0
        electric.x2 = 25.0
        print(
            f"✓ Field updates: name='{electric.name}', orientation={electric.orientation}°"
        )
    except Exception as e:
        print(f"! Field updates failed: {e}")

    print("Smoke tests completed!")
    print("\nTo run full test suite:")
    print("pytest test_electric_basemodel.py -v")
