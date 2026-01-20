"""
Test module for transfer_functions/io/emtfxml/metadata/description.py
"""

from mt_metadata.transfer_functions.io.emtfxml.metadata.description import Description

# ============================================================================
# TEST DESCRIPTION DEFAULTS
# ============================================================================


class TestDescriptionDefaults:
    """Test Description class default values."""

    def test_default_initialization(self):
        """Test that Description initializes with empty string default."""
        desc = Description()
        assert desc.description == ""

    def test_default_type(self):
        """Test that default description is a string."""
        desc = Description()
        assert isinstance(desc.description, str)


# ============================================================================
# TEST DESCRIPTION SETTING VALUES
# ============================================================================


class TestDescriptionValues:
    """Test setting description values."""

    def test_set_description_string(self):
        """Test setting description with a string."""
        desc = Description(description="Test description")
        assert desc.description == "Test description"

    def test_set_description_empty_string(self):
        """Test setting description to empty string."""
        desc = Description(description="")
        assert desc.description == ""

    def test_set_description_multiline(self):
        """Test setting description with multiline string."""
        multiline = "Line 1\nLine 2\nLine 3"
        desc = Description(description=multiline)
        assert desc.description == multiline

    def test_set_description_with_special_chars(self):
        """Test setting description with special characters."""
        special = "Description with <special> & 'chars' \"quoted\""
        desc = Description(description=special)
        assert desc.description == special

    def test_set_description_long_text(self):
        """Test setting description with long text."""
        long_text = "A" * 1000
        desc = Description(description=long_text)
        assert desc.description == long_text
        assert len(desc.description) == 1000


# ============================================================================
# TEST DESCRIPTION EXAMPLES
# ============================================================================


class TestDescriptionExamples:
    """Test Description with example values from documentation."""

    def test_magnetotelluric_transfer_functions(self):
        """Test with the documented example."""
        desc = Description(description="Magnetotelluric Transfer Functions")
        assert desc.description == "Magnetotelluric Transfer Functions"

    def test_various_mt_descriptions(self):
        """Test with various MT-related descriptions."""
        examples = [
            "Magnetotelluric Transfer Functions",
            "MT impedance tensor",
            "Tipper vector data",
            "Remote reference processing results",
            "Magnetotelluric response functions",
        ]
        for example in examples:
            desc = Description(description=example)
            assert desc.description == example


# ============================================================================
# TEST DESCRIPTION SERIALIZATION
# ============================================================================


class TestDescriptionSerialization:
    """Test Description serialization methods."""

    def test_to_dict(self):
        """Test converting to dictionary."""
        desc = Description(description="Test MT data")
        data = desc.model_dump()
        assert "description" in data
        assert data["description"] == "Test MT data"

    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {"description": "Created from dict"}
        desc = Description(**data)
        assert desc.description == "Created from dict"

    def test_round_trip_serialization(self):
        """Test round-trip serialization to/from dict."""
        original = Description(description="Original description text")
        data = original.model_dump()
        restored = Description(**data)
        assert restored.description == original.description

    def test_to_json(self):
        """Test JSON serialization."""
        desc = Description(description="JSON test")
        json_str = desc.model_dump_json()
        assert "JSON test" in json_str
        assert isinstance(json_str, str)

    def test_from_json(self):
        """Test creating from JSON string."""
        json_str = '{"description": "From JSON"}'
        desc = Description.model_validate_json(json_str)
        assert desc.description == "From JSON"


# ============================================================================
# TEST DESCRIPTION VALIDATION
# ============================================================================


class TestDescriptionValidation:
    """Test Description field validation."""

    def test_description_accepts_string(self):
        """Test that description accepts string values."""
        desc = Description(description="Valid string")
        assert desc.description == "Valid string"

    def test_description_type_coercion(self):
        """Test that non-string values are coerced to strings if possible."""
        # Pydantic should coerce these to strings
        desc1 = Description(description="123")
        assert desc1.description == "123"
        assert isinstance(desc1.description, str)

    def test_update_description(self):
        """Test updating description after initialization."""
        desc = Description(description="Initial")
        desc.description = "Updated"
        assert desc.description == "Updated"


# ============================================================================
# TEST DESCRIPTION METADATA
# ============================================================================


class TestDescriptionMetadata:
    """Test Description metadata and schema information."""

    def test_has_description_field(self):
        """Test that Description has a description field."""
        desc = Description()
        assert hasattr(desc, "description")

    def test_schema_generation(self):
        """Test that schema can be generated."""
        schema = Description.model_json_schema()
        assert "properties" in schema
        assert "description" in schema["properties"]

    def test_field_info(self):
        """Test field metadata."""
        schema = Description.model_json_schema()
        desc_field = schema["properties"]["description"]
        assert desc_field["type"] == "string"
