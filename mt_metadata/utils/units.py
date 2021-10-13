"""
This is a placeholder module.  See github issue #30

In the mt_metadata packaage, the standard is that units are described by all
lower case strings.

The dictionaries (ABBREVIATIONS & PLOT_AXES_LABELS ) are keyed by these lower
case strings.

"""

ABBREVIATIONS = {
    "digital counts": "cts",
    "millivolts": "mV",
    "nanotesla": "nT",
    "tesla": "T",
    "volts": "V",
    "millivolt per kilometer": "mV/km",
    "millivolts per kilometer": "mV/km",
    "volt per meter": "V/m",
    "volts per meter": "V/m",
    "microvolt per meter": "uV/m",
    "microvolts per meter": "uV/m",
    "celsius": "C",
}

PLOT_AXES_LABELS = {
    "digital counts": "digital counts",
    "millivolts": "milliVolts",
    "tesla": "Tesla",
    "nanotesla": "nanoTesla",
    "volts": "Volts",
}

# =============================================================================
# Unit conversions
# =============================================================================
obspy_units_descriptions = {
    "T": "Tesla",
    "nT": "nanoTesla",
    "V": "Volts",
    "mV": "milliVolts",
    "count": "digital counts",
    "counts": "digital counts",
    "V/m": "Volts per meter",
    "mV/km": "milliVolts per kilometer",
    "m": "meters",
    "COUNTS": "digital counts",
    "millivolt per kilometer": "milliVolt per kilometer",
    "volt per meter": "Volt per meter",
    "volt": "Volt",
    "nanotesla": "nanoTesla",
}
