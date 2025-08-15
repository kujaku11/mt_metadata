"""
Comprehensive guide for replacing @property with Pydantic validators.
This demonstrates the best practices for implementing property-like behavior in Pydantic models.
"""

import json
from typing import Annotated, Any, Optional, Union

from pydantic import BaseModel, computed_field, Field, field_validator, model_validator


class PydanticPropertyDemo(BaseModel):
    """
    Demonstrates various Pydantic patterns to replace @property decorators.
    """

    # =====================================================
    # Pattern 1: Simple field with validation (replaces basic @property with setter)
    # =====================================================

    _temperature_celsius: Annotated[float, Field(default=0.0, exclude=True)]

    @field_validator("_temperature_celsius", mode="before")
    @classmethod
    def validate_temperature(cls, v):
        """Field validator acts as input validation (like a setter)."""
        if isinstance(v, str):
            try:
                v = float(v)
            except ValueError:
                raise ValueError(f"Cannot convert temperature '{v}' to float")
        if v < -273.15:  # Absolute zero check
            raise ValueError(f"Temperature {v}°C is below absolute zero")
        return float(v)

    @computed_field
    @property
    def temperature_celsius(self) -> float:
        """Computed field acts as a getter."""
        return self._temperature_celsius

    @computed_field
    @property
    def temperature_fahrenheit(self) -> float:
        """Derived property - computed from other fields."""
        return (self._temperature_celsius * 9 / 5) + 32

    # =====================================================
    # Pattern 2: Cross-field validation and updates
    # =====================================================

    name: Annotated[Optional[str], Field(default=None)]
    code: Annotated[Optional[str], Field(default=None)]

    @model_validator(mode="after")
    def sync_name_and_code(self):
        """Model validator handles cross-field relationships."""
        # If name is set but code isn't, generate code from name
        if self.name and not self.code:
            self.code = self.name.upper().replace(" ", "_")
        # If code is set but name isn't, generate name from code
        elif self.code and not self.name:
            self.name = self.code.lower().replace("_", " ").title()
        return self

    # =====================================================
    # Pattern 3: Complex property with custom setter via __setattr__
    # =====================================================

    _coordinates: Annotated[
        list[float], Field(default_factory=lambda: [0.0, 0.0, 0.0], exclude=True)
    ]

    @computed_field
    @property
    def latitude(self) -> float:
        """Latitude from coordinates."""
        return self._coordinates[0]

    @computed_field
    @property
    def longitude(self) -> float:
        """Longitude from coordinates."""
        return self._coordinates[1]

    @computed_field
    @property
    def elevation(self) -> float:
        """Elevation from coordinates."""
        return self._coordinates[2]

    def __setattr__(self, name: str, value: Any) -> None:
        """Custom setters for computed properties."""

        if name == "temperature_celsius":
            # Validate and set temperature
            if isinstance(value, str):
                try:
                    value = float(value)
                except ValueError:
                    raise ValueError(f"Cannot convert temperature '{value}' to float")
            if value < -273.15:
                raise ValueError(f"Temperature {value}°C is below absolute zero")
            super().__setattr__("_temperature_celsius", float(value))
            return

        if name == "latitude":
            coords = getattr(self, "_coordinates", [0.0, 0.0, 0.0])
            coords[0] = float(value)
            super().__setattr__("_coordinates", coords)
            return

        if name == "longitude":
            coords = getattr(self, "_coordinates", [0.0, 0.0, 0.0])
            coords[1] = float(value)
            super().__setattr__("_coordinates", coords)
            return

        if name == "elevation":
            coords = getattr(self, "_coordinates", [0.0, 0.0, 0.0])
            coords[2] = float(value)
            super().__setattr__("_coordinates", coords)
            return

        # Default behavior
        super().__setattr__(name, value)

    # =====================================================
    # Pattern 4: Explicit getter/setter methods (alternative approach)
    # =====================================================

    def set_coordinates(self, lat: float, lon: float, elev: float) -> None:
        """Explicit setter method."""
        self._coordinates = [float(lat), float(lon), float(elev)]

    def get_coordinates(self) -> list[float]:
        """Explicit getter method."""
        return self._coordinates.copy()

    # =====================================================
    # Pattern 5: Property with complex logic
    # =====================================================

    _status_code: Annotated[int, Field(default=0, exclude=True)]

    @computed_field
    @property
    def status(self) -> str:
        """Complex computed property with logic."""
        status_map = {
            0: "unknown",
            1: "active",
            2: "inactive",
            3: "error",
            4: "maintenance",
        }
        return status_map.get(self._status_code, "invalid")

    @computed_field
    @property
    def is_operational(self) -> bool:
        """Boolean computed property."""
        return self._status_code in [1, 4]  # active or maintenance

    def set_status(self, status: Union[str, int]) -> None:
        """Method to set status with validation."""
        if isinstance(status, str):
            status_map = {
                "unknown": 0,
                "active": 1,
                "inactive": 2,
                "error": 3,
                "maintenance": 4,
            }
            if status.lower() not in status_map:
                raise ValueError(f"Invalid status: {status}")
            self._status_code = status_map[status.lower()]
        elif isinstance(status, int):
            if status not in range(5):
                raise ValueError(f"Invalid status code: {status}")
            self._status_code = status
        else:
            raise ValueError(f"Status must be str or int, got {type(status)}")


class HeaderExample(BaseModel):
    """
    Example showing how to refactor the Header class properties.
    """

    # Basic fields
    name: Annotated[Optional[str], Field(default=None)]

    # Nested objects (assuming these exist)
    gps_lat: Annotated[float, Field(default=0.0)]
    gps_lon: Annotated[float, Field(default=0.0)]
    gps_datum: Annotated[Optional[str], Field(default=None)]

    elevation_value: Annotated[float, Field(default=0.0)]

    # Private fields for complex data
    _comp_dict: Annotated[dict, Field(default_factory=dict, exclude=True)]

    # =====================================================
    # Computed properties (replacing @property getters)
    # =====================================================

    @computed_field
    @property
    def latitude(self) -> float:
        """Get latitude (replaces @property def latitude)."""
        return self.gps_lat

    @computed_field
    @property
    def longitude(self) -> float:
        """Get longitude (replaces @property def longitude)."""
        return self.gps_lon

    @computed_field
    @property
    def elevation(self) -> float:
        """Get elevation (replaces @property def elevation)."""
        return self.elevation_value

    @computed_field
    @property
    def datum(self) -> Optional[str]:
        """Get datum (replaces @property def datum)."""
        return self.gps_datum.upper() if self.gps_datum else None

    # =====================================================
    # Custom setters (replacing @property.setter)
    # =====================================================

    def __setattr__(self, name: str, value: Any) -> None:
        """Custom setters (replaces @latitude.setter, etc.)."""

        if name == "latitude":
            if isinstance(value, str):
                try:
                    value = float(value)
                except ValueError:
                    raise ValueError(f"Invalid latitude: {value}")
            if not -90 <= value <= 90:
                raise ValueError(f"Latitude must be between -90 and 90, got {value}")
            super().__setattr__("gps_lat", float(value))
            return

        if name == "longitude":
            if isinstance(value, str):
                try:
                    value = float(value)
                except ValueError:
                    raise ValueError(f"Invalid longitude: {value}")
            if not -180 <= value <= 180:
                raise ValueError(f"Longitude must be between -180 and 180, got {value}")
            super().__setattr__("gps_lon", float(value))
            return

        if name == "elevation":
            if isinstance(value, str):
                try:
                    value = float(value)
                except ValueError:
                    raise ValueError(f"Invalid elevation: {value}")
            super().__setattr__("elevation_value", float(value))
            return

        # Default behavior
        super().__setattr__(name, value)


def demo_usage():
    """Demonstrate the usage of Pydantic property patterns."""

    print("=== Pydantic Property Patterns Demo ===\n")

    # Create instance
    demo = PydanticPropertyDemo()

    # Pattern 1: Temperature with validation
    print("1. Temperature with validation:")
    demo.temperature_celsius = 25.0
    print(f"   Celsius: {demo.temperature_celsius}°C")
    print(f"   Fahrenheit: {demo.temperature_fahrenheit}°F")

    try:
        demo.temperature_celsius = "-300"  # Should raise error
    except ValueError as e:
        print(f"   Validation error: {e}")

    # Pattern 2: Cross-field validation
    print("\n2. Cross-field validation:")
    demo.name = "Test Station"
    print(f"   Name: {demo.name}")
    print(f"   Auto-generated code: {demo.code}")

    # Pattern 3: Coordinates with custom setters
    print("\n3. Coordinates with custom setters:")
    demo.latitude = 45.123
    demo.longitude = -123.456
    demo.elevation = 1500.0
    print(f"   Latitude: {demo.latitude}")
    print(f"   Longitude: {demo.longitude}")
    print(f"   Elevation: {demo.elevation}")
    print(f"   All coordinates: {demo.get_coordinates()}")

    # Pattern 4: Status with logic
    print("\n4. Status with complex logic:")
    demo.set_status("active")
    print(f"   Status: {demo.status}")
    print(f"   Is operational: {demo.is_operational}")

    demo.set_status(3)  # error code
    print(f"   Status: {demo.status}")
    print(f"   Is operational: {demo.is_operational}")

    # Serialization
    print("\n5. Serialization:")
    data = demo.model_dump()
    print(f"   Serialized: {json.dumps(data, indent=2)}")

    # Header example
    print("\n=== Header Example ===")
    header = HeaderExample()
    header.latitude = 45.0
    header.longitude = -123.0
    header.elevation = 1000.0

    print(f"Latitude: {header.latitude}")
    print(f"Longitude: {header.longitude}")
    print(f"Elevation: {header.elevation}")
    print(f"Datum: {header.datum}")

    print(f"Serialized: {header.model_dump()}")


# Key takeaways for converting @property to Pydantic:
"""
CONVERSION PATTERNS:

1. Simple @property getter:
   OLD: @property def field(self): return self._field
   NEW: @computed_field @property def field(self) -> Type: return self._field

2. @property with setter:
   OLD: @property def field(self): return self._field
        @field.setter def field(self, value): self._field = value
   NEW: - Use @computed_field @property for getter
        - Use __setattr__ override for setter
        - Or use field_validator for input validation

3. Cross-field relationships:
   OLD: Complex setter logic updating multiple fields
   NEW: @model_validator(mode='after') for post-initialization logic

4. Validation on input:
   OLD: Property setter with validation
   NEW: @field_validator(mode='before') for input validation

5. Derived/computed properties:
   OLD: @property that computes from other fields
   NEW: @computed_field @property (automatically recomputed)

BENEFITS OF PYDANTIC APPROACH:
- Automatic serialization/deserialization
- Built-in validation
- Type checking
- Schema generation
- Better IDE support
- Consistent with Pydantic patterns
"""

if __name__ == "__main__":
    demo_usage()
