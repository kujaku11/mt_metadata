# -*- coding: utf-8 -*-
"""
Comprehensive pytest test suite for DataQualityNotes basemodel class.

This module tests the DataQualityNotes basemodel class from the transfer_functions.io.emtfxml.metadata
module, including validation, XML generation, dictionary parsing, and comment integration.
"""

from unittest.mock import patch
from xml.etree import cElementTree as et

import pytest

from mt_metadata.transfer_functions.io.emtfxml.metadata.comment_basemodel import Comment
from mt_metadata.transfer_functions.io.emtfxml.metadata.data_quality_notes_basemodel import (
    DataQualityNotes,
)


@pytest.fixture(scope="module")
def basic_comment():
    """Return a basic Comment instance for testing."""
    return Comment(
        value="Test comment about data quality",
        author="Test Author",
        time_stamp="2023-07-01T12:00:00+00:00",
    )


@pytest.fixture(scope="module")
def minimal_data_quality():
    """Return a DataQualityNotes instance with minimal data."""
    return DataQualityNotes()


@pytest.fixture(scope="module")
def basic_data_quality(basic_comment):
    """Return a DataQualityNotes instance with basic data."""
    return DataQualityNotes(
        rating=4, good_from_period=0.01, good_to_period=1000.0, comments=basic_comment
    )


@pytest.fixture(scope="module")
def complete_data_quality():
    """Return a DataQualityNotes instance with all fields populated."""
    comment = Comment(
        value="Complete data quality assessment - excellent signal quality",
        author="Quality Analyst",
        time_stamp="2023-12-15T14:30:00+00:00",
    )
    return DataQualityNotes(
        rating=5, good_from_period=0.001, good_to_period=10000.0, comments=comment
    )


@pytest.fixture(
    params=[
        {"rating": 0, "good_from_period": None, "good_to_period": None},
        {"rating": 1, "good_from_period": 1.0, "good_to_period": 100.0},
        {"rating": 2, "good_from_period": 0.1, "good_to_period": 500.0},
        {"rating": 3, "good_from_period": 0.01, "good_to_period": 1000.0},
        {"rating": 4, "good_from_period": 0.001, "good_to_period": 5000.0},
        {"rating": 5, "good_from_period": 0.0001, "good_to_period": 10000.0},
    ]
)
def various_ratings(request):
    """Return various rating configurations for testing."""
    return request.param


@pytest.fixture(
    params=[
        0.0001,  # Very small period
        0.001,  # Small period
        0.01,  # Common minimum
        0.1,  # Medium-low
        1.0,  # Medium
        10.0,  # Medium-high
        100.0,  # High
        1000.0,  # Very high
        10000.0,  # Extremely high
    ]
)
def period_values(request):
    """Return various period values for testing."""
    return request.param


@pytest.fixture(
    params=[
        "Simple quality comment",
        "Data quality is excellent with clear signals",
        "Some noise detected in higher frequencies",
        "Significant interference from 60Hz power lines",
        "Weather conditions affected data collection",
        "",  # Empty comment
    ]
)
def comment_values(request):
    """Return various comment values for testing."""
    return request.param


@pytest.fixture(
    params=[
        {
            "data_quality_notes": {
                "rating": 4,
                "good_from_period": 0.01,
                "good_to_period": 1000.0,
                "comments": "Good data",
            }
        },
        {"data_quality_notes": {"rating": 3, "comments": "Average quality"}},
        {"data_quality_notes": {"good_from_period": 0.1, "good_to_period": 500.0}},
        {"data_quality_notes": {"rating": 5}},
        {"data_quality_notes": {}},  # Empty dict
    ]
)
def valid_dict_inputs(request):
    """Return valid dictionary inputs for read_dict testing."""
    return request.param


@pytest.fixture(
    params=[
        {"wrong_key": {"rating": 4}},  # Wrong top-level key
        {"data_quality_notes": "not_a_dict"},  # Wrong type
        {"data_quality_notes": None},  # None value
    ]
)
def invalid_dict_inputs(request):
    """Return invalid dictionary inputs for read_dict testing."""
    return request.param


class TestDataQualityNotesBasicFunctionality:
    """Test basic DataQualityNotes functionality."""

    def test_default_initialization(self, minimal_data_quality):
        """Test DataQualityNotes with default values."""
        assert minimal_data_quality.good_from_period is None
        assert minimal_data_quality.good_to_period is None
        assert minimal_data_quality.rating is None
        assert isinstance(minimal_data_quality.comments, Comment)

    def test_basic_initialization(self, basic_data_quality):
        """Test DataQualityNotes with basic values."""
        assert basic_data_quality.rating == 4
        assert basic_data_quality.good_from_period == 0.01
        assert basic_data_quality.good_to_period == 1000.0
        assert isinstance(basic_data_quality.comments, Comment)
        assert basic_data_quality.comments.value == "Test comment about data quality"

    def test_complete_initialization(self, complete_data_quality):
        """Test DataQualityNotes with all fields populated."""
        assert complete_data_quality.rating == 5
        assert complete_data_quality.good_from_period == 0.001
        assert complete_data_quality.good_to_period == 10000.0
        assert isinstance(complete_data_quality.comments, Comment)
        assert (
            complete_data_quality.comments.value
            == "Complete data quality assessment - excellent signal quality"
        )
        assert complete_data_quality.comments.author == "Quality Analyst"

    def test_field_assignment_after_creation(self, minimal_data_quality):
        """Test field assignment after DataQualityNotes creation."""
        minimal_data_quality.rating = 3
        minimal_data_quality.good_from_period = 0.1
        minimal_data_quality.good_to_period = 500.0
        minimal_data_quality.comments = Comment(value="Updated comment")

        assert minimal_data_quality.rating == 3
        assert minimal_data_quality.good_from_period == 0.1
        assert minimal_data_quality.good_to_period == 500.0
        assert minimal_data_quality.comments.value == "Updated comment"


class TestDataQualityNotesValidation:
    """Test DataQualityNotes validation logic."""

    def test_rating_validation(self):
        """Test rating field validation."""
        # Test valid ratings (0-5)
        for rating in [0, 1, 2, 3, 4, 5]:
            dq = DataQualityNotes(rating=rating)
            assert dq.rating == rating

        # Test None rating
        dq = DataQualityNotes(rating=None)
        assert dq.rating is None

    def test_rating_bounds(self):
        """Test rating field bounds."""
        # Valid integer ratings
        valid_ratings = [0, 1, 2, 3, 4, 5]
        for rating in valid_ratings:
            dq = DataQualityNotes(rating=rating)
            assert dq.rating == rating

        # Note: The model doesn't enforce 0-5 range validation,
        # so negative or > 5 values might be accepted

    def test_period_validation(self, period_values):
        """Test period field validation with various values."""
        dq = DataQualityNotes(
            good_from_period=period_values, good_to_period=period_values * 10
        )
        assert dq.good_from_period == period_values
        assert dq.good_to_period == period_values * 10

    def test_negative_periods(self):
        """Test period validation with negative values."""
        # Negative periods might be invalid in practice but test what happens
        dq = DataQualityNotes(good_from_period=-1.0, good_to_period=-10.0)
        assert dq.good_from_period == -1.0
        assert dq.good_to_period == -10.0

    def test_zero_periods(self):
        """Test period validation with zero values."""
        dq = DataQualityNotes(good_from_period=0.0, good_to_period=0.0)
        assert dq.good_from_period == 0.0
        assert dq.good_to_period == 0.0

    def test_comments_string_validation(self, comment_values):
        """Test comments field validation with string input."""
        dq = DataQualityNotes(comments=comment_values)
        assert isinstance(dq.comments, Comment)
        assert dq.comments.value == comment_values

    def test_comments_comment_object_validation(self, basic_comment):
        """Test comments field validation with Comment object input."""
        dq = DataQualityNotes(comments=basic_comment)
        assert isinstance(dq.comments, Comment)
        assert dq.comments == basic_comment

    def test_comments_none_validation(self):
        """Test comments field validation with None input."""
        dq = DataQualityNotes(comments=None)
        assert dq.comments is None

    def test_various_rating_configurations(self, various_ratings):
        """Test DataQualityNotes with various rating configurations."""
        params = various_ratings.copy()
        if (
            params["good_from_period"] is not None
            and params["good_to_period"] is not None
        ):
            params["comments"] = "Test comment for this configuration"

        dq = DataQualityNotes(**params)
        assert dq.rating == params["rating"]
        assert dq.good_from_period == params["good_from_period"]
        assert dq.good_to_period == params["good_to_period"]


class TestDataQualityNotesReadDict:
    """Test DataQualityNotes read_dict functionality."""

    def test_read_dict_complete_input(self):
        """Test read_dict with complete dictionary input."""
        dq = DataQualityNotes()
        input_dict = {
            "data_quality_notes": {
                "rating": 4,
                "good_from_period": 0.01,
                "good_to_period": 1000.0,
                "comments": "Excellent data quality",
            }
        }

        dq.read_dict(input_dict)
        assert dq.rating == 4
        assert dq.good_from_period == 0.01
        assert dq.good_to_period == 1000.0
        assert isinstance(dq.comments, Comment)
        assert dq.comments.value == "Excellent data quality"

    def test_read_dict_partial_input(self):
        """Test read_dict with partial dictionary input."""
        dq = DataQualityNotes()
        input_dict = {"data_quality_notes": {"rating": 3, "comments": "Partial data"}}

        dq.read_dict(input_dict)
        assert dq.rating == 3
        assert dq.good_from_period is None
        assert dq.good_to_period is None
        assert isinstance(dq.comments, Comment)
        assert dq.comments.value == "Partial data"

    def test_read_dict_no_comments(self):
        """Test read_dict with no comments in input."""
        dq = DataQualityNotes()
        input_dict = {
            "data_quality_notes": {
                "rating": 5,
                "good_from_period": 0.001,
                "good_to_period": 10000.0,
            }
        }

        dq.read_dict(input_dict)
        assert dq.rating == 5
        assert dq.good_from_period == 0.001
        assert dq.good_to_period == 10000.0
        assert isinstance(dq.comments, Comment)
        assert dq.comments.value == ""  # Default empty comment

    def test_read_dict_empty_input(self):
        """Test read_dict with empty dictionary input."""
        dq = DataQualityNotes()
        input_dict = {"data_quality_notes": {}}

        dq.read_dict(input_dict)
        # Should have default Comment with empty value
        assert isinstance(dq.comments, Comment)
        assert dq.comments.value == ""

    def test_read_dict_valid_inputs(self, valid_dict_inputs):
        """Test read_dict with various valid inputs."""
        dq = DataQualityNotes()
        dq.read_dict(valid_dict_inputs)

        # Should not raise exceptions
        assert isinstance(dq, DataQualityNotes)
        assert isinstance(dq.comments, Comment)

    @patch("mt_metadata.transfer_functions.io.emtfxml.metadata.helpers._read_element")
    def test_read_dict_calls_helper(self, mock_read_element):
        """Test that read_dict calls the helper function correctly."""
        dq = DataQualityNotes()
        input_dict = {"data_quality_notes": {"rating": 4, "comments": "Test"}}

        dq.read_dict(input_dict)

        # Verify that the helper was called
        mock_read_element.assert_called_once()
        call_args = mock_read_element.call_args
        assert isinstance(
            call_args[0][0], DataQualityNotes
        )  # self is DataQualityNotes instance
        assert call_args[0][1] == input_dict  # input_dict argument
        assert call_args[0][2] == "data_quality_notes"  # element name


class TestDataQualityNotesXMLGeneration:
    """Test DataQualityNotes XML generation functionality."""

    def test_xml_generation_complete(self, complete_data_quality):
        """Test XML generation with complete data."""
        xml_element = complete_data_quality.to_xml(string=False)

        assert isinstance(xml_element, et.Element)

    def test_xml_generation_string_output(self, complete_data_quality):
        """Test XML generation with string output."""
        xml_string = complete_data_quality.to_xml(string=True)

        assert isinstance(xml_string, str)
        # Should contain the rating and period values
        assert "5" in xml_string  # rating
        assert "0.001" in xml_string  # good_from_period
        assert "10000" in xml_string  # good_to_period

    def test_xml_generation_minimal(self, minimal_data_quality):
        """Test XML generation with minimal data."""
        xml_element = minimal_data_quality.to_xml(string=False)

        assert isinstance(xml_element, et.Element)

    def test_xml_generation_parameters(self, basic_data_quality):
        """Test XML generation with different parameters."""
        # Test required=True
        xml_required = basic_data_quality.to_xml(required=True)
        assert isinstance(xml_required, (et.Element, str))

        # Test required=False
        xml_optional = basic_data_quality.to_xml(required=False)
        assert isinstance(xml_optional, (et.Element, str))

    @patch("mt_metadata.transfer_functions.io.emtfxml.metadata.helpers.to_xml")
    def test_xml_generation_order(self, mock_to_xml, complete_data_quality):
        """Test that XML generation uses correct field order."""
        complete_data_quality.to_xml()

        # Check that helpers.to_xml was called with correct order
        mock_to_xml.assert_called_once()
        call_args = mock_to_xml.call_args

        # Verify the order parameter
        assert "order" in call_args.kwargs
        expected_order = [
            "rating",
            "good_from_period",
            "good_to_period",
            "comments",
        ]
        assert call_args.kwargs["order"] == expected_order

    def test_xml_with_none_values(self):
        """Test XML generation with None values."""
        dq = DataQualityNotes(
            rating=None, good_from_period=None, good_to_period=None, comments=None
        )

        xml_result = dq.to_xml(string=True)
        assert isinstance(xml_result, str)

    def test_xml_with_edge_case_values(self):
        """Test XML generation with edge case values."""
        dq = DataQualityNotes(
            rating=0,
            good_from_period=0.0,
            good_to_period=float("inf"),  # Test infinity
            comments="Edge case test",
        )

        xml_result = dq.to_xml(string=True)
        assert isinstance(xml_result, str)
        assert "0" in xml_result


class TestDataQualityNotesEdgeCases:
    """Test DataQualityNotes edge cases and special scenarios."""

    def test_extreme_period_values(self):
        """Test DataQualityNotes with extreme period values."""
        dq = DataQualityNotes(
            good_from_period=1e-10, good_to_period=1e10  # Very small  # Very large
        )

        assert dq.good_from_period == 1e-10
        assert dq.good_to_period == 1e10

    def test_scientific_notation_periods(self):
        """Test DataQualityNotes with scientific notation periods."""
        dq = DataQualityNotes(good_from_period=1.5e-3, good_to_period=2.5e4)

        assert dq.good_from_period == 1.5e-3
        assert dq.good_to_period == 2.5e4

    def test_rating_edge_values(self):
        """Test rating with edge values."""
        # Test boundary values
        edge_ratings = [-1, 0, 1, 5, 6, 100]

        for rating in edge_ratings:
            dq = DataQualityNotes(rating=rating)
            assert dq.rating == rating

    def test_period_order_validation(self):
        """Test periods where from > to (might be invalid but test behavior)."""
        dq = DataQualityNotes(
            good_from_period=1000.0,  # Larger than to_period
            good_to_period=0.01,  # Smaller than from_period
        )

        # The model doesn't validate this relationship
        assert dq.good_from_period == 1000.0
        assert dq.good_to_period == 0.01

    def test_float_precision(self):
        """Test floating point precision handling."""
        precise_value = 0.123456789123456789
        dq = DataQualityNotes(
            good_from_period=precise_value, good_to_period=precise_value * 10
        )

        # Python float precision limits apply
        assert abs(dq.good_from_period - precise_value) < 1e-15

    def test_comment_with_special_content(self):
        """Test comments with special content."""
        special_comment = Comment(
            value="Comment with XML chars: <>&\"'", author="Author & Co."
        )

        dq = DataQualityNotes(rating=4, comments=special_comment)

        assert dq.comments.value == "Comment with XML chars: <>&\"'"
        assert dq.comments.author == "Author & Co."


class TestDataQualityNotesPerformance:
    """Test DataQualityNotes performance characteristics."""

    def test_bulk_creation_performance(self):
        """Test creating many DataQualityNotes instances."""
        data_quality_notes = []
        for i in range(100):
            dq = DataQualityNotes(
                rating=i % 6,  # 0-5
                good_from_period=0.001 * (i + 1),
                good_to_period=1000.0 * (i + 1),
                comments=f"Performance test comment {i}",
            )
            data_quality_notes.append(dq)

        assert len(data_quality_notes) == 100
        assert all(isinstance(dq, DataQualityNotes) for dq in data_quality_notes)

    def test_xml_generation_performance(self, complete_data_quality):
        """Test XML generation performance."""
        xml_results = []
        for _ in range(50):
            xml_result = complete_data_quality.to_xml(string=True)
            xml_results.append(xml_result)

        assert len(xml_results) == 50
        assert all(isinstance(xml, str) for xml in xml_results)

    def test_read_dict_performance(self):
        """Test read_dict performance."""
        base_dict = {
            "data_quality_notes": {"rating": 4, "comments": "Performance test"}
        }

        data_quality_notes = []
        for i in range(50):
            dq = DataQualityNotes()
            test_dict = {
                "data_quality_notes": {
                    "rating": i % 6,
                    "comments": f"Performance test {i}",
                }
            }
            dq.read_dict(test_dict)
            data_quality_notes.append(dq)

        assert len(data_quality_notes) == 50
        assert all(
            dq.comments.value.startswith("Performance test")
            for dq in data_quality_notes
        )


class TestDataQualityNotesIntegration:
    """Test DataQualityNotes integration with other components."""

    def test_comment_integration(self):
        """Test integration with Comment objects."""
        comment = Comment(
            value="Integration test comment",
            author="Integration Tester",
            time_stamp="2023-07-15T14:30:00+00:00",
        )

        dq = DataQualityNotes(
            rating=5, good_from_period=0.01, good_to_period=1000.0, comments=comment
        )

        assert dq.comments == comment
        assert dq.comments.value == "Integration test comment"
        assert dq.comments.author == "Integration Tester"

    def test_comment_string_to_object_conversion(self):
        """Test automatic conversion of string to Comment object."""
        dq = DataQualityNotes(
            comments="String comment that should become Comment object"
        )

        assert isinstance(dq.comments, Comment)
        assert dq.comments.value == "String comment that should become Comment object"

    def test_helpers_integration(self):
        """Test integration with helpers module."""
        dq = DataQualityNotes(
            rating=4,
            good_from_period=0.1,
            good_to_period=500.0,
            comments="Helper integration test",
        )

        # Test that helpers functions are properly imported and used
        xml_result = dq.to_xml(string=True)
        assert isinstance(xml_result, str)

    def test_field_modification_after_read_dict(self):
        """Test field modification after using read_dict."""
        dq = DataQualityNotes()
        input_dict = {
            "data_quality_notes": {
                "rating": 3,
                "good_from_period": 0.1,
                "comments": "Initial comment",
            }
        }

        dq.read_dict(input_dict)

        # Modify fields after read_dict
        dq.rating = 5
        dq.good_to_period = 2000.0
        dq.comments.value = "Modified comment"

        assert dq.rating == 5
        assert dq.good_from_period == 0.1  # Unchanged
        assert dq.good_to_period == 2000.0
        assert dq.comments.value == "Modified comment"

    def test_inheritance_from_metadata_base(self):
        """Test that DataQualityNotes properly inherits from MetadataBase."""
        from mt_metadata.base import MetadataBase

        dq = DataQualityNotes()

        assert isinstance(dq, MetadataBase)
        # Test that it has MetadataBase methods
        assert hasattr(dq, "to_dict")
        assert hasattr(dq, "from_dict")


if __name__ == "__main__":
    pytest.main([__file__])
