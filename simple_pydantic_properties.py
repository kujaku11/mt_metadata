"""
WORKING SOLUTION: How to implement property-like behavior in Pydantic BaseModel

This shows the CORRECT way to replace @property with Pydantic patterns.
"""

from typing import Annotated, Optional, Union

from pydantic import BaseModel, computed_field, Field, field_validator


class PydanticPropertyExample(BaseModel):
    """
    Complete working example showing how to replace @property in Pydantic.
    """

    # ========================================
    # PATTERN 1: Simple fields (no properties needed)
    # ========================================

    # Instead of @property getter/setter, just use validated fields
    name: Annotated[Optional[str], Field(default=None)]
    latitude: Annotated[float, Field(default=0.0)]
    longitude: Annotated[float, Field(default=0.0)]
    elevation: Annotated[float, Field(default=0.0)]

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v):
        """Validate and clean name input."""
        if v is None or v == "":
            return None
        return str(v).strip()

    @field_validator("latitude", "longitude", "elevation", mode="before")
    @classmethod
    def validate_coordinates(cls, v):
        """Convert string coordinates to float."""
        if isinstance(v, str):
            try:
                return float(v.strip())
            except ValueError:
                raise ValueError(f"Cannot convert '{v}' to float")
        return float(v) if v is not None else 0.0

    # ========================================
    # PATTERN 2: Computed properties (read-only)
    # ========================================

    @computed_field
    @property
    def coordinates(self) -> list[float]:
        """Get coordinates as list - READ ONLY."""
        return [self.latitude, self.longitude, self.elevation]

    @computed_field
    @property
    def location_string(self) -> str:
        """Format location as string - READ ONLY."""
        return f"{self.latitude:.4f}, {self.longitude:.4f} @ {self.elevation:.1f}m"

    @computed_field
    @property
    def is_valid_location(self) -> bool:
        """Check if coordinates are valid - READ ONLY."""
        return -90 <= self.latitude <= 90 and -180 <= self.longitude <= 180

    # ========================================
    # PATTERN 3: Methods for complex setters
    # ========================================

    def set_location(
        self,
        lat: Union[str, float],
        lon: Union[str, float],
        elev: Union[str, float] = None,
    ):
        """Method to set location with validation (replaces property setter)."""
        # Validation happens automatically via field validators
        self.latitude = lat  # Will go through field_validator
        self.longitude = lon  # Will go through field_validator
        if elev is not None:
            self.elevation = elev  # Will go through field_validator

    def update_coordinates(self, **kwargs):
        """Update any coordinate values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


def test_working_patterns():
    """Test all the working patterns."""
    print("=== Pydantic Property Replacement Patterns ===\n")

    # Create instance
    station = PydanticPropertyExample()
    print(f"1. Initial state: {station.model_dump()}")

    # Set values directly (replaces property setters)
    station.name = "Test Station"
    station.latitude = "45.123"  # String will be converted to float
    station.longitude = -123.456
    station.elevation = 1500

    print(f"2. After direct assignment:")
    print(f"   Name: {station.name}")
    print(f"   Coordinates: {station.coordinates}")  # computed property
    print(f"   Location: {station.location_string}")  # computed property
    print(f"   Valid: {station.is_valid_location}")  # computed property

    # Use method for complex setting (replaces property setter)
    station.set_location("46.0", "-124.0", "2000")
    print(f"3. After set_location method:")
    print(f"   Location: {station.location_string}")

    # Create with constructor (validation happens automatically)
    station2 = PydanticPropertyExample(
        name="Station 2",
        latitude="47.5",  # String input
        longitude="-122.3",
        elevation="500",
    )
    print(f"4. Constructor with validation:")
    print(f"   {station2.location_string}")
    print(f"   Valid: {station2.is_valid_location}")

    print(f"5. Full serialization: {station2.model_dump()}")


if __name__ == "__main__":
    test_working_patterns()
