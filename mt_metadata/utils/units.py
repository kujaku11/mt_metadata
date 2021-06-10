"""
This is a placeholder module.  See github issue #30

In the mt_metadata packaage, the standard is that units are described by all
lower case strings.

The dictionaries (ABBREVIATIONS & PLOT_AXES_LABELS ) are keyed by these lower
case strings.

"""

ABBREVIATIONS = {"digital counts":"cts",
                 "millivolts": "mV",
                 "nanotesla": "nT",
                 "tesla": "T",
                 "volts": "V"}

PLOT_AXES_LABELS  = {"digital counts": "digital counts",
                     "millivolts": "milliVolts",
                     "tesla": "Tesla",
                     "nanotesla": "nanoTesla",
                     "volts": "Volts"}

# =============================================================================
# Unit conversions
# =============================================================================
obspy_units_descriptions = {
    "T": "Tesla",
    "nT": "nanoTesla",
    "V": "Volts",
    "mV": "milliVolts",
    "count": "digital counts",
    "V/m": "Volts per meter",
    "mV/km": "milliVolts per kilometer",
    "m": "meters",
    "COUNTS": "digital counts",
}
