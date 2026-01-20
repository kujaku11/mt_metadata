"""
Test module for transfer_functions/io/emtfxml/metadata/value.py
"""

import pytest

from mt_metadata.transfer_functions.io.emtfxml.metadata.value import Value

# ============================================================================
# TEST VALUE DEFAULTS
# ============================================================================


class TestValueDefaults:
    """Test Value class default values."""

    def test_default_initialization(self):
        """Test that Value initializes with empty string defaults."""
        val = Value()
        assert val.name == ""
        assert val.output == ""
        assert val.input == ""
        assert val.value == ""

    def test_default_types(self):
        """Test that default values are all strings."""
        val = Value()
        assert isinstance(val.name, str)
        assert isinstance(val.output, str)
        assert isinstance(val.input, str)
        assert isinstance(val.value, str)


# ============================================================================
# TEST VALUE FIELD SETTING
# ============================================================================


class TestValueFieldSetting:
    """Test setting individual Value fields."""

    def test_set_name(self):
        """Test setting the name field."""
        val = Value(name="tx")
        assert val.name == "tx"

    def test_set_output(self):
        """Test setting the output field."""
        val = Value(output="ex")
        assert val.output == "ex"

    def test_set_input(self):
        """Test setting the input field."""
        val = Value(input="hy")
        assert val.input == "hy"

    def test_set_value(self):
        """Test setting the value field."""
        val = Value(value="10.1 + 11j")
        assert val.value == "10.1 + 11j"

    def test_set_all_fields(self):
        """Test setting all fields at once."""
        val = Value(name="zxx", output="ex", input="hx", value="5.2 + 3.1j")
        assert val.name == "zxx"
        assert val.output == "ex"
        assert val.input == "hx"
        assert val.value == "5.2 + 3.1j"


# ============================================================================
# TEST VALUE WITH EXAMPLES
# ============================================================================


class TestValueExamples:
    """Test Value with documented example values."""

    def test_example_from_documentation(self):
        """Test with examples from field documentation."""
        val = Value(name="tx", output="ex", input="hy", value="10.1 + 11j")
        assert val.name == "tx"
        assert val.output == "ex"
        assert val.input == "hy"
        assert val.value == "10.1 + 11j"

    @pytest.mark.parametrize(
        "name, output, input_ch, value",
        [
            ("zxx", "ex", "hx", "1.0 + 0.5j"),
            ("zxy", "ex", "hy", "2.0 + 1.5j"),
            ("zyx", "ey", "hx", "-2.0 - 1.5j"),
            ("zyy", "ey", "hy", "1.0 + 0.5j"),
            ("tx", "hz", "hx", "0.1 + 0.2j"),
            ("ty", "hz", "hy", "0.3 + 0.4j"),
        ],
    )
    def test_various_component_combinations(self, name, output, input_ch, value):
        """Test various MT component combinations."""
        val = Value(name=name, output=output, input=input_ch, value=value)
        assert val.name == name
        assert val.output == output
        assert val.input == input_ch
        assert val.value == value


# ============================================================================
# TEST VALUE WITH COMPONENT NAMES
# ============================================================================


class TestValueComponentNames:
    """Test Value with different MT component names."""

    @pytest.mark.parametrize(
        "component",
        ["ex", "ey", "hx", "hy", "hz", "Ez", "Hx", "Hy", "Hz"],
    )
    def test_electric_and_magnetic_components(self, component):
        """Test with various electric and magnetic field components."""
        val = Value(output=component)
        assert val.output == component

    def test_impedance_tensor_names(self):
        """Test with impedance tensor element names."""
        tensor_names = ["zxx", "zxy", "zyx", "zyy"]
        for name in tensor_names:
            val = Value(name=name)
            assert val.name == name

    def test_tipper_names(self):
        """Test with tipper element names."""
        tipper_names = ["tx", "ty", "tzx", "tzy"]
        for name in tipper_names:
            val = Value(name=name)
            assert val.name == name


# ============================================================================
# TEST VALUE WITH NUMERIC VALUES
# ============================================================================


class TestValueNumericRepresentations:
    """Test Value with different numeric value representations."""

    @pytest.mark.parametrize(
        "value_str",
        [
            "1.0",
            "10.5",
            "1.0 + 2.0j",
            "10.1 + 11j",
            "-5.3 - 2.1j",
            "0.0 + 0.0j",
            "1e-5",
            "1.23e-3 + 4.56e-2j",
        ],
    )
    def test_various_numeric_formats(self, value_str):
        """Test with various numeric string formats."""
        val = Value(value=value_str)
        assert val.value == value_str

    def test_real_value(self):
        """Test with real-only value."""
        val = Value(value="42.5")
        assert val.value == "42.5"

    def test_complex_value(self):
        """Test with complex value."""
        val = Value(value="3.14 + 2.71j")
        assert val.value == "3.14 + 2.71j"

    def test_scientific_notation(self):
        """Test with scientific notation."""
        val = Value(value="1.5e-6 + 2.3e-5j")
        assert val.value == "1.5e-6 + 2.3e-5j"


# ============================================================================
# TEST VALUE SERIALIZATION
# ============================================================================


class TestValueSerialization:
    """Test Value serialization methods."""

    def test_to_dict(self):
        """Test converting to dictionary."""
        val = Value(name="zxy", output="ex", input="hy", value="5.0 + 3.0j")
        data = val.model_dump()
        assert data["name"] == "zxy"
        assert data["output"] == "ex"
        assert data["input"] == "hy"
        assert data["value"] == "5.0 + 3.0j"

    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {
            "name": "tx",
            "output": "hz",
            "input": "hx",
            "value": "0.1 + 0.2j",
        }
        val = Value(**data)
        assert val.name == "tx"
        assert val.output == "hz"
        assert val.input == "hx"
        assert val.value == "0.1 + 0.2j"

    def test_round_trip_serialization(self):
        """Test round-trip serialization to/from dict."""
        original = Value(name="zyy", output="ey", input="hy", value="2.5 + 1.5j")
        data = original.model_dump()
        restored = Value(**data)
        assert restored.name == original.name
        assert restored.output == original.output
        assert restored.input == original.input
        assert restored.value == original.value

    def test_to_json(self):
        """Test JSON serialization."""
        val = Value(name="zxx", output="ex", input="hx", value="1.0 + 0.5j")
        json_str = val.model_dump_json()
        assert "zxx" in json_str
        assert "ex" in json_str
        assert "hx" in json_str
        assert isinstance(json_str, str)

    def test_from_json(self):
        """Test creating from JSON string."""
        json_str = (
            '{"name": "ty", "output": "hz", "input": "hy", "value": "0.3 + 0.4j"}'
        )
        val = Value.model_validate_json(json_str)
        assert val.name == "ty"
        assert val.output == "hz"
        assert val.input == "hy"
        assert val.value == "0.3 + 0.4j"


# ============================================================================
# TEST VALUE UPDATES
# ============================================================================


class TestValueUpdates:
    """Test updating Value fields after initialization."""

    def test_update_name(self):
        """Test updating name field."""
        val = Value(name="zxx")
        val.name = "zxy"
        assert val.name == "zxy"

    def test_update_output(self):
        """Test updating output field."""
        val = Value(output="ex")
        val.output = "ey"
        assert val.output == "ey"

    def test_update_input(self):
        """Test updating input field."""
        val = Value(input="hx")
        val.input = "hy"
        assert val.input == "hy"

    def test_update_value(self):
        """Test updating value field."""
        val = Value(value="1.0 + 1.0j")
        val.value = "2.0 + 2.0j"
        assert val.value == "2.0 + 2.0j"

    def test_update_all_fields(self):
        """Test updating all fields."""
        val = Value(name="zxx", output="ex", input="hx", value="1.0 + 0.5j")
        val.name = "zyy"
        val.output = "ey"
        val.input = "hy"
        val.value = "2.0 + 1.0j"
        assert val.name == "zyy"
        assert val.output == "ey"
        assert val.input == "hy"
        assert val.value == "2.0 + 1.0j"


# ============================================================================
# TEST VALUE SCHEMA
# ============================================================================


class TestValueSchema:
    """Test Value schema and metadata."""

    def test_has_all_required_fields(self):
        """Test that Value has all required fields."""
        val = Value()
        assert hasattr(val, "name")
        assert hasattr(val, "output")
        assert hasattr(val, "input")
        assert hasattr(val, "value")

    def test_schema_generation(self):
        """Test that schema can be generated."""
        schema = Value.model_json_schema()
        assert "properties" in schema
        assert "name" in schema["properties"]
        assert "output" in schema["properties"]
        assert "input" in schema["properties"]
        assert "value" in schema["properties"]

    def test_field_types_in_schema(self):
        """Test that fields have correct types in schema."""
        schema = Value.model_json_schema()
        for field in ["name", "output", "input", "value"]:
            assert schema["properties"][field]["type"] == "string"
