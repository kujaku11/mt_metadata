"""
Comprehensive guide for implementing property-like behavior in Pydantic models.
This shows various approaches to replace @property with setter/getter patterns
using Pydantic's field validators and model validators.
"""

from typing import Annotated, Any, Dict, Optional

from pydantic import computed_field, Field, field_validator, model_validator

from mt_metadata.base import MetadataBase


class PydanticPropertyExamples(MetadataBase):
    """
    Examples of how to implement property-like behavior in Pydantic models
    using field validators, computed fields, and model validators.
    """

    # =====================================================
    # Method 1: Using field_validator for input validation/transformation
    # =====================================================

    # Example: A field that automatically formats/validates input
    _elevation: Annotated[
        float, Field(default=0.0, description="Elevation in meters", alias="elevation")
    ]

    @field_validator("_elevation", mode="before")
    @classmethod
    def validate_elevation(cls, v):
        """Field validator acts like a setter - transforms input before storage."""
        if v is None:
            return 0.0
        # Convert string to float if needed
        if isinstance(v, str):
            try:
                v = float(v.strip())
            except ValueError:
                raise ValueError(f"Cannot convert '{v}' to float")
        # Ensure it's a float
        return float(v)

    # =====================================================
    # Method 2: Using computed_field for derived properties
    # =====================================================

    # Store the underlying data
    _gps_lat: Annotated[
        float, Field(default=0.0, exclude=True)
    ]  # exclude from serialization
    _gps_lon: Annotated[float, Field(default=0.0, exclude=True)]

    @computed_field  # This creates a read-only property
    @property
    def latitude(self) -> float:
        """Computed field acts like a getter - derived from other fields."""
        return self._gps_lat

    @computed_field
    @property
    def longitude(self) -> float:
        """Another computed field example."""
        return self._gps_lon

    # =====================================================
    # Method 3: Using model_validator for complex cross-field validation
    # =====================================================

    # Fields that interact with each other
    center_x: Annotated[Optional[float], Field(default=None)]
    center_y: Annotated[Optional[float], Field(default=None)]
    center_z: Annotated[Optional[float], Field(default=None)]

    @model_validator(mode="after")
    def validate_coordinates(self):
        """Model validator can act like a setter for multiple related fields."""
        # Example: If center coordinates are provided, update GPS coordinates
        if self.center_x is not None and self.center_y is not None:
            # Convert UTM to lat/lon (simplified example)
            self._gps_lat = self.center_y / 111000.0  # Rough conversion
            self._gps_lon = self.center_x / 111000.0

        return self

    # =====================================================
    # Method 4: Custom setters using __setattr__ override
    # =====================================================

    def __setattr__(self, name: str, value: Any) -> None:
        """Override setattr to implement custom setter behavior."""
        # Custom setter for latitude
        if name == "latitude":
            if isinstance(value, str):
                try:
                    value = float(value)
                except ValueError:
                    raise ValueError(f"Cannot convert latitude '{value}' to float")
            super().__setattr__("_gps_lat", value)
            return

        # Custom setter for longitude
        if name == "longitude":
            if isinstance(value, str):
                try:
                    value = float(value)
                except ValueError:
                    raise ValueError(f"Cannot convert longitude '{value}' to float")
            super().__setattr__("_gps_lon", value)
            return

        # Custom setter for elevation that also updates center_z
        if name == "elevation":
            if isinstance(value, str):
                try:
                    value = float(value)
                except ValueError:
                    raise ValueError(f"Cannot convert elevation '{value}' to float")
            super().__setattr__("_elevation", value)
            super().__setattr__("center_z", value)
            return

        # Default behavior for all other attributes
        super().__setattr__(name, value)

    # =====================================================
    # Method 5: Using private fields with public methods
    # =====================================================

    _station_name: Annotated[Optional[str], Field(default=None, exclude=True)]

    def get_station(self) -> Optional[str]:
        """Explicit getter method."""
        return self._station_name

    def set_station(self, value: str) -> None:
        """Explicit setter method with validation."""
        if value is not None:
            value = str(value).strip().upper()  # Format station names
        self._station_name = value

    # Property-like access using methods
    @property
    def station(self) -> Optional[str]:
        return self.get_station()

    @station.setter
    def station(self, value: str) -> None:
        self.set_station(value)


# =====================================================
# Real-world example for the Header class
# =====================================================


class ImprovedHeader(MetadataBase):
    """
    Improved Header class using Pydantic validators instead of @property decorators.
    """

    # Basic fields
    name: Annotated[Optional[str], Field(default=None, description="Station name")]

    # GPS coordinates stored privately
    _gps_lat: Annotated[float, Field(default=0.0, exclude=True)]
    _gps_lon: Annotated[float, Field(default=0.0, exclude=True)]
    _elevation: Annotated[float, Field(default=0.0, exclude=True)]

    # Center location components
    center_x: Annotated[Optional[float], Field(default=None)]
    center_y: Annotated[Optional[float], Field(default=None)]
    center_z: Annotated[Optional[float], Field(default=None)]

    # Component dictionary for complex data
    _comp_dict: Annotated[Dict[str, Any], Field(default_factory=dict, exclude=True)]

    # =====================================================
    # Computed fields (read-only properties)
    # =====================================================

    @computed_field
    @property
    def latitude(self) -> float:
        """Get latitude from GPS data."""
        return self._gps_lat

    @computed_field
    @property
    def longitude(self) -> float:
        """Get longitude from GPS data."""
        return self._gps_lon

    @computed_field
    @property
    def elevation(self) -> float:
        """Get elevation, preferring center_location if available."""
        if self.center_z is not None:
            return self.center_z
        return self._elevation

    @computed_field
    @property
    def easting(self) -> Optional[float]:
        """Get easting from center location."""
        return self.center_x

    @computed_field
    @property
    def northing(self) -> Optional[float]:
        """Get northing from center location."""
        return self.center_y

    # =====================================================
    # Field validators (input validation/transformation)
    # =====================================================

    @field_validator("_gps_lat", "_gps_lon", "_elevation", mode="before")
    @classmethod
    def validate_float_coordinates(cls, v):
        """Validate and convert coordinate inputs."""
        if v is None:
            return 0.0
        if isinstance(v, str):
            try:
                return float(v.strip())
            except ValueError:
                raise ValueError(f"Cannot convert '{v}' to float")
        return float(v)

    @field_validator("center_x", "center_y", "center_z", mode="before")
    @classmethod
    def validate_optional_coordinates(cls, v):
        """Validate optional coordinate inputs."""
        if v is None or v == "":
            return None
        if isinstance(v, str):
            try:
                return float(v.strip())
            except ValueError:
                raise ValueError(f"Cannot convert '{v}' to float")
        return float(v)

    @field_validator("name", mode="before")
    @classmethod
    def validate_station_name(cls, v):
        """Validate and format station names."""
        if v is None:
            return None
        return str(v).strip()

    # =====================================================
    # Model validators (cross-field validation)
    # =====================================================

    @model_validator(mode="after")
    def update_coordinates(self):
        """Update related coordinate fields when others change."""
        # If center coordinates are set, they take precedence
        if self.center_z is not None:
            # Elevation from center_z overrides _elevation
            pass  # elevation property already handles this

        return self

    # =====================================================
    # Custom setattr for write access to computed properties
    # =====================================================

    def __setattr__(self, name: str, value: Any) -> None:
        """Custom setters for computed properties."""

        # Setter for latitude
        if name == "latitude":
            if isinstance(value, str):
                try:
                    value = float(value.strip())
                except ValueError:
                    raise ValueError(f"Invalid latitude: {value}")
            super().__setattr__("_gps_lat", float(value))
            return

        # Setter for longitude
        if name == "longitude":
            if isinstance(value, str):
                try:
                    value = float(value.strip())
                except ValueError:
                    raise ValueError(f"Invalid longitude: {value}")
            super().__setattr__("_gps_lon", float(value))
            return

        # Setter for elevation
        if name == "elevation":
            if isinstance(value, str):
                try:
                    value = float(value.strip())
                except ValueError:
                    raise ValueError(f"Invalid elevation: {value}")
            # Set both _elevation and center_z to keep them in sync
            super().__setattr__("_elevation", float(value))
            super().__setattr__("center_z", float(value))
            return

        # Default behavior
        super().__setattr__(name, value)

    # =====================================================
    # Additional methods for complex property behavior
    # =====================================================

    def set_center_location(self, x: float, y: float, z: float) -> None:
        """Set all center location coordinates at once."""
        self.center_x = x
        self.center_y = y
        self.center_z = z

    def get_center_location(self) -> Optional[list[float]]:
        """Get center location as a list."""
        if all(
            coord is not None for coord in [self.center_x, self.center_y, self.center_z]
        ):
            return [self.center_x, self.center_y, self.center_z]
        return None

    def set_gps_coordinates(self, lat: float, lon: float) -> None:
        """Set GPS coordinates."""
        self.latitude = lat  # Uses custom setter
        self.longitude = lon  # Uses custom setter


# =====================================================
# Usage examples
# =====================================================

if __name__ == "__main__":
    # Example 1: Basic property-like behavior
    print("=== Example 1: Basic Usage ===")
    header = ImprovedHeader()

    # Setting values through computed properties (uses custom setters)
    header.latitude = 45.123
    header.longitude = -123.456
    header.elevation = 1500.0

    print(f"Latitude: {header.latitude}")
    print(f"Longitude: {header.longitude}")
    print(f"Elevation: {header.elevation}")

    # Example 2: Field validation in action
    print("\n=== Example 2: Field Validation ===")
    header2 = ImprovedHeader()

    # String inputs are automatically converted
    header2.latitude = "45.123"  # String converted to float
    header2.longitude = "-123.456"
    header2.elevation = "1500"

    print(f"Converted latitude: {header2.latitude}")
    print(f"Converted longitude: {header2.longitude}")
    print(f"Converted elevation: {header2.elevation}")

    # Example 3: Model validation
    print("\n=== Example 3: Center Location Priority ===")
    header3 = ImprovedHeader()
    header3.elevation = 1000.0  # Set elevation first
    header3.center_z = 1500.0  # Center location takes precedence

    print(f"Elevation (from center_z): {header3.elevation}")  # Shows 1500.0

    # Example 4: Serialization
    print("\n=== Example 4: Serialization ===")
    data = header.model_dump()
    print(f"Serialized data: {data}")

    # Private fields are excluded, computed fields are included
    # Only the actual stored fields and computed values appear
