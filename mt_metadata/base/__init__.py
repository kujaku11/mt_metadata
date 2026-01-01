"""
Base classes for holding metadata and schema objects

MetadataBase Overview
=====================

MetadataBase is the foundational class for all metadata objects in mt_metadata,
providing robust, validated data structures with extensive serialization capabilities.

Built on Pydantic
-----------------
MetadataBase inherits from Pydantic's BaseModel, leveraging the powerful benefits
of Pydantic for data validation and management:

* **Automatic Type Validation**: All attributes are validated against their defined
  types at assignment time, catching errors early
* **Data Parsing**: Automatically converts and coerces input data to the correct
  types (e.g., strings to floats, lists to arrays)
* **IDE Support**: Full autocomplete and type hints for enhanced developer experience
* **Performance**: Fast validation using compiled Rust code (via pydantic-core)
* **Serialization**: Built-in support for converting to/from dictionaries and JSON

Extended Functionality
----------------------
MetadataBase extends Pydantic's BaseModel with specialized features:

* **Dot-Separated Attribute Names**: Set nested attributes using dot notation
  (e.g., `survey.id = "MT001"` or `station.location.latitude = 45.0`)
* **Default Values**: Accepts default values from schemas and validates them to
  proper types automatically
* **Flexible I/O Methods**:
  - `to_dict()` / `from_dict()` - Dictionary conversion
  - `to_json()` / `from_json()` - JSON string/file handling
  - `to_xml()` / `from_xml()` - XML element handling
  - `to_series()` / `from_series()` - Pandas Series integration
* **Attribute Introspection**:
  - `get_attribute_list()` - Get all attribute names
  - `attribute_information` - Detailed metadata about each field
  - `update_attribute()` - Programmatically update attributes with validation
  - `add_new_field()` - Dynamically add new fields with validation rules
* **Standards Compliance**: Integrates with metadata standards and schemas for
  consistent, validated magnetotelluric data interchange

This design ensures that metadata objects are always in a valid state, with type
safety, comprehensive validation, and flexible data exchange formats.

"""

from .metadata import MetadataBase
from .schema import BaseDict

__all__ = ["MetadataBase", "BaseDict"]
