# -*- coding: utf-8 -*-
"""
Test suite for Dipole basemodel
"""
from unittest.mock import patch

import pytest

from mt_metadata.transfer_functions.io.emtfxml.metadata import Dipole, Electrode
from mt_metadata.transfer_functions.io.emtfxml.metadata.electrode import LocationEnum


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture
def basic_dipole_data():
    """Basic dipole data for testing."""
    return {
        "manufacturer": "MT Gurus",
        "length": 100.0,
        "azimuth": 90.0,
        "name": "dipole_ex",
        "type": "wire",
    }


@pytest.fixture
def electrode_data():
    """Electrode data for testing."""
    return [
        {
            "number": "1",
            "location": "N",
            "comments": "Test electrode 1",
        },
        {
            "number": "2",
            "location": "S",
            "comments": "Test electrode 2",
        },
    ]


@pytest.fixture
def dipole_with_electrodes_data(basic_dipole_data, electrode_data):
    """Complete dipole data with electrodes."""
    return {
        **basic_dipole_data,
        "electrode": electrode_data,
    }


@pytest.fixture
def empty_dipole():
    """Empty dipole instance."""
    return Dipole()


@pytest.fixture
def basic_dipole(basic_dipole_data):
    """Basic dipole instance."""
    return Dipole(**basic_dipole_data)


@pytest.fixture
def dipole_with_electrodes(dipole_with_electrodes_data):
    """Dipole instance with electrodes."""
    return Dipole(**dipole_with_electrodes_data)


# =============================================================================
# Test Class: Dipole Instantiation
# =============================================================================
class TestDipoleInstantiation:
    """Test dipole instantiation scenarios."""

    def test_empty_dipole_creation(self, empty_dipole):
        """Test creating an empty dipole."""
        assert empty_dipole.manufacturer is None
        assert empty_dipole.length is None
        assert empty_dipole.azimuth is None
        assert empty_dipole.name is None
        assert empty_dipole.type is None
        assert empty_dipole.electrode == []

    def test_basic_dipole_creation(self, basic_dipole, basic_dipole_data):
        """Test creating a basic dipole with valid data."""
        assert basic_dipole.manufacturer == basic_dipole_data["manufacturer"]
        assert basic_dipole.length == basic_dipole_data["length"]
        assert basic_dipole.azimuth == basic_dipole_data["azimuth"]
        assert basic_dipole.name == basic_dipole_data["name"]
        assert basic_dipole.type == basic_dipole_data["type"]
        assert basic_dipole.electrode == []

    @pytest.mark.parametrize(
        "field,value,expected",
        [
            ("manufacturer", "Test Corp", "Test Corp"),
            ("manufacturer", "", ""),
            ("manufacturer", None, None),
            ("length", 50.0, 50.0),
            ("length", 0.0, 0.0),
            ("length", None, None),
            ("azimuth", 45.0, 45.0),
            ("azimuth", 0.0, 0.0),
            ("azimuth", 360.0, 360.0),
            ("azimuth", None, None),
            ("name", "custom_dipole", "custom_dipole"),
            ("name", "", ""),
            ("name", None, None),
            ("type", "cable", "cable"),
            ("type", "", ""),
            ("type", None, None),
        ],
    )
    def test_field_assignment(self, empty_dipole, field, value, expected):
        """Test individual field assignment."""
        setattr(empty_dipole, field, value)
        assert getattr(empty_dipole, field) == expected

    def test_dipole_with_electrode_objects(self):
        """Test creating dipole with Electrode objects."""
        electrode1 = Electrode(number="1", location=LocationEnum.N, comments="test1")
        electrode2 = Electrode(number="2", location=LocationEnum.S, comments="test2")

        dipole = Dipole(name="test_dipole", electrode=[electrode1, electrode2])

        assert len(dipole.electrode) == 2
        assert isinstance(dipole.electrode[0], Electrode)
        assert isinstance(dipole.electrode[1], Electrode)
        assert dipole.electrode[0].number == "1"
        assert dipole.electrode[1].number == "2"

    def test_dipole_with_electrode_dicts(self, electrode_data):
        """Test creating dipole with electrode dictionaries."""
        dipole = Dipole(name="test_dipole", electrode=electrode_data)

        assert len(dipole.electrode) == 2
        assert all(isinstance(e, Electrode) for e in dipole.electrode)
        assert dipole.electrode[0].number == "1"
        assert dipole.electrode[1].number == "2"


# =============================================================================
# Test Class: Electrode Validation
# =============================================================================
class TestElectrodeValidation:
    """Test electrode field validation."""

    def test_electrode_validator_with_list_of_dicts(self, empty_dipole):
        """Test electrode validator with list of dictionaries."""
        electrode_dicts = [
            {"number": "1", "location": "N"},
            {"number": "2", "location": "S"},
        ]

        empty_dipole.electrode = electrode_dicts

        assert len(empty_dipole.electrode) == 2
        assert all(isinstance(e, Electrode) for e in empty_dipole.electrode)

    def test_electrode_validator_with_list_of_objects(self, empty_dipole):
        """Test electrode validator with list of Electrode objects."""
        electrodes = [
            Electrode(number="1", location=LocationEnum.N, comments="test1"),
            Electrode(number="2", location=LocationEnum.S, comments="test2"),
        ]

        empty_dipole.electrode = electrodes

        assert len(empty_dipole.electrode) == 2
        assert all(isinstance(e, Electrode) for e in empty_dipole.electrode)

    def test_electrode_validator_with_single_dict(self, empty_dipole):
        """Test electrode validator with single dictionary."""
        electrode_dict = {"number": "1", "location": "N"}

        empty_dipole.electrode = electrode_dict

        assert len(empty_dipole.electrode) == 1
        assert isinstance(empty_dipole.electrode[0], Electrode)
        assert empty_dipole.electrode[0].number == "1"

    def test_electrode_validator_with_single_object(self, empty_dipole):
        """Test electrode validator with single Electrode object."""
        electrode = Electrode(number="1", location=LocationEnum.N, comments="test")

        empty_dipole.electrode = electrode

        assert len(empty_dipole.electrode) == 1
        assert isinstance(empty_dipole.electrode[0], Electrode)

    def test_electrode_validator_with_invalid_type(self, empty_dipole):
        """Test electrode validator with invalid type raises TypeError."""
        with pytest.raises(
            TypeError,
            match="Electrode must be an instance of Electrode class or a dict",
        ):
            empty_dipole.electrode = ["invalid_string"]

    def test_electrode_validator_with_mixed_types(self, empty_dipole):
        """Test electrode validator with mixed valid types."""
        electrode_obj = Electrode(number="1", location=LocationEnum.N, comments="test1")
        electrode_dict = {"number": "2", "location": "S"}

        empty_dipole.electrode = [electrode_obj, electrode_dict]

        assert len(empty_dipole.electrode) == 2
        assert all(isinstance(e, Electrode) for e in empty_dipole.electrode)
        assert empty_dipole.electrode[0].number == "1"
        assert empty_dipole.electrode[1].number == "2"


# =============================================================================
# Test Class: XML Serialization
# =============================================================================
class TestXMLSerialization:
    """Test XML serialization functionality."""

    def test_to_xml_empty_dipole(self, empty_dipole):
        """Test XML serialization of empty dipole."""
        xml_element = empty_dipole.to_xml()

        assert xml_element.tag == "Dipole"
        assert xml_element.attrib["name"] is None
        assert xml_element.attrib["type"] is None
        # Empty dipole still has manufacturer element with None text
        assert len(xml_element) == 1
        manufacturer_elem = xml_element.find("manufacturer")
        assert manufacturer_elem is not None
        assert manufacturer_elem.text is None

    def test_to_xml_basic_dipole(self, basic_dipole):
        """Test XML serialization of basic dipole."""
        xml_element = basic_dipole.to_xml()

        assert xml_element.tag == "Dipole"
        assert xml_element.attrib["name"] == "dipole_ex"
        assert xml_element.attrib["type"] == "wire"

        # Check child elements
        children = {child.tag: child for child in xml_element}
        assert "manufacturer" in children
        assert children["manufacturer"].text == "MT Gurus"
        assert "length" in children
        assert children["length"].text == "100.000"
        assert children["length"].attrib["units"] == "meters"
        assert "azimuth" in children
        assert children["azimuth"].text == "90.000"
        assert children["azimuth"].attrib["units"] == "degrees"

    def test_to_xml_with_electrodes(self, dipole_with_electrodes):
        """Test XML serialization of dipole with electrodes."""
        xml_element = dipole_with_electrodes.to_xml()

        assert xml_element.tag == "Dipole"

        # Count electrode elements
        electrode_elements = [
            child for child in xml_element if child.tag == "Electrode"
        ]
        assert len(electrode_elements) == 2

    @pytest.mark.parametrize(
        "field,value,expected_xml_text",
        [
            ("manufacturer", "Test Corp", "Test Corp"),
            ("manufacturer", "", ""),
            ("length", 25.5, "25.500"),
            ("length", 0.0, "0.000"),
            ("azimuth", 180.0, "180.000"),
            ("azimuth", 45.123, "45.123"),
        ],
    )
    def test_to_xml_field_formatting(
        self, empty_dipole, field, value, expected_xml_text
    ):
        """Test XML formatting of individual fields."""
        setattr(empty_dipole, field, value)
        empty_dipole.name = "test"
        empty_dipole.type = "test"

        xml_element = empty_dipole.to_xml()

        if field in ["length", "azimuth"]:
            child = xml_element.find(field)
            assert child is not None
            assert child.text == expected_xml_text
        elif field == "manufacturer":
            child = xml_element.find(field)
            if value is not None:
                assert child is not None
                assert child.text == expected_xml_text

    def test_to_xml_string_output(self, basic_dipole):
        """Test XML string output."""
        with patch(
            "mt_metadata.transfer_functions.io.emtfxml.metadata.helpers.element_to_string"
        ) as mock_element_to_string:
            mock_element_to_string.return_value = "<Dipole>test</Dipole>"

            xml_string = basic_dipole.to_xml(string=True)

            mock_element_to_string.assert_called_once()
            assert xml_string == "<Dipole>test</Dipole>"

    def test_to_xml_no_manufacturer_debug_log(self, empty_dipole):
        """Test that missing manufacturer logs debug message."""
        empty_dipole.name = "test"
        empty_dipole.type = "test"

        # The debug log is only called on AttributeError, not when manufacturer is None
        # So we need to test with an object that doesn't have manufacturer attribute
        with patch(
            "mt_metadata.transfer_functions.io.emtfxml.metadata.dipole_basemodel.logger"
        ) as mock_logger:
            # Remove the manufacturer attribute to trigger AttributeError
            delattr(empty_dipole, "manufacturer")
            xml_element = empty_dipole.to_xml()

            mock_logger.debug.assert_called_once_with(
                "Dipole has no manufacturer information"
            )

    def test_to_xml_none_values_skipped(self, empty_dipole):
        """Test that None values are properly skipped in XML."""
        empty_dipole.name = "test"
        empty_dipole.type = "test"
        empty_dipole.manufacturer = None
        empty_dipole.length = None
        empty_dipole.azimuth = None

        xml_element = empty_dipole.to_xml()

        # Should have name and type in attributes, manufacturer element with None text
        assert xml_element.attrib["name"] == "test"
        assert xml_element.attrib["type"] == "test"
        # Manufacturer element is created but has None text
        assert len(xml_element) == 1
        manufacturer_elem = xml_element.find("manufacturer")
        assert manufacturer_elem is not None
        assert manufacturer_elem.text is None


# =============================================================================
# Test Class: Edge Cases and Error Handling
# =============================================================================
class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.parametrize(
        "invalid_value",
        [
            "not_a_number",
            [],
            {},
            object(),
        ],
    )
    def test_invalid_numeric_fields(self, empty_dipole, invalid_value):
        """Test assignment of invalid values to numeric fields."""
        with pytest.raises((ValueError, TypeError)):
            empty_dipole.length = invalid_value

    @pytest.mark.parametrize(
        "extreme_value",
        [
            -1000.0,
            1e10,
            float("inf"),
            -float("inf"),
        ],
    )
    def test_extreme_numeric_values(self, empty_dipole, extreme_value):
        """Test handling of extreme numeric values."""
        # Should accept extreme but finite values
        if extreme_value not in [float("inf"), -float("inf")]:
            empty_dipole.length = extreme_value
            assert empty_dipole.length == extreme_value

            empty_dipole.azimuth = extreme_value
            assert empty_dipole.azimuth == extreme_value

    def test_very_long_strings(self, empty_dipole):
        """Test handling of very long strings."""
        long_string = "x" * 1000

        empty_dipole.manufacturer = long_string
        assert empty_dipole.manufacturer == long_string

        empty_dipole.name = long_string
        assert empty_dipole.name == long_string

        empty_dipole.type = long_string
        assert empty_dipole.type == long_string

    def test_unicode_strings(self, empty_dipole):
        """Test handling of unicode strings."""
        unicode_string = "测试中文字符🌍🔬"

        empty_dipole.manufacturer = unicode_string
        assert empty_dipole.manufacturer == unicode_string

        empty_dipole.name = unicode_string
        assert empty_dipole.name == unicode_string

    def test_electrode_list_modification(self, dipole_with_electrodes):
        """Test modification of electrode list after creation."""
        original_count = len(dipole_with_electrodes.electrode)

        new_electrode = Electrode(number="3", location=LocationEnum.E, comments="test")
        dipole_with_electrodes.electrode.append(new_electrode)

        assert len(dipole_with_electrodes.electrode) == original_count + 1
        assert dipole_with_electrodes.electrode[-1].number == "3"

    def test_empty_electrode_list_xml(self, basic_dipole):
        """Test XML generation with empty electrode list."""
        assert basic_dipole.electrode == []

        xml_element = basic_dipole.to_xml()
        electrode_children = [
            child for child in xml_element if child.tag == "Electrode"
        ]

        assert len(electrode_children) == 0


# =============================================================================
# Test Class: Serialization and Deserialization
# =============================================================================
class TestSerialization:
    """Test serialization and deserialization methods."""

    def test_to_dict_empty_dipole(self, empty_dipole):
        """Test dictionary serialization of empty dipole."""
        result = empty_dipole.to_dict()

        assert isinstance(result, dict)
        assert "dipole" in result
        dipole_data = result["dipole"]
        # Empty dipole has no keys in the nested dict
        assert len(dipole_data) == 0

    def test_to_dict_basic_dipole(self, basic_dipole, basic_dipole_data):
        """Test dictionary serialization of basic dipole."""
        result = basic_dipole.to_dict()

        assert isinstance(result, dict)
        assert "dipole" in result
        dipole_data = result["dipole"]
        for key, expected_value in basic_dipole_data.items():
            assert dipole_data[key] == expected_value

    def test_to_dict_with_electrodes(self, dipole_with_electrodes):
        """Test dictionary serialization of dipole with electrodes."""
        result = dipole_with_electrodes.to_dict()

        assert isinstance(result, dict)
        assert "dipole" in result
        dipole_data = result["dipole"]
        assert "electrode" in dipole_data
        assert isinstance(dipole_data["electrode"], list)
        assert len(dipole_data["electrode"]) == 2
        assert all(isinstance(e, dict) for e in dipole_data["electrode"])

    def test_from_dict_round_trip(self, dipole_with_electrodes_data):
        """Test round-trip serialization via dictionary."""
        original_dipole = Dipole(**dipole_with_electrodes_data)
        dipole_dict = original_dipole.to_dict()
        reconstructed_dipole = Dipole(**dipole_dict)

        assert original_dipole.manufacturer == reconstructed_dipole.manufacturer
        assert original_dipole.length == reconstructed_dipole.length
        assert original_dipole.azimuth == reconstructed_dipole.azimuth
        assert original_dipole.name == reconstructed_dipole.name
        assert original_dipole.type == reconstructed_dipole.type
        assert len(original_dipole.electrode) == len(reconstructed_dipole.electrode)

    def test_json_schema_extra_metadata(self, empty_dipole):
        """Test that json_schema_extra metadata is preserved."""
        schema = empty_dipole.model_json_schema()

        # Check that each field has the expected json_schema_extra properties
        for field_name in [
            "manufacturer",
            "length",
            "azimuth",
            "name",
            "type",
            "electrode",
        ]:
            field_schema = schema["properties"][field_name]
            assert "units" in field_schema
            assert "required" in field_schema
            assert "examples" in field_schema


# =============================================================================
# Test Class: Integration Tests
# =============================================================================
class TestIntegration:
    """Test integration scenarios."""

    def test_complex_dipole_xml_integration(self):
        """Test complex dipole with multiple electrodes XML generation."""
        # Create electrodes with different configurations
        electrode1 = Electrode(
            number="1", location=LocationEnum.N, comments="Northern electrode"
        )
        electrode2 = Electrode(
            number="2", location=LocationEnum.S, comments="Southern electrode"
        )

        # Create dipole
        dipole = Dipole(
            manufacturer="Advanced MT Systems",
            length=150.0,
            azimuth=0.0,
            name="ns_dipole",
            type="cable",
            electrode=[electrode1, electrode2],
        )

        # Generate XML
        xml_element = dipole.to_xml()

        # Verify structure
        assert xml_element.tag == "Dipole"
        assert xml_element.attrib["name"] == "ns_dipole"
        assert xml_element.attrib["type"] == "cable"

        # Verify child elements
        children = {child.tag: child for child in xml_element}
        assert children["manufacturer"].text == "Advanced MT Systems"
        assert children["length"].text == "150.000"
        assert children["azimuth"].text == "0.000"

        # Verify electrode children
        electrode_elements = [
            child for child in xml_element if child.tag == "Electrode"
        ]
        assert len(electrode_elements) == 2

    def test_dipole_with_partial_data(self):
        """Test dipole creation and XML with partial data."""
        dipole = Dipole(
            name="partial_dipole",
            azimuth=45.0,
            # Missing manufacturer, length, type, electrodes use defaults
        )

        xml_element = dipole.to_xml()

        assert xml_element.tag == "Dipole"
        assert xml_element.attrib["name"] == "partial_dipole"
        assert xml_element.attrib["type"] is None

        # Should have azimuth but not length or manufacturer
        children = {child.tag: child for child in xml_element}
        assert "azimuth" in children
        assert "length" not in children
        # Manufacturer should not be in children due to AttributeError handling


# =============================================================================
# Test Class: Performance Tests
# =============================================================================
class TestPerformance:
    """Test performance aspects."""

    def test_large_electrode_list_performance(self):
        """Test performance with large electrode list."""
        # Create many electrodes
        electrodes = []
        for i in range(100):
            electrodes.append(
                {
                    "number": f"{i}",
                    "location": "N" if i % 2 == 0 else "S",
                }
            )

        # Should create without significant delay
        dipole = Dipole(name="large_dipole", electrode=electrodes)

        assert len(dipole.electrode) == 100
        assert all(isinstance(e, Electrode) for e in dipole.electrode)

    def test_xml_generation_performance(self, dipole_with_electrodes):
        """Test XML generation performance."""
        # Should generate XML without significant delay
        xml_element = dipole_with_electrodes.to_xml()
        xml_string = dipole_with_electrodes.to_xml(string=True)

        assert xml_element is not None
        assert isinstance(xml_string, str)

    def test_repeated_field_access(self, basic_dipole):
        """Test repeated field access performance."""
        # Repeated access should be fast
        for _ in range(1000):
            _ = basic_dipole.manufacturer
            _ = basic_dipole.length
            _ = basic_dipole.azimuth
            _ = basic_dipole.name
            _ = basic_dipole.type
            _ = basic_dipole.electrode


# =============================================================================
# Test Class: Boundary Value Tests
# =============================================================================
class TestBoundaryValues:
    """Test boundary value scenarios."""

    @pytest.mark.parametrize(
        "azimuth_value",
        [
            0.0,
            90.0,
            180.0,
            270.0,
            360.0,
            -180.0,
            450.0,  # > 360
            -450.0,  # < -360
        ],
    )
    def test_azimuth_boundary_values(self, empty_dipole, azimuth_value):
        """Test azimuth boundary values."""
        empty_dipole.azimuth = azimuth_value
        assert empty_dipole.azimuth == azimuth_value

    @pytest.mark.parametrize(
        "length_value",
        [
            0.0,
            0.001,  # Very small positive
            1000000.0,  # Very large
        ],
    )
    def test_length_boundary_values(self, empty_dipole, length_value):
        """Test length boundary values."""
        empty_dipole.length = length_value
        assert empty_dipole.length == length_value

    def test_empty_string_fields(self, empty_dipole):
        """Test empty string handling."""
        empty_dipole.manufacturer = ""
        empty_dipole.name = ""
        empty_dipole.type = ""

        assert empty_dipole.manufacturer == ""
        assert empty_dipole.name == ""
        assert empty_dipole.type == ""

        # XML should handle empty strings
        xml_element = empty_dipole.to_xml()
        assert xml_element.attrib["name"] == ""
        assert xml_element.attrib["type"] == ""
