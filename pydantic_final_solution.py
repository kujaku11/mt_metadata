"""
FINAL WORKING SOLUTION: Pydantic Property Patterns

This demonstrates the CORRECT way to replace @property decorators in Pydantic BaseModel.
Key insight: Field validators only work during construction, not assignment.
"""

from typing import Annotated, Optional, Union

from pydantic import BaseModel, computed_field, Field, field_validator


class HeaderBestPractice(BaseModel):
    """
    Best practice for replacing @property with Pydantic patterns.

    RULE 1: Use Optional fields with defaults to avoid required parameters
    RULE 2: Field validators only work during construction, not assignment
    RULE 3: Use computed_field for read-only properties
    RULE 4: Use methods or __setattr__ for complex setters
    """

    # Fields with Optional and defaults to avoid constructor issues
    name: Annotated[Optional[str], Field(default=None)]
    gps_lat: Annotated[Optional[float], Field(default=None)]
    gps_lon: Annotated[Optional[float], Field(default=None)]
    gps_datum: Annotated[Optional[str], Field(default=None)]
    gps_utm_zone: Annotated[Optional[str], Field(default=None)]
    elevation_m: Annotated[Optional[float], Field(default=None)]
    station_id: Annotated[Optional[str], Field(default=None)]

    # Field validators work during construction and model validation
    @field_validator("gps_lat", "gps_lon", "elevation_m", mode="before")
    @classmethod
    def convert_numeric_strings(cls, v):
        """Convert string numbers to float during construction."""
        if v is None or v == "":
            return None
        if isinstance(v, str):
            try:
                return float(v.strip())
            except ValueError:
                raise ValueError(f"Cannot convert '{v}' to float")
        return float(v)

    @field_validator("name", "gps_datum", "gps_utm_zone", "station_id", mode="before")
    @classmethod
    def clean_strings(cls, v):
        """Clean string fields during construction."""
        if v is None or v == "":
            return None
        return str(v).strip()

    # Computed fields for property-like read access
    @computed_field
    @property
    def latitude(self) -> Optional[float]:
        """Read-only property for latitude."""
        return self.gps_lat

    @computed_field
    @property
    def longitude(self) -> Optional[float]:
        """Read-only property for longitude."""
        return self.gps_lon

    @computed_field
    @property
    def elevation(self) -> Optional[float]:
        """Read-only property for elevation."""
        return self.elevation_m

    @computed_field
    @property
    def station(self) -> Optional[str]:
        """Read-only property for station."""
        return self.station_id

    @computed_field
    @property
    def datum(self) -> Optional[str]:
        """Read-only property for datum."""
        return self.gps_datum.upper() if self.gps_datum else None

    @computed_field
    @property
    def utm_zone(self) -> Optional[str]:
        """Read-only property for UTM zone."""
        return self.gps_utm_zone

    @computed_field
    @property
    def location_summary(self) -> str:
        """Computed property showing location info."""
        if self.gps_lat is not None and self.gps_lon is not None:
            elev_str = f" @ {self.elevation_m}m" if self.elevation_m else ""
            return f"{self.gps_lat:.4f}, {self.gps_lon:.4f}{elev_str}"
        return "No location set"

    # Methods for setting values with validation (replaces property setters)
    def set_latitude(self, value: Union[str, float, None]) -> None:
        """Set latitude with validation."""
        if value is None:
            self.gps_lat = None
            return

        if isinstance(value, str):
            try:
                value = float(value.strip())
            except ValueError:
                raise ValueError(f"Cannot convert latitude '{value}' to float")

        if not -90 <= value <= 90:
            raise ValueError(f"Latitude must be between -90 and 90, got {value}")

        self.gps_lat = float(value)

    def set_longitude(self, value: Union[str, float, None]) -> None:
        """Set longitude with validation."""
        if value is None:
            self.gps_lon = None
            return

        if isinstance(value, str):
            try:
                value = float(value.strip())
            except ValueError:
                raise ValueError(f"Cannot convert longitude '{value}' to float")

        if not -180 <= value <= 180:
            raise ValueError(f"Longitude must be between -180 and 180, got {value}")

        self.gps_lon = float(value)

    def set_elevation(self, value: Union[str, float, None]) -> None:
        """Set elevation with validation."""
        if value is None:
            self.elevation_m = None
            return

        if isinstance(value, str):
            try:
                value = float(value.strip())
            except ValueError:
                raise ValueError(f"Cannot convert elevation '{value}' to float")

        self.elevation_m = float(value)

    def set_station(self, value: Union[str, None]) -> None:
        """Set station with validation."""
        if value is None or value == "":
            self.station_id = None
        else:
            self.station_id = str(value).strip()

    def set_location(
        self,
        lat: Union[str, float, None],
        lon: Union[str, float, None],
        elev: Union[str, float, None] = None,
    ) -> None:
        """Set all location values at once."""
        self.set_latitude(lat)
        self.set_longitude(lon)
        if elev is not None:
            self.set_elevation(elev)


class LegacyHeaderComparison:
    """
    Traditional Python class with @property decorators for comparison.
    """

    def __init__(self):
        self._name = None
        self._gps_lat = None
        self._gps_lon = None
        self._elevation = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            self._name = None
        else:
            self._name = str(value).strip()

    @property
    def latitude(self):
        return self._gps_lat

    @latitude.setter
    def latitude(self, value):
        if value is None:
            self._gps_lat = None
        else:
            if isinstance(value, str):
                value = float(value)
            if not -90 <= value <= 90:
                raise ValueError(f"Invalid latitude: {value}")
            self._gps_lat = value


def demonstrate_conversion():
    """Demonstrate how to convert from @property to Pydantic patterns."""

    print("=== PYDANTIC PROPERTY CONVERSION DEMO ===\n")

    # 1. Create empty instance (no required parameters)
    header = HeaderBestPractice()
    print("1. Empty header:", header.model_dump())

    # 2. Set values using methods (replaces property setters)
    header.set_latitude("45.123")  # String input
    header.set_longitude(-123.456)  # Float input
    header.set_elevation("1500")  # String input
    header.set_station("TEST_01")
    header.name = "Test Station"  # Direct field assignment
    header.gps_datum = "WGS84"  # Direct field assignment

    print("2. After setting values:")
    print(f"   Name: {header.name}")
    print(f"   Location: {header.location_summary}")
    print(f"   Station: {header.station}")
    print(f"   Datum: {header.datum}")

    # 3. Access via computed properties (replaces property getters)
    print("3. Property-like access:")
    print(f"   Latitude: {header.latitude}")
    print(f"   Longitude: {header.longitude}")
    print(f"   Elevation: {header.elevation}")

    # 4. Create with constructor validation
    header2 = HeaderBestPractice(
        name="Station 2",
        gps_lat="46.5",  # String will be converted
        gps_lon="-122.3",  # String will be converted
        elevation_m=500.0,  # Float direct
        gps_datum="NAD83",
    )
    print("4. Constructor with validation:")
    print(f"   {header2.location_summary}")
    print(f"   Serialized: {header2.model_dump()}")

    # 5. Validation in action
    try:
        header.set_latitude("200")  # Invalid latitude
    except ValueError as e:
        print(f"5. Validation caught error: {e}")

    # 6. Compare with legacy approach
    print("\n=== LEGACY VS PYDANTIC COMPARISON ===")

    legacy = LegacyHeaderComparison()
    legacy.name = "Legacy Station"
    legacy.latitude = "45.0"

    pydantic = HeaderBestPractice()
    pydantic.name = "Pydantic Station"
    pydantic.set_latitude("45.0")

    print(f"Legacy latitude: {legacy.latitude}")
    print(f"Pydantic latitude: {pydantic.latitude}")
    print(f"Pydantic serialized: {pydantic.model_dump()}")


# Summary of conversion patterns
CONVERSION_GUIDE = """
=== PROPERTY TO PYDANTIC CONVERSION GUIDE ===

1. SIMPLE @property getter → computed_field
   OLD: @property def latitude(self): return self._lat
   NEW: @computed_field @property def latitude(self) -> float: return self.gps_lat

2. @property with setter → method + field
   OLD: @property def latitude(self): return self._lat
        @latitude.setter def latitude(self, v): self._lat = validate(v)
   NEW: gps_lat: Optional[float] = Field(default=None)
        def set_latitude(self, v): self.gps_lat = validate(v)

3. Constructor validation → field_validator
   OLD: def __init__(self, lat=None): self.latitude = lat  # calls setter
   NEW: gps_lat: Optional[float] = Field(default=None)
        @field_validator('gps_lat', mode='before')
        def validate_lat(cls, v): return validate(v)

4. Access patterns:
   OLD: obj.latitude = "45.0"  # calls setter
        print(obj.latitude)    # calls getter
   NEW: obj.set_latitude("45.0")  # method call
        print(obj.latitude)       # computed property

5. Serialization:
   OLD: Need custom __dict__ or to_dict() method
   NEW: obj.model_dump() automatically includes all fields

KEY PRINCIPLES:
- Use Optional fields with defaults to avoid constructor issues
- Field validators only work during construction
- Use computed_field for read-only property access
- Use methods for complex setter logic
- Direct field assignment works for simple cases
"""

if __name__ == "__main__":
    demonstrate_conversion()
    print(CONVERSION_GUIDE)
