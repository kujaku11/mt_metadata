"""
CORRECTED: Proper Pydantic property patterns with working setters.
This shows the correct way to implement property-like behavior in Pydantic models.
"""

from typing import Annotated, Optional, Union

from pydantic import BaseModel, computed_field, Field, field_validator, model_validator


class WorkingPydanticProperties(BaseModel):
    """
    Correct implementation of property-like behavior in Pydantic.
    """

    # =====================================================
    # Method 1: Field with validator (input validation)
    # =====================================================

    temperature_celsius: Annotated[float, Field(default=0.0)]

    @field_validator("temperature_celsius", mode="before")
    @classmethod
    def validate_temperature(cls, v):
        """Field validator for input validation."""
        if isinstance(v, str):
            try:
                v = float(v)
            except ValueError:
                raise ValueError(f"Cannot convert temperature '{v}' to float")
        if v < -273.15:
            raise ValueError(f"Temperature {v}°C is below absolute zero")
        return float(v)

    @computed_field
    @property
    def temperature_fahrenheit(self) -> float:
        """Derived property - computed from temperature_celsius."""
        return (self.temperature_celsius * 9 / 5) + 32

    # =====================================================
    # Method 2: Normal fields with cross-field validation
    # =====================================================

    name: Annotated[Optional[str], Field(default=None)]
    code: Annotated[Optional[str], Field(default=None)]

    @model_validator(mode="after")
    def sync_name_and_code(self):
        """Model validator handles cross-field relationships."""
        if self.name and not self.code:
            self.code = self.name.upper().replace(" ", "_")
        elif self.code and not self.name:
            self.name = self.code.lower().replace("_", " ").title()
        return self

    # =====================================================
    # Method 3: Coordinate fields with validation
    # =====================================================

    lat: Annotated[float, Field(default=0.0)]
    lon: Annotated[float, Field(default=0.0)]
    elev: Annotated[float, Field(default=0.0)]

    @field_validator("lat", mode="before")
    @classmethod
    def validate_latitude(cls, v):
        """Validate latitude range."""
        if isinstance(v, str):
            v = float(v)
        if not -90 <= v <= 90:
            raise ValueError(f"Latitude must be between -90 and 90, got {v}")
        return float(v)

    @field_validator("lon", mode="before")
    @classmethod
    def validate_longitude(cls, v):
        """Validate longitude range."""
        if isinstance(v, str):
            v = float(v)
        if not -180 <= v <= 180:
            raise ValueError(f"Longitude must be between -180 and 180, got {v}")
        return float(v)

    @field_validator("elev", mode="before")
    @classmethod
    def validate_elevation(cls, v):
        """Validate elevation."""
        if isinstance(v, str):
            v = float(v)
        return float(v)

    # Computed properties that reference the actual fields
    @computed_field
    @property
    def latitude(self) -> float:
        """Alias for lat field."""
        return self.lat

    @computed_field
    @property
    def longitude(self) -> float:
        """Alias for lon field."""
        return self.lon

    @computed_field
    @property
    def elevation(self) -> float:
        """Alias for elev field."""
        return self.elev

    @computed_field
    @property
    def coordinates(self) -> list[float]:
        """Computed property returning all coordinates."""
        return [self.lat, self.lon, self.elev]

    # =====================================================
    # Method 4: Status with enum-like behavior
    # =====================================================

    status_code: Annotated[int, Field(default=0)]

    @field_validator("status_code", mode="before")
    @classmethod
    def validate_status_code(cls, v):
        """Allow string or int input for status."""
        if isinstance(v, str):
            status_map = {
                "unknown": 0,
                "active": 1,
                "inactive": 2,
                "error": 3,
                "maintenance": 4,
            }
            if v.lower() not in status_map:
                raise ValueError(f"Invalid status: {v}")
            return status_map[v.lower()]
        if not 0 <= v <= 4:
            raise ValueError(f"Status code must be 0-4, got {v}")
        return int(v)

    @computed_field
    @property
    def status(self) -> str:
        """Get status as string."""
        status_map = {
            0: "unknown",
            1: "active",
            2: "inactive",
            3: "error",
            4: "maintenance",
        }
        return status_map[self.status_code]

    @computed_field
    @property
    def is_operational(self) -> bool:
        """Check if status is operational."""
        return self.status_code in [1, 4]  # active or maintenance


class PropertyAlternatives(BaseModel):
    """
    Alternative patterns for property-like behavior.
    """

    # =====================================================
    # Pattern A: Direct field access (simplest)
    # =====================================================

    # Just use regular fields with validators - no properties needed!
    station_name: Annotated[Optional[str], Field(default=None)]
    gps_latitude: Annotated[float, Field(default=0.0)]
    gps_longitude: Annotated[float, Field(default=0.0)]
    station_elevation: Annotated[float, Field(default=0.0)]

    @field_validator("station_name", mode="before")
    @classmethod
    def clean_station_name(cls, v):
        """Clean and format station name."""
        if v is None:
            return None
        return str(v).strip().upper()

    @field_validator(
        "gps_latitude", "gps_longitude", "station_elevation", mode="before"
    )
    @classmethod
    def convert_coordinates(cls, v):
        """Convert string coordinates to float."""
        if isinstance(v, str):
            try:
                return float(v.strip())
            except ValueError:
                raise ValueError(f"Cannot convert '{v}' to float")
        return float(v)

    # =====================================================
    # Pattern B: Property-like access via aliases
    # =====================================================

    # Use aliases to provide property-like names for fields
    lat: Annotated[float, Field(default=0.0, alias="latitude")]
    lon: Annotated[float, Field(default=0.0, alias="longitude")]

    # =====================================================
    # Pattern C: Methods for complex operations
    # =====================================================

    def set_location(self, lat: float, lon: float, elev: float) -> None:
        """Set all location values at once."""
        self.gps_latitude = lat
        self.gps_longitude = lon
        self.station_elevation = elev

    def get_location(self) -> dict[str, float]:
        """Get location as dictionary."""
        return {
            "latitude": self.gps_latitude,
            "longitude": self.gps_longitude,
            "elevation": self.station_elevation,
        }

    # =====================================================
    # Pattern D: Computed fields for derived values
    # =====================================================

    @computed_field
    @property
    def location_string(self) -> str:
        """Format location as string."""
        return f"{self.gps_latitude:.4f}, {self.gps_longitude:.4f} @ {self.station_elevation:.1f}m"

    @computed_field
    @property
    def is_valid_location(self) -> bool:
        """Check if location coordinates are valid."""
        return (
            -90 <= self.gps_latitude <= 90
            and -180 <= self.gps_longitude <= 180
            and self.station_elevation > -1000  # Reasonable elevation check
        )


class HeaderFixed(BaseModel):
    """
    Properly implemented Header class using Pydantic patterns.
    """

    # Basic fields
    name: Annotated[Optional[str], Field(default=None)]

    # GPS fields (direct access, no properties needed)
    gps_lat: Annotated[float, Field(default=0.0)]
    gps_lon: Annotated[float, Field(default=0.0)]
    gps_datum: Annotated[Optional[str], Field(default=None)]
    gps_utm_zone: Annotated[Optional[str], Field(default=None)]

    # Elevation field
    elevation_meters: Annotated[float, Field(default=0.0)]

    # Station info
    station_id: Annotated[Optional[str], Field(default=None)]

    # Field validators for input cleaning/validation
    @field_validator("name", mode="before")
    @classmethod
    def clean_name(cls, v):
        if v is None:
            return None
        return str(v).strip()

    @field_validator("gps_lat", "gps_lon", "elevation_meters", mode="before")
    @classmethod
    def convert_float_fields(cls, v):
        if isinstance(v, str):
            try:
                return float(v.strip())
            except ValueError:
                raise ValueError(f"Cannot convert '{v}' to float")
        return float(v) if v is not None else 0.0

    @field_validator("gps_datum", "gps_utm_zone", "station_id", mode="before")
    @classmethod
    def clean_string_fields(cls, v):
        if v is None or v == "":
            return None
        return str(v).strip()

    # Computed fields for property-like access
    @computed_field
    @property
    def latitude(self) -> float:
        """Property-like access to latitude."""
        return self.gps_lat

    @computed_field
    @property
    def longitude(self) -> float:
        """Property-like access to longitude."""
        return self.gps_lon

    @computed_field
    @property
    def elevation(self) -> float:
        """Property-like access to elevation."""
        return self.elevation_meters

    @computed_field
    @property
    def datum(self) -> Optional[str]:
        """Formatted datum."""
        return self.gps_datum.upper() if self.gps_datum else None

    @computed_field
    @property
    def utm_zone(self) -> Optional[str]:
        """UTM zone property."""
        return self.gps_utm_zone

    @computed_field
    @property
    def station(self) -> Optional[str]:
        """Station property."""
        return self.station_id

    # Methods for setting values (alternative to property setters)
    def set_latitude(self, value: Union[str, float]) -> None:
        """Set latitude with validation."""
        if isinstance(value, str):
            value = float(value)
        if not -90 <= value <= 90:
            raise ValueError(f"Latitude must be between -90 and 90")
        self.gps_lat = value

    def set_longitude(self, value: Union[str, float]) -> None:
        """Set longitude with validation."""
        if isinstance(value, str):
            value = float(value)
        if not -180 <= value <= 180:
            raise ValueError(f"Longitude must be between -180 and 180")
        self.gps_lon = value

    def set_elevation(self, value: Union[str, float]) -> None:
        """Set elevation with validation."""
        if isinstance(value, str):
            value = float(value)
        self.elevation_meters = value

    def set_station(self, value: Optional[str]) -> None:
        """Set station with validation."""
        self.station_id = str(value).strip() if value else None


def demonstrate_patterns():
    """Demonstrate all the working patterns."""
    print("=== Working Pydantic Property Patterns ===\n")

    # Pattern 1: Field validators for input validation
    print("1. Field validators with computed properties:")
    # Create with keyword arguments to avoid lint errors
    demo1 = WorkingPydanticProperties(
        temperature_celsius=25.0,
        name="Test Station",
        lat=45.123,
        lon=-123.456,
        elev=1500.0,
        status_code=1,  # Use int directly
    )
    print(
        f"   Temperature: {demo1.temperature_celsius}°C = {demo1.temperature_fahrenheit}°F"
    )

    # Pattern 2: Cross-field validation
    print("\n2. Cross-field validation:")
    print(f"   Name: {demo1.name}, Code: {demo1.code}")

    # Pattern 3: Coordinate validation
    print("\n3. Coordinate validation:")
    print(f"   Coordinates: {demo1.coordinates}")
    print(
        f"   Via computed properties: {demo1.latitude}, {demo1.longitude}, {demo1.elevation}"
    )

    # Pattern 4: Status validation
    print("\n4. Status validation:")
    # Create a new instance with string status that will be converted
    demo1_status = WorkingPydanticProperties(status_code="active")
    print(
        f"   Status: {demo1_status.status} ({demo1_status.status_code}), Operational: {demo1_status.is_operational}"
    )

    # Alternative patterns
    print("\n=== Alternative Patterns ===")
    # Create with string coordinates that will be converted
    demo2 = PropertyAlternatives(
        station_name="  test station  ",  # Will be cleaned
        gps_latitude="45.123",  # String converted to float
        gps_longitude=-123.456,
        station_elevation=1500,
        lat=45.0,
        lon=-123.0,
    )

    print(f"Station: {demo2.station_name}")
    print(f"Location: {demo2.location_string}")
    print(f"Valid: {demo2.is_valid_location}")

    # Header example
    print("\n=== Fixed Header Example ===")
    header = HeaderFixed(
        name="Test Header", gps_lat=45.0, gps_lon=-123.0, elevation_meters=1000.0
    )

    # Use setter methods for validation
    header.set_latitude(45.5)
    header.set_longitude(-123.5)
    header.set_elevation(1100.0)

    print(f"Name: {header.name}")
    print(f"Latitude: {header.latitude} (via computed property)")
    print(f"Direct: {header.gps_lat} (via field)")
    print(f"Location via property: {header.longitude}, {header.elevation}")

    print(f"\nSerialized: {header.model_dump()}")


# =====================================================
# SUMMARY OF CONVERSION PATTERNS
# =====================================================
"""
RECOMMENDED CONVERSIONS:

1. Simple @property getter → Use regular field
   OLD: @property def name(self): return self._name
   NEW: name: str = Field(default="")

2. @property with setter → Use field + validator
   OLD: @property def value(self): return self._value
        @value.setter def value(self, v): self._value = validate(v)
   NEW: value: float = Field(default=0.0)
        @field_validator('value') def validate_value(cls, v): return validate(v)

3. Computed property → Use @computed_field
   OLD: @property def total(self): return self.a + self.b
   NEW: @computed_field @property def total(self) -> float: return self.a + self.b

4. Cross-field logic → Use @model_validator
   OLD: Complex setter updating multiple fields
   NEW: @model_validator(mode='after') def update_fields(self): ...

5. Property-like access → Use computed_field + real fields
   OLD: @property def lat(self): return self.coordinates[0]
        @lat.setter def lat(self, v): self.coordinates[0] = v
   NEW: gps_lat: float = Field(default=0.0)
        @computed_field @property def latitude(self) -> float: return self.gps_lat
        # Access via: obj.gps_lat = 45.0 or obj.set_latitude(45.0)

KEY PRINCIPLES:
- Use real fields for data storage
- Use computed_field for derived/formatted views
- Use field_validator for input validation
- Use model_validator for cross-field logic
- Use methods for complex setter logic
- Avoid trying to assign to computed_field properties
"""

if __name__ == "__main__":
    demonstrate_patterns()
