# -*- coding: utf-8 -*-
"""
Simplified pytest suite for mt_metadata.utils.summarize module

Tests core functionality with realistic scenarios and actual behavior.
"""

import pandas as pd
import pytest
from pydantic import Field

from mt_metadata.base import MetadataBase

# Import the module under test
from mt_metadata.utils import summarize


@pytest.fixture
def sample_test_class():
    """Create a simple test class for validation"""

    class TestMetadata(MetadataBase):
        """Test metadata class"""

        simple_string: str = Field(
            default="default_value",
            description="A simple string field",
            alias="simple_str",
            json_schema_extra={"examples": ["example1", "example2"]},
        )

        required_field: str = Field(description="A required field with no default")

        number_field: int = Field(
            default=42,
            description="A number field",
            json_schema_extra={"units": "meters"},
        )

    return TestMetadata


class TestExtractMetadataFieldsFromPydantic:
    """Test the main extract function"""

    def test_extract_returns_dict(self, sample_test_class):
        """Test that extract returns a dictionary"""
        result = summarize.extract_metadata_fields_from_pydantic(sample_test_class)
        assert isinstance(result, dict)
        assert len(result) >= 3  # Should have at least 3 fields

    def test_extracted_fields_have_required_keys(self, sample_test_class):
        """Test that extracted fields have all required keys"""
        result = summarize.extract_metadata_fields_from_pydantic(sample_test_class)
        expected_keys = {
            "type",
            "required",
            "style",
            "units",
            "description",
            "options",
            "alias",
            "example",
            "default",
        }

        for field_name, field_data in result.items():
            assert isinstance(field_data, dict)
            for key in expected_keys:
                assert (
                    key in field_data
                ), f"Key '{key}' missing from field '{field_name}'"

    def test_field_types_are_correct(self, sample_test_class):
        """Test that field types are correctly identified"""
        result = summarize.extract_metadata_fields_from_pydantic(sample_test_class)

        # Check string field
        assert result["simple_string"]["type"] == "string"
        # Check integer field
        assert result["number_field"]["type"] == "integer"

    def test_required_field_detection(self, sample_test_class):
        """Test that required fields are correctly identified"""
        result = summarize.extract_metadata_fields_from_pydantic(sample_test_class)

        # Field with default should not be required
        assert result["simple_string"]["required"] is False
        assert result["number_field"]["required"] is False
        # Field without default should be required
        assert result["required_field"]["required"] is True

    def test_empty_class(self):
        """Test with empty class"""

        class EmptyClass(MetadataBase):
            pass

        result = summarize.extract_metadata_fields_from_pydantic(EmptyClass)
        assert isinstance(result, dict)
        assert len(result) == 0


class TestSummarizePydanticStandards:
    """Test the summarize_pydantic_standards function"""

    def test_summarize_timeseries(self):
        """Test summarizing timeseries module"""
        result = summarize.summarize_pydantic_standards("timeseries")
        assert isinstance(result, summarize.BaseDict)
        assert len(result) > 0  # Should have some entries

    def test_summarize_transfer_functions(self):
        """Test summarizing transfer_functions module"""
        result = summarize.summarize_pydantic_standards("transfer_functions")
        assert isinstance(result, summarize.BaseDict)


class TestSummarizeStandards:
    """Test the main summarize_standards function"""

    def test_returns_dataframe(self):
        """Test that summarize_standards returns a DataFrame"""
        result = summarize.summarize_standards("timeseries")
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_dataframe_has_expected_columns(self):
        """Test that the returned DataFrame has expected columns"""
        result = summarize.summarize_standards("timeseries")

        # These are the columns that should be present based on the actual implementation
        expected_columns = [
            "attribute",
            "type",
            "required",
            "style",
            "units",
            "description",
            "options",
            "alias",
            "example",
            "default",
        ]

        # Check that all expected columns are present
        for col in expected_columns:
            assert col in result.columns, f"Column '{col}' missing from result"

        # Verify we have exactly the expected number of columns
        assert len(result.columns) == len(expected_columns)

    def test_with_save_path(self, tmp_path):
        """Test saving to CSV file"""
        save_file = tmp_path / "test_output.csv"
        result = summarize.summarize_standards("timeseries", save_file)

        # Should still return DataFrame
        assert isinstance(result, pd.DataFrame)

        # File should exist
        assert save_file.exists()

        # Should be able to read the CSV
        df_from_file = pd.read_csv(save_file)
        assert len(df_from_file) > 0


class TestHelperFunctions:
    """Test the helper functions with real Pydantic fields"""

    def test_get_field_style_with_pattern(self, sample_test_class):
        """Test _get_field_style with a field that has a pattern"""
        # Get a real field from the class
        model_fields = sample_test_class.model_fields
        field_info = model_fields["simple_string"]

        result = summarize._get_field_style(field_info)
        # Should return either "free form" or a pattern string
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_field_units_with_units(self, sample_test_class):
        """Test _get_field_units with a field that has units"""
        model_fields = sample_test_class.model_fields
        field_info = model_fields["number_field"]

        result = summarize._get_field_units(field_info)
        # This field has units specified in json_schema_extra
        assert result == "meters"

    def test_get_field_units_without_units(self, sample_test_class):
        """Test _get_field_units with a field that has no units"""
        model_fields = sample_test_class.model_fields
        field_info = model_fields["simple_string"]

        result = summarize._get_field_units(field_info)
        # Should return None for fields without units
        assert result is None

    def test_get_field_description(self, sample_test_class):
        """Test _get_field_description"""
        model_fields = sample_test_class.model_fields
        field_info = model_fields["simple_string"]

        result = summarize._get_field_description(field_info)
        assert result == "A simple string field"

    def test_get_field_alias(self, sample_test_class):
        """Test _get_field_alias"""
        model_fields = sample_test_class.model_fields
        field_info = model_fields["simple_string"]

        result = summarize._get_field_alias(field_info)
        assert result == "simple_str"

    def test_get_field_example(self, sample_test_class):
        """Test _get_field_example"""
        model_fields = sample_test_class.model_fields
        field_info = model_fields["simple_string"]

        result = summarize._get_field_example(field_info)
        # Should return the first example as a string
        assert result == "example1"

    def test_get_field_default(self, sample_test_class):
        """Test _get_field_default"""
        model_fields = sample_test_class.model_fields

        # Test field with default
        field_info = model_fields["simple_string"]
        result = summarize._get_field_default(field_info)
        assert result == "default_value"

        # Test field without default
        field_info = model_fields["required_field"]
        result = summarize._get_field_default(field_info)
        assert result == ""


class TestIntegration:
    """Integration tests for the complete workflow"""

    def test_end_to_end_workflow(self, tmp_path):
        """Test the complete workflow from module to CSV"""
        output_file = tmp_path / "complete_test.csv"

        # Run the complete workflow
        df = summarize.summarize_standards("timeseries", output_file)

        # Verify DataFrame result
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

        # Verify file output
        assert output_file.exists()

        # Verify file contents
        df_from_file = pd.read_csv(output_file)
        assert len(df_from_file) == len(df)
        assert list(df_from_file.columns) == list(df.columns)

    def test_different_modules(self):
        """Test that different modules can be processed"""
        # Test timeseries
        df1 = summarize.summarize_standards("timeseries")
        assert isinstance(df1, pd.DataFrame)
        assert len(df1) > 0

        # Test transfer_functions
        df2 = summarize.summarize_standards("transfer_functions")
        assert isinstance(df2, pd.DataFrame)

        # Should have different content
        # (transfer_functions will likely have fewer entries)
        assert len(df1) != len(df2) or not df1.equals(df2)
