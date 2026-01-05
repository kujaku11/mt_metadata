
Introduction
-------------
The goal of **MT Metadata** is to develop a standard format and tools for archiving 
magnetotelluric (MT) time series and transfer function data.

Metadata standards for MT have been historically relaxed to user dependent.  The goal of this module is to formalize and provide tools for users of MT timeseries and metadata.  

The metadata for time series follows the standards proposed by the `IRIS-PASSCAL MT
Software working
group <https://www.iris.edu/hq/about_iris/governance/mt_soft>`__ published at Peacock, J.R., Frassetto, A., Kelbert, A., Egbert, G., Smirnov, M., Schultz, A.C., Kappler, K.N., Ronan, T., and Trabant, C., 2021, Metadata Standards for Magnetotelluric Time Series Data: U.S. Geological Survey data release, ` <https://doi.org/10.5066/P9AXGKEV>`__.

The metadata for transfer functions follows those proposed by Anna Kelbert `EMTF XML: New data interchange format and conversion tools for electromagnetic transfer functions <http://mr.crossref.org/iPage?doi=10.1190%2Fgeo2018-0679.1>`__. 

Architecture
-------------
**MT Metadata** is built on `Pydantic <https://docs.pydantic.dev/>`__ BaseModel objects, providing a robust and modern approach to metadata management. This architectural choice offers several key advantages:

**Data Validation**
    Pydantic provides automatic validation of metadata attributes, ensuring data integrity and type safety. Invalid data is caught immediately with clear error messages, preventing downstream issues.

**Performance**
    Pydantic's Rust-based core (v2+) delivers exceptional performance for serialization, deserialization, and validation operations, making metadata handling efficient even for large datasets.

**Maintainability**
    The declarative syntax and type hints make the codebase more readable and maintainable. IDE support provides better autocomplete and inline documentation, reducing development errors.

**Serialization**
    Built-in support for JSON, dictionary, and other formats simplifies data interchange. Metadata can be easily exported, shared, and stored in various formats.

**Extensibility**
    Custom validators and field types allow for domain-specific validation rules while maintaining a consistent API across all metadata classes.

This modern foundation ensures **MT Metadata** remains robust, performant, and easy to extend as standards evolve.

MetadataBase
^^^^^^^^^^^^^
All metadata classes in **MT Metadata** inherit from ``MetadataBase``, a specialized Pydantic BaseModel that provides a consistent interface for defining and managing MT metadata attributes.

**Field Definition**
    Fields in ``MetadataBase`` are defined using Pydantic's ``Field`` descriptor, which encapsulates both the data type and metadata about each attribute::

        from pydantic import Field
        
        class Station(MetadataBase):
            id: str = Field(
                default="",
                description="Station identification name",
                json_schema_extra={"style": "name", "required": True}
            )
            latitude: float = Field(
                default=0.0,
                description="Latitude in decimal degrees WGS84",
                json_schema_extra={"units": "degrees", "style": "number"}
            )

**Field Attributes**
    Each field can specify:
    
    - **default**: The default value if not provided
    - **description**: Human-readable documentation
    - **json_schema_extra**: Additional metadata including units, style, options, and validation rules
    - **type annotations**: Python type hints for automatic validation

**Benefits**
    This approach provides:
    
    - **Self-documenting code**: Field descriptions and types serve as inline documentation
    - **Automatic validation**: Type checking and custom validators ensure data integrity
    - **JSON Schema generation**: Automatic schema creation for API documentation and validation
    - **Consistent API**: All metadata objects share the same interface for getting/setting attributes

The ``MetadataBase`` class also provides methods for serialization (to_dict, to_json), comparison, and updating attributes, ensuring a uniform experience across all metadata types.

.. note:: This version is stable, but if you encounter any issues or have suggestions, feel free to comment by raising an issue on GitHub in the repository `mt_metadata <https://github.com/kujaku11/mt_metadata>`__ 

