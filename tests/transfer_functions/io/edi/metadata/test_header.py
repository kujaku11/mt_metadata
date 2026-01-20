# -*- coding: utf-8 -*-
"""
Comprehensive pytest test suite for the Header class in header_basemodel.py.

This module provides extensive testing for the Header class which inherits from
StationLocation and manages EDI file header information using Pydantic BaseModel.
"""

from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from pydantic import ValidationError

from mt_metadata.common import GeographicReferenceFrameEnum, StdEDIversionsEnum
from mt_metadata.common.mttime import MTime
from mt_metadata.transfer_functions.io.edi.metadata import Header

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def default_header():
    """Return a Header instance with default values."""
    return Header()


@pytest.fixture
def populated_header():
    """Return a Header instance with populated values."""
    return Header(
        acqby="Test Researcher",
        dataid="MT001",
        project="TestProject",
        prospect="TestProspect",
        loc="Test Location, CA",
        elev=1234.56,
        survey="Test Survey",
        fileby="Data Processor",
        progname="mt_metadata",
        progvers="1.0.0",
        latitude=37.7749,
        longitude=-122.4194,
        elevation=1234.56,
        datum="WGS84",
        coordinate_system="geographic",
        state="CA",
        stdvers="SEG 1.0",
        units="millivolts_per_kilometer_per_nanotesla",
    )


@pytest.fixture
def sample_edi_lines():
    """Return sample EDI header lines for testing."""
    return [
        ">HEAD",
        "    ACQBY=Test Researcher",
        "    ACQDATE=2023-01-15",
        "    COORDINATE_SYSTEM=geographic",
        "    DATAID=MT001",
        "    ENDDATE=2023-01-20",
        "    EMPTY=1E+32",
        "    FILEBY=Data Processor",
        "    FILEDATE=2023-02-01",
        "    PROGDATE=2023-01-01",
        "    PROGNAME=mt_metadata",
        "    PROGVERS=1.0.0",
        "    PROJECT=TestProject",
        "    PROSPECT=TestProspect",
        "    LOC=Test Location, CA",
        "    ELEV=1234.560",
        "    STDVERS=SEG 1.0",
        "    SURVEY=Test Survey",
        "    UNITS=millivolts_per_kilometer_per_nanotesla",
        "    LAT=37.7749",
        "    LON=-122.4194",
        "",
        ">INFO",
        "    Site information follows",
    ]


@pytest.fixture
def sample_edi_file(tmp_path):
    """Create a temporary EDI file for testing."""
    edi_content = """
        >HEAD
            ACQBY=Test Researcher
            ACQDATE=2023-01-15
            COORDINATE_SYSTEM=geographic
            DATAID=MT001
            ENDDATE=2023-01-20
            EMPTY=1E+32
            FILEBY=Data Processor
            FILEDATE=2023-02-01
            PROGDATE=2023-01-01
            PROGNAME=mt_metadata
            PROGVERS=1.0.0
            PROJECT=TestProject
            PROSPECT=TestProspect
            LOC=Test Location, CA
            ELEV=1234.560
            STDVERS=SEG 1.0
            SURVEY=Test Survey
            UNITS=millivolts_per_kilometer_per_nanotesla
            LAT=37.7749
            LON=-122.4194

        >INFO
            Site information follows
        """

    file_path = tmp_path / "test_header.edi"
    file_path.write_text(edi_content.strip())
    return file_path


@pytest.fixture
def invalid_edi_lines():
    """Return invalid EDI header lines for testing."""
    return [
        ">HEAD",
        "    ACQBY=Test Researcher",
        "    ACQDATE=invalid_date",
        "    COORDINATE_SYSTEM=unknown_system",
        "    DATAID=",  # Empty required field
        "    UNITS=invalid_units",
        "",
    ]


# =============================================================================
# Test Classes
# =============================================================================


class TestHeaderInitialization:
    """Test Header initialization and default values."""

    def test_default_initialization(self, default_header, subtests):
        """Test Header initialization with default values."""
        with subtests.test(msg="acqby default"):
            assert default_header.acqby is None

        with subtests.test(msg="acqdate default"):
            assert isinstance(default_header.acqdate, MTime)

        with subtests.test(msg="coordinate_system default"):
            assert default_header.coordinate_system == "geographic"

        with subtests.test(msg="dataid default"):
            assert default_header.dataid == ""

        with subtests.test(msg="empty default"):
            assert default_header.empty == 1e32

        with subtests.test(msg="fileby default"):
            assert default_header.fileby == ""

        with subtests.test(msg="progname default"):
            assert default_header.progname == "mt_metadata"

        with subtests.test(msg="progvers default"):
            assert default_header.progvers == "0.1.6"

        with subtests.test(msg="stdvers default"):
            assert default_header.stdvers == "SEG 1.0"

        with subtests.test(msg="units default"):
            assert default_header.units == "milliVolt per kilometer per nanoTesla"

        with subtests.test(msg="latitude default"):
            assert default_header.latitude == 0.0

        with subtests.test(msg="longitude default"):
            assert default_header.longitude == 0.0

        with subtests.test(msg="elevation default"):
            assert default_header.elevation == 0.0

    def test_populated_initialization(self, populated_header, subtests):
        """Test Header initialization with provided values."""
        with subtests.test(msg="acqby populated"):
            assert populated_header.acqby == "Test Researcher"

        with subtests.test(msg="dataid populated"):
            assert populated_header.dataid == "MT001"

        with subtests.test(msg="project populated"):
            assert populated_header.project == "TestProject"

        with subtests.test(msg="elev populated"):
            assert populated_header.elev == 1234.56

        with subtests.test(msg="latitude populated"):
            assert populated_header.latitude == 37.7749

        with subtests.test(msg="longitude populated"):
            assert populated_header.longitude == -122.4194


class TestHeaderFieldValidation:
    """Test field validation and type conversion."""

    def test_date_field_validation(self, subtests):
        """Test validation of date fields."""
        header = Header()

        # Test string date
        with subtests.test(msg="string date"):
            header.acqdate = "2023-01-15T10:30:00"
            assert isinstance(header.acqdate, MTime)

        # Test pandas Timestamp
        with subtests.test(msg="pandas Timestamp"):
            ts = pd.Timestamp("2023-01-15 10:30:00")
            header.acqdate = ts
            assert isinstance(header.acqdate, MTime)

        # Test numpy datetime64
        with subtests.test(msg="numpy datetime64"):
            np_dt = np.datetime64("2023-01-15T10:30:00")
            header.acqdate = np_dt
            assert isinstance(header.acqdate, MTime)

    def test_coordinate_system_validation(self, subtests):
        """Test coordinate system field validation."""
        header = Header()

        # Test valid values
        valid_systems = [
            GeographicReferenceFrameEnum.geographic,
            GeographicReferenceFrameEnum.geomagnetic,
        ]
        for system in valid_systems:
            with subtests.test(msg=f"Valid system: {system}"):
                header.coordinate_system = system
                assert header.coordinate_system == system

        # Test invalid value
        with subtests.test(msg="Invalid coordinate system"):
            with pytest.raises(ValidationError):
                header.coordinate_system = "invalid_system"

    def test_stdvers_validation(self, subtests):
        """Test standards version field validation."""
        header = Header()

        # Test valid version
        with subtests.test(msg="Valid stdvers"):
            header.stdvers = StdEDIversionsEnum.SEG_1
            assert header.stdvers == "SEG 1.0"

        # Test invalid version
        with subtests.test(msg="Invalid stdvers"):
            with pytest.raises(ValidationError):
                header.stdvers = "INVALID 2.0"

    def test_units_validation(self, subtests):
        """Test units field validation."""
        header = Header()

        # Test valid units
        with subtests.test(msg="Valid units"):
            header.units = "millivolt per kilometer per nanotesla"
            assert header.units == "milliVolt per kilometer per nanoTesla"

        # Test empty units
        with subtests.test(msg="Empty units"):
            header.units = ""
            assert header.units == ""

        # Test None units
        with subtests.test(msg="None units"):
            header.units = None
            assert header.units == ""


class TestHeaderReadMethods:
    """Test Header read methods."""

    def test_get_header_list(self, default_header, sample_edi_lines, subtests):
        """Test get_header_list method."""
        header_list = default_header.get_header_list(sample_edi_lines)

        with subtests.test(msg="Returns list"):
            assert isinstance(header_list, list)

        with subtests.test(msg="Contains expected entries"):
            expected_entries = [
                "ACQBY=Test Researcher",
                "DATAID=MT001",
                "PROJECT=TestProject",
            ]
            for entry in expected_entries:
                assert entry in header_list

        with subtests.test(msg="Filters out empty lines"):
            assert all(len(line.strip()) > 2 for line in header_list)

    def test_get_header_list_no_header(self, default_header):
        """Test get_header_list with lines that don't contain header."""
        lines_without_header = [
            ">INFO",
            "    Site information",
            ">FREQ",
            "    1.0e-1",
        ]

        header_list = default_header.get_header_list(lines_without_header)
        assert header_list == []

    def test_read_header(self, default_header, sample_edi_lines, subtests):
        """Test read_header method."""
        default_header.read_header(sample_edi_lines)

        with subtests.test(msg="acqby read"):
            assert default_header.acqby == "Test Researcher"

        with subtests.test(msg="dataid read"):
            assert default_header.dataid == "MT001"

        with subtests.test(msg="project read"):
            assert default_header.project == "TestProject"

        with subtests.test(msg="coordinate_system read"):
            assert default_header.coordinate_system == "geographic"

        with subtests.test(msg="elev read"):
            assert default_header.elevation == 1234.560

        with subtests.test(msg="latitude read"):
            assert default_header.latitude == 37.7749

        with subtests.test(msg="longitude read"):
            assert default_header.longitude == -122.4194

    def test_read_header_coordinate_system_variations(self, subtests):
        """Test reading header with different coordinate system formats."""
        test_cases = [
            ("geomagnetic north", "geomagnetic"),
            ("Geographic North", "geographic"),
            ("station coordinates", "station"),
        ]

        for input_value, expected_value in test_cases:
            with subtests.test(msg=f"Coordinate system: {input_value}"):
                lines = [">HEAD", f"    COORDINATE_SYSTEM={input_value}", ""]
                header = Header()
                header.read_header(lines)
                assert header.coordinate_system == expected_value

    def test_read_header_stdvers_defaults(self, subtests):
        """Test reading header with stdvers default values."""
        test_cases = ["N/A", "None", "null"]

        for invalid_value in test_cases:
            with subtests.test(msg=f"Invalid stdvers: {invalid_value}"):
                lines = [">HEAD", f"    STDVERS={invalid_value}", ""]
                header = Header()
                header.read_header(lines)
                assert header.stdvers == "SEG 1.0"


class TestHeaderWriteMethods:
    """Test Header write methods."""

    @patch("mt_metadata.transfer_functions.io.edi.metadata.header.get_now_utc")
    @patch(
        "mt_metadata.transfer_functions.io.edi.metadata.header.__version__",
        "1.0.0",
    )
    def test_write_header(self, mock_get_now_utc, populated_header, subtests):
        """Test write_header method."""
        mock_get_now_utc.return_value = MTime()

        header_lines = populated_header.write_header()

        with subtests.test(msg="Returns list"):
            assert isinstance(header_lines, list)

        with subtests.test(msg="Starts with >HEAD"):
            assert header_lines[0] == ">HEAD\n"

        with subtests.test(msg="Ends with blank line"):
            assert header_lines[-1] == "\n"

        with subtests.test(msg="Contains expected fields"):
            header_text = "".join(header_lines)
            expected_fields = [
                "ACQBY=Test Researcher",
                "DATAID=MT001",
                "PROJECT=TestProject",
                "PROGNAME=mt_metadata",
                "PROGVERS=1.0.0",
            ]
            for field in expected_fields:
                assert field in header_text

        with subtests.test(msg="Latitude format"):
            header_text = "".join(header_lines)
            assert "LAT=" in header_text

        with subtests.test(msg="Longitude format"):
            header_text = "".join(header_lines)
            assert "LON=" in header_text

        with subtests.test(msg="Elevation format"):
            header_text = "".join(header_lines)
            assert "ELEV=1234.560" in header_text

    def test_write_header_longitude_format(self, populated_header, subtests):
        """Test write_header with different longitude formats."""
        with subtests.test(msg="LON format"):
            lines = populated_header.write_header(longitude_format="LON")
            header_text = "".join(lines)
            assert "LON=" in header_text
            assert "LONG=" not in header_text

        with subtests.test(msg="LONG format"):
            lines = populated_header.write_header(longitude_format="LONG")
            header_text = "".join(lines)
            assert "LONG=" in header_text
            assert "LON=" not in header_text

    def test_write_header_latlon_format(self, populated_header, subtests):
        """Test write_header with different lat/lon formats."""
        with subtests.test(msg="Decimal degrees format"):
            lines = populated_header.write_header(latlon_format="dd")
            header_text = "".join(lines)
            assert "LAT=37.774900" in header_text

        with subtests.test(msg="DMS format"):
            lines = populated_header.write_header(latlon_format="dms")
            header_text = "".join(lines)
            # DMS format should be different from decimal
            assert "LAT=37.774900" not in header_text

    def test_write_header_skip_none_values(self, subtests):
        """Test that None values are skipped in write_header."""
        header = Header(
            dataid="TEST",
            acqby=None,
            project=None,
        )

        lines = header.write_header()
        header_text = "".join(lines)

        with subtests.test(msg="Includes non-None values"):
            assert "DATAID=TEST" in header_text

        with subtests.test(msg="Skips None values"):
            assert "ACQBY=" not in header_text
            assert "PROJECT=" not in header_text

    def test_write_header_required_only(self, populated_header):
        """Test write_header with required=True."""
        lines = populated_header.write_header(required=True)
        header_text = "".join(lines)

        # Should contain required fields
        required_fields = ["DATAID", "FILEBY", "FILEDATE", "PROGNAME", "PROGVERS"]
        for field in required_fields:
            assert field in header_text


class TestHeaderStringMethods:
    """Test Header string representation methods."""

    def test_str_method(self, populated_header):
        """Test __str__ method."""
        str_output = str(populated_header)

        assert isinstance(str_output, str)
        assert ">HEAD" in str_output
        assert "DATAID=MT001" in str_output
        assert "PROJECT=TestProject" in str_output

    def test_repr_method(self, populated_header):
        """Test __repr__ method."""
        repr_output = repr(populated_header)
        str_output = str(populated_header)

        filedate = repr_output[
            repr_output.find("FILEDATE=") + 9 : repr_output.find("FILEDATE=") + 41
        ]
        str_output = (
            str_output[: str_output.find("FILEDATE=") + 9]
            + filedate
            + str_output[str_output.find("FILEDATE=") + 41 :]
        )

        assert repr_output == str_output


class TestHeaderValidation:
    """Test Header validation methods."""

    def test_validate_header_list(self, default_header, subtests):
        """Test _validate_header_list method."""
        # Test with valid header list
        valid_list = [
            "ACQBY=Test Researcher",
            "DATAID=MT001",
            "PROJECT=TestProject",
        ]

        result = default_header._validate_header_list(valid_list)

        with subtests.test(msg="Returns list"):
            assert isinstance(result, list)

        with subtests.test(msg="Normalizes keys"):
            assert "acqby=Test Researcher" in result
            assert "dataid=MT001" in result

        # Test with None input
        with subtests.test(msg="Handles None input"):
            result = default_header._validate_header_list(None)
            assert result is None

        # Test with invalid entries
        with subtests.test(msg="Filters invalid entries"):
            invalid_list = [
                "ACQBY=Test Researcher",
                "INVALID_LINE_WITHOUT_EQUALS",
                "",
                "   ",
                "KEY=VALUE=EXTRA",  # Multiple equals
            ]
            result = default_header._validate_header_list(invalid_list)
            assert len(result) == 1  # Only the valid entry should remain
            assert "acqby=Test Researcher" in result


class TestHeaderIntegration:
    """Integration tests for Header class."""

    def test_read_write_cycle_file(self, sample_edi_file, tmp_path, subtests):
        """Test complete read-write cycle using files."""
        # Read from sample file
        original_header = Header()

        # Read the file manually since Header doesn't have read_file method
        with open(sample_edi_file, "r") as f:
            lines = f.readlines()

        original_header.read_header(lines)

        # Write to new file
        output_file = tmp_path / "output_header.edi"
        header_lines = original_header.write_header()

        with open(output_file, "w") as f:
            f.writelines(header_lines)

        # Read back the written file
        new_header = Header()
        with open(output_file, "r") as f:
            new_lines = f.readlines()

        new_header.read_header(new_lines)

        # Compare key attributes
        with subtests.test(msg="dataid preserved"):
            assert original_header.dataid == new_header.dataid

        with subtests.test(msg="project preserved"):
            assert original_header.project == new_header.project

        with subtests.test(msg="coordinate_system preserved"):
            assert original_header.coordinate_system == new_header.coordinate_system

        with subtests.test(msg="elevation preserved"):
            if (
                original_header.elevation is not None
                and new_header.elevation is not None
            ):
                assert abs(original_header.elevation - new_header.elevation) < 0.001

    def test_read_write_cycle_lines(self, sample_edi_lines, subtests):
        """Test complete read-write cycle using line arrays."""
        # Read from sample lines
        original_header = Header()
        original_header.read_header(sample_edi_lines)

        # Write to new lines
        written_lines = original_header.write_header()

        # Read back the written lines
        new_header = Header()
        new_header.read_header(written_lines)

        # Compare key attributes
        with subtests.test(msg="dataid preserved"):
            assert original_header.dataid == new_header.dataid

        with subtests.test(msg="acqby preserved"):
            assert original_header.acqby == new_header.acqby

        with subtests.test(msg="coordinate_system preserved"):
            assert original_header.coordinate_system == new_header.coordinate_system


class TestHeaderErrorHandling:
    """Test error handling in Header class."""

    def test_invalid_date_handling(self, subtests):
        """Test handling of invalid date values."""
        header = Header()

        with subtests.test(msg="Invalid date string"):
            # This should not raise an exception but create a default MTime
            with pytest.raises(ValueError):
                header.acqdate = "invalid_date_string"

        with subtests.test(msg="None date"):
            header.acqdate = None
            assert isinstance(header.acqdate, MTime)

    def test_invalid_units_handling(self, subtests):
        """Test handling of invalid units."""
        header = Header(units="bad_units")
        with subtests.test(msg="Valid units"):
            assert header.units == "unknown"

    def test_empty_header_list(self, default_header):
        """Test reading from empty header list."""
        # Should not raise exceptions
        default_header.read_header([])

        # Header should maintain default values
        assert default_header.dataid == ""
        assert default_header.progname == "mt_metadata"

    def test_malformed_header_lines(self, default_header, subtests):
        """Test reading malformed header lines."""
        malformed_lines = [
            ">HEAD",
            "    ACQBY",  # Missing equals sign
            "    =NoKey",  # Missing key
            "    DATAID=MT001=EXTRA",  # Multiple equals signs
            "    VALID=ValidValue",
            "",
        ]

        # Should not raise exceptions
        default_header.read_header(malformed_lines)

        # Should maintain defaults for invalid lines
        with subtests.test(msg="Maintains defaults for invalid lines"):
            assert default_header.acqby is None


class TestHeaderPerformance:
    """Performance tests for Header class."""

    @pytest.mark.skip("Performance tests are not run by default")
    def test_large_header_list_performance(self, benchmark):
        """Test performance with large header lists."""
        # Create a large header list
        large_header_list = [">HEAD"]
        for i in range(1000):
            large_header_list.append(f"    FIELD{i}=Value{i}")
        large_header_list.append("")

        header = Header()

        # Benchmark reading
        def read_large_header():
            header.read_header(large_header_list)

        benchmark(read_large_header)

    @pytest.mark.skip("Performance tests are not run by default")
    def test_write_performance(self, benchmark, populated_header):
        """Test write performance."""
        benchmark(populated_header.write_header)


class TestHeaderFieldTypes:
    """Test specific field types and their behavior."""

    def test_numeric_fields(self, subtests):
        """Test numeric field types."""
        header = Header()

        with subtests.test(msg="Empty field as float"):
            header.empty = 1e35
            assert isinstance(header.empty, float)

        with subtests.test(msg="Elevation as float"):
            header.elevation = 1234.56
            assert isinstance(header.elevation, float)
            assert header.elevation == 1234.56

        with subtests.test(msg="Elevation as None"):
            header.elevation = None
            assert header.elevation == 0.0

    def test_string_fields(self, subtests):
        """Test string field types."""
        header = Header()

        with subtests.test(msg="Required string field"):
            header.dataid = "MT001"
            assert header.dataid == "MT001"

        with subtests.test(msg="Optional string field"):
            header.acqby = "Test Researcher"
            assert header.acqby == "Test Researcher"

        with subtests.test(msg="Optional string field as None"):
            header.acqby = None
            assert header.acqby is None

    def test_enum_fields(self, subtests):
        """Test enumeration field types."""
        header = Header()

        with subtests.test(msg="Coordinate system enum"):
            valid_values = [
                GeographicReferenceFrameEnum.geographic,
                GeographicReferenceFrameEnum.geomagnetic,
            ]
            for value in valid_values:
                header.coordinate_system = value
                assert header.coordinate_system == value

        with subtests.test(msg="Standards version enum"):
            header.stdvers = StdEDIversionsEnum.SEG_1
            assert header.stdvers == "SEG 1.0"


# =============================================================================
# Parametrized Tests
# =============================================================================


@pytest.mark.parametrize(
    "field_name,test_value,expected_type",
    [
        ("acqby", "Test Researcher", str),
        ("dataid", "MT001", str),
        ("project", "TestProject", str),
        ("prospect", "TestProspect", str),
        ("loc", "Test Location", (str, type(None))),
        ("survey", "Test Survey", str),
        ("empty", 1e32, float),
        ("elev", 1234.56, float),
        ("latitude", 37.7749, float),
        ("longitude", -122.4194, float),
    ],
)
def test_field_assignment(field_name, test_value, expected_type):
    """Test field assignment and type validation."""
    header = Header()
    setattr(header, field_name, test_value)
    actual_value = getattr(header, field_name)

    if isinstance(expected_type, tuple):
        assert type(actual_value) in expected_type
    else:
        assert isinstance(actual_value, expected_type)

    assert actual_value == test_value


@pytest.mark.parametrize("date_field", ["acqdate", "enddate", "filedate", "progdate"])
def test_date_field_types(date_field):
    """Test date field validation with different input types."""
    header = Header()

    # Test with string
    setattr(header, date_field, "2023-01-15T10:30:00")
    assert isinstance(getattr(header, date_field), MTime)

    # Test with pandas Timestamp
    ts = pd.Timestamp("2023-01-15 10:30:00")
    setattr(header, date_field, ts)
    assert isinstance(getattr(header, date_field), MTime)


@pytest.mark.parametrize(
    "coordinate_system",
    [GeographicReferenceFrameEnum.geographic, GeographicReferenceFrameEnum.geomagnetic],
)
def test_coordinate_system_values(coordinate_system):
    """Test valid coordinate system values."""
    header = Header()
    header.coordinate_system = coordinate_system
    assert header.coordinate_system == coordinate_system


@pytest.mark.parametrize(
    "longitude_format,expected_key",
    [
        ("LON", "LON"),
        ("LONG", "LONG"),
    ],
)
def test_longitude_format_in_output(longitude_format, expected_key, populated_header):
    """Test longitude format in write_header output."""
    lines = populated_header.write_header(longitude_format=longitude_format)
    header_text = "".join(lines)
    assert f"{expected_key}=" in header_text


if __name__ == "__main__":
    pytest.main(["-v", __file__])
