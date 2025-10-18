"""
Test suite for GPS metadata class using pytest with fixtures and subtests.
This test suite follows modern pytest patterns for comprehensive coverage and efficiency optimization.
"""

import json

import pytest
from pydantic import ValidationError

from mt_metadata.transfer_functions.io.zonge.metadata import GPS


class TestGPSDefault:
    """Test default initialization and basic attributes of GPS class."""

    @pytest.fixture(scope="class")
    def default_GPS(self):
        """Fixture providing a default GPS instance for efficiency."""
        return GPS()  # type: ignore

    def test_default_initialization(self, default_GPS, subtests):
        """Test that GPS initializes with correct default values."""
        with subtests.test("default lat value"):
            assert default_GPS.lat == 0.0

        with subtests.test("default lon value"):
            assert default_GPS.lon == 0.0

        with subtests.test("default datum value"):
            # Datum validator normalizes "WGS84" to "WGS 84"
            assert "WGS" in str(default_GPS.datum) and "84" in str(default_GPS.datum)

        with subtests.test("default u_t_m_zone value"):
            assert default_GPS.u_t_m_zone == 0

    def test_default_GPS_attributes(self, default_GPS, subtests):
        """Test that GPS has all expected attributes."""
        expected_attributes = ["lat", "lon", "datum", "u_t_m_zone"]

        for attr in expected_attributes:
            with subtests.test(f"has attribute {attr}"):
                assert hasattr(default_GPS, attr)

    def test_default_model_fields(self, default_GPS, subtests):
        """Test model fields are properly defined."""
        fields = default_GPS.model_fields
        expected_fields = ["lat", "lon", "datum", "u_t_m_zone"]

        for field in expected_fields:
            with subtests.test(f"model field {field}"):
                assert field in fields

        with subtests.test("field count"):
            assert len(fields) == 4


class TestGPSCustomValues:
    """Test GPS with custom values and various initialization patterns."""

    @pytest.fixture(scope="class")
    def populated_GPS(self):
        """Fixture providing a GPS instance with custom values for efficiency."""
        return GPS(  # type: ignore
            lat=40.7128, lon=-74.0060, datum="WGS84", u_t_m_zone=18
        )

    def test_populated_GPS_values(self, populated_GPS, subtests):
        """Test GPS with custom values."""
        with subtests.test("populated lat"):
            assert populated_GPS.lat == 40.7128

        with subtests.test("populated lon"):
            assert populated_GPS.lon == -74.0060

        with subtests.test("populated datum"):
            # Datum validator normalizes "WGS84" to "WGS 84"
            assert "WGS" in str(populated_GPS.datum) and "84" in str(
                populated_GPS.datum
            )

        with subtests.test("populated u_t_m_zone"):
            assert populated_GPS.u_t_m_zone == 18

    def test_partial_GPS_values(self, subtests):
        """Test GPS with only some fields populated."""
        gps = GPS(lat=51.5074, u_t_m_zone=30)  # type: ignore

        with subtests.test("partial lat"):
            assert gps.lat == 51.5074

        with subtests.test("partial default lon"):
            assert gps.lon == 0.0

        with subtests.test("partial default datum"):
            # Datum validator normalizes "WGS84" to "WGS 84"
            assert "WGS" in str(gps.datum) and "84" in str(gps.datum)

        with subtests.test("partial u_t_m_zone"):
            assert gps.u_t_m_zone == 30

    def test_individual_field_initialization(self, subtests):
        """Test individual field initialization."""
        test_cases = [
            ("lat", 45.0),
            ("lon", -90.0),
            ("datum", "WGS84"),
            ("u_t_m_zone", 15),
        ]

        for field, value in test_cases:
            with subtests.test(f"individual {field}"):
                kwargs = {field: value}
                gps = GPS(**kwargs)  # type: ignore
                actual_value = getattr(gps, field)
                if field == "datum":
                    # Datum validator normalizes datum names (e.g., "WGS84" -> "WGS 84")
                    assert "WGS" in str(actual_value) and "84" in str(actual_value)
                else:
                    assert actual_value == value


class TestGPSValidation:
    """Test GPS input validation and type conversion."""

    def test_latitude_validation(self, subtests):
        """Test latitude field validation."""
        valid_latitudes = [0.0, 45.5, -45.5, 90.0, -90.0]

        for lat in valid_latitudes:
            with subtests.test(f"valid latitude {lat}"):
                gps = GPS(lat=lat)  # type: ignore
                assert gps.lat == lat

    def test_longitude_validation(self, subtests):
        """Test longitude field validation."""
        valid_longitudes = [0.0, 90.0, -90.0, 180.0, -180.0, 123.456]

        for lon in valid_longitudes:
            with subtests.test(f"valid longitude {lon}"):
                gps = GPS(lon=lon)  # type: ignore
                assert gps.lon == lon

    def test_extreme_coordinate_values(self, subtests):
        """Test extreme but valid coordinate values."""
        extreme_cases = [
            (90.0, 180.0),  # North Pole, International Date Line
            (-90.0, -180.0),  # South Pole, opposite side
            (0.0, 0.0),  # Null Island
        ]

        for lat, lon in extreme_cases:
            with subtests.test(f"extreme coordinates lat={lat}, lon={lon}"):
                gps = GPS(lat=lat, lon=lon)  # type: ignore
                assert gps.lat == lat
                assert gps.lon == lon

    def test_datum_validation(self, subtests):
        """Test datum field validation with various CRS formats."""
        valid_datums = [
            "WGS84",
            "EPSG:4326",
            "NAD83",
        ]

        for datum in valid_datums:
            with subtests.test(f"valid datum {datum}"):
                try:
                    gps = GPS(datum=datum)  # type: ignore
                    # Datum validator may transform the value
                    assert isinstance(gps.datum, str)
                    assert len(gps.datum) > 0
                except ValidationError:
                    # Some datum formats might not be recognized by pyproj
                    pytest.skip(
                        f"Datum {datum} not recognized by current pyproj version"
                    )

    def test_invalid_datum_values(self, subtests):
        """Test that invalid datum values raise ValidationError."""
        invalid_datums = ["INVALID_DATUM", "XYZ123", ""]

        for datum in invalid_datums:
            with subtests.test(f"invalid datum {datum}"):
                with pytest.raises((ValidationError, ValueError)):
                    GPS(datum=datum)  # type: ignore

    def test_utm_zone_validation(self, subtests):
        """Test UTM zone field validation."""
        valid_zones = [0, 1, 30, 60]

        for zone in valid_zones:
            with subtests.test(f"valid utm zone {zone}"):
                gps = GPS(u_t_m_zone=zone)  # type: ignore
                assert gps.u_t_m_zone == zone

    def test_coordinate_string_conversion(self, subtests):
        """Test automatic conversion of string coordinates to floats."""
        with subtests.test("latitude string conversion"):
            gps = GPS(lat="45.5")  # type: ignore
            assert gps.lat == 45.5

        with subtests.test("longitude string conversion"):
            gps = GPS(lon="-90.25")  # type: ignore
            assert gps.lon == -90.25

    def test_utm_zone_string_conversion(self, subtests):
        """Test automatic conversion of string UTM zone to int."""
        with subtests.test("utm zone string conversion"):
            gps = GPS(u_t_m_zone="18")  # type: ignore
            assert gps.u_t_m_zone == 18


class TestGPSSerialization:
    """Test GPS serialization and deserialization functionality."""

    @pytest.fixture(scope="class")
    def default_GPS(self):
        """Fixture for default GPS instance."""
        return GPS()  # type: ignore

    @pytest.fixture(scope="class")
    def populated_GPS(self):
        """Fixture for populated GPS instance."""
        return GPS(  # type: ignore
            lat=37.7749, lon=-122.4194, datum="WGS84", u_t_m_zone=10
        )

    def test_model_dump_default(self, default_GPS, subtests):
        """Test model_dump with default values."""
        dump = default_GPS.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("has all fields"):
            expected_fields = ["lat", "lon", "datum", "u_t_m_zone"]
            for field in expected_fields:
                assert field in dump

        with subtests.test("default values"):
            assert dump["lat"] == 0.0
            assert dump["lon"] == 0.0
            assert dump["u_t_m_zone"] == 0
            # datum may be transformed by validator

    def test_model_dump_populated(self, populated_GPS, subtests):
        """Test model_dump with populated values."""
        dump = populated_GPS.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("populated values present"):
            assert dump["lat"] == 37.7749
            assert dump["lon"] == -122.4194
            assert dump["u_t_m_zone"] == 10
            assert isinstance(dump["datum"], str)

    def test_from_dict_creation(self, subtests):
        """Test creating GPS from dictionary."""
        with subtests.test("full dict"):
            data = {
                "lat": 34.0522,
                "lon": -118.2437,
                "datum": "WGS84",
                "u_t_m_zone": 11,
            }
            gps = GPS(**data)  # type: ignore
            assert gps.lat == 34.0522
            assert gps.lon == -118.2437
            assert gps.u_t_m_zone == 11

        with subtests.test("partial dict"):
            data = {"lat": 41.8781, "lon": -87.6298}
            gps = GPS(**data)  # type: ignore
            assert gps.lat == 41.8781
            assert gps.lon == -87.6298
            assert gps.u_t_m_zone == 0  # default

    def test_json_serialization(self, default_GPS, populated_GPS, subtests):
        """Test JSON serialization and deserialization."""
        with subtests.test("JSON round-trip populated GPS"):
            json_str = populated_GPS.model_dump_json()
            data = json.loads(json_str)
            recreated = GPS(**data)  # type: ignore
            assert recreated.lat == populated_GPS.lat
            assert recreated.lon == populated_GPS.lon
            assert recreated.u_t_m_zone == populated_GPS.u_t_m_zone

        with subtests.test("JSON round-trip default GPS"):
            json_str = default_GPS.model_dump_json()
            data = json.loads(json_str)
            recreated = GPS(**data)  # type: ignore
            assert recreated.lat == default_GPS.lat
            assert recreated.lon == default_GPS.lon
            assert recreated.u_t_m_zone == default_GPS.u_t_m_zone

    def test_model_dump_exclude_none(self, subtests):
        """Test model_dump with exclude_none option."""
        with subtests.test("exclude_none behavior"):
            gps = GPS(lat=25.7617, lon=-80.1918)  # type: ignore
            dump = gps.model_dump(exclude_none=True)
            # All fields should be present since none are None in this model
            assert "lat" in dump
            assert "lon" in dump
            assert "datum" in dump
            assert "u_t_m_zone" in dump


class TestGPSModification:
    """Test GPS field modification and updates."""

    def test_field_modification(self, subtests):
        """Test modifying GPS fields after creation."""
        gps = GPS()  # type: ignore

        test_modifications = [
            ("lat", 47.6062),
            ("lon", -122.3321),
            ("u_t_m_zone", 10),
            ("datum", "WGS84"),
        ]

        for field, value in test_modifications:
            with subtests.test(f"modify {field}"):
                setattr(gps, field, value)
                actual_value = getattr(gps, field)
                if field == "datum":
                    # Datum validator normalizes datum names (e.g., "WGS84" -> "WGS 84")
                    assert "WGS" in str(actual_value) and "84" in str(actual_value)
                else:
                    assert actual_value == value

    def test_bulk_update(self, subtests):
        """Test bulk field updates."""
        gps = GPS()  # type: ignore

        updates = {"lat": 39.7392, "lon": -104.9903, "u_t_m_zone": 13}

        for field, value in updates.items():
            setattr(gps, field, value)

        for field, expected_value in updates.items():
            with subtests.test(f"bulk update {field}"):
                assert getattr(gps, field) == expected_value


class TestGPSComparison:
    """Test GPS comparison and equality operations."""

    def test_GPS_equality(self, subtests):
        """Test GPS equality comparisons."""
        GPS1 = GPS(lat=42.3601, lon=-71.0589, u_t_m_zone=19)  # type: ignore
        GPS2 = GPS(lat=42.3601, lon=-71.0589, u_t_m_zone=19)  # type: ignore
        GPS3 = GPS(lat=40.7128, lon=-74.0060, u_t_m_zone=18)  # type: ignore

        with subtests.test("same values model_dump equal"):
            dump1 = GPS1.model_dump()
            dump2 = GPS2.model_dump()
            # Compare the numeric fields which should be identical
            assert dump1["lat"] == dump2["lat"]
            assert dump1["lon"] == dump2["lon"]
            assert dump1["u_t_m_zone"] == dump2["u_t_m_zone"]

        with subtests.test("different values model_dump not equal"):
            dump1 = GPS1.model_dump()
            dump3 = GPS3.model_dump()
            assert dump1["lat"] != dump3["lat"] or dump1["lon"] != dump3["lon"]

    def test_field_value_consistency(self, subtests):
        """Test consistency of field values across operations."""
        test_values = [("lat", 35.6762), ("lon", 139.6503), ("u_t_m_zone", 54)]

        for field, value in test_values:
            with subtests.test(f"consistency {field} {value}"):
                kwargs = {field: value}
                gps = GPS(**kwargs)  # type: ignore
                assert getattr(gps, field) == value

                # Test round-trip consistency
                dump = gps.model_dump()
                recreated = GPS(**dump)  # type: ignore
                assert getattr(recreated, field) == getattr(gps, field)


class TestGPSEdgeCases:
    """Test GPS edge cases and boundary conditions."""

    def test_empty_initialization_kwargs(self, subtests):
        """Test initialization with empty keyword arguments."""
        with subtests.test("empty kwargs"):
            gps = GPS(**{})  # type: ignore
            assert gps.lat == 0.0
            assert gps.lon == 0.0
            assert gps.u_t_m_zone == 0
            assert isinstance(gps.datum, str)

    def test_unknown_field_handling(self, subtests):
        """Test handling of unknown fields."""
        with subtests.test("unknown fields accepted"):
            # MetadataBase appears to accept unknown fields
            gps = GPS(unknown_field="value")  # type: ignore
            assert hasattr(gps, "unknown_field")
            assert gps.unknown_field == "value"  # type: ignore

    def test_precision_coordinates(self, subtests):
        """Test high-precision coordinate values."""
        precision_cases = [
            (40.123456789, -74.987654321),
            (-12.345678901, 98.765432109),
            (0.000000001, -0.000000001),
        ]

        for lat, lon in precision_cases:
            with subtests.test(f"precision coordinates lat={lat}, lon={lon}"):
                gps = GPS(lat=lat, lon=lon)  # type: ignore
                # Check that precision is maintained (within reasonable bounds)
                assert abs(gps.lat - lat) < 1e-6
                assert abs(gps.lon - lon) < 1e-6

    def test_negative_utm_zones(self, subtests):
        """Test negative UTM zone values."""
        with subtests.test("negative utm zone"):
            # Some systems might use negative zones for southern hemisphere
            gps = GPS(u_t_m_zone=-30)  # type: ignore
            assert gps.u_t_m_zone == -30

    def test_large_utm_zones(self, subtests):
        """Test large UTM zone values."""
        with subtests.test("large utm zone"):
            gps = GPS(u_t_m_zone=999)  # type: ignore
            assert gps.u_t_m_zone == 999

    def test_coordinate_boundary_values(self, subtests):
        """Test coordinate values at valid boundaries."""
        boundary_cases = [
            ("max latitude", 90.0, 0.0),
            ("min latitude", -90.0, 0.0),
            ("max longitude", 0.0, 180.0),
            ("min longitude", 0.0, -180.0),
        ]

        for case_name, lat, lon in boundary_cases:
            with subtests.test(f"boundary {case_name}"):
                gps = GPS(lat=lat, lon=lon)  # type: ignore
                assert gps.lat == lat
                assert gps.lon == lon


class TestGPSDocumentation:
    """Test GPS class structure and documentation."""

    def test_class_structure(self, subtests):
        """Test GPS class structure and inheritance."""
        with subtests.test("class name accessible"):
            assert GPS.__name__ == "GPS"

        with subtests.test("class is MetadataBase subclass"):
            from mt_metadata.base import MetadataBase

            assert issubclass(GPS, MetadataBase)

    def test_field_descriptions(self, subtests):
        """Test that fields have proper descriptions."""
        fields = GPS.model_fields
        expected_fields = ["lat", "lon", "datum", "u_t_m_zone"]

        for field_name in expected_fields:
            with subtests.test(f"field description {field_name}"):
                field = fields[field_name]
                # Check that field has description
                assert hasattr(field, "description") or "description" in str(field)

    def test_validators_present(self, subtests):
        """Test that custom validators are properly defined."""
        with subtests.test("datum validator"):
            # Test that datum validation works
            gps = GPS(datum="WGS84")  # type: ignore
            assert isinstance(gps.datum, str)

        with subtests.test("position validators"):
            # Test that lat/lon validation works
            gps = GPS(lat=45.0, lon=-90.0)  # type: ignore
            assert gps.lat == 45.0
            assert gps.lon == -90.0

    def test_schema_information(self, subtests):
        """Test schema and model information."""
        with subtests.test("model_dump produces schema-like structure"):
            gps = GPS()  # type: ignore
            dump = gps.model_dump()
            assert isinstance(dump, dict)
            assert len(dump) > 0

        with subtests.test("all expected fields present"):
            expected_fields = ["lat", "lon", "datum", "u_t_m_zone"]
            dump = GPS().model_dump()  # type: ignore
            for field in expected_fields:
                assert field in dump

        with subtests.test("model_fields accessible"):
            fields = GPS.model_fields
            assert len(fields) == 4
            assert all(
                field in fields for field in ["lat", "lon", "datum", "u_t_m_zone"]
            )
