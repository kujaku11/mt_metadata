# -*- coding: utf-8 -*-
"""
===============================
Transfer Functions Metadata
===============================

This module provides a central container (TF) for magnetotelluric transfer functions,
which represent the electromagnetic response of the Earth. Transfer functions relate
the measured magnetic and electric fields and are fundamental to magnetotelluric
interpretation.

The primary goal is to create a unified transfer function object that can read from
and write to various industry-standard file formats through the io module, enabling
seamless data interchange and analysis across different MT software packages.

MetadataBase Objects
--------------------
* TF - Main transfer function container with impedance, tipper, and associated metadata
* Station - Station-level metadata specific to transfer function processing
* TransferFunction - Core transfer function metadata (impedance, tipper, processing info)
* StatisticalEstimate - Statistical quality metrics and error estimates for transfer functions

Supported File Formats (io module)
----------------------------------
The io module supports reading and writing the following transfer function formats:

* **EDI** - SEG (Society of Exploration Geophysicists) EDI format, the most common
  MT interchange format
* **EMTFXML** - EMTF (Electromagnetic Transfer Function) XML format with extended
  metadata support
* **ZMM** - BIRRP processing output format (impedance and vertical field data)
* **JFile** - EMTF/BIRRP .j format for transfer function coefficients
* **ZongeMTAvg** - Zonge International averaged MT data format

Channel Nomenclature
--------------------
The module supports multiple channel naming conventions from different acquisition
systems (default, LEMI, Phoenix, Musgraves, NIMS), with automatic mapping between
standard channel names (hx, hy, hz, ex, ey) and system-specific labels.

Usage
-----
The TF object serves as a central repository that:
- Stores transfer functions in an xarray.Dataset for efficient computation
- Provides helper methods to access impedance, tipper, errors, and covariances
- Reads/writes to multiple file formats transparently
- Maintains full metadata provenance and processing history
- Supports coordinate rotations and datum transformations

"""

# Define allowed sets of channel labellings
STANDARD_INPUT_CHANNELS = [
    "hx",
    "hy",
]
STANDARD_OUTPUT_CHANNELS = [
    "ex",
    "ey",
    "hz",
]

# channel nomenclature mappings
CHANNEL_MAPS = {
    "default": {"hx": "hx", "hy": "hy", "hz": "hz", "ex": "ex", "ey": "ey"},
    "lemi12": {"hx": "bx", "hy": "by", "hz": "bz", "ex": "e1", "ey": "e2"},
    "lemi34": {"hx": "bx", "hy": "by", "hz": "bz", "ex": "e3", "ey": "e4"},
    "phoenix123": {"hx": "h1", "hy": "h2", "hz": "h3", "ex": "e1", "ey": "e2"},
    "musgraves": {"hx": "bx", "hy": "by", "hz": "bz", "ex": "ex", "ey": "ey"},
}
CHANNEL_MAPS["nims"] = CHANNEL_MAPS[
    "default"
]  # Alias NIMS system to use same config as default


def get_allowed_channel_names(standard_names):
    """
    :param standard_names: one of STANDARD_INPUT_NAMES, or STANDARD_OUTPUT_NAMES
    :type standard_names: list
    :return: allowed_names: list of channel names that are supported
    :rtype: list
    """
    allowed_names = []
    for ch in standard_names:
        for _, channel_map in CHANNEL_MAPS.items():
            allowed_names.append(channel_map[ch])
    allowed_names = list(set(allowed_names))
    return allowed_names


ALLOWED_INPUT_CHANNELS = get_allowed_channel_names(STANDARD_INPUT_CHANNELS)
ALLOWED_OUTPUT_CHANNELS = get_allowed_channel_names(STANDARD_OUTPUT_CHANNELS)

from .core import TF


__all__ = ["TF"]
