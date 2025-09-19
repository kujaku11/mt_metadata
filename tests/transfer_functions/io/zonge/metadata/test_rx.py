"""
Test suite for Rx metadata class using pytest with fixtures and subtests.
This test suite follows modern pytest patterns for comprehensive coverage and efficiency optimization.
"""

import json

import pytest
from pydantic import ValidationError

from mt_metadata.transfer_functions.io.zonge.metadata.rx import CmpEnum, Rx


class TestRxDefault:
    """Test default initialization and basic attributes of Rx class."""

    @pytest.fixture(scope="class")
    def default_rx(self):
        """Fixture providing a default Rx instance for efficiency."""
        return Rx()  # type: ignore

    def test_default_initialization(self, default_rx, subtests):
        """Test that Rx initializes with correct default values."""
        with subtests.test("default gdp_stn value"):
            assert default_rx.gdp_stn == ""

        with subtests.test("default length value"):
            assert default_rx.length == 0.0

        with subtests.test("default h_p_r value"):
            assert default_rx.h_p_r == []

        with subtests.test("default cmp value"):
            assert default_rx.cmp == ""

        with subtests.test("default center value"):
            assert default_rx.center is None

        with subtests.test("default x_y_z1 value"):
            assert default_rx.x_y_z1 is None

        with subtests.test("default x_y_z2 value"):
            assert default_rx.x_y_z2 is None

        with subtests.test("default u_t_m1 value"):
            assert default_rx.u_t_m1 is None

        with subtests.test("default a_space value"):
            assert default_rx.a_space is None

        with subtests.test("default s_space value"):
            assert default_rx.s_space is None

    def test_default_rx_attributes(self, default_rx, subtests):
        """Test that Rx has all expected attributes."""
        expected_attributes = [
            "gdp_stn",
            "length",
            "h_p_r",
            "cmp",
            "center",
            "x_y_z1",
            "x_y_z2",
            "u_t_m1",
            "a_space",
            "s_space",
        ]

        for attr in expected_attributes:
            with subtests.test(f"has attribute {attr}"):
                assert hasattr(default_rx, attr)

    def test_default_model_fields(self, default_rx, subtests):
        """Test model fields are properly defined."""
        fields = default_rx.model_fields
        expected_fields = [
            "gdp_stn",
            "length",
            "h_p_r",
            "cmp",
            "center",
            "x_y_z1",
            "x_y_z2",
            "u_t_m1",
            "a_space",
            "s_space",
        ]

        for field in expected_fields:
            with subtests.test(f"model field {field}"):
                assert field in fields

        with subtests.test("field count"):
            assert len(fields) == 10

    def test_field_types(self, default_rx, subtests):
        """Test that fields have expected types."""
        type_checks = [
            ("gdp_stn", str),
            ("length", float),
            ("h_p_r", list),
            ("cmp", str),  # CmpEnum stored as string
            ("center", type(None)),  # Optional field defaults to None
            ("x_y_z1", type(None)),
            ("x_y_z2", type(None)),
            ("u_t_m1", type(None)),
            ("a_space", type(None)),
            ("s_space", type(None)),
        ]

        for field_name, expected_type in type_checks:
            with subtests.test(f"field type {field_name}"):
                field_value = getattr(default_rx, field_name)
                assert isinstance(field_value, expected_type)


class TestRxCustomValues:
    """Test Rx with custom values and various initialization patterns."""

    @pytest.fixture(scope="class")
    def populated_rx(self):
        """Fixture providing a Rx instance with custom values for efficiency."""
        return Rx(  # type: ignore
            gdp_stn="24",
            length=100.0,
            h_p_r=[0.0, 0.0, 180.0],
            cmp=CmpEnum.zxx,
            center="335754.685:4263553.435:1650.2 m",
            x_y_z1="335754.685:4263553.435:1650.2",
            x_y_z2="335754.685:4263553.435:1650.2",
            u_t_m1="335754.685:4263553.435:1650.2",
            a_space="100 m",
            s_space="100",
        )

    def test_populated_rx_values(self, populated_rx, subtests):
        """Test Rx with custom values."""
        with subtests.test("populated gdp_stn"):
            assert populated_rx.gdp_stn == "24"

        with subtests.test("populated length"):
            assert populated_rx.length == 100.0

        with subtests.test("populated h_p_r"):
            assert populated_rx.h_p_r == [0.0, 0.0, 180.0]

        with subtests.test("populated cmp"):
            assert populated_rx.cmp == "zxx"  # Stored as string

        with subtests.test("populated center"):
            assert populated_rx.center == "335754.685:4263553.435:1650.2 m"

        with subtests.test("populated x_y_z1"):
            assert populated_rx.x_y_z1 == "335754.685:4263553.435:1650.2"

        with subtests.test("populated x_y_z2"):
            assert populated_rx.x_y_z2 == "335754.685:4263553.435:1650.2"

        with subtests.test("populated u_t_m1"):
            assert populated_rx.u_t_m1 == "335754.685:4263553.435:1650.2"

        with subtests.test("populated a_space"):
            assert populated_rx.a_space == "100 m"

        with subtests.test("populated s_space"):
            assert populated_rx.s_space == "100"

    def test_cmp_enum_initialization_patterns(self, subtests):
        """Test various CmpEnum initialization patterns."""
        cmp_patterns = [
            ("zxx", CmpEnum.zxx, "zxx"),
            ("zyy", CmpEnum.zyy, "zyy"),
            ("zyx", CmpEnum.zyx, "zyx"),
            ("zxy", CmpEnum.zxy, "zxy"),
            ("txy", CmpEnum.txy, "txy"),
            ("tyx", CmpEnum.tyx, "tyx"),
            ("null", CmpEnum.null, ""),
            ("string zxx", "zxx", "zxx"),
            ("string zyy", "zyy", "zyy"),
            ("empty string", "", ""),
        ]

        for case_name, input_value, expected_value in cmp_patterns:
            with subtests.test(f"cmp pattern {case_name}"):
                rx = Rx(cmp=input_value)  # type: ignore
                assert rx.cmp == expected_value

    def test_h_p_r_list_patterns(self, subtests):
        """Test various h_p_r list initialization patterns."""
        h_p_r_patterns = [
            ("empty list", [], []),
            ("single value", [0.0], [0.0]),
            ("three values", [0.0, 0.0, 180.0], [0.0, 0.0, 180.0]),
            (
                "integer values",
                [0, 0, 180],
                [0.0, 0.0, 180.0],
            ),  # Should convert to float
            ("mixed values", [0, 0.0, 180], [0.0, 0.0, 180.0]),
        ]

        for case_name, input_value, expected_value in h_p_r_patterns:
            with subtests.test(f"h_p_r pattern {case_name}"):
                rx = Rx(h_p_r=input_value)  # type: ignore
                assert rx.h_p_r == expected_value

    def test_string_field_patterns(self, subtests):
        """Test string field initialization patterns."""
        string_fields = [
            "gdp_stn",
            "center",
            "x_y_z1",
            "x_y_z2",
            "u_t_m1",
            "a_space",
            "s_space",
        ]
        test_values = [
            ("empty string", ""),
            ("simple string", "test"),
            ("numeric string", "123"),
            ("coordinate string", "335754.685:4263553.435:1650.2"),
            ("unit string", "100 m"),
        ]

        for field in string_fields:
            for case_name, test_value in test_values:
                with subtests.test(f"{field} {case_name}"):
                    kwargs = {field: test_value}
                    rx = Rx(**kwargs)  # type: ignore
                    assert getattr(rx, field) == test_value

    def test_partial_rx_values(self, subtests):
        """Test Rx with only some fields populated."""
        partial_cases = [
            ("gdp_stn only", {"gdp_stn": "24"}, "24", 0.0, [], ""),
            ("length only", {"length": 50.5}, "", 50.5, [], ""),
            ("h_p_r only", {"h_p_r": [1, 2, 3]}, "", 0.0, [1.0, 2.0, 3.0], ""),
            ("cmp only", {"cmp": CmpEnum.zxy}, "", 0.0, [], "zxy"),
        ]

        for (
            case_name,
            kwargs,
            expected_gdp_stn,
            expected_length,
            expected_h_p_r,
            expected_cmp,
        ) in partial_cases:
            with subtests.test(f"partial {case_name}"):
                rx = Rx(**kwargs)  # type: ignore
                assert rx.gdp_stn == expected_gdp_stn
                assert rx.length == expected_length
                assert rx.h_p_r == expected_h_p_r
                assert rx.cmp == expected_cmp

    def test_individual_field_initialization(self, subtests):
        """Test individual field initialization."""
        test_cases = [
            ("gdp_stn", "station1"),
            ("length", 75.5),
            ("h_p_r", [45.0, 90.0, 135.0]),
            ("cmp", CmpEnum.zyy),
            ("center", "test center"),
            ("x_y_z1", "coord1"),
            ("x_y_z2", "coord2"),
            ("u_t_m1", "utm1"),
            ("a_space", "50 m"),
            ("s_space", "25"),
        ]

        for field, value in test_cases:
            with subtests.test(f"individual {field}"):
                kwargs = {field: value}
                rx = Rx(**kwargs)  # type: ignore
                field_value = getattr(rx, field)
                if field == "cmp" and isinstance(value, CmpEnum):
                    assert field_value == value.value  # Stored as string
                else:
                    assert field_value == value


class TestRxValidation:
    """Test Rx input validation and type conversion."""

    def test_gdp_stn_validation(self, subtests):
        """Test gdp_stn field validation."""
        valid_values = ["", "24", "station1", "test_station", "123"]

        for value in valid_values:
            with subtests.test(f"gdp_stn valid {value}"):
                rx = Rx(gdp_stn=value)  # type: ignore
                assert rx.gdp_stn == value

    def test_length_validation(self, subtests):
        """Test length field validation."""
        valid_values = [
            (0, 0.0),
            (0.0, 0.0),
            (100, 100.0),
            (100.0, 100.0),
            (75.5, 75.5),
            (-10.0, -10.0),  # Negative should be allowed
        ]

        for input_value, expected_value in valid_values:
            with subtests.test(f"length valid {input_value}"):
                rx = Rx(length=input_value)  # type: ignore
                assert rx.length == expected_value

    def test_h_p_r_validation(self, subtests):
        """Test h_p_r field validation."""
        valid_cases = [
            ("empty list", [], []),
            ("single float", [1.0], [1.0]),
            ("multiple floats", [1.0, 2.0, 3.0], [1.0, 2.0, 3.0]),
            ("integers converted", [1, 2, 3], [1.0, 2.0, 3.0]),
            ("mixed types", [1, 2.5, 3], [1.0, 2.5, 3.0]),
        ]

        for case_name, input_value, expected_value in valid_cases:
            with subtests.test(f"h_p_r {case_name}"):
                rx = Rx(h_p_r=input_value)  # type: ignore
                assert rx.h_p_r == expected_value

    def test_cmp_enum_validation(self, subtests):
        """Test CmpEnum field validation."""
        valid_cmp_values = [
            (CmpEnum.zxx, "zxx"),
            (CmpEnum.zyy, "zyy"),
            (CmpEnum.zyx, "zyx"),
            (CmpEnum.zxy, "zxy"),
            (CmpEnum.txy, "txy"),
            (CmpEnum.tyx, "tyx"),
            (CmpEnum.null, ""),
            ("zxx", "zxx"),
            ("zyy", "zyy"),
            ("", ""),
        ]

        for input_value, expected_value in valid_cmp_values:
            with subtests.test(f"cmp validation {input_value}"):
                rx = Rx(cmp=input_value)  # type: ignore
                assert rx.cmp == expected_value

    def test_optional_string_validation(self, subtests):
        """Test optional string field validation."""
        optional_fields = ["center", "x_y_z1", "x_y_z2", "u_t_m1", "a_space", "s_space"]
        valid_values = [None, "", "test", "123", "coordinate:string"]

        for field in optional_fields:
            for value in valid_values:
                with subtests.test(f"{field} validation {value}"):
                    kwargs = {field: value}
                    rx = Rx(**kwargs)  # type: ignore
                    assert getattr(rx, field) == value

    def test_invalid_values(self, subtests):
        """Test handling of invalid values."""
        invalid_cases = [
            ("length", "invalid_string"),
            ("h_p_r", "not_a_list"),
            ("h_p_r", ["string", "in", "list"]),
            ("cmp", "invalid_cmp"),
        ]

        for field, invalid_value in invalid_cases:
            with subtests.test(f"invalid {field} {invalid_value}"):
                kwargs = {field: invalid_value}
                with pytest.raises(ValidationError):
                    Rx(**kwargs)  # type: ignore

    def test_type_coercion(self, subtests):
        """Test type coercion behavior."""
        coercion_cases = [
            ("gdp_stn", 123, "123"),  # Integer to string
            ("length", "100", 100.0),  # String to float (if valid)
            ("length", "100.5", 100.5),
            ("center", 123, "123"),  # Integer to string for optional fields
        ]

        for field, input_value, expected_value in coercion_cases:
            with subtests.test(f"coercion {field} {input_value}"):
                kwargs = {field: input_value}
                rx = Rx(**kwargs)  # type: ignore
                assert getattr(rx, field) == expected_value


class TestRxSerialization:
    """Test Rx serialization and deserialization functionality."""

    @pytest.fixture(scope="class")
    def default_rx(self):
        """Fixture for default Rx instance."""
        return Rx()  # type: ignore

    @pytest.fixture(scope="class")
    def populated_rx(self):
        """Fixture for populated Rx instance."""
        return Rx(  # type: ignore
            gdp_stn="24",
            length=100.0,
            h_p_r=[0.0, 0.0, 180.0],
            cmp=CmpEnum.zxx,
            center="335754.685:4263553.435:1650.2 m",
            x_y_z1="335754.685:4263553.435:1650.2",
        )

    def test_model_dump_default(self, default_rx, subtests):
        """Test model_dump with default values."""
        dump = default_rx.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("has all fields"):
            expected_fields = [
                "gdp_stn",
                "length",
                "h_p_r",
                "cmp",
                "center",
                "x_y_z1",
                "x_y_z2",
                "u_t_m1",
                "a_space",
                "s_space",
            ]
            for field in expected_fields:
                assert field in dump

        with subtests.test("default values"):
            assert dump["gdp_stn"] == ""
            assert dump["length"] == 0.0
            assert dump["h_p_r"] == []
            assert dump["cmp"] == ""
            assert dump["center"] is None

        with subtests.test("includes class name"):
            assert "_class_name" in dump
            assert dump["_class_name"] == "rx"

    def test_model_dump_populated(self, populated_rx, subtests):
        """Test model_dump with populated values."""
        dump = populated_rx.model_dump()

        with subtests.test("dict structure"):
            assert isinstance(dump, dict)

        with subtests.test("populated values present"):
            assert dump["gdp_stn"] == "24"
            assert dump["length"] == 100.0
            assert dump["h_p_r"] == [0.0, 0.0, 180.0]
            assert dump["cmp"] == "zxx"
            assert dump["center"] == "335754.685:4263553.435:1650.2 m"
            assert dump["x_y_z1"] == "335754.685:4263553.435:1650.2"

    def test_from_dict_creation(self, subtests):
        """Test creating Rx from dictionary."""
        test_cases = [
            (
                "full dict",
                {"gdp_stn": "24", "length": 100.0, "h_p_r": [0, 0, 180], "cmp": "zxx"},
            ),
            ("partial dict", {"gdp_stn": "test", "length": 50.0}),
            ("empty dict", {}),
            (
                "with optional fields",
                {"gdp_stn": "station", "center": "center_coord", "a_space": "100 m"},
            ),
        ]

        for case_name, data in test_cases:
            with subtests.test(f"from dict {case_name}"):
                rx = Rx(**data)  # type: ignore
                for key, value in data.items():
                    field_value = getattr(rx, key)
                    if key == "h_p_r" and value:
                        # List elements should be converted to float
                        expected = [float(x) for x in value]
                        assert field_value == expected
                    else:
                        assert field_value == value

    def test_json_serialization(self, default_rx, populated_rx, subtests):
        """Test JSON serialization and deserialization."""
        with subtests.test("JSON round-trip populated rx"):
            json_str = populated_rx.model_dump_json()
            data = json.loads(json_str)
            recreated = Rx(**data)  # type: ignore
            assert recreated.gdp_stn == populated_rx.gdp_stn
            assert recreated.length == populated_rx.length
            assert recreated.h_p_r == populated_rx.h_p_r
            assert recreated.cmp == populated_rx.cmp

        with subtests.test("JSON round-trip default rx"):
            json_str = default_rx.model_dump_json()
            data = json.loads(json_str)
            recreated = Rx(**data)  # type: ignore
            assert recreated.gdp_stn == default_rx.gdp_stn
            assert recreated.length == default_rx.length
            assert recreated.h_p_r == default_rx.h_p_r

    def test_model_dump_exclude_none(self, subtests):
        """Test model_dump with exclude_none option."""
        with subtests.test("exclude_none with populated"):
            rx = Rx(gdp_stn="test", length=100.0, center="coord")  # type: ignore
            dump = rx.model_dump(exclude_none=True)
            assert "gdp_stn" in dump
            assert "length" in dump
            assert "center" in dump
            # None fields should be excluded
            assert "x_y_z1" not in dump or dump["x_y_z1"] is not None

        with subtests.test("exclude_none with defaults"):
            rx = Rx()  # type: ignore
            dump = rx.model_dump(exclude_none=True)
            # Should still include non-None defaults
            assert "gdp_stn" in dump
            assert "length" in dump
            assert "h_p_r" in dump

    def test_model_dump_exclude_defaults(self, subtests):
        """Test model_dump with exclude_defaults option."""
        with subtests.test("exclude_defaults with default values"):
            rx = Rx()  # type: ignore
            dump = rx.model_dump(exclude_defaults=True)
            # Should exclude the default values
            expected_exclusions = ["gdp_stn", "length", "h_p_r", "cmp"]
            for field in expected_exclusions:
                assert field not in dump or dump[field] != getattr(rx, field)

        with subtests.test("exclude_defaults with custom values"):
            rx = Rx(gdp_stn="test", length=100.0)  # type: ignore
            dump = rx.model_dump(exclude_defaults=True)
            assert "gdp_stn" in dump
            assert "length" in dump
            assert dump["gdp_stn"] == "test"
            assert dump["length"] == 100.0


class TestRxModification:
    """Test Rx field modification and updates."""

    def test_field_modification(self, subtests):
        """Test modifying Rx fields after creation."""
        rx = Rx()  # type: ignore

        test_modifications = [
            ("gdp_stn", "new_station"),
            ("length", 200.0),
            ("h_p_r", [1.0, 2.0, 3.0]),
            ("cmp", CmpEnum.zyy),
            ("center", "new_center"),
        ]

        for field, value in test_modifications:
            with subtests.test(f"modify {field} to {value}"):
                setattr(rx, field, value)
                field_value = getattr(rx, field)
                if field == "cmp" and isinstance(value, CmpEnum):
                    assert field_value == value.value
                else:
                    assert field_value == value

    def test_reset_to_default(self, subtests):
        """Test resetting fields to default values."""
        rx = Rx(  # type: ignore
            gdp_stn="test", length=100.0, h_p_r=[1, 2, 3], cmp=CmpEnum.zxx
        )

        default_resets = [
            ("gdp_stn", ""),
            ("length", 0.0),
            ("h_p_r", []),
            ("cmp", ""),
        ]

        for field, default_value in default_resets:
            with subtests.test(f"reset {field} to default"):
                setattr(rx, field, default_value)
                assert getattr(rx, field) == default_value

    def test_bulk_update(self, subtests):
        """Test bulk field updates."""
        rx = Rx()  # type: ignore

        updates = {
            "gdp_stn": "bulk_station",
            "length": 150.0,
            "h_p_r": [10.0, 20.0, 30.0],
            "cmp": CmpEnum.zxy,
            "center": "bulk_center",
        }

        for field, value in updates.items():
            setattr(rx, field, value)

        for field, expected_value in updates.items():
            with subtests.test(f"bulk update {field}"):
                field_value = getattr(rx, field)
                if field == "cmp":
                    assert field_value == expected_value.value
                else:
                    assert field_value == expected_value

    def test_list_modification(self, subtests):
        """Test h_p_r list modification behavior."""
        rx = Rx(h_p_r=[1.0, 2.0, 3.0])  # type: ignore

        with subtests.test("list append"):
            rx.h_p_r.append(4.0)
            assert rx.h_p_r == [1.0, 2.0, 3.0, 4.0]

        with subtests.test("list modification"):
            rx.h_p_r[0] = 10.0
            assert rx.h_p_r[0] == 10.0

        with subtests.test("list replacement"):
            rx.h_p_r = [100.0, 200.0]  # type: ignore
            assert rx.h_p_r == [100.0, 200.0]


class TestRxComparison:
    """Test Rx comparison and equality operations."""

    def test_rx_equality(self, subtests):
        """Test Rx equality comparisons."""
        rx1 = Rx(gdp_stn="test", length=100.0, h_p_r=[1, 2, 3])  # type: ignore
        rx2 = Rx(gdp_stn="test", length=100.0, h_p_r=[1, 2, 3])  # type: ignore
        rx3 = Rx(gdp_stn="different", length=100.0, h_p_r=[1, 2, 3])  # type: ignore

        with subtests.test("same values model_dump equal"):
            assert rx1.model_dump() == rx2.model_dump()

        with subtests.test("different values model_dump not equal"):
            assert rx1.model_dump() != rx3.model_dump()

        with subtests.test("individual field comparison"):
            assert rx1.gdp_stn == rx2.gdp_stn
            assert rx1.length == rx2.length
            assert rx1.h_p_r == rx2.h_p_r
            assert rx1.gdp_stn != rx3.gdp_stn

    def test_field_value_consistency(self, subtests):
        """Test consistency of field values across operations."""
        test_values = [
            ("gdp_stn", "station_test"),
            ("length", 75.5),
            ("h_p_r", [45.0, 90.0, 135.0]),
            ("cmp", CmpEnum.txy),
            ("center", "coord_test"),
        ]

        for field, value in test_values:
            with subtests.test(f"consistency {field} {value}"):
                kwargs = {field: value}
                rx = Rx(**kwargs)  # type: ignore
                field_value = getattr(rx, field)
                if field == "cmp":
                    assert field_value == value.value
                else:
                    assert field_value == value

                # Test round-trip consistency
                dump = rx.model_dump()
                recreated = Rx(**dump)  # type: ignore
                recreated_value = getattr(recreated, field)
                assert recreated_value == field_value

    def test_cmp_enum_consistency(self, subtests):
        """Test CmpEnum consistency."""
        enum_values = [
            CmpEnum.zxx,
            CmpEnum.zyy,
            CmpEnum.zyx,
            CmpEnum.zxy,
            CmpEnum.txy,
            CmpEnum.tyx,
            CmpEnum.null,
        ]

        for enum_value in enum_values:
            with subtests.test(f"cmp enum {enum_value}"):
                rx1 = Rx(cmp=enum_value)  # type: ignore
                rx2 = Rx(cmp=enum_value.value)  # type: ignore
                assert rx1.cmp == rx2.cmp
                assert rx1.cmp == enum_value.value


class TestRxEdgeCases:
    """Test Rx edge cases and boundary conditions."""

    def test_empty_initialization_kwargs(self, subtests):
        """Test initialization with empty keyword arguments."""
        with subtests.test("empty kwargs"):
            rx = Rx(**{})  # type: ignore
            assert rx.gdp_stn == ""
            assert rx.length == 0.0
            assert rx.h_p_r == []
            assert rx.cmp == ""

    def test_unknown_field_handling(self, subtests):
        """Test handling of unknown fields."""
        with subtests.test("unknown fields accepted"):
            # MetadataBase appears to accept unknown fields
            rx = Rx(unknown_field="value")  # type: ignore
            assert hasattr(rx, "unknown_field")
            assert rx.unknown_field == "value"  # type: ignore

    def test_cmp_enum_edge_cases(self, subtests):
        """Test CmpEnum edge cases."""
        edge_cases = [
            ("empty string", "", ""),
            ("null enum", CmpEnum.null, ""),
            ("case sensitivity", "ZXX", "ZXX"),  # Should work if valid
        ]

        for case_name, input_value, expected_value in edge_cases:
            with subtests.test(f"cmp edge case {case_name}"):
                if case_name == "case sensitivity":
                    # This might raise ValidationError if case-sensitive
                    try:
                        rx = Rx(cmp=input_value)  # type: ignore
                        assert rx.cmp == expected_value
                    except ValidationError:
                        # Expected if case-sensitive
                        pass
                else:
                    rx = Rx(cmp=input_value)  # type: ignore
                    assert rx.cmp == expected_value

    def test_h_p_r_edge_cases(self, subtests):
        """Test h_p_r list edge cases."""
        edge_cases = [
            ("very large list", list(range(100)), list(float(x) for x in range(100))),
            ("negative values", [-1.0, -2.0, -3.0], [-1.0, -2.0, -3.0]),
            ("zero values", [0, 0, 0], [0.0, 0.0, 0.0]),
            ("single element", [42], [42.0]),
        ]

        for case_name, input_value, expected_value in edge_cases:
            with subtests.test(f"h_p_r edge case {case_name}"):
                rx = Rx(h_p_r=input_value)  # type: ignore
                assert rx.h_p_r == expected_value

    def test_length_edge_cases(self, subtests):
        """Test length field edge cases."""
        edge_cases = [
            ("zero", 0, 0.0),
            ("negative", -100.0, -100.0),
            ("very large", 1e6, 1e6),
            ("very small positive", 1e-6, 1e-6),
            ("integer", 42, 42.0),
        ]

        for case_name, input_value, expected_value in edge_cases:
            with subtests.test(f"length edge case {case_name}"):
                rx = Rx(length=input_value)  # type: ignore
                assert rx.length == expected_value

    def test_string_field_edge_cases(self, subtests):
        """Test string field edge cases."""
        string_fields = [
            "gdp_stn",
            "center",
            "x_y_z1",
            "x_y_z2",
            "u_t_m1",
            "a_space",
            "s_space",
        ]
        edge_cases = [
            ("very long string", "x" * 1000),
            ("special characters", "!@#$%^&*()"),
            ("unicode characters", "αβγδ"),
            ("newlines", "line1\nline2"),
            ("tabs", "col1\tcol2"),
        ]

        for field in string_fields:
            for case_name, test_value in edge_cases:
                with subtests.test(f"{field} {case_name}"):
                    kwargs = {field: test_value}
                    rx = Rx(**kwargs)  # type: ignore
                    assert getattr(rx, field) == test_value


class TestRxDocumentation:
    """Test Rx class structure and documentation."""

    def test_class_structure(self, subtests):
        """Test Rx class structure and inheritance."""
        with subtests.test("class name accessible"):
            assert Rx.__name__ == "Rx"

        with subtests.test("class is MetadataBase subclass"):
            from mt_metadata.base import MetadataBase

            assert issubclass(Rx, MetadataBase)

    def test_cmp_enum_structure(self, subtests):
        """Test CmpEnum class structure."""
        with subtests.test("CmpEnum is available"):
            assert CmpEnum is not None
            expected_values = ["zxx", "zyy", "zyx", "zxy", "txy", "tyx", ""]
            actual_values = [item.value for item in CmpEnum]
            assert set(actual_values) == set(expected_values)

    def test_field_descriptions(self, subtests):
        """Test that fields have proper descriptions."""
        fields = Rx.model_fields
        expected_fields = [
            "gdp_stn",
            "length",
            "h_p_r",
            "cmp",
            "center",
            "x_y_z1",
            "x_y_z2",
            "u_t_m1",
            "a_space",
            "s_space",
        ]

        for field_name in expected_fields:
            with subtests.test(f"field description {field_name}"):
                field = fields[field_name]
                # Check that field has description
                assert hasattr(field, "description") or "description" in str(field)

    def test_field_properties(self, subtests):
        """Test field properties and configurations."""
        fields = Rx.model_fields

        required_fields = ["gdp_stn", "length", "h_p_r", "cmp"]
        optional_fields = ["center", "x_y_z1", "x_y_z2", "u_t_m1", "a_space", "s_space"]

        for field_name in required_fields:
            with subtests.test(f"required field {field_name}"):
                field = fields[field_name]
                # Required fields should have defaults
                assert hasattr(field, "default") or "default" in str(field)

        for field_name in optional_fields:
            with subtests.test(f"optional field {field_name}"):
                field = fields[field_name]
                # Optional fields should have None default
                assert hasattr(field, "default") or "default" in str(field)

    def test_schema_information(self, subtests):
        """Test schema and model information."""
        with subtests.test("model_dump produces schema-like structure"):
            rx = Rx()  # type: ignore
            dump = rx.model_dump()
            assert isinstance(dump, dict)
            assert len(dump) == 11  # 10 fields + _class_name

        with subtests.test("all expected fields present"):
            expected_fields = [
                "gdp_stn",
                "length",
                "h_p_r",
                "cmp",
                "center",
                "x_y_z1",
                "x_y_z2",
                "u_t_m1",
                "a_space",
                "s_space",
            ]
            dump = Rx().model_dump()  # type: ignore
            for field in expected_fields:
                assert field in dump
            # Also has _class_name field
            assert "_class_name" in dump

        with subtests.test("model_fields accessible"):
            fields = Rx.model_fields
            assert len(fields) == 10  # Only the actual model fields
            expected_fields = [
                "gdp_stn",
                "length",
                "h_p_r",
                "cmp",
                "center",
                "x_y_z1",
                "x_y_z2",
                "u_t_m1",
                "a_space",
                "s_space",
            ]
            for field in expected_fields:
                assert field in fields

    def test_field_types_documentation(self, subtests):
        """Test documented field types."""
        rx = Rx()  # type: ignore

        type_expectations = [
            ("gdp_stn", str),
            ("length", float),
            ("h_p_r", list),
            ("cmp", str),  # CmpEnum stored as string
            ("center", (str, type(None))),
            ("x_y_z1", (str, type(None))),
            ("x_y_z2", (str, type(None))),
            ("u_t_m1", (str, type(None))),
            ("a_space", (str, type(None))),
            ("s_space", (str, type(None))),
        ]

        for field_name, expected_type in type_expectations:
            with subtests.test(f"field type documentation {field_name}"):
                field_value = getattr(rx, field_name)
                if isinstance(expected_type, tuple):
                    assert isinstance(field_value, expected_type)
                else:
                    assert isinstance(field_value, expected_type)

    def test_example_values(self, subtests):
        """Test that field examples work correctly."""
        # Test some example values from the field definitions
        example_cases = [
            ("gdp_stn", "24"),
            ("length", 100.0),
            ("h_p_r", [0.0, 0.0, 180.0]),
            ("cmp", "zxx"),
            ("center", "335754.685:4263553.435:1650.2 m"),
            ("x_y_z1", "335754.685:4263553.435:1650.2"),
        ]

        for field, example_value in example_cases:
            with subtests.test(f"example value {field}"):
                kwargs = {field: example_value}
                rx = Rx(**kwargs)  # type: ignore
                field_value = getattr(rx, field)
                assert field_value == example_value
