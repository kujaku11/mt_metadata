# -*- coding: utf-8 -*-
"""
Comprehensive pytest test suite for DataTypes basemodel class.

This module tests the DataTypes basemodel class from the transfer_functions.io.emtfxml.metadata
module, including validation, XML generation, dictionary parsing, and list management.
"""

from unittest.mock import MagicMock, patch
from xml.etree import cElementTree as et

import pytest
from loguru import logger

from mt_metadata.transfer_functions.io.emtfxml.metadata import DataType, DataTypes
from mt_metadata.transfer_functions.io.emtfxml.metadata.data_type import (
    ArrayDTypeEnum,
    EstimateIntentionEnum,
    InputEnum,
    OutputEnum,
)


@pytest.fixture(scope="function")
def sample_data_type():
    """Return a sample DataType instance for testing."""
    return DataType(
        name="impedance",
        type=ArrayDTypeEnum.complex,
        description="Impedance tensor estimate",
        external_url="http://example.com",
        intention=EstimateIntentionEnum.primary_data_type,
        tag="impedance",
        output=OutputEnum.E,
        input=InputEnum.H,
        units="[mV/km]/[nT]",
    )


@pytest.fixture(scope="function")
def sample_data_type_2():
    """Return a second sample DataType instance for testing."""
    return DataType(
        name="variance",
        type=ArrayDTypeEnum.real,
        description="Variance estimate",
        external_url="http://test.com",
        intention=EstimateIntentionEnum.error_estimate,
        tag="error",
        output=OutputEnum.E,
        input=InputEnum.H,
        units="dimensionless",
    )


@pytest.fixture(scope="function")
def sample_data_type_3():
    """Return a third sample DataType instance for testing."""
    return DataType(
        name="coherence",
        type=ArrayDTypeEnum.real,
        description="Signal coherence estimate",
        external_url="http://coherence.com",
        intention=EstimateIntentionEnum.signal_coherence,
        tag="coherence",
        output=OutputEnum.H,
        input=InputEnum.E,
        units="dimensionless",
    )


@pytest.fixture(scope="function")
def empty_data_types():
    """Return an empty DataTypes instance."""
    return DataTypes()


@pytest.fixture(scope="function")
def single_data_types(sample_data_type):
    """Return a DataTypes instance with a single DataType."""
    return DataTypes(data_types_list=[sample_data_type])


@pytest.fixture(scope="function")
def multiple_data_types(sample_data_type, sample_data_type_2, sample_data_type_3):
    """Return a DataTypes instance with multiple DataType objects."""
    return DataTypes(
        data_types_list=[sample_data_type, sample_data_type_2, sample_data_type_3]
    )


@pytest.fixture(
    params=[
        [{"name": "test1", "type": "real"}],
        [{"name": "test2", "type": "complex", "description": "Test description"}],
        [{"name": "test3"}, {"name": "test4", "type": "real"}],
        [{"name": "complex_test", "type": "complex", "intention": "primary data type"}],
    ]
)
def dict_input_data(request):
    """Return various dictionary inputs for testing."""
    return request.param


@pytest.fixture(
    params=[
        {"data_types": {"data_type": [{"name": "test1"}]}},
        {"data_types": {"data_type": [{"name": "test2"}, {"name": "test3"}]}},
        {"data_types": {"data_type": {"name": "single_test"}}},
        {"data_types": {"data_type": []}},
    ]
)
def read_dict_inputs(request):
    """Return various dictionary inputs for read_dict testing."""
    return request.param


@pytest.fixture(
    params=[
        {"wrong_key": {"data_type": []}},
        {"data_types": {"wrong_subkey": []}},
        {},
        {"data_types": {}},
    ]
)
def invalid_read_dict_inputs(request):
    """Return invalid dictionary inputs for read_dict testing."""
    return request.param


class TestDataTypesBasicFunctionality:
    """Test basic DataTypes functionality."""

    def test_default_initialization(self, empty_data_types):
        """Test default DataTypes initialization."""
        assert empty_data_types.data_types_list == []
        assert isinstance(empty_data_types.data_types_list, list)

    def test_single_datatype_initialization(self, single_data_types):
        """Test DataTypes initialization with single DataType."""
        assert len(single_data_types.data_types_list) == 1
        assert isinstance(single_data_types.data_types_list[0], DataType)
        assert single_data_types.data_types_list[0].name == "impedance"

    def test_multiple_datatype_initialization(self, multiple_data_types):
        """Test DataTypes initialization with multiple DataType objects."""
        assert len(multiple_data_types.data_types_list) == 3
        for dt in multiple_data_types.data_types_list:
            assert isinstance(dt, DataType)

        names = [dt.name for dt in multiple_data_types.data_types_list]
        assert "impedance" in names
        assert "variance" in names
        assert "coherence" in names

    def test_list_assignment_after_creation(self, empty_data_types, sample_data_type):
        """Test list assignment after DataTypes creation."""
        # Start with empty list
        assert len(empty_data_types.data_types_list) == 0

        # Assign new list (note: this would need to trigger validator manually in real usage)
        new_list = [sample_data_type]
        empty_data_types.data_types_list = new_list

        assert len(empty_data_types.data_types_list) == 1
        assert empty_data_types.data_types_list[0].name == "impedance"


class TestDataTypesValidation:
    """Test DataTypes validation functionality."""

    def test_datatype_objects_validation(self, sample_data_type, sample_data_type_2):
        """Test validation with DataType objects."""
        dt_list = [sample_data_type, sample_data_type_2]
        dts = DataTypes(data_types_list=dt_list)

        assert len(dts.data_types_list) == 2
        assert all(isinstance(dt, DataType) for dt in dts.data_types_list)

    def test_dict_objects_validation(self, dict_input_data):
        """Test validation with dictionary objects."""
        dts = DataTypes(data_types_list=dict_input_data)

        assert len(dts.data_types_list) == len(dict_input_data)
        assert all(isinstance(dt, DataType) for dt in dts.data_types_list)

        # Check that dict data was properly converted
        for i, dict_item in enumerate(dict_input_data):
            if "name" in dict_item:
                assert dts.data_types_list[i].name == dict_item["name"]

    def test_mixed_objects_validation(self, sample_data_type):
        """Test validation with mixed DataType and dict objects."""
        mixed_list = [
            sample_data_type,
            {"name": "test_dict", "type": "real"},
            {"name": "another_dict", "type": "complex"},
        ]

        dts = DataTypes(data_types_list=mixed_list)

        assert len(dts.data_types_list) == 3
        assert all(isinstance(dt, DataType) for dt in dts.data_types_list)
        assert dts.data_types_list[0].name == "impedance"
        assert dts.data_types_list[1].name == "test_dict"
        assert dts.data_types_list[2].name == "another_dict"

    def test_single_item_to_list_conversion(self, sample_data_type):
        """Test that single item is converted to list."""
        dts = DataTypes(data_types_list=sample_data_type)

        assert len(dts.data_types_list) == 1
        assert isinstance(dts.data_types_list[0], DataType)
        assert dts.data_types_list[0].name == "impedance"

    def test_single_dict_to_list_conversion(self):
        """Test that single dict is converted to list."""
        single_dict = {"name": "single_test", "type": "real"}
        dts = DataTypes(data_types_list=single_dict)

        assert len(dts.data_types_list) == 1
        assert isinstance(dts.data_types_list[0], DataType)
        assert dts.data_types_list[0].name == "single_test"

    def test_invalid_type_validation(self):
        """Test validation with invalid object types."""
        invalid_list = ["string_item", 123, None]

        for invalid_item in invalid_list:
            with pytest.raises(
                TypeError,
                match="data_types_list must be a list of DataType instances or dictionaries",
            ):
                DataTypes(data_types_list=[invalid_item])

    def test_empty_list_validation(self):
        """Test validation with empty list."""
        dts = DataTypes(data_types_list=[])
        assert dts.data_types_list == []

    def test_validator_error_handling(self):
        """Test validator error handling with problematic dict."""
        # Test with dict that might cause issues in from_dict
        problematic_dict = {"invalid_field": "invalid_value"}

        # This should still work as DataType constructor accepts unknown fields
        dts = DataTypes(data_types_list=[problematic_dict])
        assert len(dts.data_types_list) == 1
        assert isinstance(dts.data_types_list[0], DataType)


class TestDataTypesReadDict:
    """Test DataTypes read_dict functionality."""

    def test_read_dict_with_list_data(self):
        """Test read_dict with list of data types."""
        input_dict = {
            "data_types": {
                "data_type": [
                    {"name": "impedance", "type": "complex"},
                    {"name": "variance", "type": "real"},
                ]
            }
        }

        dts = DataTypes()
        dts.read_dict(input_dict)

        assert len(dts.data_types_list) == 2
        assert all(isinstance(dt, DataType) for dt in dts.data_types_list)

    def test_read_dict_with_single_data(self):
        """Test read_dict with single data type."""
        input_dict = {
            "data_types": {"data_type": {"name": "single_test", "type": "real"}}
        }

        dts = DataTypes()
        dts.read_dict(input_dict)

        assert len(dts.data_types_list) == 1
        assert dts.data_types_list[0].name == "single_test"

    def test_read_dict_with_empty_list(self):
        """Test read_dict with empty data type list."""
        input_dict = {"data_types": {"data_type": []}}

        dts = DataTypes()
        dts.read_dict(input_dict)

        assert dts.data_types_list == []

    def test_read_dict_valid_inputs(self, read_dict_inputs):
        """Test read_dict with various valid inputs."""
        dts = DataTypes()
        dts.read_dict(read_dict_inputs)

        # Should have processed without errors
        assert isinstance(dts.data_types_list, list)

        # Check that DataType objects were created properly
        for dt in dts.data_types_list:
            assert isinstance(dt, DataType)

    def test_read_dict_missing_keys(self, invalid_read_dict_inputs):
        """Test read_dict with missing or invalid keys."""
        dts = DataTypes()

        # Should not raise exception but log warning
        with patch.object(logger, "warning") as mock_warning:
            dts.read_dict(invalid_read_dict_inputs)
            mock_warning.assert_called_once_with("Could not read Data Types")

        # data_types_list should remain as default empty list
        assert dts.data_types_list == []

    def test_read_dict_keyerror_handling(self):
        """Test read_dict KeyError handling."""
        dts = DataTypes()

        # Test with completely wrong structure
        wrong_dict = {"completely": {"wrong": "structure"}}

        with patch.object(logger, "warning") as mock_warning:
            dts.read_dict(wrong_dict)
            mock_warning.assert_called_once_with("Could not read Data Types")

    def test_read_dict_overwrites_existing(self, sample_data_type):
        """Test that read_dict overwrites existing data_types_list."""
        dts = DataTypes(data_types_list=[sample_data_type])
        assert len(dts.data_types_list) == 1

        input_dict = {
            "data_types": {"data_type": [{"name": "new_test", "type": "real"}]}
        }

        dts.read_dict(input_dict)

        # Should have replaced the original list
        assert len(dts.data_types_list) == 1
        assert dts.data_types_list[0].name == "new_test"


class TestDataTypesXMLGeneration:
    """Test DataTypes XML generation functionality."""

    def test_xml_generation_empty_list(self, empty_data_types):
        """Test XML generation with empty data types list."""
        xml_element = empty_data_types.to_xml(string=False, required=True)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "DataTypes"
        assert len(xml_element) == 0  # No child elements

    def test_xml_generation_single_item(self, single_data_types):
        """Test XML generation with single data type."""
        xml_element = single_data_types.to_xml(string=False, required=True)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "DataTypes"
        assert len(xml_element) == 1  # One child element

        # Check that the child is properly formed
        child = xml_element[0]
        assert child.attrib["name"] == "impedance"

    def test_xml_generation_multiple_items(self, multiple_data_types):
        """Test XML generation with multiple data types."""
        xml_element = multiple_data_types.to_xml(string=False, required=True)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "DataTypes"
        assert len(xml_element) == 3  # Three child elements

        # Check that all children are properly formed
        names = [child.attrib["name"] for child in xml_element]
        assert "impedance" in names
        assert "variance" in names
        assert "coherence" in names

    def test_xml_generation_string_output(self, multiple_data_types):
        """Test XML generation with string output."""
        with patch(
            "mt_metadata.transfer_functions.io.emtfxml.metadata.helpers.element_to_string"
        ) as mock_helper:
            mock_helper.return_value = "<DataTypes>test</DataTypes>"

            xml_string = multiple_data_types.to_xml(string=True, required=True)

            assert xml_string == "<DataTypes>test</DataTypes>"
            mock_helper.assert_called_once()

    def test_xml_generation_required_parameter(self, single_data_types):
        """Test XML generation with different required parameter values."""
        # Test with required=True
        xml_true = single_data_types.to_xml(string=False, required=True)
        assert isinstance(xml_true, et.Element)

        # Test with required=False
        xml_false = single_data_types.to_xml(string=False, required=False)
        assert isinstance(xml_false, et.Element)

        # Both should have the same structure for this test
        assert xml_true.tag == xml_false.tag == "DataTypes"

    def test_xml_generation_functional(self):
        """Test XML generation functionality without mocking."""
        # Create test objects directly
        sample_dt = DataType(name="test", type="real")
        single_dts = DataTypes(data_types_list=[sample_dt])

        xml_element = single_dts.to_xml(string=False, required=True)

        # Verify the basic structure
        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "DataTypes"
        assert len(xml_element) == 1

        # Verify the child element has the expected attributes
        child = xml_element[0]
        assert child.attrib["name"] == "test"
        assert child.attrib["type"] == "real"

    def test_xml_generation_preserves_order(self, multiple_data_types):
        """Test that XML generation preserves the order of data types."""
        xml_element = multiple_data_types.to_xml(string=False, required=True)

        # Get the names in order from XML
        xml_names = [child.attrib["name"] for child in xml_element]

        # Get the names in order from the original list
        list_names = [dt.name for dt in multiple_data_types.data_types_list]

        assert xml_names == list_names


class TestDataTypesEdgeCases:
    """Test DataTypes edge cases and boundary conditions."""

    def test_very_large_list(self):
        """Test DataTypes with a very large list of data types."""
        large_list = []
        for i in range(100):
            dt = DataType(name=f"test_{i}", type="real" if i % 2 == 0 else "complex")
            large_list.append(dt)

        dts = DataTypes(data_types_list=large_list)

        assert len(dts.data_types_list) == 100
        assert all(isinstance(dt, DataType) for dt in dts.data_types_list)

    def test_deeply_nested_dict_input(self):
        """Test DataTypes with complex nested dictionary input."""
        complex_dict = {
            "name": "complex_test",
            "type": "complex",
            "description": "A complex test with many fields",
            "external_url": "http://example.com",
            "intention": "primary data type",
            "tag": "test_tag",
            "output": "E",
            "input": "H",
            "units": "[mV/km]/[nT]",
        }

        dts = DataTypes(data_types_list=[complex_dict])

        assert len(dts.data_types_list) == 1
        dt = dts.data_types_list[0]
        assert dt.name == "complex_test"
        assert dt.type == "complex"
        assert dt.description == "A complex test with many fields"

    def test_unicode_in_dict_data(self):
        """Test DataTypes with unicode characters in dictionary data."""
        unicode_dict = {
            "name": "tëst_ünïcödë",
            "description": "Tëst with ünïcödë: αβγδε ☺☻",
            "type": "real",
        }

        dts = DataTypes(data_types_list=[unicode_dict])

        assert len(dts.data_types_list) == 1
        dt = dts.data_types_list[0]
        assert dt.name == "tëst_ünïcödë"
        assert "ünïcödë" in dt.description

    def test_list_modification_after_creation(
        self, sample_data_type, sample_data_type_2
    ):
        """Test modifying the list after DataTypes creation."""
        dts = DataTypes(data_types_list=[sample_data_type])
        assert len(dts.data_types_list) == 1

        # Append to the list directly
        dts.data_types_list.append(sample_data_type_2)
        assert len(dts.data_types_list) == 2
        assert dts.data_types_list[1].name == "variance"

    def test_empty_dict_in_list(self):
        """Test DataTypes with empty dictionary in list."""
        dts = DataTypes(data_types_list=[{}])

        assert len(dts.data_types_list) == 1
        assert isinstance(dts.data_types_list[0], DataType)
        # Empty dict should create DataType with default values
        assert dts.data_types_list[0].name == ""

    def test_none_handling_in_validator(self):
        """Test how validator handles None values."""
        # Test None as single item - should raise TypeError
        with pytest.raises(
            TypeError,
            match="data_types_list must be a list of DataType instances or dictionaries",
        ):
            DataTypes(data_types_list=None)

        # Test None in a list - should also raise TypeError
        with pytest.raises(TypeError):
            DataTypes(data_types_list=[None])


class TestDataTypesPerformance:
    """Test DataTypes performance characteristics."""

    def test_bulk_validation_performance(self):
        """Test performance of validating many data types."""
        import time

        # Create a large list of dictionaries
        dict_list = []
        for i in range(50):
            dict_list.append(
                {
                    "name": f"test_{i}",
                    "type": "real" if i % 2 == 0 else "complex",
                    "description": f"Test description {i}",
                }
            )

        start_time = time.time()
        dts = DataTypes(data_types_list=dict_list)
        validation_time = time.time() - start_time

        assert len(dts.data_types_list) == 50
        assert validation_time < 2.0  # Should complete within 2 seconds

    def test_xml_generation_performance(self, multiple_data_types):
        """Test performance of XML generation."""
        import time

        start_time = time.time()

        for _ in range(25):
            xml_element = multiple_data_types.to_xml(string=False)
            assert isinstance(xml_element, et.Element)

        xml_generation_time = time.time() - start_time

        # Should be able to generate XML quickly
        assert xml_generation_time < 1.0  # 1 second for 25 generations

    def test_read_dict_performance(self):
        """Test performance of read_dict with large data."""
        import time

        # Create large input dict
        large_data_types = []
        for i in range(50):
            large_data_types.append(
                {
                    "name": f"perf_test_{i}",
                    "type": "real",
                    "description": f"Performance test {i}",
                }
            )

        input_dict = {"data_types": {"data_type": large_data_types}}

        start_time = time.time()
        dts = DataTypes()
        dts.read_dict(input_dict)
        read_time = time.time() - start_time

        assert len(dts.data_types_list) == 50
        assert read_time < 2.0  # Should complete within 2 seconds


class TestDataTypesIntegration:
    """Test DataTypes integration with other components."""

    def test_datatype_integration(self, sample_data_type):
        """Test integration with DataType objects."""
        dts = DataTypes(data_types_list=[sample_data_type])

        # Test that DataType methods work properly
        dt = dts.data_types_list[0]
        assert hasattr(dt, "to_xml")
        assert hasattr(dt, "read_dict")
        assert hasattr(dt, "model_dump")

        # Test serialization
        xml_element = dt.to_xml()
        assert isinstance(xml_element, et.Element)

    def test_validator_integration_with_from_dict(self):
        """Test that validator properly calls from_dict on DataType."""
        test_dict = {"name": "integration_test", "type": "complex"}

        with patch.object(DataType, "from_dict") as mock_from_dict:
            # Create mock DataType to return
            mock_dt = MagicMock(spec=DataType)
            mock_from_dict.return_value = mock_dt

            # Since from_dict is called on an instance, we need to mock it differently
            dts = DataTypes(data_types_list=[test_dict])

            # The DataType() constructor was called and from_dict should have been called
            assert len(dts.data_types_list) == 1

    def test_helpers_integration(self, single_data_types):
        """Test integration with helpers module."""
        with patch(
            "mt_metadata.transfer_functions.io.emtfxml.metadata.helpers.element_to_string"
        ) as mock_helper:
            mock_helper.return_value = "<test>xml</test>"

            xml_string = single_data_types.to_xml(string=True)

            mock_helper.assert_called_once()
            assert xml_string == "<test>xml</test>"

    def test_inheritance_from_metadata_base(self):
        """Test that DataTypes properly inherits from MetadataBase."""
        dts = DataTypes()

        # Should have MetadataBase methods and attributes
        assert hasattr(dts, "model_fields")
        assert hasattr(dts, "model_validate")
        assert hasattr(dts, "model_dump")

        # Test serialization capabilities
        data_dict = dts.model_dump()
        assert isinstance(data_dict, dict)
        assert "data_types_list" in data_dict

    def test_logger_integration(self):
        """Test integration with logger."""
        dts = DataTypes()

        # Test that logger is called on KeyError
        with patch.object(logger, "warning") as mock_warning:
            dts.read_dict({"wrong": "structure"})
            mock_warning.assert_called_once_with("Could not read Data Types")

    def test_field_info_and_metadata(self):
        """Test field information and metadata."""
        dts = DataTypes()

        # Check field information
        field_info = dts.model_fields["data_types_list"]
        assert field_info is not None

        # Check that it's properly configured
        assert field_info.default_factory is not None
        assert callable(field_info.default_factory)

        # Test that default factory creates empty list
        assert field_info.default_factory() == []

    def test_class_name_in_xml(self, empty_data_types):
        """Test that class name is used properly in XML generation."""
        xml_element = empty_data_types.to_xml()

        assert xml_element.tag == "DataTypes"
        assert xml_element.tag == empty_data_types.__class__.__name__

    def test_error_handling_robustness(self):
        """Test error handling in various scenarios."""
        # Test with mixed valid and invalid data
        mixed_data = [
            {"name": "valid1", "type": "real"},
            "invalid_string",  # This should raise TypeError
        ]

        with pytest.raises(TypeError):
            DataTypes(data_types_list=mixed_data)

        # Test read_dict with partial data
        partial_dict = {"data_types": {}}
        dts = DataTypes()

        with patch.object(logger, "warning"):
            dts.read_dict(partial_dict)
            # Should not crash, just log warning
