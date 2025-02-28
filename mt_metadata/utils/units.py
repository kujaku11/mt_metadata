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

# =============================================================================


class Unit:
    def __init__(self, **kwargs):
        self.name = None
        self.description = None
        self.abbreviation = None
        self.plot_label = None
        self.alias = None

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        lines = [
            f"name:         {self.name}",
            f"description:  {self.description}",
            f"abbreviation: {self.abbreviation}",
            f"plot_label:   {self.plot_label}",
            f"alias:        {self.alias}",
        ]
        return "\n".join(lines)

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "abbreviation": self.abbreviation,
            "plot_label": self.plot_label,
            "alias": self.alias,
        }

    def from_dict(self, value):
        for k, v in value.items():
            setattr(self, k, v)


# List of available units
UNITS_LIST = [
    {
        "name": "unknown",
        "description": "unknown",
        "abbreviation": "unknown",
        "plot_label": "Unknown",
        "alias": "unknown",
    },
    {
        "name": "digital counts",
        "description": "digital counts from data logger",
        "abbreviation": "count",
        "plot_label": "Digital Counts",
        "alias": "counts",
    },
    {
        "name": "volt",
        "description": "electric potential",
        "abbreviation": "V",
        "plot_label": "Volt",
        "alias": "volts",
    },
    {
        "name": "millivolt",
        "description": "electric potential",
        "abbreviation": "mV",
        "plot_label": "milliVolt",
        "alias": "millivolts",
    },
    {
        "name": "microvolt",
        "description": "electric potential",
        "abbreviation": "\u03BCV",
        "plot_label": "microVolt",
        "alias": "microvolts",
    },
    {
        "name": "tesla",
        "description": "magnetic field",
        "abbreviation": "T",
        "plot_label": "Tesla",
        "alias": "",
    },
    {
        "name": "millitesla",
        "description": "magnetic field",
        "abbreviation": "mT",
        "plot_label": "milliTesla",
        "alias": "",
    },
    {
        "name": "microtesla",
        "description": "magnetic field",
        "abbreviation": "\u03BCT",
        "plot_label": "microTesla",
        "alias": "",
    },
    {
        "name": "nanotesla",
        "description": "magnetic field",
        "abbreviation": "nT",
        "plot_label": "nanoTesla",
        "alias": "",
    },
    {
        "name": "volt per meter",
        "description": "electric field",
        "abbreviation": "V/m",
        "plot_label": "Volt per Meter",
        "alias": "volts per meter",
    },
    {
        "name": "volt per kilometer",
        "description": "electric field",
        "abbreviation": "V/km",
        "plot_label": "Volt per Kilometer",
        "alias": "volts per kilometer",
    },
    {
        "name": "millivolt per kilometer",
        "description": "electric field",
        "abbreviation": "mV/km",
        "plot_label": "milliVolt per Kilometer",
        "alias": "millivolts per kilometer",
    },
    {
        "name": "millivolt per meter",
        "description": "electric field",
        "abbreviation": "mV/m",
        "plot_label": "milliVolt per meter",
        "alias": "millivolts per meter",
    },
    {
        "name": "microvolt per meter",
        "description": "electric field",
        "abbreviation": "\u03BCV/m",
        "plot_label": "microVolt per Meter",
        "alias": "microvolts per meter",
    },
    {
        "name": "millivolt per kilometer per nanotesla",
        "description": "EM transfer function",
        "abbreviation": "mV/km/nT",
        "plot_label": "[mV/km]/[nT]",
        "alias": "millivolts per kilometer per nanotesla",
    },
    {
        "name": "volt per meter per tesla",
        "description": "EM transfer function",
        "abbreviation": "V/m/T",
        "plot_label": "[V/m]/[T]",
        "alias": "volts per meter per tesla",
    },
    {
        "name": "meter",
        "description": "length",
        "abbreviation": "m",
        "plot_label": "Meter",
        "alias": "meters",
    },
    {
        "name": "kilometer",
        "description": "length",
        "abbreviation": "km",
        "plot_label": "Kilometer",
        "alias": "kilometers",
    },
    {
        "name": "celsius",
        "description": "temperature",
        "abbreviation": "C",
        "plot_label": "Celsius",
        "alias": "celsius",
    },
]

# put the units into a data frame for easier searching
UNITS_DF = pd.DataFrame(UNITS_LIST)


def get_unit_object(unit, allow_none=True):
    """

    :param unit: unit name or abbreviation
    :type value: string
    :return: unit dictionary
    :rtype: dict

    """

    # try to find in name first
    def get_df(col, value):
        if value is None:
            if allow_none:
                value = "unknown"
            else:
                return None

        unit_df = UNITS_DF[UNITS_DF[col].str.lower() == value.lower()]
        if len(unit_df) == 1:
            unit_dict = unit_df.to_dict("records")[0]
            return Unit(**unit_dict)

        elif len(unit_df) == 0:
            return None

    for col in ["name", "abbreviation", "alias"]:
        unit_df = get_df(col, unit)
        if unit_df is not None:
            return unit_df

    if unit_df is None:
        raise KeyError(
            f"Could not find {unit} in accetable units.  "
            "See mt_metadata.utils.units.py for more information"
        )
