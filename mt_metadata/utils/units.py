"""
This is a placeholder module.  See github issue #30

In the mt_metadata packaage, the standard is that units are described by all
lower case strings.

The dictionaries (ABBREVIATIONS & PLOT_AXES_LABELS ) are keyed by these lower
case strings.

"""

UNITS = {'digital counts': {'description': 'digital counts from data logger',
  'abbreviation': 'cnts',
  'plot_label': 'Digital Counts'},
 'volts': {'description': 'electric potential',
  'abbreviation': 'V',
  'plot_label': 'Volts'},
 'millivolts': {'description': 'electric potential',
  'abbreviation': 'mV',
  'plot_label': 'milliVolts'},
 'microvolts': {'description': 'electric potential',
  'abbreviation': 'mircoV',
  'plot_label': 'microVolts'},
 'tesla': {'description': 'magnetic field',
  'abbreviation': 'T',
  'plot_label': 'Tesla'},
 'millitesla': {'description': 'magnetic field',
  'abbreviation': 'mT',
  'plot_label': 'milliTesla'},
 'microtesla': {'description': 'magnetic field',
  'abbreviation': 'microT',
  'plot_label': 'microTesla'},
 'nanotesla': {'description': 'magnetic field',
  'abbreviation': 'nT',
  'plot_label': 'nanoTesla'},
 'volts per meter': {'description': 'electric field',
  'abbreviation': 'V/m',
  'plot_label': 'Volts per Meter'},
 'millivolts per kilometer': {'description': 'electric field',
  'abbreviation': 'mV/km',
  'plot_label': 'milliVolts per Kilometer'},
 'microvolts per meter': {'description': 'electric field',
  'abbreviation': 'microV/m',
  'plot_label': 'microVolts per Meter'},
 'millivolts per kilometer per nanotesla': {'description': 'EM transfer function',
  'abbreviation': 'mV/km/nT',
  'plot_label': '[mV/km]/[nT]'},
 'volts per meter per tesla': {'description': 'EM transfer function',
  'abbreviation': 'V/m/T',
  'plot_label': '[V/m]/[T]'},
 'meter': {'description': 'length',
  'abbreviation': 'm',
  'plot_label': 'Meter'},
 'kilometer': {'description': 'length',
  'abbreviation': 'km',
  'plot_label': 'Kilometer'},
 'celsius': {'description': 'temperature',
  'abbreviation': 'C',
  'plot_label': 'Celsius'}}

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
    "microvolt per meter": "\u03BCV/m",
    "microvolts per meter": "\u03BCV/m",
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
