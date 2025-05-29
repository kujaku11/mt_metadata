# -*- coding: utf-8 -*-
"""
Tests for the Information class in EDI metadata.

This module tests the Information class functionality including reading/writing
information sections, parsing metadata and handling different file formats.
"""

from unittest.mock import patch

import pytest

from mt_metadata.transfer_functions.io.edi.metadata.information import Information


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def default_information():
    """Return an Information instance with default values."""
    return Information()


@pytest.fixture(scope="module")
def sample_standard_edi_lines():
    """Return sample standard format EDI lines for testing."""
    return [
        "Line before info",
        ">INFO",
        "    Project = MT Survey 2023",
        "    Survey = DEMO-A",
        "    SiteName = SITE001",
        "    ProcessedBy = Data Analyst",
        "    ProcessingTag = 1.0",
        "    SignConvention = +",
        "    Ex_len = 100.0",
        "    Ey_len = 100.0",
        "    Ex_resistance = 1.2",
        "    Ey_resistance = 1.5",
        "    HX = 1234",
        "    HY = 5678",
        "    HZ = 9012",
        "    Year = 2023",
        "    NFFT = 4096",
        "    RemoteSite = [SITE002]",
        "    RunList = [MT001a]",
        ">DEFINEMEAS",
    ]


@pytest.fixture(scope="module")
def sample_phoenix_edi_lines():
    """Return sample Phoenix format EDI lines for testing."""
    return [
        "Line before info",
        ">INFO",
        "    Survey: MT2023             Job: Geothermal Project",
        "    Stn Number: SITE001        MTU-Box Serial Number: 2345",
        "    Hardware: V8               MTUProg Version: v3.16",
        "    Ex Pot Resist: 0.8 kOhm    Ey Pot Resist: 1.1 kOhm",
        "    Ex Voltage: AC=0.2mV, DC=0.5mV    Ey Voltage: AC=0.3mV, DC=0.4mV",
        "    Hx Sen: 1234              Hy Sen: 5678",
        "    Hz Sen: 9012              Run Information Station",
        "    Start-up: 2023-05-01       End-Time: 2023-05-10",
        "    XPR Weighting: Robust      Company: Example Inc",
        ">DEFINEMEAS",
    ]


@pytest.fixture(scope="module")
def sample_empower_edi_lines():
    """Return sample Empower format EDI lines for testing."""
    return [
        "Line before info",
        ">INFO",
        "    EMPower Data",
        "    ProcessingSoftware = EMPower MT Processing",
        "    SiteName = SITE001",
        "    Year = 2023",
        "    Process_Date = 2023-06-15",
        "    Declination = 12.5",
        "    Station_name = SITE001",
        "    Electrics",
        "        E1",
        "            Component = E1",
        "            Length = 100",
        "            AC = 0.1",
        "            DC = 0.3",
        "            Negative_res = 1.2",
        "            Positive_res = 1.0",
        "        E2",
        "            Component = E2",
        "            Length = 100",
        "            AC = 0.2",
        "            DC = 0.4",
        "            Negative_res = 1.4",
        "            Positive_res = 1.3",
        "    Magnetics",
        "        H1",
        "            Component = H1",
        "            Sensor_type = MFS-06e",
        "            Azimuth = 0",
        "            Sensor_serial = 1234",
        "            Cal_name = cal_1234",
        "            Saturation = 0%",
        "        H2",
        "            Component = H2",
        "            Sensor_type = MFS-06e",
        "            Azimuth = 90",
        "            Sensor_serial = 5678",
        "            Cal_name = cal_5678",
        "            Saturation = 0%",
        "        H3",
        "            Component = H3",
        "            Sensor_type = MFS-06e",
        "            Azimuth = 0",
        "            Sensor_serial = 9012",
        "            Cal_name = cal_9012",
        "            Saturation = 0%",
        ">DEFINEMEAS",
    ]


@pytest.fixture(scope="module")
def sample_lat_lon_info_lines():
    """Return sample EDI lines with different latitude/longitude formats."""
    return [
        ">INFO",
        "    Lat 45.123 Long -120.456",
        "    Lat=45.124 Lng=-120.457",
        "    Latitude: 45.125 Longitude: -120.458",
        "    Lat 45 30 30 Lon -120 30 30",
        ">DEFINEMEAS",
    ]


# =============================================================================
# Tests
# =============================================================================


class TestInformationInitialization:
    """Test initialization of the Information class."""

    def test_default_values(self, default_information):
        """Test default values of Information instance."""
        assert len(default_information.info_list) == 0
        assert len(default_information.info_dict) == 0
        assert default_information._phoenix_file is False
        assert default_information._empower_file is False


class TestInformationStandardFormat:
    """Test Information class with standard EDI format."""

    def test_read_standard_info(
        self, default_information, sample_standard_edi_lines, subtests
    ):
        """Test reading standard format info section."""
        default_information.read_info(sample_standard_edi_lines)

        # Check parsed attributes
        with subtests.test(msg="basic attributes"):
            assert len(default_information.info_list) > 0
            assert len(default_information.info_dict) > 0
            assert default_information._phoenix_file is False
            assert default_information._empower_file is False

        # Check specific values
        expected_values = {
            "survey.id": "DEMO-A",
            "survey.project": "MT Survey 2023",
            "station.geographic_name": "SITE001",
            "transfer_function.processed_by.name": "Data Analyst",
            "transfer_function.id": "1.0",
            "transfer_function.sign_convention": "+",
            "run.ex.dipole_length": "100.0",
            "run.ey.dipole_length": "100.0",
            "run.ex.contact_resistance.start": "1.2",
            "run.ey.contact_resistance.start": "1.5",
            "run.hx.sensor.id": "1234",
            "run.hy.sensor.id": "5678",
            "run.hz.sensor.id": "9012",
            "survey.time_period.start_date": "2023",
        }

        for key, expected in expected_values.items():
            with subtests.test(msg=f"parsed {key}"):
                assert default_information.info_dict.get(key) == expected

        # Check processing parameters
        assert (
            "transfer_function.processing_parameters" in default_information.info_dict
        )
        assert any(
            "NFFT=4096" in param
            for param in default_information.info_dict[
                "transfer_function.processing_parameters"
            ]
        )

    def test_write_standard_info(self, default_information, subtests):
        """Test writing standard format info section."""
        info_lines = default_information.write_info()

        with subtests.test(msg="info header"):
            assert ">INFO" in info_lines[0]

        with subtests.test(msg="line count"):
            # +1 for header line
            assert len(info_lines) > 1

        # Check content
        content = "".join(info_lines)
        with subtests.test(msg="contains original items"):
            assert "Project = MT Survey 2023" in content
            assert "Survey = DEMO-A" in content
            assert "SiteName = SITE001" in content


class TestInformationPhoenixFormat:
    """Test Information class with Phoenix format EDI."""

    def test_read_phoenix_info(
        self, default_information, sample_phoenix_edi_lines, subtests
    ):
        """Test reading Phoenix format info section."""
        default_information.read_info(sample_phoenix_edi_lines)

        # Check format detection
        with subtests.test(msg="phoenix format detected"):
            assert default_information._phoenix_file is True
            assert default_information._empower_file is False

        # Check phoenix-specific parsed values
        expected_values = {
            "survey.id": "MT2023",
            "survey.project": "Geothermal Project",
            "station.id": "SITE001",
            "run.data_logger.id": "2345",
            "run.data_logger.model": "V8",
            "run.data_logger.firmware.version": "v3.16",
            "run.ex.contact_resistance.start": "0.8",
            "run.ey.contact_resistance.start": "1.1",
            "run.ex.ac.start": "0.2",
            "run.ex.dc.start": "0.5",
            "run.ey.ac.start": "0.3",
            "run.ey.dc.start": "0.4",
            "run.hx.sensor.id": "1234",
            "run.hy.sensor.id": "5678",
            "run.hz.sensor.id": "9012",
            "station.acquired_by.organization": "Example Inc",
        }

        for key, expected in expected_values.items():
            with subtests.test(msg=f"phoenix parsed {key}"):
                assert default_information.info_dict.get(key) == expected

        # Check sensor metadata
        with subtests.test(msg="phoenix sensor metadata"):
            assert (
                default_information.info_dict.get("hx.sensor.manufacturer")
                == "Phoenix Geophysics"
            )
            assert (
                default_information.info_dict.get("hx.sensor.type") == "Induction Coil"
            )


class TestInformationEmpowerFormat:
    """Test Information class with Empower format EDI."""

    def test_read_empower_info(
        self, default_information, sample_empower_edi_lines, subtests
    ):
        """Test reading Empower format info section."""
        default_information.read_info(sample_empower_edi_lines)

        # Check format detection
        with subtests.test(msg="empower format detected"):
            assert default_information._phoenix_file is False
            assert default_information._empower_file is True

        # Check empower-specific parsed values
        expected_values = {
            "transfer_function.software.name": "EMPower MT Processing",
            "station.geographic_name": "SITE001",
            "survey.time_period.start_date": "2023",
            "transfer_function.processed_date": "2023-06-15",
            "station.location.declination.value": "12.5",
            "run.ex.dipole_length": "100",
            "run.ex.ac.end": "0.1",
            "run.ex.dc.end": "0.3",
            "run.ex.contact_resistance.start": "1.2",
            "run.ex.contact_resistance.end": "1.0",
            "run.ey.dipole_length": "100",
            "run.ey.ac.end": "0.2",
            "run.ey.dc.end": "0.4",
            "run.ey.contact_resistance.start": "1.4",
            "run.ey.contact_resistance.end": "1.3",
            "run.hx.sensor.model": "mfs-06e",
            "run.hx.measured_azimuth": "0",
            "run.hx.sensor.id": "1234",
            "run.hx.comments": "cal_name=cal_1234,saturation=0",
        }

        for key, expected in expected_values.items():
            with subtests.test(msg=f"empower parsed {key}"):
                assert default_information.info_dict.get(key) == expected


class TestInformationParsingSpecialCases:
    """Test special cases for Information parsing."""

    def test_latitude_longitude_parsing(
        self, default_information, sample_lat_lon_info_lines, subtests
    ):
        """Test parsing of latitude and longitude in different formats."""
        default_information.read_info(sample_lat_lon_info_lines)

        # Check latitude/longitude parsing
        # The exact keys will depend on format detection and parsing logic
        info_dict = default_information.info_dict

        with subtests.test(msg="lat/lon present"):
            lat_keys = [key for key in info_dict.keys() if "lat" in key.lower()]
            lon_keys = [
                key
                for key in info_dict.keys()
                if "lon" in key.lower() or "lng" in key.lower()
            ]

            assert len(lat_keys) > 0
            assert len(lon_keys) > 0

        with subtests.test(msg="lat/lon values parsed"):
            for key in lat_keys:
                assert "45" in info_dict[key]

            for key in lon_keys:
                assert "-120" in info_dict[key]

    def test_separator_detection(self, default_information, subtests):
        """Test detection of different separators in info lines."""
        separators = {
            "Key = Value": "=",
            "Key: Value": ":",
            "Key = Value: More": "=",  # Should take first separator
            "Key: Value = More": ":",  # Should take first separator
            "No separator line": None,
        }

        for line, expected_sep in separators.items():
            with subtests.test(msg=f"separator in '{line}'"):
                sep = default_information._get_separator(line)
                assert sep == expected_sep

    def test_line_reading(self, default_information, subtests):
        """Test reading different line formats."""
        test_lines = {
            "Key = Value": ("Key", "Value"),
            "Key: Value": ("Key", "Value"),
            "Key = [Value1,Value2]": ("Key", ["Value1", "Value2"]),
            "Key = [Value1;Value2]": ("Key", ["Value1", "Value2"]),
            "Key = [Value1:Value2]": ("Key", ["Value1", "Value2"]),
            "No separator line": ("No separator line", None),
        }

        for line, expected in test_lines.items():
            with subtests.test(msg=f"reading '{line}'"):
                key, value = default_information._read_line(line)
                assert key == expected[0]

                # For list values, check each item
                if isinstance(expected[1], list) and isinstance(value, list):
                    assert len(value) == len(expected[1])
                    for i, item in enumerate(value):
                        assert item == expected[1][i]
                else:
                    assert value == expected[1]


class TestInformationMethods:
    """Test general methods of the Information class."""

    def test_string_representation(self, default_information):
        """Test string representation of Information."""
        with patch.object(
            default_information, "write_info", return_value=["Line1\n", "Line2\n"]
        ):
            str_rep = str(default_information)
            assert str_rep == "Line1\nLine2\n"

            # Also check __repr__
            repr_str = repr(default_information)
            assert repr_str == str_rep

    def test_validate_info_list(self, default_information, subtests):
        """Test validation of info list items."""
        input_list = [
            ">INFO",
            "",
            "  ",
            "Valid Line 1",
            "Valid Line 2",
            "Valid Line 2",  # Duplicate
            ">Other marker",
        ]

        # Test with sorting
        with subtests.test(msg="validate with sorting"):
            result = default_information._validate_info_list(input_list, sort=True)
            assert len(result) == 2  # Only valid unique lines
            assert ">INFO" not in result
            assert ">Other marker" not in result
            assert "" not in result
            assert "  " not in result
            assert "Valid Line 1" in result
            assert "Valid Line 2" in result
            assert len(result) == len(set(result))  # No duplicates

        # Test without sorting
        with subtests.test(msg="validate without sorting"):
            result = default_information._validate_info_list(input_list, sort=False)
            assert len(result) == 3  # Includes duplicate
            assert ">INFO" not in result
            assert ">Other marker" not in result
            assert "" not in result
            assert "  " not in result

            # Count occurrences of "Valid Line 2"
            vl2_count = sum(1 for item in result if item == "Valid Line 2")
            assert vl2_count == 2  # Should keep duplicates


class TestInformationEdgeCases:
    """Test edge cases for Information handling."""

    def test_empty_info_section(self, default_information):
        """Test handling of an empty info section."""
        empty_lines = [
            "Line before info",
            ">INFO",
            ">DEFINEMEAS",
        ]

        default_information.read_info(empty_lines)
        assert len(default_information.info_list) == 0
        assert len(default_information.info_dict) == 0

    def test_missing_info_section(self, default_information):
        """Test handling when info section is missing."""
        no_info_lines = [
            "Line with no info section",
            ">DEFINEMEAS",
        ]

        default_information.read_info(no_info_lines)
        assert len(default_information.info_list) == 0
        assert len(default_information.info_dict) == 0

    def test_malformed_info_line(self, default_information):
        """Test handling of malformed info lines."""
        malformed_lines = [
            ">INFO",
            "    Key with no value",
            "    = Value with no key",
            "    Multiple = equals = signs",
            "    : Multiple : colons",
            ">DEFINEMEAS",
        ]

        default_information.read_info(malformed_lines)
        # Should not raise exceptions
        assert len(default_information.info_list) > 0


if __name__ == "__main__":
    pytest.main(["-v", __file__])
