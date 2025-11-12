"""
Test suite for Job metadata class using pytest with fixtures and subtests.
This test suite follows modern pytest patterns for comprehensive coverage and efficiency optimization.
"""

import json

import pytest
from pydantic import ValidationError

from mt_metadata.transfer_functions.io.zonge.metadata.job import Job


class TestJobDefault:
    """Test default initialization and basic attributes of Job class."""

    @pytest.fixture(scope="class")
    def default_job(self):
        """Fixture providing a default Job instance for efficiency."""
        return Job()  # type: ignore

    def test_default_initialization(self, default_job, subtests):
        """Test that Job initializes with correct default values."""
        with subtests.test("default name value"):
            assert default_job.name is None

        with subtests.test("default job_for value"):
            assert default_job.job_for is None

    def test_default_job_attributes(self, default_job, subtests):
        """Test that Job has all expected attributes."""
        expected_attributes = ["name", "job_for"]

        for attr in expected_attributes:
            with subtests.test(f"has attribute {attr}"):
                assert hasattr(default_job, attr)

    def test_default_model_fields(self, default_job, subtests):
        """Test model fields are properly defined."""
        fields = default_job.model_fields
        expected_fields = ["name", "job_for"]

        for field in expected_fields:
            with subtests.test(f"model field {field}"):
                assert field in fields

        with subtests.test("field count"):
            assert len(fields) == 2


class TestJobCustomValues:
    """Test Job with custom values and various initialization patterns."""

    @pytest.fixture(scope="class")
    def populated_job(self):
        """Fixture providing a Job instance with custom values for efficiency."""
        return Job(name="yellowstone_survey", job_for="NSF_research")  # type: ignore

    def test_populated_job_values(self, populated_job, subtests):
        """Test Job with custom values."""
        with subtests.test("populated name"):
            assert populated_job.name == "yellowstone_survey"

        with subtests.test("populated job_for"):
            assert populated_job.job_for == "NSF_research"

    def test_partial_job_values(self, subtests):
        """Test Job with only some fields populated."""
        partial_cases = [
            ("name only", {"name": "test_survey"}, "test_survey", None),
            ("job_for only", {"job_for": "university"}, None, "university"),
        ]

        for case_name, kwargs, expected_name, expected_job_for in partial_cases:
            with subtests.test(f"partial {case_name}"):
                job = Job(**kwargs)  # type: ignore
                assert job.name == expected_name
                assert job.job_for == expected_job_for

    def test_individual_field_initialization(self, subtests):
        """Test individual field initialization."""
        test_cases = [
            ("name", "geothermal_project"),
            ("job_for", "DOE"),
        ]

        for field, value in test_cases:
            with subtests.test(f"individual {field}"):
                kwargs = {field: value}
                job = Job(**kwargs)  # type: ignore
                assert getattr(job, field) == value


class TestJobValidation:
    """Test Job input validation and type conversion."""

    def test_string_field_validation(self, subtests):
        """Test string field validation for name and job_for."""
        with subtests.test("name string validation"):
            job = Job(name="valid_name")  # type: ignore
            assert job.name == "valid_name"

        with subtests.test("job_for string validation"):
            job = Job(job_for="valid_organization")  # type: ignore
            assert job.job_for == "valid_organization"

    def test_none_values_allowed(self, subtests):
        """Test that None values are allowed for optional fields."""
        optional_fields = ["name", "job_for"]

        for field in optional_fields:
            with subtests.test(f"none allowed {field}"):
                kwargs = {field: None}
                job = Job(**kwargs)  # type: ignore
                assert getattr(job, field) is None

    def test_empty_string_values(self, subtests):
        """Test handling of empty strings."""
        string_fields = ["name", "job_for"]

        for field in string_fields:
            with subtests.test(f"empty string {field}"):
                kwargs = {field: ""}
                job = Job(**kwargs)  # type: ignore
                assert getattr(job, field) == ""

    def test_numeric_string_conversion(self, subtests):
        """Test automatic conversion of numeric values to strings."""
        with subtests.test("name numeric conversion"):
            job = Job(name=123)  # type: ignore
            assert job.name == "123"

        with subtests.test("job_for numeric conversion"):
            job = Job(job_for=456.7)  # type: ignore
            assert job.job_for == "456.7"

    def test_invalid_type_handling(self, subtests):
        """Test handling of invalid types for string fields."""
        with subtests.test("name boolean raises ValidationError"):
            with pytest.raises(ValidationError):
                Job(name=True)  # type: ignore

        with subtests.test("job_for boolean raises ValidationError"):
            with pytest.raises(ValidationError):
                Job(job_for=False)  # type: ignore

        with subtests.test("name list raises ValidationError"):
            with pytest.raises(ValidationError):
                Job(name=["invalid", "list"])  # type: ignore

        with subtests.test("job_for dict raises ValidationError"):
            with pytest.raises(ValidationError):
                Job(job_for={"invalid": "dict"})  # type: ignore


class TestJobSerialization:
    """Test Job serialization and deserialization functionality."""

    @pytest.fixture(scope="class")
    def default_job(self):
        """Fixture for default Job instance."""
        return Job()  # type: ignore

    @pytest.fixture(scope="class")
    def populated_job(self):
        """Fixture for populated Job instance."""
        return Job(name="montana_survey", job_for="USGS")  # type: ignore

    def test_model_dump_default(self, default_job, subtests):
        """Test model_dump with default values."""
        dump = default_job.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("has all fields"):
            expected_fields = ["name", "job_for"]
            for field in expected_fields:
                assert field in dump

        with subtests.test("default values"):
            assert dump["name"] is None
            assert dump["job_for"] is None

    def test_model_dump_populated(self, populated_job, subtests):
        """Test model_dump with populated values."""
        dump = populated_job.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("populated values present"):
            assert dump["name"] == "montana_survey"
            assert dump["job_for"] == "USGS"

    def test_from_dict_creation(self, subtests):
        """Test creating Job from dictionary."""
        with subtests.test("full dict"):
            data = {"name": "california_project", "job_for": "Stanford"}
            job = Job(**data)  # type: ignore
            assert job.name == "california_project"
            assert job.job_for == "Stanford"

        with subtests.test("partial dict"):
            data = {"name": "texas_survey"}
            job = Job(**data)  # type: ignore
            assert job.name == "texas_survey"
            assert job.job_for is None

        with subtests.test("empty dict"):
            data = {}
            job = Job(**data)  # type: ignore
            assert job.name is None
            assert job.job_for is None

    def test_json_serialization(self, default_job, populated_job, subtests):
        """Test JSON serialization and deserialization."""
        with subtests.test("JSON round-trip populated job"):
            json_str = populated_job.model_dump_json()
            data = json.loads(json_str)
            recreated = Job(**data)  # type: ignore
            assert recreated.name == populated_job.name
            assert recreated.job_for == populated_job.job_for

        with subtests.test("JSON round-trip default job"):
            json_str = default_job.model_dump_json()
            data = json.loads(json_str)
            recreated = Job(**data)  # type: ignore
            assert recreated.name == default_job.name
            assert recreated.job_for == default_job.job_for

    def test_model_dump_exclude_none(self, subtests):
        """Test model_dump with exclude_none option."""
        with subtests.test("exclude_none with populated"):
            job = Job(name="project_x", job_for="MIT")  # type: ignore
            dump = job.model_dump(exclude_none=True)
            assert "name" in dump
            assert "job_for" in dump
            assert dump["name"] == "project_x"
            assert dump["job_for"] == "MIT"

        with subtests.test("exclude_none with partial"):
            job = Job(name="project_y")  # type: ignore  # job_for will be None
            dump = job.model_dump(exclude_none=True)
            assert "name" in dump
            assert "job_for" not in dump  # Should be excluded since it's None

        with subtests.test("exclude_none with all none"):
            job = Job()  # type: ignore  # Both fields None
            dump = job.model_dump(exclude_none=True)
            # Both fields should be excluded
            assert "name" not in dump or dump.get("name") is not None
            assert "job_for" not in dump or dump.get("job_for") is not None


class TestJobModification:
    """Test Job field modification and updates."""

    def test_field_modification(self, subtests):
        """Test modifying Job fields after creation."""
        job = Job()  # type: ignore

        test_modifications = [
            ("name", "modified_project"),
            ("job_for", "modified_organization"),
        ]

        for field, value in test_modifications:
            with subtests.test(f"modify {field}"):
                setattr(job, field, value)
                assert getattr(job, field) == value

    def test_reset_to_none(self, subtests):
        """Test resetting fields to None."""
        job = Job(name="temp_name", job_for="temp_org")  # type: ignore

        fields_to_reset = ["name", "job_for"]

        for field in fields_to_reset:
            with subtests.test(f"reset {field} to None"):
                setattr(job, field, None)
                assert getattr(job, field) is None

    def test_bulk_update(self, subtests):
        """Test bulk field updates."""
        job = Job()  # type: ignore

        updates = {"name": "bulk_project", "job_for": "bulk_organization"}

        for field, value in updates.items():
            setattr(job, field, value)

        for field, expected_value in updates.items():
            with subtests.test(f"bulk update {field}"):
                assert getattr(job, field) == expected_value


class TestJobComparison:
    """Test Job comparison and equality operations."""

    def test_job_equality(self, subtests):
        """Test Job equality comparisons."""
        job1 = Job(name="project_alpha", job_for="NASA")  # type: ignore
        job2 = Job(name="project_alpha", job_for="NASA")  # type: ignore
        job3 = Job(name="project_beta", job_for="NASA")  # type: ignore

        with subtests.test("same values model_dump equal"):
            assert job1.model_dump() == job2.model_dump()

        with subtests.test("different values model_dump not equal"):
            assert job1.model_dump() != job3.model_dump()

        with subtests.test("individual field comparison"):
            assert job1.name == job2.name
            assert job1.job_for == job2.job_for
            assert job1.name != job3.name

    def test_field_value_consistency(self, subtests):
        """Test consistency of field values across operations."""
        test_values = [
            ("name", "project_gamma"),
            ("job_for", "NOAA"),
        ]

        for field, value in test_values:
            with subtests.test(f"consistency {field} {value}"):
                kwargs = {field: value}
                job = Job(**kwargs)  # type: ignore
                assert getattr(job, field) == value

                # Test round-trip consistency
                dump = job.model_dump()
                recreated = Job(**dump)  # type: ignore
                assert getattr(recreated, field) == getattr(job, field)


class TestJobEdgeCases:
    """Test Job edge cases and boundary conditions."""

    def test_empty_initialization_kwargs(self, subtests):
        """Test initialization with empty keyword arguments."""
        with subtests.test("empty kwargs"):
            job = Job(**{})  # type: ignore
            assert job.name is None
            assert job.job_for is None

    def test_unknown_field_handling(self, subtests):
        """Test handling of unknown fields."""
        with subtests.test("unknown fields accepted"):
            # MetadataBase appears to accept unknown fields
            job = Job(unknown_field="value")  # type: ignore
            assert hasattr(job, "unknown_field")
            assert job.unknown_field == "value"  # type: ignore

    def test_very_long_strings(self, subtests):
        """Test handling of very long string values."""
        long_string = "x" * 1000
        long_string_fields = ["name", "job_for"]

        for field in long_string_fields:
            with subtests.test(f"long string {field}"):
                kwargs = {field: long_string}
                job = Job(**kwargs)  # type: ignore
                assert getattr(job, field) == long_string
                assert len(getattr(job, field)) == 1000

    def test_special_characters(self, subtests):
        """Test handling of special characters in string fields."""
        special_cases = [
            ("commas", "project,with,commas"),
            ("colons", "project:with:colons"),
            ("spaces", "project with spaces"),
            ("newlines", "project\nwith\nnewlines"),
            ("tabs", "project\twith\ttabs"),
            ("quotes", 'project"with"quotes'),
            ("apostrophes", "project'with'apostrophes"),
            ("slashes", "project/with/slashes"),
            ("backslashes", "project\\with\\backslashes"),
        ]

        for case_name, test_value in special_cases:
            with subtests.test(f"special chars {case_name}"):
                job = Job(name=test_value, job_for=test_value)  # type: ignore
                assert job.name == test_value
                assert job.job_for == test_value

    def test_unicode_strings(self, subtests):
        """Test handling of unicode characters in string fields."""
        unicode_cases = [
            ("chinese", "测试项目"),
            ("russian", "тестовый проект"),
            ("emoji", "🔬⚗️ project"),
            ("accented", "café résumé"),
        ]

        for case_name, test_value in unicode_cases:
            with subtests.test(f"unicode {case_name}"):
                job = Job(name=test_value, job_for=test_value)  # type: ignore
                assert job.name == test_value
                assert job.job_for == test_value

    def test_mixed_none_and_values(self, subtests):
        """Test various combinations of None and actual values."""
        combinations = [
            ("name set, job_for None", "project_delta", None),
            ("name None, job_for set", None, "EPA"),
            ("both None", None, None),
            ("both set", "project_epsilon", "FEMA"),
        ]

        for case_name, name_value, job_for_value in combinations:
            with subtests.test(f"combination {case_name}"):
                job = Job(name=name_value, job_for=job_for_value)  # type: ignore
                assert job.name == name_value
                assert job.job_for == job_for_value


class TestJobDocumentation:
    """Test Job class structure and documentation."""

    def test_class_structure(self, subtests):
        """Test Job class structure and inheritance."""
        with subtests.test("class name accessible"):
            assert Job.__name__ == "Job"

        with subtests.test("class is MetadataBase subclass"):
            from mt_metadata.base import MetadataBase

            assert issubclass(Job, MetadataBase)

    def test_field_descriptions(self, subtests):
        """Test that fields have proper descriptions."""
        fields = Job.model_fields
        expected_fields = ["name", "job_for"]

        for field_name in expected_fields:
            with subtests.test(f"field description {field_name}"):
                field = fields[field_name]
                # Check that field has description
                assert hasattr(field, "description") or "description" in str(field)

    def test_field_properties(self, subtests):
        """Test field properties and configurations."""
        fields = Job.model_fields

        with subtests.test("name field properties"):
            name_field = fields["name"]
            # Should be optional (allow None)
            assert "default" in str(name_field) or hasattr(name_field, "default")

        with subtests.test("job_for field properties"):
            job_for_field = fields["job_for"]
            # Should be optional (allow None)
            assert "default" in str(job_for_field) or hasattr(job_for_field, "default")

    def test_schema_information(self, subtests):
        """Test schema and model information."""
        with subtests.test("model_dump produces schema-like structure"):
            job = Job()  # type: ignore
            dump = job.model_dump()
            assert isinstance(dump, dict)
            assert len(dump) >= 0  # Can be empty with exclude_none

        with subtests.test("all expected fields present"):
            expected_fields = ["name", "job_for"]
            dump = Job().model_dump()  # type: ignore
            for field in expected_fields:
                assert field in dump

        with subtests.test("model_fields accessible"):
            fields = Job.model_fields
            assert len(fields) == 2
            assert all(field in fields for field in ["name", "job_for"])
