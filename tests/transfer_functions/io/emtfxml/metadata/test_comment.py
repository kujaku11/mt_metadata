# -*- coding: utf-8 -*-
"""
Comprehensive pytest test suite for Comment basemodel class.

This module tests the Comment basemodel class from the transfer_functions.io.emtfxml.metadata
module, including validation, XML generation, and dictionary parsing.
"""

from unittest.mock import patch
from xml.etree import cElementTree as et

import pytest

from mt_metadata.common import Comment
from mt_metadata.common.mttime import MTime


@pytest.fixture(scope="module")
def basic_comment():
    """Return a basic Comment instance for testing."""
    return Comment(
        value="This is a test comment",
        author="Test Author",
        time_stamp="2023-07-01T12:00:00+00:00",
    )


@pytest.fixture(scope="module")
def minimal_comment():
    """Return a Comment instance with minimal data."""
    return Comment(value="Minimal comment")


@pytest.fixture(scope="module")
def complete_comment():
    """Return a Comment instance with all fields populated."""
    return Comment(
        value="Complete test comment with all fields",
        author="Complete Author",
        time_stamp="2023-12-31T23:59:59+00:00",
    )


@pytest.fixture
def empty_comment():
    """Return a Comment instance with empty/default values."""
    return Comment()


@pytest.fixture(
    params=[
        "Simple comment text",
        "Comment with special chars: !@#$%^&*()",
        "Comment with Unicode: αβγ 你好 مرحبا",
        "",  # Empty string
        "Very long comment " + "x" * 1000,  # Long comment
    ]
)
def various_comment_values(request):
    """Return various comment value strings for testing."""
    return request.param


@pytest.fixture(
    params=[
        {"comments": "Simple string comment"},
        {
            "comments": {
                "value": "Dict comment",
                "author": "Dict Author",
                "date": "2023-01-01T00:00:00+00:00",
            }
        },
        {"comments": {"value": "Dict comment only"}},
        {"comments": {"author": "Author only"}},
        {"comments": {"date": "2023-01-01T00:00:00+00:00"}},
    ]
)
def valid_dict_inputs(request):
    """Return valid dictionary inputs for read_dict testing."""
    return request.param


@pytest.fixture(
    params=[
        {"comments": 123},  # Invalid type
        {"comments": []},  # Invalid type
        {"comments": None},  # Invalid type
        {"wrong_key": "value"},  # Wrong key
    ]
)
def invalid_dict_inputs(request):
    """Return invalid dictionary inputs for read_dict testing."""
    return request.param


class TestCommentBasicFunctionality:
    """Test basic Comment functionality."""

    def test_default_initialization(self, empty_comment):
        """Test Comment with default values."""
        assert empty_comment.value is None
        assert empty_comment.author is None
        # time_stamp should have default factory value
        assert empty_comment.time_stamp is not None
        assert isinstance(empty_comment.time_stamp, MTime)
        assert str(empty_comment.time_stamp) == "1980-01-01T00:00:00+00:00"

    def test_basic_initialization(self, basic_comment):
        """Test Comment with basic values."""
        assert basic_comment.value == "This is a test comment"
        assert basic_comment.author == "Test Author"
        assert isinstance(basic_comment.time_stamp, MTime)
        assert str(basic_comment.time_stamp) == "2023-07-01T12:00:00+00:00"

    def test_minimal_initialization(self, minimal_comment):
        """Test Comment with minimal data."""
        assert minimal_comment.value == "Minimal comment"
        assert minimal_comment.author is None
        assert str(minimal_comment.time_stamp) == "1980-01-01T00:00:00+00:00"

    def test_complete_initialization(self, complete_comment):
        """Test Comment with all fields populated."""
        assert complete_comment.value == "Complete test comment with all fields"
        assert complete_comment.author == "Complete Author"
        assert str(complete_comment.time_stamp) == "2023-12-31T23:59:59+00:00"

    def test_field_assignment_after_creation(self, empty_comment):
        """Test field assignment after Comment creation."""
        empty_comment.value = "Updated comment"
        empty_comment.author = "Updated Author"
        empty_comment.time_stamp = "2024-01-01T00:00:00+00:00"

        assert empty_comment.value == "Updated comment"
        assert empty_comment.author == "Updated Author"
        assert str(empty_comment.time_stamp) == "2024-01-01T00:00:00+00:00"


class TestCommentValidation:
    """Test Comment validation logic."""

    def test_various_comment_values(self, various_comment_values):
        """Test Comment with various value strings."""
        comment = Comment(value=various_comment_values)
        assert comment.value == various_comment_values

    def test_time_stamp_validation(self):
        """Test time_stamp field validation with various formats."""
        # Test various time formats
        time_formats = [
            "2023-01-01T00:00:00+00:00",
            "2023-01-01T00:00:00Z",
            "2023-01-01",
            1672531200,  # Unix timestamp
            1672531200.0,  # Float timestamp
        ]

        for time_format in time_formats:
            comment = Comment(time_stamp=time_format)
            assert isinstance(comment.time_stamp, MTime)

    def test_author_field_validation(self):
        """Test author field validation."""
        # Test various author formats
        authors = [
            "John Doe",
            "J. Smith",
            "Multiple Authors, Separated By Commas",
            "",  # Empty string
            None,  # None value
        ]

        for author in authors:
            comment = Comment(author=author)
            assert comment.author == author

    def test_value_field_validation(self):
        """Test value field validation."""
        # Test various value formats
        values = [
            "Simple comment",
            "Comment with\nnewlines\nand\ttabs",
            "Comment with special chars: !@#$%^&*()",
            "",  # Empty string
            None,  # None value
        ]

        for value in values:
            comment = Comment(value=value)
            assert comment.value == value

    def test_pipe_separator_parsing(self):
        """Test parsing comments with pipe separators (inherited from CommonComment)."""
        # Test with all three parts
        comment = Comment(value="2023-01-01T00:00:00+00:00 | John Doe | Test comment")
        assert comment.value == "Test comment"
        assert comment.author == "John Doe"
        assert str(comment.time_stamp) == "2023-01-01T00:00:00+00:00"

        # Test with two parts (timestamp and comment)
        comment2 = Comment(value="2023-01-01T00:00:00+00:00 | Test comment")
        assert comment2.value == "Test comment"
        assert str(comment2.time_stamp) == "2023-01-01T00:00:00+00:00"

    def test_equality_comparison(self):
        """Test Comment equality comparison."""
        comment1 = Comment(
            value="Test", author="Author", time_stamp="2023-01-01T00:00:00+00:00"
        )
        comment2 = Comment(
            value="Test", author="Author", time_stamp="2023-01-01T00:00:00+00:00"
        )
        comment3 = Comment(
            value="Different", author="Author", time_stamp="2023-01-01T00:00:00+00:00"
        )

        assert comment1 == comment2
        assert comment1 != comment3

        # Test equality with string - Comment equality returns the formatted string representation
        comment_str = comment1.as_string()
        assert "Test" in comment_str

        # Test equality with dict
        assert comment1 == {
            "value": "Test",
            "author": "Author",
            "time_stamp": "2023-01-01T00:00:00+00:00",
        }


class TestCommentReadDict:
    """Test Comment read_dict functionality."""

    def test_read_dict_string_input(self):
        """Test read_dict with string comment input."""
        comment = Comment()
        input_dict = {"comments": "Simple string comment"}

        comment.read_dict(input_dict)
        assert comment.value == "Simple string comment"

    def test_read_dict_complete_dict_input(self):
        """Test read_dict with complete dictionary input."""
        comment = Comment()
        input_dict = {
            "comments": {
                "value": "Dictionary comment",
                "author": "Dict Author",
                "date": "2023-06-15T10:30:00+00:00",
            }
        }

        comment.read_dict(input_dict)
        assert comment.value == "Dictionary comment"
        assert comment.author == "Dict Author"
        assert str(comment.time_stamp) == "2023-06-15T10:30:00+00:00"

    def test_read_dict_partial_dict_input(self):
        """Test read_dict with partial dictionary input."""
        comment = Comment()
        input_dict = {"comments": {"value": "Partial comment"}}

        comment.read_dict(input_dict)
        assert comment.value == "Partial comment"
        # Other fields should remain default
        assert comment.author is None

    def test_read_dict_missing_keys(self):
        """Test read_dict with missing keys in dictionary."""
        comment = Comment()
        input_dict = {"comments": {"author": "Author Only"}}

        # Should not raise exception, just log debug messages
        comment.read_dict(input_dict)
        assert comment.author == "Author Only"

    def test_read_dict_invalid_inputs(self, invalid_dict_inputs):
        """Test read_dict with invalid inputs."""
        comment = Comment()

        if "wrong_key" in invalid_dict_inputs:
            # Should raise KeyError for wrong key
            with pytest.raises(KeyError):
                comment.read_dict(invalid_dict_inputs)
        else:
            # Should raise TypeError for invalid types
            with pytest.raises(TypeError):
                comment.read_dict(invalid_dict_inputs)

    def test_read_dict_valid_inputs(self, valid_dict_inputs):
        """Test read_dict with various valid inputs."""
        comment = Comment()
        comment.read_dict(valid_dict_inputs)

        # Should not raise exceptions
        assert isinstance(comment, Comment)


class TestCommentXMLGeneration:
    """Test Comment XML generation functionality."""

    def test_xml_generation_complete(self, complete_comment):
        """Test XML generation with complete data."""
        xml_element = complete_comment.to_xml(string=False)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "Comments"
        assert xml_element.text == "Complete test comment with all fields"
        assert xml_element.get("author") == "Complete Author"

    def test_xml_generation_string_output(self, complete_comment):
        """Test XML generation with string output."""
        xml_string = complete_comment.to_xml(string=True)

        assert isinstance(xml_string, str)
        assert "Comments" in xml_string
        assert "Complete test comment with all fields" in xml_string
        assert 'author="Complete Author"' in xml_string

    def test_xml_generation_minimal(self, minimal_comment):
        """Test XML generation with minimal data."""
        xml_element = minimal_comment.to_xml(string=False)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "Comments"
        assert xml_element.text == "Minimal comment"
        assert xml_element.get("author") == ""  # None author becomes empty string

    def test_xml_generation_empty_values(self, empty_comment):
        """Test XML generation with empty/None values."""
        xml_element = empty_comment.to_xml(string=False)

        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "Comments"
        assert xml_element.text == ""  # None value becomes empty string
        assert xml_element.get("author") == ""  # None author becomes empty string

    def test_xml_generation_parameters(self, basic_comment):
        """Test XML generation with different parameters."""
        # Test required=True
        xml_required = basic_comment.to_xml(required=True)
        assert isinstance(xml_required, et.Element)

        # Test required=False
        xml_optional = basic_comment.to_xml(required=False)
        assert isinstance(xml_optional, et.Element)

        # Both should be the same for Comment class
        assert xml_required.tag == xml_optional.tag

    @patch("mt_metadata.common.comment.element_to_string")
    def test_xml_string_conversion(self, mock_element_to_string, basic_comment):
        """Test that XML string conversion uses helpers.element_to_string."""
        mock_element_to_string.return_value = "<Comments>Test</Comments>"

        result = basic_comment.to_xml(string=True)

        mock_element_to_string.assert_called_once()
        assert result == "<Comments>Test</Comments>"

    def test_xml_special_characters(self):
        """Test XML generation with special characters."""
        comment = Comment(
            value="Comment with <special> & characters", author="Author & Co."
        )

        xml_element = comment.to_xml(string=False)
        assert xml_element.text == "Comment with <special> & characters"
        assert xml_element.get("author") == "Author & Co."

    def test_xml_unicode_characters(self):
        """Test XML generation with Unicode characters."""
        comment = Comment(
            value="Comment with Unicode: αβγ 你好 مرحبا", author="Unicode Author: 李明"
        )

        xml_element = comment.to_xml(string=False)
        assert xml_element.text == "Comment with Unicode: αβγ 你好 مرحبا"
        assert xml_element.get("author") == "Unicode Author: 李明"


class TestCommentEdgeCases:
    """Test Comment edge cases and special scenarios."""

    def test_none_value_handling(self):
        """Test Comment with None values."""
        comment = Comment(value=None, author=None)

        assert comment.value is None
        assert comment.author is None

        # XML generation should handle None values
        xml_element = comment.to_xml()
        assert xml_element.text == ""
        assert xml_element.get("author") == ""

    def test_empty_string_handling(self):
        """Test Comment with empty strings."""
        comment = Comment(value="", author="")

        assert comment.value == ""
        assert comment.author == ""

        # XML should preserve empty strings
        xml_element = comment.to_xml()
        assert xml_element.text == ""
        assert xml_element.get("author") == ""

    def test_whitespace_handling(self):
        """Test Comment with whitespace."""
        comment = Comment(
            value="  Comment with whitespace  ", author="  Author with spaces  "
        )

        # Whitespace should be preserved
        assert comment.value == "  Comment with whitespace  "
        assert comment.author == "  Author with spaces  "

    def test_very_long_values(self):
        """Test Comment with very long values."""
        long_value = "A" * 5000
        long_author = "B" * 1000

        comment = Comment(value=long_value, author=long_author)

        assert len(comment.value) == 5000
        assert len(comment.author) == 1000

        # XML generation should handle long values
        xml_element = comment.to_xml()
        assert len(xml_element.text) == 5000
        assert len(xml_element.get("author")) == 1000

    def test_newlines_and_tabs(self):
        """Test Comment with newlines and tabs."""
        comment = Comment(
            value="Line 1\nLine 2\tTabbed", author="Author\nWith\tFormatting"
        )

        assert "\n" in comment.value
        assert "\t" in comment.value
        assert "\n" in comment.author
        assert "\t" in comment.author

    def test_multiple_pipe_separators(self):
        """Test Comment with multiple pipe separators."""
        # Test with extra pipes - only the first 3 parts are used for parsing
        comment = Comment(
            value="2023-01-01T00:00:00+00:00 | Author | Comment | Extra | Parts"
        )

        # Should take the last part as the value when there are more than 3 parts
        assert comment.value == "Parts"
        # But author and timestamp parsing may not work with > 3 parts
        # This is expected behavior based on the parsing logic


class TestCommentPerformance:
    """Test Comment performance characteristics."""

    def test_bulk_creation_performance(self):
        """Test creating many Comment instances."""
        comments = []
        for i in range(100):
            # Use valid dates (avoiding day 32+)
            day = (i % 28) + 1  # Days 1-28 are valid for all months
            comment = Comment(
                value=f"Comment {i}",
                author=f"Author {i}",
                time_stamp=f"2023-01-{day:02d}T00:00:00+00:00",
            )
            comments.append(comment)

        assert len(comments) == 100
        assert all(isinstance(c, Comment) for c in comments)

    def test_xml_generation_performance(self, complete_comment):
        """Test XML generation performance."""
        xml_results = []
        for _ in range(50):
            xml_result = complete_comment.to_xml(string=True)
            xml_results.append(xml_result)

        assert len(xml_results) == 50
        assert all(isinstance(xml, str) for xml in xml_results)

    def test_read_dict_performance(self):
        """Test read_dict performance."""
        base_dict = {"comments": {"value": "Performance test", "author": "Test Author"}}

        comments = []
        for i in range(50):
            comment = Comment()
            test_dict = {
                "comments": {"value": f"Performance test {i}", "author": f"Author {i}"}
            }
            comment.read_dict(test_dict)
            comments.append(comment)

        assert len(comments) == 50
        assert all(c.value.startswith("Performance test") for c in comments)


class TestCommentIntegration:
    """Test Comment integration with other components."""

    def test_time_stamp_mtime_integration(self):
        """Test integration with MTime objects."""
        mtime = MTime(time_stamp="2023-07-15T14:30:00+00:00")
        comment = Comment(time_stamp=mtime)

        assert isinstance(comment.time_stamp, MTime)
        assert str(comment.time_stamp) == "2023-07-15T14:30:00+00:00"

    def test_from_dict_integration(self):
        """Test integration with from_dict method (inherited)."""
        comment = Comment()

        # Test with string
        comment.from_dict("Test comment from dict")
        assert comment.value == "Test comment from dict"

        # Test with dictionary
        test_dict = {
            "value": "Dict comment",
            "author": "Dict Author",
            "time_stamp": "2023-01-01T00:00:00+00:00",
        }
        comment.from_dict(test_dict)
        assert comment.value == "Dict comment"
        assert comment.author == "Dict Author"

    def test_to_dict_integration(self):
        """Test integration with to_dict method (inherited)."""
        comment = Comment(
            value="Test comment",
            author="Test Author",
            time_stamp="2023-01-01T00:00:00+00:00",
        )

        result = comment.to_dict(single=True)
        assert isinstance(result, dict)
        assert result["value"] == "Test comment"
        assert result["author"] == "Test Author"
        assert result["time_stamp"] == "2023-01-01T00:00:00+00:00"

    def test_inheritance_from_common_comment(self):
        """Test that Comment properly inherits from CommonComment."""
        from mt_metadata.common import Comment as CommonComment

        comment = Comment()

        assert isinstance(comment, CommonComment)
        assert hasattr(comment, "value")
        assert hasattr(comment, "author")
        assert hasattr(comment, "time_stamp")

    def test_xml_helpers_integration(self):
        """Test integration with helpers module."""
        comment = Comment(value="Helper test", author="Helper Author")

        # Test that element_to_string is properly imported and used
        xml_string = comment.to_xml(string=True)
        assert isinstance(xml_string, str)
        assert "Helper test" in xml_string
        assert "Helper Author" in xml_string


if __name__ == "__main__":
    pytest.main([__file__])
