"""
This is a placeholder module.  See github issue #30

In the mt_metadata packaage, the standard is that units are described by all
lower case strings.

The dictionaries UNITS is keyed by these lower
case strings.

"""

# =============================================================================
# Import
# =============================================================================
import pandas as pd
from typing import Annotated
from collections import OrderedDict
from loguru import logger

from pydantic import BaseModel, Field, ConfigDict, AliasChoices

# =============================================================================

# Define SI prefixes
prefixes = {
    "": "",
    "yotta": "Y",
    "zetta": "Z",
    "exa": "E",
    "peta": "P",
    "tera": "T",
    "giga": "G",
    "mega": "M",
    "kilo": "k",
    "hecto": "h",
    "deca": "da",
    "deci": "d",
    "centi": "c",
    "milli": "m",
    "micro": "μ",
    "nano": "n",
    "pico": "p",
    "femto": "f",
    "atto": "a",
    "zepto": "z",
    "yocto": "y",
}

# Define base units
base_units = {
    "meter": {"symbol": "m", "description": "Unit of length", "unicode_symbol": "m"},
    "kilogram": {"symbol": "kg", "description": "Unit of mass", "unicode_symbol": "kg"},
    "second": {"symbol": "s", "description": "Unit of time", "unicode_symbol": "s"},
    "ampere": {
        "symbol": "A",
        "description": "Unit of electric current",
        "unicode_symbol": "A",
    },
    "kelvin": {
        "symbol": "K",
        "description": "Unit of thermodynamic temperature",
        "unicode_symbol": "K",
    },
    "mole": {
        "symbol": "mol",
        "description": "Unit of amount of substance",
        "unicode_symbol": "mol",
    },
    "candela": {
        "symbol": "cd",
        "description": "Unit of luminous intensity",
        "unicode_symbol": "cd",
    },
    "radian": {
        "symbol": "rad",
        "description": "Unit of angle",
        "unicode_symbol": "rad",
    },
}

# Define derived units
derived_units = {
    "hertz": {
        "symbol": "Hz",
        "description": "Unit of frequency",
        "unicode_symbol": "Hz",
    },
    "newton": {"symbol": "N", "description": "Unit of force", "unicode_symbol": "N"},
    "joule": {"symbol": "J", "description": "Unit of energy", "unicode_symbol": "J"},
    "watt": {"symbol": "W", "description": "Unit of power", "unicode_symbol": "W"},
    "pascal": {
        "symbol": "Pa",
        "description": "Unit of pressure",
        "unicode_symbol": "Pa",
    },
    "coulomb": {
        "symbol": "C",
        "description": "Unit of electric charge",
        "unicode_symbol": "C",
    },
    "volt": {
        "symbol": "V",
        "description": "Unit of electric potential",
        "unicode_symbol": "V",
    },
    "ohm": {
        "symbol": "Ω",
        "description": "Unit of electrical resistance",
        "unicode_symbol": "\u03a9",
    },
    "siemens": {
        "symbol": "S",
        "description": "Unit of electrical conductance",
        "unicode_symbol": "S",
    },
    "weber": {
        "symbol": "Wb",
        "description": "Unit of magnetic flux",
        "unicode_symbol": "Wb",
    },
    "tesla": {
        "symbol": "T",
        "description": "Unit of magnetic flux density",
        "unicode_symbol": "T",
    },
    "henry": {
        "symbol": "H",
        "description": "Unit of inductance",
        "unicode_symbol": "H",
    },
}

# Combine prefixes with base and derived units
all_units = [
    {
        "name": "unknown",
        "description": "unknown",
        "symbol": "unknown",
        "plot_label": "Unknown",
    },
    {
        "name": "digital counts",
        "description": "digital counts from data logger",
        "symbol": "count",
        "plot_label": "Digital Counts",
    },
    {
        "name": "digital counts",
        "description": "digital counts from data logger",
        "symbol": "counts",
        "plot_label": "Digital Counts",
    },
    {
        "name": "samples",
        "description": "number of samples",
        "symbol": "samples",
        "plot_label": "Samples",
    },
    {
        "name": "celsius",
        "description": "Unit of temperature",
        "symbol": "C",
        "plot_label": "Celsius",
    },
]
for prefix_name, prefix_symbol in prefixes.items():
    for unit_name, unit_details in {**base_units, **derived_units}.items():
        all_units.append(
            {
                "name": f"{prefix_name}{unit_name}",
                "symbol": f"{prefix_symbol}{unit_details['symbol']}",
                "description": f"{prefix_name.capitalize()} {unit_details['description']}",
                "plot_label": f"{prefix_symbol}{unit_details['unicode_symbol']}",
            }
        )

# Convert to a pandas DataFrame
UNITS_DF = pd.DataFrame(all_units)


class Unit(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        extra="allow",
        use_enum_values=True,
        coerce_numbers_to_str=True,
    )

    name: Annotated[str, Field(default=None, description="Common name of the unit.")]
    description: Annotated[
        str, Field(default=None, description="Description of the unit.")
    ]
    symbol: Annotated[
        str,
        Field(
            default=None,
            description="Symbol like representation of the unit",
            validation_alias=AliasChoices("symbol", "abbrviation"),
        ),
    ]
    plot_label: Annotated[
        str, Field(default=None, description="Plot label of the unit.")
    ]

    def __str__(self):
        lines = [
            f"name:         {self.name}",
            f"description:  {self.description}",
            f"symbol: {self.symbol}",
            f"plot_label:   {self.plot_label}",
        ]
        return "\n".join(lines)

    def __repr__(self):
        return self.__str__()

    def combine(self, other, separator="/"):
        """
        Combine two unit objects into a single string representation.

        Parameters
        ----------
        other : Unit
            The other unit object to combine with.
        separator : str, optional
            The separator to use between the two units, by default "/"

        Returns
        -------
        str
            Combined string representation of the two units.
        """
        if not isinstance(other, Unit):
            raise TypeError("The other object must be an instance of the Unit class.")

        if separator in ["/", "per", " per "]:
            name_separator = " per "
            symbol_separator = "/"
        else:
            name_separator = " "
            symbol_separator = " "

        combined_unit = Unit(
            name=f"{self.name}{name_separator}{other.name}",
            description=f"{self.description}{name_separator}{other.description}",
            symbol=f"{self.symbol}{symbol_separator}{other.symbol}",
            plot_label=f"{self.plot_label}{symbol_separator}{other.plot_label}",
        )
        return combined_unit

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "symbol": self.symbol,
            "plot_label": self.plot_label,
        }

    def from_dict(self, value):
        for k, v in value.items():
            setattr(self, k, v)


def find_separator(unit_string: str) -> str:
    """
    Find the first separator in a unit string.

    Parameters
    ----------
    unit_string : str
        The unit string to search for separators.

    Returns
    -------
    str
        The first separator found in the unit string.
    """

    find_dict = {}
    for sep in ["/", " per ", " "]:
        find_dict[sep] = unit_string.find(sep)
    # Sort the dictionary by the index of the separator in the unit string
    # and return the first separator found
    find_dict = OrderedDict(sorted(find_dict.items(), key=lambda item: item[1]))
    for sep in find_dict.keys():
        if find_dict[sep] > -1:
            return sep
    return


def parse_unit_string(unit_string: str) -> list[dict]:
    """
    Parse a unit string into a list of units and separators, including nested units and brackets.

    Parameters
    ----------
    unit_string : str
        The unit string to parse (e.g., "mV nT/[km ohm]").

    Returns
    -------
    list[dict]
        A list of dictionaries, each containing a unit name and its separator.
        Example: [{"name": "mV", "sep": " "}, {"name": "nT", "sep": "/"}, {"name": "[", "sep": None},
                  {"name": "km", "sep": " "}, {"name": "ohm", "sep": None}, {"name": "]", "sep": None}]
    """
    if not isinstance(unit_string, str):
        raise TypeError("The unit_string must be a string.")
    unit_string = unit_string.replace("[", "").replace("]", "")
    result = []
    separator = ""
    while separator != None:
        separator = find_separator(unit_string)
        parts = unit_string.split(separator, 1)
        if parts == []:
            break

        if parts[0].strip() not in ["", " per "]:
            result.append({"name": parts[0].strip(), "sep": separator})
        try:
            unit_string = parts[1].strip()
        except IndexError:
            break
    # change order of separators
    if len(result) == 0:
        raise ValueError("No unit found in the unit string.")
    elif len(result) == 1:
        return result
    elif len(result) > 1:
        new_result = [result[0].copy()]
        new_result[0]["sep"] = ""
        for index, entry in enumerate(result[1:], start=0):
            new_result.append({"name": entry["name"], "sep": result[index]["sep"]})
        return new_result


def get_unit_object(unit: str, allow_none=True) -> Unit:
    """
    From the unit name or symbol return a Unit object.
    This function will search the unit name, symbol and
    plot_label for a match.
    If the unit is not found, a KeyError will be raised.
    If allow_none is True, None will be returned if the unit is not found.


    Parameters
    ----------
    unit : str
        name or symbol of the unit to search for.
    allow_none : bool, optional
        If the unit isn't found return an empty unit of unknons,
        by default True

    Returns
    -------
    Unit
        Unit object with the unit name, symbol, description and plot_label.

    Raises
    ------
    KeyError
        If the unit is not found in the DataFrame.
    """

    units_parts = parse_unit_string(unit)
    if len(units_parts) == 1:
        return get_unit_from_df(units_parts[0]["name"], allow_none=allow_none)
    elif len(units_parts) == 0:
        raise ValueError(f"No unit found in the unit string.")
    elif len(units_parts) > 1:
        unit = get_unit_from_df(units_parts[0]["name"], allow_none=allow_none)
        for entry in units_parts[1:]:
            unit = unit.combine(
                get_unit_from_df(entry["name"], allow_none=allow_none),
                separator=entry["sep"],
            )

    return unit


def get_unit_from_df(value: str, allow_none=True) -> Unit:
    """
    Retrieve a row from the UNITS_DF DataFrame based on the unit's name or symbol.

    Parameters
    ----------
    value : str
        The name or symbol of the unit to search for.

    Returns
    -------
    pd.Series
        A row from the UNITS_DF DataFrame corresponding to the given name or symbol.

    Raises
    ------
    KeyError
        If the unit is not found in the DataFrame.
    """
    # Search for the unit by name or symbol
    unit_row = UNITS_DF[
        (UNITS_DF["name"].str.lower() == value.lower()) | (UNITS_DF["symbol"] == value)
    ]

    # Check if a match was found
    if not unit_row.empty:
        return Unit(
            **unit_row.iloc[0].to_dict()
        )  # Return the first matching row as a Series
    else:
        if allow_none:
            logger.warning(
                f"Unit '{value}' not found in accepted units, setting to 'unknown'. "
                "If this is an error raise an issue to add a unit. If an error needs "
                "to be raised, set allow_none=False."
            )
            return Unit(
                name="unknown",
                description="unknown",
                symbol="unknown",
                plot_label="Unknown",
            )
        else:
            raise KeyError(
                f"Unit '{value}' not found in the UNITS_DF DataFrame. "
                "If the units are real an need to be added raise an issue to add the unit."
            )
