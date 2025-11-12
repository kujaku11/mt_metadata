# -*- coding: utf-8 -*-
"""
Comprehensive pytest test suite for DataQualityWarnings basemodel class.

This module tests the DataQualityWarnings basemodel class from the transfer_functions.io.emtfxml.metadata
module, including validation, XML generation, dictionary parsing, and comment integration.
"""

from unittest.mock import patch
from xml.etree import cElementTree as et

import pytest

from mt_metadata.common import Comment
from mt_metadata.transfer_functions.io.emtfxml.metadata import DataQualityWarnings


@pytest.fixture(scope="module")
def basic_comment():
    """Return a basic Comment instance for testing."""
    return Comment(
        value="Basic warning comment",
        author="Test Author",
        time_stamp="2023-07-01T12:00:00+00:00",
    )


@pytest.fixture(scope="module")
def minimal_warnings():
    """Return a DataQualityWarnings instance with minimal data."""
    return DataQualityWarnings()


@pytest.fixture(scope="module")
def basic_warnings(basic_comment):
    """Return a DataQualityWarnings instance with basic data."""
    return DataQualityWarnings(flag=1, comments=basic_comment)


@pytest.fixture(scope="module")
def complete_warnings():
    """Return a DataQualityWarnings instance with all fields populated."""
    comment = Comment(
        value="Complete warning about data quality issues detected",
        author="Quality Control Analyst",
        time_stamp="2023-12-15T14:30:00+00:00",
    )
    return DataQualityWarnings(flag=2, comments=comment)


@pytest.fixture(params=[0, 1, 2, 3, 4, 5, -1, 10, 100, None])
def various_flags(request):
    """Return various flag values for testing."""
    return request.param


@pytest.fixture(
    params=[
        "Simple warning message",
        "Data quality warning: high noise levels detected",
        "Critical issue: power line interference at 60Hz",
        "Minor warning: occasional dropouts in channel Ex",
        "Temperature effects on sensor detected",
        "",  # Empty comment
    ]
)
def warning_comments(request):
    """Return various warning comment values for testing."""
    return request.param


@pytest.fixture(
    params=[
        {"data_quality_warnings": {"flag": 1, "comments": "Warning message"}},
        {"data_quality_warnings": {"flag": 2}},
        {"data_quality_warnings": {"comments": "Only comment"}},
        {"data_quality_warnings": {}},  # Empty dict
    ]
)
def valid_dict_inputs(request):
    """Return valid dictionary inputs for read_dict testing."""
    return request.param


@pytest.fixture(
    params=[
        {"wrong_key": {"flag": 1}},  # Wrong top-level key
        {"data_quality_warnings": "not_a_dict"},  # Wrong type
        {"data_quality_warnings": None},  # None value
    ]
)
def invalid_dict_inputs(request):
    """Return invalid dictionary inputs for read_dict testing."""
    return request.param


class TestDataQualityWarningsBasicFunctionality:
    """Test basic DataQualityWarnings functionality."""

    def test_default_initialization(self, minimal_warnings):
        """Test DataQualityWarnings with default values."""
        assert minimal_warnings.flag is None
        assert isinstance(minimal_warnings.comments, Comment)
        # Default Comment should have None values except for default timestamp
        assert minimal_warnings.comments.value is None
        assert minimal_warnings.comments.author is None

    def test_basic_initialization(self, basic_warnings):
        """Test DataQualityWarnings with basic values."""
        assert basic_warnings.flag == 1
        assert isinstance(basic_warnings.comments, Comment)
        assert basic_warnings.comments.value == "Basic warning comment"
        assert basic_warnings.comments.author == "Test Author"

    def test_complete_initialization(self, complete_warnings):
        """Test DataQualityWarnings with all fields populated."""
        assert complete_warnings.flag == 2
        assert isinstance(complete_warnings.comments, Comment)
        assert (
            complete_warnings.comments.value
            == "Complete warning about data quality issues detected"
        )
        assert complete_warnings.comments.author == "Quality Control Analyst"

    def test_field_assignment_after_creation(self, minimal_warnings):
        """Test field assignment after DataQualityWarnings creation."""
        minimal_warnings.flag = 3
        minimal_warnings.comments = Comment(value="Updated warning comment")

        assert minimal_warnings.flag == 3
        assert minimal_warnings.comments.value == "Updated warning comment"


class TestDataQualityWarningsValidation:
    """Test DataQualityWarnings validation logic."""

    def test_flag_validation(self, various_flags):
        """Test flag field validation with various values."""
        dqw = DataQualityWarnings(flag=various_flags)
        assert dqw.flag == various_flags

    def test_flag_none_validation(self):
        """Test flag field validation with None input."""
        dqw = DataQualityWarnings(flag=None)
        assert dqw.flag is None

    def test_flag_type_validation(self):
        """Test flag field with various types."""
        # Test integer flags
        for flag_val in [0, 1, 2, 5, 10, -1]:
            dqw = DataQualityWarnings(flag=flag_val)
            assert dqw.flag == flag_val
            assert isinstance(dqw.flag, int)

    def test_comments_string_validation(self, warning_comments):
        """Test comments field validation with string input."""
        dqw = DataQualityWarnings(comments=warning_comments)
        assert isinstance(dqw.comments, Comment)
        assert dqw.comments.value == warning_comments

    def test_comments_comment_object_validation(self, basic_comment):
        """Test comments field validation with Comment object input."""
        dqw = DataQualityWarnings(comments=basic_comment)
        assert isinstance(dqw.comments, Comment)
        assert dqw.comments == basic_comment

    def test_comments_none_validation(self):
        """Test comments field validation with None input."""
        dqw = DataQualityWarnings(comments=None)
        assert isinstance(dqw.comments, Comment)
        # None should create a default Comment object
        assert dqw.comments.value is None

    def test_comments_validator_with_invalid_type(self):
        """Test comments validator with invalid input type."""
        with pytest.raises(
            TypeError, match="comments must be a Comment instance or a string"
        ):
            DataQualityWarnings(comments=123)

    def test_default_factory_behavior(self):
        """Test that default_factory creates Comment instances correctly."""
        # Create multiple instances to ensure each gets its own Comment
        dqw1 = DataQualityWarnings()
        dqw2 = DataQualityWarnings()

        assert isinstance(dqw1.comments, Comment)
        assert isinstance(dqw2.comments, Comment)
        # They should be different instances
        assert dqw1.comments is not dqw2.comments


class TestDataQualityWarningsReadDict:
    """Test DataQualityWarnings read_dict functionality."""

    def test_read_dict_complete_input(self):
        """Test read_dict with complete dictionary input."""
        dqw = DataQualityWarnings()
        input_dict = {
            "data_quality_warnings": {
                "flag": 2,
                "comments": "Comprehensive warning message",
            }
        }

        dqw.read_dict(input_dict)
        assert dqw.flag == 2

    def test_read_dict_partial_input(self):
        """Test read_dict with partial dictionary input."""
        dqw = DataQualityWarnings()
        input_dict = {"data_quality_warnings": {"flag": 1}}

        dqw.read_dict(input_dict)
        assert dqw.flag == 1

    def test_read_dict_flag_only(self):
        """Test read_dict with only flag in input."""
        dqw = DataQualityWarnings()
        input_dict = {"data_quality_warnings": {"flag": 3}}

        dqw.read_dict(input_dict)
        assert dqw.flag == 3

    def test_read_dict_empty_input(self):
        """Test read_dict with empty dictionary input."""
        dqw = DataQualityWarnings()
        input_dict = {"data_quality_warnings": {}}

        dqw.read_dict(input_dict)
        # Should not raise exceptions
        assert isinstance(dqw, DataQualityWarnings)

    def test_read_dict_valid_inputs(self, valid_dict_inputs):
        """Test read_dict with various valid inputs."""
        dqw = DataQualityWarnings()
        dqw.read_dict(valid_dict_inputs)

        # Should not raise exceptions
        assert isinstance(dqw, DataQualityWarnings)

    @patch("mt_metadata.transfer_functions.io.emtfxml.metadata.helpers._read_element")
    def test_read_dict_calls_helper(self, mock_read_element):
        """Test that read_dict calls the helper function correctly."""
        dqw = DataQualityWarnings()
        input_dict = {"data_quality_warnings": {"flag": 1, "comments": "Test"}}

        dqw.read_dict(input_dict)

        # Verify that the helper was called
        mock_read_element.assert_called_once()
        call_args = mock_read_element.call_args
        assert isinstance(
            call_args[0][0], DataQualityWarnings
        )  # self is DataQualityWarnings instance
        assert call_args[0][1] == input_dict  # input_dict argument
        assert call_args[0][2] == "data_quality_warnings"  # element name


class TestDataQualityWarningsXMLGeneration:
    """Test DataQualityWarnings XML generation functionality."""

    def test_xml_generation_complete(self, complete_warnings):
        """Test XML generation with complete data."""
        xml_element = complete_warnings.to_xml(string=False)

        assert isinstance(xml_element, et.Element) or isinstance(xml_element, str)

    def test_xml_generation_string_output(self, complete_warnings):
        """Test XML generation with string output."""
        xml_string = complete_warnings.to_xml(string=True)

        assert isinstance(xml_string, str)
        # Should contain the flag value
        assert "2" in xml_string  # flag value

    def test_xml_generation_minimal(self, minimal_warnings):
        """Test XML generation with minimal data."""
        xml_element = minimal_warnings.to_xml(string=False)

        assert isinstance(xml_element, et.Element) or isinstance(xml_element, str)

    def test_xml_generation_parameters(self, basic_warnings):
        """Test XML generation with different parameters."""
        # Test required=True
        xml_required = basic_warnings.to_xml(required=True)
        assert xml_required is not None

        # Test required=False
        xml_optional = basic_warnings.to_xml(required=False)
        assert xml_optional is not None

    @patch("mt_metadata.transfer_functions.io.emtfxml.metadata.helpers.to_xml")
    def test_xml_generation_order(self, mock_to_xml, complete_warnings):
        """Test that XML generation uses correct field order."""
        complete_warnings.to_xml()

        # Check that helpers.to_xml was called with correct order
        mock_to_xml.assert_called_once()
        call_args = mock_to_xml.call_args

        # Verify the order parameter
        assert "order" in call_args.kwargs
        expected_order = ["flag", "comments"]
        assert call_args.kwargs["order"] == expected_order

    def test_xml_with_none_values(self):
        """Test XML generation with None values."""
        dqw = DataQualityWarnings(flag=None)

        xml_result = dqw.to_xml(string=True)
        assert isinstance(xml_result, str)

    def test_xml_with_various_flags(self):
        """Test XML generation with various flag values."""
        test_flags = [0, 1, 2, 5, 10, -1]

        for flag in test_flags:
            dqw = DataQualityWarnings(
                flag=flag, comments="Test warning for flag " + str(flag)
            )

            xml_result = dqw.to_xml(string=True)
            assert isinstance(xml_result, str)
            assert str(flag) in xml_result


class TestDataQualityWarningsEdgeCases:
    """Test DataQualityWarnings edge cases and special scenarios."""

    def test_extreme_flag_values(self):
        """Test DataQualityWarnings with extreme flag values."""
        extreme_flags = [-1000, 0, 1000, 999999]

        for flag in extreme_flags:
            dqw = DataQualityWarnings(flag=flag)
            assert dqw.flag == flag

    def test_comments_with_special_characters(self):
        """Test comments with special characters."""
        special_comment = "Warning: Special chars <>&\"' and Unicode αβγ 你好"

        dqw = DataQualityWarnings(flag=1, comments=special_comment)

        assert dqw.comments.value == special_comment

    def test_comments_with_long_text(self):
        """Test comments with very long text."""
        long_comment = "A" * 5000  # 5000 character warning

        dqw = DataQualityWarnings(flag=2, comments=long_comment)

        assert len(dqw.comments.value) == 5000
        assert dqw.comments.value == long_comment

    def test_comments_with_newlines_and_tabs(self):
        """Test comments with newlines and tabs."""
        formatted_comment = "Line 1\nLine 2\tTabbed content\n\nEnd"

        dqw = DataQualityWarnings(comments=formatted_comment)

        assert "\n" in dqw.comments.value
        assert "\t" in dqw.comments.value
        assert dqw.comments.value == formatted_comment

    def test_flag_boundary_values(self):
        """Test flag with boundary values that might be meaningful."""
        # Test typical warning levels
        warning_levels = [0, 1, 2, 3, 4, 5]  # Common warning severity levels

        for level in warning_levels:
            dqw = DataQualityWarnings(flag=level)
            assert dqw.flag == level
            assert isinstance(dqw.flag, int)

    def test_field_reassignment(self):
        """Test reassigning fields after creation."""
        dqw = DataQualityWarnings(flag=1, comments="Initial comment")

        # Reassign flag
        dqw.flag = 5
        assert dqw.flag == 5

        # Reassign comments with string (should trigger validator)
        dqw.comments = "Updated warning message"
        assert isinstance(dqw.comments, Comment)
        assert dqw.comments.value == "Updated warning message"

        # Reassign comments with Comment object
        new_comment = Comment(value="Another comment", author="New Author")
        dqw.comments = new_comment
        assert dqw.comments == new_comment


class TestDataQualityWarningsPerformance:
    """Test DataQualityWarnings performance characteristics."""

    def test_bulk_creation_performance(self):
        """Test creating many DataQualityWarnings instances."""
        warnings = []
        for i in range(100):
            dqw = DataQualityWarnings(
                flag=i % 6, comments=f"Performance test warning {i}"  # 0-5 cycle
            )
            warnings.append(dqw)

        assert len(warnings) == 100
        assert all(isinstance(w, DataQualityWarnings) for w in warnings)

    def test_xml_generation_performance(self, complete_warnings):
        """Test XML generation performance."""
        xml_results = []
        for _ in range(50):
            xml_result = complete_warnings.to_xml(string=True)
            xml_results.append(xml_result)

        assert len(xml_results) == 50
        assert all(isinstance(xml, str) for xml in xml_results)

    def test_comment_validation_performance(self):
        """Test comment validation performance."""
        test_comments = [f"Warning message {i}" for i in range(100)]

        warnings = []
        for comment in test_comments:
            dqw = DataQualityWarnings(comments=comment)
            warnings.append(dqw)

        assert len(warnings) == 100
        assert all(w.comments.value.startswith("Warning message") for w in warnings)


class TestDataQualityWarningsIntegration:
    """Test DataQualityWarnings integration with other components."""

    def test_comment_integration(self):
        """Test integration with Comment objects."""
        comment = Comment(
            value="Integration test warning",
            author="Integration Tester",
            time_stamp="2023-07-15T14:30:00+00:00",
        )

        dqw = DataQualityWarnings(flag=3, comments=comment)

        assert dqw.comments == comment
        assert dqw.comments.value == "Integration test warning"
        assert dqw.comments.author == "Integration Tester"

    def test_comment_string_to_object_conversion(self):
        """Test automatic conversion of string to Comment object."""
        dqw = DataQualityWarnings(
            comments="String warning that should become Comment object"
        )

        assert isinstance(dqw.comments, Comment)
        assert dqw.comments.value == "String warning that should become Comment object"

    def test_helpers_integration(self):
        """Test integration with helpers module."""
        dqw = DataQualityWarnings(flag=2, comments="Helper integration test")

        # Test that helpers functions are properly imported and used
        xml_result = dqw.to_xml(string=True)
        assert isinstance(xml_result, str)

    def test_inheritance_from_metadata_base(self):
        """Test that DataQualityWarnings properly inherits from MetadataBase."""
        from mt_metadata.base import MetadataBase

        dqw = DataQualityWarnings()

        assert isinstance(dqw, MetadataBase)
        # Test that it has MetadataBase methods
        assert hasattr(dqw, "to_dict")
        assert hasattr(dqw, "from_dict")

    def test_validator_error_handling(self):
        """Test validator error handling with invalid inputs."""
        # Test with list (invalid type)
        with pytest.raises(TypeError):
            DataQualityWarnings(comments=[1, 2, 3])

        # Test with dict (invalid type)
        with pytest.raises(TypeError):
            DataQualityWarnings(comments={"invalid": "dict"})

        # Test with number (invalid type)
        with pytest.raises(TypeError):
            DataQualityWarnings(comments=42)

    def test_flag_and_comment_interaction(self):
        """Test interaction between flag and comments fields."""
        # Test that flag and comments work together properly
        test_cases = [
            (0, "No warning"),
            (1, "Minor warning"),
            (2, "Moderate warning"),
            (3, "Major warning"),
            (4, "Critical warning"),
            (5, "Severe warning"),
        ]

        for flag, comment_text in test_cases:
            dqw = DataQualityWarnings(flag=flag, comments=comment_text)
            assert dqw.flag == flag
            assert dqw.comments.value == comment_text

            # Test XML generation includes both
            xml_result = dqw.to_xml(string=True)
            assert str(flag) in xml_result
            assert comment_text in xml_result


if __name__ == "__main__":
    pytest.main([__file__])
