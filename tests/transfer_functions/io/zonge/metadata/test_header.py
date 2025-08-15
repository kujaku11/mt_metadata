"""
Test suite for Header metadata class using pytest with fixtures and subtests.
This test suite follows modern pytest patterns for comprehensive coverage and efficiency optimization.
"""

import json
from unittest.mock import Mock

import pytest

# Import using the new consolidated import approach
from mt_metadata.transfer_functions.io.zonge.metadata import (
    CH,
    GDP,
    GPS,
    Header,
    Job,
    Line,
    MTEdit,
    MTFT24,
    Rx,
    STN,
    Survey,
    Tx,
    Unit,
)


class TestHeaderDefault:
    """Test default initialization and basic attributes of Header class."""

    @pytest.fixture(scope="class")
    def default_header(self):
        """Fixture providing a default Header instance for efficiency."""
        return Header()

    def test_default_initialization(self, default_header, subtests):
        """Test that Header initializes with correct default values."""
        with subtests.test("default name value"):
            assert default_header.name is None

        with subtests.test("default elevation value"):
            assert default_header.elevation == 0.0

        with subtests.test("header has basic attributes"):
            assert hasattr(default_header, "name")
            assert hasattr(default_header, "elevation")
            assert hasattr(default_header, "gps")
            assert hasattr(default_header, "rx")

        with subtests.test("computed properties accessible"):
            # These should work - testing latitude/longitude computed properties
            assert isinstance(default_header.latitude, (int, float))
            assert isinstance(default_header.longitude, (int, float))

    def test_default_nested_objects(self, default_header, subtests):
        """Test that nested metadata objects are properly initialized."""
        nested_objects = [
            ("survey", Survey),
            ("tx", Tx),
            ("rx", Rx),
            ("m_t_edit", MTEdit),
            ("m_t_f_t24", MTFT24),
            ("gps", GPS),
            ("gdp", GDP),
            ("ch", CH),
            ("stn", STN),
            ("line", Line),
            ("unit", Unit),
            ("job", Job),
        ]

        for attr_name, expected_type in nested_objects:
            with subtests.test(f"has {attr_name} of type {expected_type.__name__}"):
                assert hasattr(default_header, attr_name)
                assert isinstance(getattr(default_header, attr_name), expected_type)

    def test_default_header_attributes(self, default_header, subtests):
        """Test that Header has all expected attributes."""
        expected_attributes = [
            "name",
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
            "elevation",
        ]

        for attr in expected_attributes:
            with subtests.test(f"has attribute {attr}"):
                assert hasattr(default_header, attr)

    def test_default_model_fields(self, default_header, subtests):
        """Test model fields are properly defined."""
        fields = default_header.model_fields
        expected_fields = [
            "name",
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
            "elevation",
        ]

        for field in expected_fields:
            with subtests.test(f"model has field {field}"):
                assert field in fields

    def test_header_keys_constant(self, default_header, subtests):
        """Test that _header_keys is properly defined."""
        with subtests.test("header_keys exists"):
            assert hasattr(default_header, "_header_keys")

        with subtests.test("header_keys is list"):
            assert isinstance(default_header._header_keys, list)

        with subtests.test("header_keys not empty"):
            assert len(default_header._header_keys) > 0

        expected_keys = [
            "survey.type",
            "survey.array",
            "tx.type",
            "m_t_edit.version",
            "m_t_edit.auto.phase_flip",
            "m_t_edit.phase_slope.smooth",
            "m_t_edit.phase_slope.to_z_mag",
            "m_t_edit.d_plus.use",
            "rx.gdp_stn",
            "rx.length",
            "rx.h_p_r",
            "g_p_s.lat",
            "g_p_s.lon",
            "unit.length",
        ]

        for key in expected_keys:
            with subtests.test(f"header_keys contains {key}"):
                assert key in default_header._header_keys


class TestHeaderComputedProperties:
    """Test computed properties (read-only) of Header class."""

    @pytest.fixture(scope="class")
    def header_with_gps(self):
        """Fixture providing Header with GPS data."""
        header = Header()
        header.gps.lat = 45.123
        header.gps.lon = -123.456
        header.gps.datum = "WGS84"
        header.gps.u_t_m_zone = 10
        return header

    @pytest.fixture(scope="class")
    def header_with_rx(self):
        """Fixture providing Header with RX data."""
        header = Header()
        header.rx.gdp_stn = "TEST_STATION"
        return header

    @pytest.fixture(scope="class")
    def header_with_gdp(self):
        """Fixture providing Header with GDP data."""
        header = Header()
        header.gdp.type = "gdp32"
        header.gdp.prog_ver = "1.23:build456"
        header.gdp.date = "2023-08-15"
        header.gdp.time = "14:30:00"
        return header

    def test_latitude_property(self, header_with_gps, subtests):
        """Test latitude computed property."""
        with subtests.test("latitude from GPS"):
            assert header_with_gps.latitude == 45.123

        with subtests.test("latitude is float"):
            assert isinstance(header_with_gps.latitude, float)

    def test_longitude_property(self, header_with_gps, subtests):
        """Test longitude computed property."""
        with subtests.test("longitude from GPS"):
            assert header_with_gps.longitude == -123.456

        with subtests.test("longitude is float"):
            assert isinstance(header_with_gps.longitude, float)

    def test_datum_property(self, header_with_gps, subtests):
        """Test datum computed property."""
        with subtests.test("datum from GPS"):
            assert header_with_gps.datum == "WGS84"

        with subtests.test("datum is uppercase"):
            header_with_gps.gps.datum = "wgs84"
            assert header_with_gps.datum == "WGS84"

    def test_utm_zone_property(self, header_with_gps, subtests):
        """Test UTM zone computed property."""
        with subtests.test("utm_zone from GPS"):
            assert header_with_gps.utm_zone == "10"

        with subtests.test("utm_zone is string"):
            assert isinstance(header_with_gps.utm_zone, str)

    def test_station_property(self, header_with_rx, subtests):
        """Test station computed property."""
        with subtests.test("station from RX"):
            assert header_with_rx.station == "TEST_STATION"

    def test_instrument_type_property(self, header_with_gdp, subtests):
        """Test instrument_type computed property."""
        with subtests.test("instrument_type from GDP"):
            assert header_with_gdp.instrument_type == "GDP32"

        with subtests.test("instrument_type is uppercase"):
            header_with_gdp.gdp.type = "gdp24"
            assert header_with_gdp.instrument_type == "GDP24"

    def test_firmware_property(self, header_with_gdp, subtests):
        """Test firmware computed property."""
        with subtests.test("firmware from GDP"):
            assert header_with_gdp.firmware == "1.23"

    def test_start_time_property(self, header_with_gdp, subtests):
        """Test start_time computed property."""
        with subtests.test("start_time from GDP"):
            expected = "2023-08-15T14:30:00"
            assert header_with_gdp.start_time == expected

    def test_computed_properties_with_missing_data(self, subtests):
        """Test computed properties when underlying data is missing."""
        header = Header()

        with subtests.test("latitude with no GPS data"):
            assert header.latitude == 0.0  # Falls back to _gps_lat

        with subtests.test("longitude with no GPS data"):
            assert header.longitude == 0.0  # Falls back to _gps_lon

        with subtests.test("datum with no GPS data"):
            assert header.datum is None

        with subtests.test("station with no RX data"):
            assert header.station is None

        with subtests.test("instrument_type with no GDP data"):
            assert header.instrument_type is None

        with subtests.test("firmware with no GDP data"):
            assert header.firmware is None


class TestHeaderPropertySetters:
    """Test property setters using __setattr__ override."""

    @pytest.fixture
    def fresh_header(self):
        """Fixture providing a fresh Header instance for each test."""
        return Header()

    def test_latitude_setter(self, fresh_header, subtests):
        """Test latitude setter functionality."""
        with subtests.test("set latitude as float"):
            fresh_header.latitude = 45.123
            assert fresh_header.latitude == 45.123
            assert fresh_header._gps_lat == 45.123

        with subtests.test("set latitude as string"):
            fresh_header.latitude = "46.789"
            assert fresh_header.latitude == 46.789
            assert fresh_header._gps_lat == 46.789

        with subtests.test("latitude updates GPS object"):
            fresh_header.latitude = 47.555
            assert fresh_header.gps.lat == 47.555

    def test_longitude_setter(self, fresh_header, subtests):
        """Test longitude setter functionality."""
        with subtests.test("set longitude as float"):
            fresh_header.longitude = -123.456
            assert fresh_header.longitude == -123.456
            assert fresh_header._gps_lon == -123.456

        with subtests.test("set longitude as string"):
            fresh_header.longitude = "-124.789"
            assert fresh_header.longitude == -124.789
            assert fresh_header._gps_lon == -124.789

        with subtests.test("longitude updates GPS object"):
            fresh_header.longitude = -125.555
            assert fresh_header.gps.lon == -125.555

    def test_elevation_setter(self, fresh_header, subtests):
        """Test elevation setter functionality."""
        with subtests.test("set elevation as float"):
            fresh_header.elevation = 1500.0
            assert fresh_header.elevation == 1500.0
            assert fresh_header._elevation == 1500.0

        with subtests.test("set elevation as string"):
            fresh_header.elevation = "2000.5"
            assert fresh_header.elevation == 2000.5
            assert fresh_header._elevation == 2000.5

    def test_station_setter(self, fresh_header, subtests):
        """Test station setter functionality."""
        with subtests.test("set station as string"):
            fresh_header.station = "TEST_STATION_01"
            assert fresh_header.station == "TEST_STATION_01"
            assert fresh_header.rx.gdp_stn == "TEST_STATION_01"

    def test_setter_validation_errors(self, fresh_header, subtests):
        """Test validation errors in setters."""
        with subtests.test("invalid latitude string"):
            with pytest.raises(ValueError, match="Invalid latitude"):
                fresh_header.latitude = "invalid_lat"

        with subtests.test("invalid longitude string"):
            with pytest.raises(ValueError, match="Invalid longitude"):
                fresh_header.longitude = "invalid_lon"

        with subtests.test("invalid elevation string"):
            with pytest.raises(ValueError, match="Invalid elevation"):
                fresh_header.elevation = "invalid_elev"


class TestHeaderCenterLocation:
    """Test center location functionality."""

    @pytest.fixture
    def header_with_channel(self):
        """Fixture providing Header with channel data."""
        header = Header()
        # Mock the _has_channel method and component data
        header._comp_dict = {"zxx": {"rx": Mock(), "ch": Mock()}}
        header._comp_dict["zxx"]["rx"].center = "123.456 : 789.012"
        return header

    def test_center_location_property(self, header_with_channel, subtests):
        """Test center_location computed property."""
        with subtests.test("center_location parsing"):
            expected = [123.456, 789.012]
            assert header_with_channel.center_location == expected

    def test_easting_property(self, header_with_channel, subtests):
        """Test easting computed property."""
        with subtests.test("easting from center_location"):
            assert header_with_channel.easting == 123.456

    def test_northing_property(self, header_with_channel, subtests):
        """Test northing from center_location."""
        with subtests.test("northing from center_location"):
            assert header_with_channel.northing == 789.012

    def test_center_location_with_no_data(self, subtests):
        """Test center_location properties with no channel data."""
        header = Header()

        with subtests.test("center_location with no data"):
            assert header.center_location is None

        with subtests.test("easting with no data"):
            assert header.easting is None

        with subtests.test("northing with no data"):
            assert header.northing is None

    def test_instrument_id_property(self, subtests):
        """Test instrument_id computed property."""
        header = Header()

        with subtests.test("instrument_id with no data"):
            assert header.instrument_id is None

        # Test with mocked channel data
        header._comp_dict = {"zxx": {"ch": Mock()}}
        header._comp_dict["zxx"]["ch"].gdp_box = ["GDP001", "extra"]

        with subtests.test("instrument_id with channel data"):
            assert header.instrument_id == "GDP001"


class TestHeaderFileOperations:
    """Test file reading and writing operations."""

    @pytest.fixture
    def sample_header_lines(self):
        """Fixture providing sample header lines for parsing."""
        return [
            "$Survey.Type=mt",
            "$Survey.Array=5",
            "$Tx.Type=grounded_dipole",
            "$MTEdit.Version=4.0",
            "$MTEdit:Auto.PhaseFlip=true",
            "$MTEdit:PhaseSlope.Smooth=parzen",
            "$MTEdit:PhaseSlope.ToZMag=false",
            "$MTEdit:DPlus.Use=true",
            "$Rx.GdpStn=TEST001",
            "$Rx.Length=100.0",
            "$Rx.HPR=0,90,0",
            "$GPS.Lat=45.123456",
            "$GPS.Lon=-123.456789",
            "$Unit.Length=m",
            "$Rx.Cmp=ex",
            "Data line 1",
            "Data line 2",
        ]

    @pytest.fixture
    def header_for_parsing(self):
        """Fixture providing Header instance for parsing tests."""
        return Header()

    def test_read_header_basic(self, header_for_parsing, sample_header_lines, subtests):
        """Test basic header reading functionality."""
        data_lines = header_for_parsing.read_header(sample_header_lines)

        with subtests.test("returns data lines"):
            assert len(data_lines) > 0
            assert "Data line 1" in data_lines
            assert "Data line 2" in data_lines

        with subtests.test("parses component data"):
            assert "$Rx.Cmp=ex" in data_lines

    def test_read_header_attribute_setting(
        self, header_for_parsing, sample_header_lines, subtests
    ):
        """Test that read_header properly sets attributes."""
        header_for_parsing.read_header(sample_header_lines)

        # Note: These tests depend on the set_attr_from_name method working
        # We'll test what we can verify directly
        with subtests.test("component dict populated"):
            assert len(header_for_parsing._comp_dict) > 0

    def test_write_header(self, subtests):
        """Test header writing functionality."""
        header = Header()

        # Set some values to write
        header.survey.type = "mt"
        header.tx.type = "grounded_dipole"
        header.rx.gdp_stn = "TEST001"

        lines = header.write_header()

        with subtests.test("returns lines list"):
            assert isinstance(lines, list)

        with subtests.test("lines contain header format"):
            # First line should be empty
            assert lines[0] == ""

        with subtests.test("lines contain dollar prefix"):
            # At least some lines should start with $
            dollar_lines = [line for line in lines if line.startswith("$")]
            assert len(dollar_lines) > 0

    def test_has_channel_method(self, subtests):
        """Test _has_channel helper method."""
        header = Header()

        with subtests.test("no channel data"):
            assert not header._has_channel("zxx")

        # Mock channel data
        header._comp_dict = {"zxx": {"ch": Mock()}}
        header._comp_dict["zxx"]["ch"].cmp = "zxx"

        with subtests.test("has channel data"):
            assert header._has_channel("zxx")

        # Test missing component
        header._comp_dict["zxx"]["ch"].cmp = None

        with subtests.test("component exists but cmp is None"):
            assert not header._has_channel("zxx")


class TestHeaderValidation:
    """Test field validation functionality."""

    def test_coordinate_validation(self, subtests):
        """Test coordinate field validation."""
        # Test the validator directly
        from mt_metadata.transfer_functions.io.zonge.metadata import Header

        with subtests.test("valid float coordinate"):
            result = Header.validate_coordinates(45.123)
            assert result == 45.123

        with subtests.test("valid string coordinate"):
            result = Header.validate_coordinates("45.123")
            assert result == 45.123

        with subtests.test("string with spaces"):
            result = Header.validate_coordinates("  45.123  ")
            assert result == 45.123

        with subtests.test("None coordinate"):
            result = Header.validate_coordinates(None)
            assert result == 0.0

        with subtests.test("invalid string coordinate"):
            with pytest.raises(ValueError, match="Cannot convert"):
                Header.validate_coordinates("not_a_number")


class TestHeaderSerialization:
    """Test serialization and model operations."""

    @pytest.fixture
    def populated_header(self):
        """Fixture providing Header with various data populated."""
        header = Header()
        header.name = "Test Station"
        header.elevation = 1500.0
        header.gps.lat = 45.123
        header.gps.lon = -123.456
        header.gps.datum = "WGS84"
        header.rx.gdp_stn = "STATION_01"
        header.survey.type = "mt"
        return header

    def test_model_dump(self, populated_header, subtests):
        """Test model serialization."""
        data = populated_header.model_dump()

        with subtests.test("serialization returns dict"):
            assert isinstance(data, dict)

        with subtests.test("contains basic fields"):
            assert "name" in data
            assert "elevation" in data

        with subtests.test("contains nested objects"):
            assert "gps" in data
            assert "rx" in data
            assert "survey" in data

        with subtests.test("excludes private fields"):
            assert "_gps_lat" not in data
            assert "_gps_lon" not in data
            assert "_comp_dict" not in data

    def test_model_dump_json(self, populated_header, subtests):
        """Test JSON serialization."""
        json_str = populated_header.model_dump_json()

        with subtests.test("returns valid JSON string"):
            assert isinstance(json_str, str)
            # Should be parseable as JSON
            data = json.loads(json_str)
            assert isinstance(data, dict)

    def test_model_validation(self, subtests):
        """Test model validation."""
        # Test creating with invalid data
        with subtests.test("creation with invalid elevation type"):
            # This should work due to field validation
            header = Header(elevation="1500.0")
            assert header.elevation == 1500.0

    def test_model_copy(self, populated_header, subtests):
        """Test model copying."""
        copied_header = populated_header.model_copy()

        with subtests.test("copy creates new instance"):
            assert copied_header is not populated_header

        with subtests.test("copy has same values"):
            assert copied_header.name == populated_header.name
            assert copied_header.elevation == populated_header.elevation
            assert copied_header.gps.lat == populated_header.gps.lat


class TestHeaderIntegration:
    """Integration tests combining multiple Header features."""

    def test_full_workflow(self, subtests):
        """Test a complete workflow with Header."""
        # Create header
        header = Header()

        with subtests.test("initial state"):
            assert header.name is None
            assert header.latitude == 0.0

        # Set data via properties
        header.latitude = 45.123
        header.longitude = -123.456
        header.elevation = 1500.0
        header.station = "TEST_STATION"
        header.name = "Integration Test Station"

        with subtests.test("property setters work"):
            assert header.latitude == 45.123
            assert header.longitude == -123.456
            assert header.elevation == 1500.0
            assert header.station == "TEST_STATION"
            assert header.name == "Integration Test Station"

        with subtests.test("underlying objects updated"):
            assert header.gps.lat == 45.123
            assert header.gps.lon == -123.456
            assert header.rx.gdp_stn == "TEST_STATION"

        # Test serialization
        data = header.model_dump()

        with subtests.test("serialization includes all data"):
            assert data["name"] == "Integration Test Station"
            assert data["elevation"] == 1500.0
            assert data["gps"]["lat"] == 45.123
            assert data["gps"]["lon"] == -123.456
            assert data["rx"]["gdp_stn"] == "TEST_STATION"

        # Test copying
        copied = header.model_copy()

        with subtests.test("copy preserves all data"):
            assert copied.name == header.name
            assert copied.latitude == header.latitude
            assert copied.longitude == header.longitude
            assert copied.station == header.station

    def test_complex_location_data(self, subtests):
        """Test complex location data scenarios."""
        header = Header()

        # Set up component data for center location
        header._comp_dict = {"zxx": {"rx": Mock(), "ch": Mock()}}
        header._comp_dict["zxx"]["rx"].center = "456789.123 : 5012345.678"
        header._comp_dict["zxx"]["ch"].cmp = "zxx"
        header._comp_dict["zxx"]["ch"].gdp_box = ["GDP001", "extra_data"]

        with subtests.test("center location parsing"):
            assert header.center_location == [456789.123, 5012345.678]

        with subtests.test("easting and northing"):
            assert header.easting == 456789.123
            assert header.northing == 5012345.678

        with subtests.test("instrument ID"):
            assert header.instrument_id == "GDP001"

        # Test both GPS and center location data
        header.gps.lat = 45.123
        header.gps.lon = -123.456

        with subtests.test("both coordinate systems available"):
            assert header.latitude == 45.123
            assert header.longitude == -123.456
            assert header.easting == 456789.123
            assert header.northing == 5012345.678


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
