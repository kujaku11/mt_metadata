"""
HEADER CLASS CONVERSION GUIDE
============================

This shows exactly how to convert your Header class from @property to Pydantic patterns.

The working solution is demonstrated in pydantic_final_solution.py
"""


# BEFORE: Traditional Python with @property
class HeaderOld:
    def __init__(self):
        self._name = None
        self._gps_lat = None
        self._gps_lon = None

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
        if isinstance(value, str):
            value = float(value)
        self._gps_lat = value


from typing import Annotated, Optional, Union

# AFTER: Pydantic BaseModel
from pydantic import BaseModel, computed_field, Field, field_validator


class HeaderNew(BaseModel):
    # Step 1: Define fields with Optional and defaults
    name: Annotated[Optional[str], Field(default=None)]
    gps_lat: Annotated[Optional[float], Field(default=None)]
    gps_lon: Annotated[Optional[float], Field(default=None)]

    # Step 2: Field validators for construction-time validation
    @field_validator("gps_lat", "gps_lon", mode="before")
    @classmethod
    def convert_coordinates(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, str):
            return float(v.strip())
        return float(v)

    @field_validator("name", mode="before")
    @classmethod
    def clean_name(cls, v):
        if v is None or v == "":
            return None
        return str(v).strip()

    # Step 3: Computed fields for property-like read access
    @computed_field
    @property
    def latitude(self) -> Optional[float]:
        """Read-only property access to gps_lat."""
        return self.gps_lat

    # Step 4: Methods for complex setter logic
    def set_latitude(self, value: Union[str, float, None]) -> None:
        """Setter method with validation."""
        if value is None:
            self.gps_lat = None
            return
        if isinstance(value, str):
            value = float(value.strip())
        if not -90 <= value <= 90:
            raise ValueError(f"Invalid latitude: {value}")
        self.gps_lat = value


# USAGE COMPARISON
def show_usage():
    print("=== USAGE COMPARISON ===")

    # Old way
    old = HeaderOld()
    old.name = "Test"
    old.latitude = "45.123"
    print(f"Old: {old.name} at {old.latitude}")

    # New way
    new = HeaderNew()
    new.name = "Test"  # Direct field assignment
    new.set_latitude("45.123")  # Method call for complex logic
    print(f"New: {new.name} at {new.latitude}")  # Property access
    print(f"Serialized: {new.model_dump()}")  # Automatic serialization


# CONVERSION CHECKLIST
CONVERSION_STEPS = """
=== CONVERSION CHECKLIST ===

✅ 1. Replace private attributes with Optional fields
   _name → name: Optional[str] = Field(default=None)

✅ 2. Add field_validator for construction validation
   @field_validator('name', mode='before')

✅ 3. Replace @property getters with @computed_field
   @property def latitude(self) → @computed_field @property def latitude(self)

✅ 4. Replace @property setters with methods
   @latitude.setter → def set_latitude(self, value)

✅ 5. Update usage patterns
   obj.latitude = value → obj.set_latitude(value)
   print(obj.latitude) → print(obj.latitude)  # same

✅ 6. Enjoy automatic serialization
   Need custom to_dict() → obj.model_dump()

BENEFITS:
- Automatic validation during construction
- Built-in serialization/deserialization
- Type hints and IDE support
- JSON schema generation
- Integration with FastAPI, etc.

WORKING EXAMPLE:
See pydantic_final_solution.py for complete working code.
"""

if __name__ == "__main__":
    show_usage()
    print(CONVERSION_STEPS)
