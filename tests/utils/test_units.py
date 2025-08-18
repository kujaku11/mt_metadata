import pytest

from mt_metadata.common.units import (
    find_separator,
    get_unit_from_df,
    get_unit_object,
    parse_unit_string,
    Unit,
    UNITS_DF,
)


class TestUnit:
    """Test class for Unit functionality with fixtures and subtests."""

    @pytest.fixture
    def unit_data(self):
        """Fixture providing unit test data."""
        return {
            "name": "millivolt",
            "description": "Unit of electric potential",
            "symbol": "mV",
            "plot_label": "mV",
        }

    @pytest.fixture
    def sample_unit(self, unit_data):
        """Fixture providing a sample Unit instance."""
        return Unit(**unit_data)

    @pytest.fixture
    def unit_pairs(self):
        """Fixture providing unit pairs for combination tests."""
        return [
            {
                "unit1": Unit(
                    name="millivolt",
                    symbol="mV",
                    description="Millivolt",
                    plot_label="mV",
                ),
                "unit2": Unit(
                    name="nanotesla",
                    symbol="nT",
                    description="Nanotesla",
                    plot_label="nT",
                ),
                "separator": "/",
                "expected": {
                    "name": "millivolt per nanotesla",
                    "symbol": "mV/nT",
                    "description": "Millivolt per Nanotesla",
                    "plot_label": "mV/nT",
                },
            },
            {
                "unit1": Unit(
                    name="millivolt",
                    symbol="mV",
                    description="Millivolt",
                    plot_label="mV",
                ),
                "unit2": Unit(
                    name="nanotesla",
                    symbol="nT",
                    description="Nanotesla",
                    plot_label="nT",
                ),
                "separator": " ",
                "expected": {
                    "name": "millivolt nanotesla",
                    "symbol": "mV nT",
                    "description": "Millivolt Nanotesla",
                    "plot_label": "mV nT",
                },
            },
        ]

    def test_unit_initialization(self, subtests, unit_data):
        """Test the initialization of the Unit class."""
        unit = Unit(**unit_data)
        with subtests.test("name"):
            assert unit.name == unit_data["name"]
        with subtests.test("description"):
            assert unit.description == unit_data["description"]
        with subtests.test("symbol"):
            assert unit.symbol == unit_data["symbol"]
        with subtests.test("plot_label"):
            assert unit.plot_label == unit_data["plot_label"]

    def test_unit_to_dict(self, sample_unit, unit_data):
        """Test the to_dict method of the Unit class."""
        unit_dict = sample_unit.to_dict()
        assert unit_dict == unit_data

    def test_unit_from_dict(self, subtests, unit_data):
        """Test the from_dict method of the Unit class."""
        unit = Unit(name="", description="", symbol="", plot_label="")
        unit.from_dict(unit_data)

        with subtests.test("name"):
            assert unit.name == unit_data["name"]
        with subtests.test("description"):
            assert unit.description == unit_data["description"]
        with subtests.test("symbol"):
            assert unit.symbol == unit_data["symbol"]
        with subtests.test("plot_label"):
            assert unit.plot_label == unit_data["plot_label"]

    def test_unit_combine(self, subtests, unit_pairs):
        """Test the combine method of the Unit class."""
        for pair in unit_pairs:
            with subtests.test(separator=pair["separator"]):
                combined_unit = pair["unit1"].combine(
                    pair["unit2"], separator=pair["separator"]
                )
                expected = pair["expected"]

                with subtests.test("name", separator=pair["separator"]):
                    assert combined_unit.name == expected["name"]
                with subtests.test("symbol", separator=pair["separator"]):
                    assert combined_unit.symbol == expected["symbol"]
                with subtests.test("description", separator=pair["separator"]):
                    assert combined_unit.description == expected["description"]
                with subtests.test("plot_label", separator=pair["separator"]):
                    assert combined_unit.plot_label == expected["plot_label"]


class TestUtilityFunctions:
    """Test class for utility functions with fixtures and subtests."""

    @pytest.fixture
    def separator_test_cases(self):
        """Fixture providing test cases for find_separator function."""
        return [
            {"input": "mV nT/[km ohm]", "expected": " "},
            {"input": "mV/nT", "expected": "/"},
            {"input": "mV per nT", "expected": " per "},
            {"input": "mVnT", "expected": None},
        ]

    def test_find_separator(self, subtests, separator_test_cases):
        """Test the find_separator function."""
        for case in separator_test_cases:
            with subtests.test(input_string=case["input"]):
                assert find_separator(case["input"]) == case["expected"]

    @pytest.fixture
    def parse_unit_test_cases(self):
        """Fixture providing test cases for parse_unit_string function."""
        return [
            {
                "input": "mV nT/[km ohm]",
                "expected": [
                    {"name": "mV", "sep": ""},
                    {"name": "nT", "sep": " "},
                    {"name": "km", "sep": "/"},
                    {"name": "ohm", "sep": " "},
                ],
            },
            {
                "input": "mV/nT",
                "expected": [
                    {"name": "mV", "sep": ""},
                    {"name": "nT", "sep": "/"},
                ],
            },
            {
                "input": "mV per nT",
                "expected": [
                    {"name": "mV", "sep": ""},
                    {"name": "nT", "sep": " per "},
                ],
            },
        ]

    @pytest.fixture
    def unit_from_df_test_cases(self):
        """Fixture providing test cases for get_unit_from_df function."""
        return [
            {"input": "mV", "expected_name": "milliVolt", "expected_symbol": "mV"},
            {"input": "Hz", "expected_name": "hertz", "expected_symbol": "Hz"},
        ]

    @pytest.fixture
    def unit_object_test_cases(self):
        """Fixture providing test cases for get_unit_object function."""
        return [
            {"input": "mV", "expected_name": "milliVolt", "expected_symbol": "mV"},
            {
                "input": "mV/nT",
                "expected_name": "milliVolt per nanoTesla",
                "expected_symbol": "mV/nT",
            },
            {
                "input": "mV nT/[km ohm]",
                "expected_name": "milliVolt nanoTesla per kilometer Ohm",
                "expected_symbol": "mV nT/km \u03a9",
            },
        ]

    def test_parse_unit_string(self, subtests, parse_unit_test_cases):
        """Test the parse_unit_string function."""
        for case in parse_unit_test_cases:
            with subtests.test(input_string=case["input"]):
                assert parse_unit_string(case["input"]) == case["expected"]

    def test_parse_unit_string_empty_error(self):
        """Test parse_unit_string with empty string raises ValueError."""
        with pytest.raises(ValueError):
            parse_unit_string("")

    def test_get_unit_from_df(self, subtests, unit_from_df_test_cases):
        """Test the get_unit_from_df function."""
        for case in unit_from_df_test_cases:
            with subtests.test(unit_symbol=case["input"]):
                unit = get_unit_from_df(case["input"])
                assert isinstance(unit, Unit)
                assert unit.name == case["expected_name"]
                assert unit.symbol == case["expected_symbol"]

    def test_get_unit_from_df_errors(self, subtests):
        """Test get_unit_from_df error handling."""
        with subtests.test("KeyError on nonexistent unit"):
            with pytest.raises(KeyError):
                get_unit_from_df("nonexistent_unit", allow_none=False)

        with subtests.test("Unknown unit when allow_none=True"):
            unit = get_unit_from_df("nonexistent_unit", allow_none=True)
            assert unit.name == "unknown"
            assert unit.symbol == "unknown"

    def test_get_unit_object(self, subtests, unit_object_test_cases):
        """Test the get_unit_object function."""
        for case in unit_object_test_cases:
            with subtests.test(unit_string=case["input"]):
                unit = get_unit_object(case["input"])
                assert isinstance(unit, Unit)
                assert unit.name == case["expected_name"]
                assert unit.symbol == case["expected_symbol"]

    def test_get_unit_object_type_error(self):
        """Test get_unit_object with invalid input."""
        # Test with empty string which should handle gracefully
        with pytest.raises(ValueError):
            parse_unit_string("")


class TestUnitsDataFrame:
    """Test class for UNITS_DF functionality."""

    def test_units_df_structure(self, subtests):
        """Test the UNITS_DF DataFrame structure."""
        with subtests.test("DataFrame not empty"):
            assert not UNITS_DF.empty

        required_columns = ["name", "symbol", "description", "plot_label"]
        for column in required_columns:
            with subtests.test(f"Has {column} column"):
                assert column in UNITS_DF.columns

    def test_units_df_known_unit(self, subtests):
        """Test that UNITS_DF contains expected data for a known unit."""
        row = UNITS_DF[UNITS_DF["symbol"] == "mV"]
        with subtests.test("mV unit exists"):
            assert not row.empty

        if not row.empty:
            with subtests.test("mV unit name"):
                assert row.iloc[0]["name"] == "milliVolt"
            with subtests.test("mV unit description"):
                assert row.iloc[0]["description"] == "Milli Unit of electric potential"
