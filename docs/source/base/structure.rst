======================
Metadata Structure
======================

.. _structure:

======================
Metadata Structure
======================

.. _structure:

Metadata Validation with Pydantic
------------------------------------

MT Metadata now uses `Pydantic <https://pydantic.dev/>`_ for robust metadata validation and data modeling. Pydantic provides automatic validation, serialization, and documentation of data structures through Python type hints and field definitions.

The validation system is built on Pydantic's powerful features:

    * **Type Validation** - Automatic conversion and validation based on Python type hints
    * **Field Definitions** - Rich field metadata using ``pydantic.Field()``
    * **Custom Validators** - Custom validation logic for complex requirements
    * **Serialization** - Built-in JSON, dict, and other format outputs
    * **Documentation** - Automatic schema generation for API documentation

Field Configuration
~~~~~~~~~~~~~~~~~~~~~

Each metadata field is defined using Pydantic's ``Annotated`` type hints with ``Field()`` specifications:

.. code-block:: python

    from typing import Annotated
    from pydantic import Field
    from mt_metadata.common.enumerations import DataTypeEnum
    
    data_type: Annotated[
        DataTypeEnum,
        Field(
            default="BBMT",
            description="Type of data recorded. If multiple types input as a comma separated list.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["BBMT", "LP", "BBMT,LP"],
            },
        ),
    ]

Field attributes include:

    * **Type** - Python type or custom class (DataTypeEnum, str, float, int, bool, etc.)
    * **default** - Default value for the field
    * **description** - Full description of the metadata field's purpose
    * **alias** - Alternative names that can be used for the field
    * **json_schema_extra** - Additional metadata including:
        
        - **units** - Physical units of the value
        - **required** - Whether the field is required (True/False)
        - **examples** - Example values to guide users

MetadataBase Class Structure
-------------------------------

All metadata classes inherit from :class:`mt_metadata.base.metadata.MetadataBase`, which extends Pydantic's ``BaseModel`` with additional functionality for magnetotelluric data handling.

The ``MetadataBase`` class provides:

    * **Validation** - Automatic type checking and data validation
    * **Serialization** - Methods to convert to JSON, XML, and dictionary formats
    * **Dot Notation Access** - Pythonic attribute access to nested metadata
    * **Flexible Input** - Accept data from dictionaries, JSON strings, XML, or pandas Series

Example Usage
~~~~~~~~~~~~~~

Creating and using metadata objects is straightforward:

Example Usage
~~~~~~~~~~~~~~

Creating and using metadata objects is straightforward:

.. code-block:: python
    
    >>> from mt_metadata.timeseries import Station
    >>> station = Station()
    >>> station.location.latitude = 10.9
    >>> station.data_type = "BBMT"
    
The metadata automatically validates input values and provides helpful error messages:

.. code-block:: python

    >>> station.location.latitude = "not_a_number"
    ValidationError: 1 validation error for Station
    location.latitude
      Input should be a valid number [type=float_parsing, input_value='not_a_number']

Accessing Metadata
~~~~~~~~~~~~~~~~~~~

Metadata can be accessed using standard Python attribute notation. The underlying Pydantic model handles all validation automatically:

.. code-block:: python

    >>> station.location.latitude
    10.9
    >>> station.data_type
    'BBMT'

Serialization and Output
~~~~~~~~~~~~~~~~~~~~~~~~~

The metadata can be serialized to various formats:

**Dictionary representation:**

.. code-block:: python

    >>> station.model_dump()
    {
        'channel_layout': 'X',
        'channels_recorded': [],
        'data_type': 'BBMT',
        'geographic_name': None,
        'id': None,
        'location': {
            'latitude': 10.9,
            'longitude': 0.0,
            'elevation': 0.0,
            'datum': 'WGS84',
            ...
        },
        'orientation': {
            'method': None,
            'reference_frame': 'geographic'
        },
        ...
    }

**JSON representation:**

.. code-block:: python

    >>> station.model_dump_json(indent=2)
    {
      "channel_layout": "X",
      "channels_recorded": [],
      "data_type": "BBMT",
      "geographic_name": null,
      "id": null,
      "location": {
        "latitude": 10.9,
        "longitude": 0.0,
        "elevation": 0.0,
        "datum": "WGS84"
      },
      "orientation": {
        "method": null,
        "reference_frame": "geographic"
      }
    }

Loading from External Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Metadata objects can be created from various data sources:

.. code-block:: python

    # From dictionary
    >>> data = {"location": {"latitude": 45.0, "longitude": -120.0}, "data_type": "LP"}
    >>> station = Station(**data)
    
    # From JSON string
    >>> json_str = '{"location": {"latitude": 45.0}, "data_type": "BBMT"}'
    >>> station = Station.model_validate_json(json_str)

Validation and Type Safety
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pydantic provides robust validation with clear error messages:

.. code-block:: python

    >>> from mt_metadata.timeseries import Electric
    >>> electric = Electric()
    >>> electric.component = "Invalid"  # Only Ex, Ey allowed
    ValidationError: 1 validation error for Electric
    component
      Input should be 'Ex' or 'Ey' [type=enum, input_value='Invalid']

Benefits of the Pydantic Approach
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The new Pydantic-based structure provides several advantages:

    * **Type Safety** - Automatic type checking prevents common errors
    * **Rich Validation** - Custom validators ensure data integrity
    * **Documentation** - Self-documenting code through type hints and field descriptions
    * **Serialization** - Built-in support for JSON, XML, and other formats
    * **IDE Support** - Better autocomplete and type checking in development environments
    * **Performance** - Fast validation using compiled Rust code (via Pydantic v2)
    * **Standards Compliance** - JSON Schema generation for API documentation

   




 