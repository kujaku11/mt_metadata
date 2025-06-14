# -*- coding: utf-8 -*-
"""
Tests for the Information class in EDI metadata.

This module tests the Information class functionality including reading/writing
information sections, parsing metadata and handling different file formats.
"""


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
def sample_multi_column_lines():
    """Return sample multi-column lines for Phoenix format testing."""
    return [
        "    Survey: MT2023             Job: Geothermal Project",
        "    Stn Number: SITE001        MTU-Box Serial Number: 2345",
        "    Hardware: V8               MTUProg Version: v3.16",
        "    Ex Pot Resist: 0.8 kOhm    Ey Pot Resist: 1.1 kOhm",
    ]


# =============================================================================
# Tests
# =============================================================================


class TestInformationInitialization:
    """Test initialization of the Information class."""

    def test_default_values(self, default_information):
        """Test default values of Information instance."""
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
        assert default_information.info_dict[
            "transfer_function.processing_parameters"
        ] == ["nfft=4096"]


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
            "run.hx.sensor.model": "MFS-06e",
            "run.hx.measured_azimuth": "0",
            "run.hx.sensor.id": "1234",
            "run.hx.comments": ["cal_name=cal_1234", "saturation=0%"],
        }

        for key, expected in expected_values.items():
            with subtests.test(msg=f"empower parsed {key}"):
                assert default_information.info_dict.get(key) == expected


class TestInformationHelperMethods:
    """Test helper methods of Information class."""

    def test_get_separator(self, default_information, subtests):
        """Test _get_separator method."""
        test_lines = {
            "Key = Value": "=",
            "Key: Value": ":",
            "Key Value": None,
            "": None,
            "Key = Value: More": "=",  # Should take first separator
            "Key: Value = More": ":",  # Should take first separator
        }

        for line, expected in test_lines.items():
            with subtests.test(msg=f"separator in '{line}'"):
                sep = default_information._get_separator(line)
                assert sep == expected

    def test_split_phoenix_columns(
        self, default_information, sample_multi_column_lines, subtests
    ):
        """Test _split_phoenix_columns method."""
        expected_splits = [
            (True, ["Survey: MT2023", "Job: Geothermal Project"]),
            (True, ["Stn Number: SITE001", "MTU-Box Serial Number: 2345"]),
            (True, ["Hardware: V8", "MTUProg Version: v3.16"]),
            (True, ["Ex Pot Resist: 0.8 kOhm", "Ey Pot Resist: 1.1 kOhm"]),
        ]

        for i, line in enumerate(sample_multi_column_lines):
            with subtests.test(msg=f"splitting: {line}"):
                is_multi, columns = default_information._split_phoenix_columns(line)

                # Check if it detected multi-column correctly
                assert is_multi == expected_splits[i][0]

                # Check column content (ignoring extra whitespace)
                assert [col.strip() for col in columns] == [
                    col.strip() for col in expected_splits[i][1]
                ]

    def test_apply_phoenix_translation(self, default_information, subtests):
        """Test _apply_phoenix_translation method."""
        # Reset info_dict
        default_information.info_dict = {}

        # Test cases for translation
        test_cases = [
            ("Survey", "MT2023", "survey.id"),
            ("Hx Sen", "1234", "run.hx.sensor.id"),
            ("Ex Pot Resist", "0.8 kOhm", "run.ex.contact_resistance.start"),
        ]

        for key, value, expected_std_key in test_cases:
            with subtests.test(msg=f"translating {key}"):
                default_information._apply_phoenix_translation(key, value)
                assert expected_std_key in default_information.info_dict

                # For resistance values, should remove units
                if "resist" in key.lower():
                    assert default_information.info_dict[expected_std_key] == "0.8"
                else:
                    assert default_information.info_dict[expected_std_key] == value

        # Test voltage with AC/DC components
        with subtests.test(msg="translating Ex Voltage with AC/DC"):
            default_information._apply_phoenix_translation(
                "Ex Voltage", "AC=0.2mV, DC=0.5mV"
            )
            assert default_information.info_dict["run.ex.ac.start"] == "0.2"
            assert default_information.info_dict["run.ex.dc.start"] == "0.5"

    def test_get_empower_std_key(self, default_information, subtests):
        """Test _get_empower_std_key method."""
        test_cases = [
            # section, component, key, expected result
            ("general", None, "processingsoftware", "transfer_function.software.name"),
            ("general", None, "unknown_key", None),
            ("electrics", "e1", "length", "run.ex.dipole_length"),
            ("electrics", "e2", "ac", "run.ey.ac.end"),
            ("magnetics", "h1", "sensor_serial", "run.hx.sensor.id"),
            ("magnetics", "h2", "unknown_key", "run.hy.unknown_key"),
            ("magnetics", "h3", "cal_name", "run.hz.comments"),
        ]

        for section, component, key, expected in test_cases:
            with subtests.test(msg=f"{section}.{component}.{key}"):
                result = default_information._get_empower_std_key(
                    section, component, key
                )
                assert result == expected


class TestInformationNewParsingMethods:
    """Test the new parsing methods of the Information class."""

    def test_parse_standard_info(self, default_information, subtests):
        """Test _parse_standard_info method."""
        # Reset the object
        default_information.info_dict = {}

        # Standard format test lines
        standard_lines = [
            "Project = MT Survey 2023",
            "Survey = DEMO-A",
            "SiteName = SITE001",
            "NFFT = 4096",
            "RemoteSite = [SITE002, SITE003]",
            "EmptyKey = ",
            "NoValueLine",
        ]

        default_information._parse_standard_info(standard_lines)

        # Check that values were parsed correctly
        expected_values = {
            "survey.project": "MT Survey 2023",
            "survey.id": "DEMO-A",
            "station.geographic_name": "SITE001",
        }

        for key, expected in expected_values.items():
            with subtests.test(msg=f"standard parsed {key}"):
                assert default_information.info_dict.get(key) == expected

        # Check special handling for processing parameters
        with subtests.test(msg="processing parameters"):
            assert (
                "transfer_function.processing_parameters"
                in default_information.info_dict
            )
            assert (
                "nfft=4096"
                in default_information.info_dict[
                    "transfer_function.processing_parameters"
                ]
            )

        # Check list handling
        with subtests.test(msg="list handling"):
            assert (
                "remotesites" not in default_information.info_dict
            )  # Not in translation_dict

    def test_parse_empower_info(self, default_information, subtests):
        """Test _parse_empower_info method."""
        # Reset the object
        default_information.info_dict = {}

        # Empower format test lines
        empower_lines = [
            "EMPower Data",
            "ProcessingSoftware = EMPower MT Processing",
            "SiteName = SITE001",
            "Electrics",
            "    E1",
            "        Component = E1",
            "        Length = 100",
            "    E2",
            "        Component = E2",
            "        Length = 100",
            "Magnetics",
            "    H1",
            "        Sensor_type = MFS-06e",
            "        Azimuth = 0",
            "        Sensor_serial = 1234",
            "    H2",
            "        Sensor_type = MFS-06e",
            "        Azimuth = 90",
        ]

        default_information._parse_empower_info(empower_lines)

        # Check section and component parsing
        expected_values = {
            "transfer_function.software.name": "EMPower MT Processing",
            "station.geographic_name": "SITE001",
            "run.ex.dipole_length": "100",
            "run.ey.dipole_length": "100",
            "run.hx.sensor.model": "MFS-06e",
            "run.hx.measured_azimuth": "0",
            "run.hx.sensor.id": "1234",
            "run.hy.sensor.model": "MFS-06e",
            "run.hy.measured_azimuth": "90",
        }

        for key, expected in expected_values.items():
            with subtests.test(msg=f"empower parsed {key}"):
                assert default_information.info_dict.get(key) == expected


class TestInformationWriteMethod:
    """Test write method of the Information class."""

    def test_write_info(self, default_information, subtests):
        """Test write_info method."""
        # Setup test data
        default_information.info_dict = {
            "survey.id": "DEMO-A",
            "station.geographic_name": "SITE001",
            "run.ex.dipole_length": "100",
            "run.hx.sensor.id": "1234",
            "transfer_function.processing_parameters": ["NFFT=4096", "NDEC=10"],
            "empty_key": "",
            "null_key": None,
        }

        output_lines = default_information.write_info()

        # Check header
        with subtests.test(msg="info header"):
            assert output_lines[0] == ">INFO\n"

        # Check content
        content = "".join(output_lines)
        with subtests.test(msg="content keys"):
            assert "survey.id=DEMO-A" in content
            assert "station.geographic_name=SITE001" in content
            assert "run.ex.dipole_length=100" in content
            assert "run.hx.sensor.id=1234" in content
            assert (
                "transfer_function.processing_parameters=NFFT=4096,NDEC=10" in content
            )
            assert "empty_key" in content
            assert "null_key" in content  # Should be present but without value


if __name__ == "__main__":
    pytest.main(["-v", __file__])
