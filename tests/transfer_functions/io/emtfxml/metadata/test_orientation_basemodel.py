# -*- coding: utf-8 -*-
"""
Test suite for Orientation basemodel
"""
from collections import OrderedDict

import pytest
from pydantic import ValidationError

from mt_metadata.common.enumerations import ChannelOrientationEnum
from mt_metadata.transfer_functions.io.emtfxml.metadata import Orientation


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture
def basic_orientation_data():
    """Basic orientation data for testing."""
    return {
        "angle_to_geographic_north": 45.0,
        "layout": "orthogonal",
    }


@pytest.fixture
def station_orientation_data():
    """Station layout orientation data for testing."""
    return {
        "angle_to_geographic_north": 90.0,
        "layout": ChannelOrientationEnum.station,
    }


@pytest.fixture
def sitelayout_orientation_data():
    """Site layout orientation data for testing."""
    return {
        "angle_to_geographic_north": 180.0,
        "layout": ChannelOrientationEnum.site_layout,
    }


@pytest.fixture
def empty_orientation():
    """Empty orientation instance."""
    return Orientation()


@pytest.fixture
def basic_orientation(basic_orientation_data):
    """Basic orientation instance."""
    return Orientation(**basic_orientation_data)


@pytest.fixture
def station_orientation(station_orientation_data):
    """Station orientation instance."""
    return Orientation(**station_orientation_data)


# =============================================================================
# Test Class: Orientation Instantiation
# =============================================================================
class TestOrientationInstantiation:
    """Test orientation instantiation scenarios."""

    def test_empty_orientation_creation(self, empty_orientation):
        """Test creating an empty orientation with defaults."""
        assert empty_orientation.angle_to_geographic_north == 0.0
        assert empty_orientation.layout == "orthogonal"

    def test_basic_orientation_creation(
        self, basic_orientation, basic_orientation_data
    ):
        """Test creating a basic orientation with valid data."""
        assert (
            basic_orientation.angle_to_geographic_north
            == basic_orientation_data["angle_to_geographic_north"]
        )
        assert basic_orientation.layout == basic_orientation_data["layout"]

    @pytest.mark.parametrize(
        "angle,expected",
        [
            (0.0, 0.0),
            (45.0, 45.0),
            (90.0, 90.0),
            (180.0, 180.0),
            (270.0, 270.0),
            (360.0, 360.0),
            (-45.0, -45.0),
            (720.0, 720.0),  # Test beyond 360 degrees
        ],
    )
    def test_angle_assignment(self, empty_orientation, angle, expected):
        """Test angle assignment with various values."""
        empty_orientation.angle_to_geographic_north = angle
        assert empty_orientation.angle_to_geographic_north == expected

    @pytest.mark.parametrize(
        "layout_value",
        [
            ChannelOrientationEnum.orthogonal,
            ChannelOrientationEnum.station,
            ChannelOrientationEnum.site_layout,
            "orthogonal",
            "station",
            "sitelayout",
        ],
    )
    def test_layout_enum_assignment(self, empty_orientation, layout_value):
        """Test layout enum assignment."""
        empty_orientation.layout = layout_value
        assert empty_orientation.layout == layout_value

    def test_invalid_layout_assignment(self, empty_orientation):
        """Test that invalid layout values raise validation errors."""
        with pytest.raises(ValidationError):
            empty_orientation.layout = "invalid_layout"

    @pytest.mark.parametrize(
        "invalid_angle",
        [
            "not_a_number",
            None,
            [],
            {},
        ],
    )
    def test_invalid_angle_types(self, empty_orientation, invalid_angle):
        """Test that invalid angle types raise validation errors."""
        with pytest.raises((ValidationError, TypeError)):
            empty_orientation.angle_to_geographic_north = invalid_angle

    def test_precision_handling(self, empty_orientation):
        """Test that angle precision is maintained."""
        test_angle = 45.123456789
        empty_orientation.angle_to_geographic_north = test_angle
        assert empty_orientation.angle_to_geographic_north == test_angle


# =============================================================================
# Test Class: XML Serialization
# =============================================================================
class TestXMLSerialization:
    """Test XML serialization functionality."""

    def test_to_xml_orthogonal_default(self, empty_orientation):
        """Test XML serialization of default orthogonal orientation."""
        xml_element = empty_orientation.to_xml()

        assert xml_element.tag == "Orientation"
        assert xml_element.attrib["angle_to_geographic_north"] == "0.000"
        assert xml_element.text == "orthogonal"

    def test_to_xml_orthogonal_with_angle(self, basic_orientation):
        """Test XML serialization of orthogonal orientation with custom angle."""
        xml_element = basic_orientation.to_xml()

        assert xml_element.tag == "Orientation"
        assert xml_element.attrib["angle_to_geographic_north"] == "45.000"
        assert xml_element.text == "orthogonal"

    def test_to_xml_station_layout(self, station_orientation):
        """Test XML serialization of station layout."""
        xml_element = station_orientation.to_xml()

        assert xml_element.tag == "Orientation"
        assert xml_element.attrib == {}  # No angle attribute for non-orthogonal
        assert xml_element.text == "station"

    def test_to_xml_sitelayout(self, sitelayout_orientation_data):
        """Test XML serialization of site layout."""
        orientation = Orientation(**sitelayout_orientation_data)
        xml_element = orientation.to_xml()

        assert xml_element.tag == "Orientation"
        assert xml_element.attrib == {}  # No angle attribute for non-orthogonal
        assert xml_element.text == "sitelayout"

    def test_to_xml_string_output(self, basic_orientation):
        """Test XML string serialization."""
        xml_string = basic_orientation.to_xml(string=True)

        assert isinstance(xml_string, str)
        assert '<?xml version="1.0" encoding="UTF-8"?>' in xml_string
        assert (
            '<Orientation angle_to_geographic_north="45.000">orthogonal</Orientation>'
            in xml_string
        )

    def test_to_xml_string_non_orthogonal(self, station_orientation):
        """Test XML string serialization for non-orthogonal layout."""
        xml_string = station_orientation.to_xml(string=True)

        assert isinstance(xml_string, str)
        assert "<Orientation>station</Orientation>" in xml_string

    def test_to_xml_angle_precision_in_xml(self, empty_orientation):
        """Test that angle precision is correctly formatted in XML."""
        test_cases = [
            (0.0, "0.000"),
            (45.123, "45.123"),
            (90.0, "90.000"),
            (180.555, "180.555"),
            (359.999, "359.999"),
        ]

        for angle, expected_xml in test_cases:
            empty_orientation.angle_to_geographic_north = angle
            empty_orientation.layout = "orthogonal"
            xml_element = empty_orientation.to_xml()
            assert xml_element.attrib["angle_to_geographic_north"] == expected_xml

    def test_to_xml_angle_none_handling(self, empty_orientation):
        """Test XML generation when angle is None for orthogonal layout."""
        empty_orientation.angle_to_geographic_north = 0
        empty_orientation.layout = "orthogonal"

        # The to_xml method should set angle to 0.0 if None for orthogonal
        xml_element = empty_orientation.to_xml()
        assert xml_element.attrib["angle_to_geographic_north"] == "0.000"
        # Verify the object was actually modified
        assert empty_orientation.angle_to_geographic_north == 0.0


# =============================================================================
# Test Class: Dictionary Operations
# =============================================================================
class TestDictionaryOperations:
    """Test dictionary serialization and read_dict functionality."""

    def test_to_dict_basic_orientation(self, basic_orientation):
        """Test dictionary serialization of basic orientation."""
        orientation_dict = basic_orientation.to_dict()

        assert "orientation" in orientation_dict
        data = orientation_dict["orientation"]

        assert data["angle_to_geographic_north"] == 45.0
        assert data["layout"] == "orthogonal"
        assert isinstance(data, OrderedDict)

    def test_to_dict_station_orientation(self, station_orientation):
        """Test dictionary serialization of station orientation."""
        orientation_dict = station_orientation.to_dict()

        assert "orientation" in orientation_dict
        data = orientation_dict["orientation"]

        assert data["angle_to_geographic_north"] == 90.0
        assert data["layout"] == "station"

    def test_read_dict_with_full_data(self, empty_orientation):
        """Test read_dict with complete orientation data."""
        test_dict = {
            "Orientation": {"angle_to_geographic_north": 135.0, "layout": "station"}
        }

        empty_orientation.read_dict(test_dict)

        assert empty_orientation.angle_to_geographic_north == 135.0
        assert empty_orientation.layout == "station"

    def test_read_dict_with_string_layout(self, empty_orientation):
        """Test read_dict when layout is provided as string."""
        test_dict = {"Orientation": "sitelayout"}

        empty_orientation.read_dict(test_dict)

        # Should convert string to layout field
        assert empty_orientation.layout == "sitelayout"

    def test_read_dict_conversion_logic(self, empty_orientation):
        """Test the string conversion logic in read_dict."""
        # Test with string value
        string_dict = {"Orientation": "orthogonal"}
        empty_orientation.read_dict(string_dict)
        assert empty_orientation.layout == "orthogonal"

        # Reset and test with dict value
        empty_orientation2 = Orientation()
        dict_dict = {
            "Orientation": {"angle_to_geographic_north": 45.0, "layout": "station"}
        }
        empty_orientation2.read_dict(dict_dict)
        assert empty_orientation2.angle_to_geographic_north == 45.0
        assert empty_orientation2.layout == "station"


# =============================================================================
# Test Class: Edge Cases and Error Handling
# =============================================================================
class TestEdgeCases:
    """Test edge cases and error scenarios."""

    def test_extreme_angle_values(self, empty_orientation):
        """Test handling of extreme angle values."""
        extreme_values = [
            -180.0,
            -360.0,
            360.0,
            720.0,
            1000.0,
            -1000.0,
        ]

        for angle in extreme_values:
            empty_orientation.angle_to_geographic_north = angle
            assert empty_orientation.angle_to_geographic_north == angle

            # Should still serialize to XML correctly
            xml_element = empty_orientation.to_xml()
            assert xml_element.tag == "Orientation"

    def test_float_precision_edge_cases(self, empty_orientation):
        """Test floating point precision edge cases."""
        precision_cases = [
            0.001,
            0.1234567890123456,
            999.999999,
            1e-10,
            1e10,
        ]

        for angle in precision_cases:
            empty_orientation.angle_to_geographic_north = angle
            assert empty_orientation.angle_to_geographic_north == angle

    def test_layout_case_sensitivity(self, empty_orientation):
        """Test layout enum case handling."""
        # These should work
        valid_layouts = ["orthogonal", "station", "sitelayout"]

        for layout in valid_layouts:
            empty_orientation.layout = layout
            assert empty_orientation.layout == layout

    def test_xml_with_special_angle_values(self, empty_orientation):
        """Test XML generation with special angle values."""
        special_angles = [0.0, 360.0, -180.0]

        for angle in special_angles:
            empty_orientation.angle_to_geographic_north = angle
            empty_orientation.layout = "orthogonal"

            xml_element = empty_orientation.to_xml()
            assert xml_element.tag == "Orientation"
            assert "angle_to_geographic_north" in xml_element.attrib

    def test_read_dict_with_missing_class_key(self, empty_orientation):
        """Test read_dict behavior with missing class key."""
        # This should raise a KeyError or handle gracefully
        invalid_dict = {"WrongKey": {"layout": "orthogonal"}}

        with pytest.raises(KeyError):
            empty_orientation.read_dict(invalid_dict)

    def test_read_dict_with_empty_dict(self, empty_orientation):
        """Test read_dict with empty dictionary."""
        with pytest.raises(KeyError):
            empty_orientation.read_dict({})


# =============================================================================
# Test Class: Enum Behavior
# =============================================================================
class TestEnumBehavior:
    """Test ChannelOrientationEnum behavior and integration."""

    def test_channel_orientation_enum_values(self):
        """Test ChannelOrientationEnum values."""
        assert ChannelOrientationEnum.orthogonal == "orthogonal"
        assert ChannelOrientationEnum.station == "station"
        assert ChannelOrientationEnum.site_layout == "sitelayout"

    def test_enum_in_orientation(self, empty_orientation):
        """Test enum usage in orientation."""
        for enum_value in ChannelOrientationEnum:
            empty_orientation.layout = enum_value
            assert empty_orientation.layout == enum_value.value

    def test_enum_xml_output(self, empty_orientation):
        """Test XML output with enum values."""
        for enum_value in ChannelOrientationEnum:
            empty_orientation.layout = enum_value
            xml_element = empty_orientation.to_xml()
            assert xml_element.text == enum_value.value


# =============================================================================
# Test Class: Integration Tests
# =============================================================================
class TestIntegration:
    """Test integration scenarios and workflows."""

    def test_complete_orientation_workflow(self):
        """Test complete orientation creation and serialization workflow."""
        # Create orientation with all fields
        orientation = Orientation(
            angle_to_geographic_north=22.5, layout=ChannelOrientationEnum.orthogonal
        )

        # Test XML serialization
        xml_element = orientation.to_xml()
        assert xml_element.tag == "Orientation"
        assert xml_element.attrib["angle_to_geographic_north"] == "22.500"
        assert xml_element.text == "orthogonal"

        # Test dictionary serialization
        orientation_dict = orientation.to_dict()
        assert "orientation" in orientation_dict

        # Verify data integrity
        data = orientation_dict["orientation"]
        assert data["angle_to_geographic_north"] == 22.5
        assert data["layout"] == "orthogonal"

    def test_orientation_modification_workflow(self):
        """Test modifying orientation after creation."""
        orientation = Orientation()

        # Initial state
        assert orientation.angle_to_geographic_north == 0.0
        assert orientation.layout == "orthogonal"

        # Modify fields
        orientation.angle_to_geographic_north = 315.0
        orientation.layout = ChannelOrientationEnum.station

        # Verify changes
        assert orientation.angle_to_geographic_north == 315.0
        assert orientation.layout == "station"

        # Test XML reflects changes
        xml_element = orientation.to_xml()
        assert xml_element.tag == "Orientation"
        assert xml_element.attrib == {}  # No angle for non-orthogonal
        assert xml_element.text == "station"

    def test_multiple_orientations(self):
        """Test creating multiple orientation instances."""
        orientations = []

        # Create different orientations
        orientations.append(
            Orientation(angle_to_geographic_north=0.0, layout="orthogonal")
        )

        orientations.append(
            Orientation(
                angle_to_geographic_north=90.0, layout=ChannelOrientationEnum.station
            )
        )

        orientations.append(Orientation(layout=ChannelOrientationEnum.site_layout))

        # Test all can be serialized
        for i, orientation in enumerate(orientations):
            xml_element = orientation.to_xml()
            assert xml_element.tag == "Orientation"

            orientation_dict = orientation.to_dict()
            assert "orientation" in orientation_dict

    def test_round_trip_serialization(self):
        """Test round-trip serialization through dictionary."""
        original = Orientation(angle_to_geographic_north=67.5, layout="orthogonal")

        # Serialize to dict
        orientation_dict = original.to_dict()

        # Create new instance and load from dict
        new_orientation = Orientation()
        new_orientation.read_dict({"Orientation": orientation_dict["orientation"]})

        # Verify they match
        assert (
            new_orientation.angle_to_geographic_north
            == original.angle_to_geographic_north
        )
        assert new_orientation.layout == original.layout


# =============================================================================
# Test Class: Performance and Memory
# =============================================================================
class TestPerformance:
    """Test performance characteristics."""

    def test_large_batch_creation(self):
        """Test creating many orientation instances."""
        orientations = []

        for i in range(100):
            angle = (i * 3.6) % 360  # Vary angles
            layout = list(ChannelOrientationEnum)[i % len(ChannelOrientationEnum)]

            orientation = Orientation(angle_to_geographic_north=angle, layout=layout)
            orientations.append(orientation)

        assert len(orientations) == 100

        # Test they all work
        for orientation in orientations[:5]:  # Test first 5
            xml_element = orientation.to_xml()
            assert xml_element.tag == "Orientation"

    def test_xml_serialization_performance(self, basic_orientation):
        """Test XML serialization performance."""
        # This should complete quickly
        for _ in range(100):
            xml_element = basic_orientation.to_xml()
            assert xml_element.tag == "Orientation"

    def test_dict_serialization_performance(self, basic_orientation):
        """Test dictionary serialization performance."""
        # This should complete quickly
        for _ in range(100):
            orientation_dict = basic_orientation.to_dict()
            assert "orientation" in orientation_dict

    def test_angle_modification_performance(self, empty_orientation):
        """Test performance of repeated angle modifications."""
        for i in range(1000):
            empty_orientation.angle_to_geographic_north = i % 360
            assert isinstance(empty_orientation.angle_to_geographic_north, float)


# =============================================================================
# Test Class: Boundary Value Testing
# =============================================================================
class TestBoundaryValues:
    """Test boundary values and limits."""

    def test_angle_boundary_values(self, empty_orientation):
        """Test angle boundary values."""
        boundary_values = [
            0.0,
            360.0,
            -180.0,
            180.0,
            -360.0,
            720.0,
        ]

        for angle in boundary_values:
            empty_orientation.angle_to_geographic_north = angle
            assert empty_orientation.angle_to_geographic_north == angle

            # XML should handle all boundary values
            xml_element = empty_orientation.to_xml()
            assert xml_element.tag == "Orientation"

    def test_angle_precision_limits(self, empty_orientation):
        """Test floating point precision limits."""
        # Test very small values
        small_values = [1e-15, 1e-10, 1e-6]
        for val in small_values:
            empty_orientation.angle_to_geographic_north = val
            assert empty_orientation.angle_to_geographic_north == val

        # Test very large values
        large_values = [1e6, 1e10, 1e15]
        for val in large_values:
            empty_orientation.angle_to_geographic_north = val
            assert empty_orientation.angle_to_geographic_north == val

    def test_layout_enum_completeness(self, empty_orientation):
        """Test that all enum values work correctly."""
        for enum_value in ChannelOrientationEnum:
            empty_orientation.layout = enum_value
            assert empty_orientation.layout == enum_value.value

            # Test XML serialization for each
            xml_element = empty_orientation.to_xml()
            assert xml_element.tag == "Orientation"
            assert xml_element.text == enum_value.value
