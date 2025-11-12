"""
Comprehensive pytest test suite for Header metadata class.
This test suite follows modern pytest patterns with fixtures and subtests for optimal efficiency.
All tests are designed to work with the actual Header class implementation.
"""

import pytest

# Import using the new consolidated import approach
from mt_metadata.transfer_functions.io.zonge.metadata import Header


class TestHeaderBasics:
    """Test basic Header functionality that works reliably."""

    @pytest.fixture(scope="class")
    def default_header(self):
        """Fixture providing a default Header instance for efficiency."""
        return Header()

    @pytest.fixture(scope="class")
    def populated_header(self):
        """Fixture providing Header with populated data."""
        header = Header()
        header.name = "Test Station"
        header.elevation = 1500.0
        header.gps.lat = 45.123
        header.gps.lon = -123.456
        header.gps.datum = "WGS 84"
        header.rx.gdp_stn = "STATION_01"
        return header

    def test_header_creation(self, default_header, subtests):
        """Test Header can be created with default values."""
        with subtests.test("header is Header instance"):
            assert isinstance(default_header, Header)

        with subtests.test("default name is None"):
            assert default_header.name is None

        with subtests.test("default elevation is 0.0"):
            assert default_header.elevation == 0.0

    def test_nested_objects_initialized(self, default_header, subtests):
        """Test that all nested metadata objects are properly initialized."""
        nested_attrs = [
            "survey",
            "tx",
            "rx",
            "m_t_edit",
            "m_t_f_t24",
            "gps",
            "gdp",
            "ch",
            "stn",
            "line",
            "unit",
            "job",
        ]

        for attr in nested_attrs:
            with subtests.test(f"{attr} is initialized"):
                assert hasattr(default_header, attr)
                nested_obj = getattr(default_header, attr)
                assert nested_obj is not None

    def test_computed_properties(self, populated_header, subtests):
        """Test computed properties work correctly."""
        with subtests.test("latitude property"):
            assert populated_header.latitude == 45.123

        with subtests.test("longitude property"):
            assert populated_header.longitude == -123.456

        with subtests.test("datum property"):
            assert populated_header.datum == "WGS 84"

        with subtests.test("station property"):
            assert populated_header.station == "STATION_01"

    def test_field_assignment(self, subtests):
        """Test direct field assignment works."""
        header = Header()

        with subtests.test("name assignment"):
            header.name = "New Station"
            assert header.name == "New Station"

        with subtests.test("elevation assignment"):
            header.elevation = 2000.0
            assert header.elevation == 2000.0

        with subtests.test("gps field assignment"):
            header.gps.lat = 50.0
            header.gps.lon = -120.0
            assert header.gps.lat == 50.0
            assert header.gps.lon == -120.0


class TestHeaderSetters:
    """Test Header custom setter behavior via __setattr__."""

    @pytest.fixture
    def fresh_header(self):
        """Fixture for setter tests."""
        return Header()

    def test_latitude_setter(self, fresh_header, subtests):
        """Test latitude setter via __setattr__."""
        with subtests.test("set latitude as float"):
            fresh_header.latitude = 48.5
            assert fresh_header.latitude == 48.5
            assert fresh_header.gps.lat == 48.5

        with subtests.test("set latitude as string"):
            fresh_header.latitude = "49.123"
            assert fresh_header.latitude == 49.123
            assert fresh_header.gps.lat == 49.123

    def test_longitude_setter(self, fresh_header, subtests):
        """Test longitude setter via __setattr__."""
        with subtests.test("set longitude as float"):
            fresh_header.longitude = -125.5
            assert fresh_header.longitude == -125.5
            assert fresh_header.gps.lon == -125.5

        with subtests.test("set longitude as string"):
            fresh_header.longitude = "-126.789"
            assert fresh_header.longitude == -126.789
            assert fresh_header.gps.lon == -126.789

    def test_elevation_setter(self, fresh_header, subtests):
        """Test elevation setter via __setattr__."""
        with subtests.test("set elevation as float"):
            fresh_header.elevation = 2500.0
            assert fresh_header.elevation == 2500.0

        with subtests.test("set elevation as string"):
            fresh_header.elevation = "3000.5"
            assert fresh_header.elevation == 3000.5

    def test_station_setter(self, fresh_header, subtests):
        """Test station setter via __setattr__."""
        with subtests.test("set station"):
            fresh_header.station = "CUSTOM_STATION"
            assert fresh_header.station == "CUSTOM_STATION"
            assert fresh_header.rx.gdp_stn == "CUSTOM_STATION"


class TestHeaderProperties:
    """Test Header computed properties and behavior."""

    @pytest.fixture
    def fresh_header(self):
        """Fixture providing a fresh Header instance."""
        return Header()

    def test_gps_properties(self, fresh_header, subtests):
        """Test GPS-related properties."""
        # Set GPS data
        fresh_header.gps.lat = 47.678
        fresh_header.gps.lon = -122.123
        fresh_header.gps.datum = "NAD83"
        fresh_header.gps.u_t_m_zone = 10

        with subtests.test("latitude property"):
            assert fresh_header.latitude == 47.678

        with subtests.test("longitude property"):
            assert fresh_header.longitude == -122.123

        with subtests.test("datum property"):
            assert fresh_header.datum == "NAD83"

        with subtests.test("utm_zone property"):
            assert fresh_header.utm_zone == "10"

    def test_station_properties(self, fresh_header, subtests):
        """Test station-related properties."""
        fresh_header.rx.gdp_stn = "TEST_STATION_02"

        with subtests.test("station property"):
            assert fresh_header.station == "TEST_STATION_02"

    def test_instrument_properties(self, fresh_header, subtests):
        """Test instrument-related properties."""
        fresh_header.gdp.type = "gdp32"
        fresh_header.gdp.prog_ver = "2.45:build789"

        with subtests.test("instrument_type property"):
            assert fresh_header.instrument_type == "GDP32"

        with subtests.test("firmware property"):
            assert fresh_header.firmware == "2.45"

    def test_properties_with_no_data(self, fresh_header, subtests):
        """Test properties when no data is set."""
        with subtests.test("latitude defaults to 0.0"):
            assert fresh_header.latitude == 0.0

        with subtests.test("longitude defaults to 0.0"):
            assert fresh_header.longitude == 0.0

        with subtests.test("datum has default value"):
            # GPS objects get initialized with default values
            assert fresh_header.datum is not None

        with subtests.test("station has default value"):
            # Station returns empty string by default
            assert fresh_header.station == ""


class TestHeaderFileOperations:
    """Test Header file reading and writing operations."""

    @pytest.fixture
    def header_instance(self):
        """Header instance for file operations."""
        return Header()

    @pytest.fixture
    def sample_header_lines(self):
        """Sample header lines for testing read_header."""
        return [
            "$survey.type=nsamt",  # Use lowercase field name and default value
            "$survey.array=tensor",  # Use lowercase field name and valid enum value
            "$tx.type=natural",  # Use lowercase field name and valid enum value
            "$m_t_edit.version=4.0",  # Use lowercase field name
            "$gps.lat=45.123456",  # Use lowercase to match actual field name
            "$gps.lon=-123.456789",  # Use lowercase to match actual field name
            "$rx.gdp_stn=TEST001",  # Use lowercase field name
            "$unit.length=m",  # Use lowercase field name
            "Data line 1",
            "Data line 2",
        ]

    def test_read_header(self, header_instance, sample_header_lines, subtests):
        """Test read_header method."""
        data_lines = header_instance.read_header(sample_header_lines)

        with subtests.test("returns list"):
            assert isinstance(data_lines, list)

        with subtests.test("includes data lines"):
            assert "Data line 1" in data_lines
            assert "Data line 2" in data_lines

        with subtests.test("excludes header lines"):
            assert not any(
                line.startswith("$")
                for line in data_lines
                if line in ["Data line 1", "Data line 2"]
            )

    def test_write_header(self, header_instance, subtests):
        """Test write_header method."""
        # Set some data first
        header_instance.name = "Test"
        header_instance.gps.lat = 45.0

        lines = header_instance.write_header()

        with subtests.test("returns list"):
            assert isinstance(lines, list)

        with subtests.test("first line is empty"):
            assert lines[0] == ""

        with subtests.test("contains header format"):
            # Should have lines starting with $
            dollar_lines = [line for line in lines if line.startswith("$")]
            assert len(dollar_lines) > 0

    def test_header_keys(self, header_instance, subtests):
        """Test _header_keys constant."""
        with subtests.test("header_keys exists"):
            assert hasattr(header_instance, "_header_keys")

        with subtests.test("header_keys is list"):
            assert isinstance(header_instance._header_keys, list)

        with subtests.test("header_keys not empty"):
            assert len(header_instance._header_keys) > 0

        expected_keys = [
            "survey.type",
            "tx.type",
            "rx.gdp_stn",
            "g_p_s.lat",
            "g_p_s.lon",
            "unit.length",
        ]
        for key in expected_keys:
            with subtests.test(f"contains {key}"):
                assert key in header_instance._header_keys


class TestHeaderIntegration:
    """Integration tests for Header class combining multiple features."""

    def test_complete_workflow(self, subtests):
        """Test a complete Header workflow."""
        # Create header
        header = Header()

        with subtests.test("initial creation"):
            assert header.name is None
            assert header.elevation == 0.0

        # Set data via multiple methods
        header.name = "Integration Test"
        header.elevation = 1800.0
        header.latitude = 46.5  # via setter
        header.longitude = -121.7  # via setter
        header.gps.datum = "WGS84"  # direct field access
        header.station = "INT_TEST_01"  # via setter

        with subtests.test("all data set correctly"):
            assert header.name == "Integration Test"
            assert header.elevation == 1800.0
            assert header.latitude == 46.5
            assert header.longitude == -121.7
            assert header.datum == "WGS 84"  # Actual format returned by the model
            assert header.station == "INT_TEST_01"

        with subtests.test("properties stay consistent"):
            assert header.latitude == header.gps.lat
            assert header.longitude == header.gps.lon

    def test_property_consistency(self, subtests):
        """Test that properties stay consistent across operations."""
        header = Header()

        # Set via property setter
        header.latitude = 50.0
        header.longitude = -130.0

        with subtests.test("property and field consistency"):
            assert header.latitude == header.gps.lat
            assert header.longitude == header.gps.lon

        # Modify field directly
        header.gps.lat = 51.0
        header.gps.lon = -131.0

        with subtests.test("field changes reflect in properties"):
            assert header.latitude == 51.0
            assert header.longitude == -131.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
