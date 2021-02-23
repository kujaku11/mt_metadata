# -*- coding: utf-8 -*-
"""

Tools for FDSN standards

Created on Wed Sep 30 11:47:01 2020

:author: Jared Peacock

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
import logging
import numpy as np

# =============================================================================
logger = logging.getLogger(__name__)

release_dict = {
    "CC-0": "open",
    "CC-BY": "partial",
    "CC-BY-SA": "partial",
    "CC-BY-ND": "partial",
    "CC-BY-NC-SA": "partial",
    "CC-BY-NC-NC": "closed",
    None: "open",
}

period_code_dict = {
    "F": {"min": 1000, "max": 5000},
    "G": {"min": 1000, "max": 5000},
    "D": {"min": 250, "max": 1000},
    "C": {"min": 250, "max": 1000},
    "E": {"min": 80, "max": 250},
    "S": {"min": 10, "max": 80},
    "H": {"min": 80, "max": 250},
    "B": {"min": 10, "max": 80},
    "M": {"min": 1, "max": 10},
    "L": {"min": 0.95, "max": 1.05},
    "V": {"min": 0.095, "max": 0.105},
    "U": {"min": 0.0095, "max": 0.0105},
    "R": {"min": 0.0001, "max": 0.001},
    "P": {"min": 0.00001, "max": 0.0001},
    "T": {"min": 0.000001, "max": 0.00001},
    "Q": {"min": 0, "max": 0.000001},
}

measurement_code_dict = {
    "tilt": "A",
    "creep": "B",
    "calibration": "C",
    "pressure": "D",
    "magnetic": "F",
    "gravity": "G",
    "humidity": "I",
    "temperature": "K",
    "water_current": "O",
    "electric": "Q",
    "rain_fall": "R",
    "linear_strain": "S",
    "tide": "T",
    "wind": "W",
}

measurement_code_dict_reverse = dict([(v, k) for k, v in measurement_code_dict.items()])


def angle(value):
        return abs(np.cos(np.deg2rad(value)))
# parts of a unit circle
orientation_code_dict = {
    "N": {"angle": 0, "variance": 15},
    "E": {"angle": 90, "variance": 15},
    "Z": {"angle": 0, "variance": 15},
    "1": {"angle": 30, "variance": 15},
    "2": {"angle": 60, "variance": 15},
    "3": {"angle": 0, "variance": 15},
}

mt_components_dict = {
    "electric": "e",
    "magnetic": "h",
    "temperature": "temperature"}

mt_orientation_dict = {
    "N": "x",
    "E": "y",
    "Z": "z",
    "1": "x",
    "2": "y",
    "3": "z"}

# SI units short name
units_names = {
    "millivolts per kilometer": "mV/km",
    "volts": "V",
    "millivolts": "mV",
    "volts per meter": "V/m",
    "millivolts per kilometer": "mV/km",
    "nanotesla": "nT",
    "tesla": "T",
    "celsius": "C",
    "ohms": "Ohm",
    "ohm meters": "Ohm-m",
}


def create_location_code(channel_obj):
    """
    Get the location code given the components and channel number

    :param channel_obj: Channel object
    :type channel_obj: :class:`~mth5.metadata.Channel`
    :return: 2 character location code
    :rtype: string

    """

    location_code = "{0}{1}".format(
        channel_obj.component[0].upper(), channel_obj.channel_number % 10
    )

    return location_code


def get_period_code(sample_rate):
    """
    Get the SEED sampling rate code given a sample rate

    :param sample_rate: sample rate in samples per second
    :type sample_rate: float
    :return: single character SEED sampling code
    :rtype: string

    """
    period_code = "A"
    for key, v_dict in sorted(period_code_dict.items()):
        if (sample_rate >= v_dict["min"]) and (sample_rate <= v_dict["max"]):
            period_code = key
            break
    return period_code


def get_measurement_code(measurement):
    """
    get SEED sensor code given the measurement type

    :param measurement: measurement type, e.g.
        * temperature
        * electric
        * magnetic
    :type measurement: string
    :return: single character SEED sensor code, if the measurement type has
             not been defined yet Y is returned.
    :rtype: string

    """
    sensor_code = "Y"
    for key, code in measurement_code_dict.items():
        if measurement.lower() in key:
            sensor_code = code
    return sensor_code


def get_orientation_code(azimuth, orientation="horizontal"):
    """
    Get orientation code given angle and orientation.  This is a general
    code and the true azimuth is stored in channel

    :param azimuth: angel assuming 0 is north, 90 is east, 0 is vertical down
    :type azimuth: float
    :return: single character SEED orientation code
    :rtype: string

    """
    # angles are only from 0 to 360
    azimuth = azimuth % 360

    value = abs(np.cos(np.deg2rad(azimuth)))

    if orientation == "horizontal":
        if value >= angle(15):
            return "N"
        elif value <= angle(105):
            return "E"
        elif (value < angle(15)) and (value >= angle(45)):
            return "1"
        elif (value < angle(45)) and (value >= angle(105)):
            return "2"

    elif orientation == "vertical":
        if value >= angle(15):
            return "Z"
        else:
            return "3"


def make_channel_code(sample_rate, measurement_type, azimuth, orientation="horizontal"):
    """

    Make channel code from given parameters

    :param sample_rate: sample rate in samples per second
    :type sample_rate: float
    :param measurement_type: type of measurement, e.g. 'electric'
    :type measurement_type: string
    :param orientation: orientation azimuth (degrees)
    :type orientation: float
    :return: three letter channel code
    :rtype: string

    """

    period_code = get_period_code(sample_rate)
    sensor_code = get_measurement_code(measurement_type)
    orientation_code = get_orientation_code(azimuth, orientation=orientation)

    channel_code = f"{period_code}{sensor_code}{orientation_code}"

    return channel_code


def read_channel_code(channel_code):
    """
    read FDSN channel code

    :param channel_code: Three character string {Period}{Component}{Orientation}
    :type channel_code: string
    :return: DESCRIPTION
    :rtype: TYPE

    """

    if len(channel_code) != 3:
        msg = "Input FDSN channel code is not proper format, should be 3 letters"
        logger.error(msg)
        raise ValueError(msg)

    try:
        period_range = period_code_dict[channel_code[0]]
    except KeyError:
        msg = (
            f"Could not find period range for {channel_code[0]}. ",
            "Setting to 1",
        )
        period_range = {"min": 1, "max": 1}

    try:
        component = measurement_code_dict_reverse[channel_code[1]]
    except KeyError:
        msg = f"Could not find component for {channel_code[1]}"
        logger.error(msg)
        raise ValueError(msg)

    try:
        orientation = orientation_code_dict[channel_code[2]]
    except KeyError:
        msg = (
            f"Could not find orientation for {channel_code[2]}. ",
            "Setting to 0.",
        )
        logger.error(msg)
        raise ValueError(msg)

    return {
        "period": period_range,
        "measurement": component,
        "orientation": orientation,
    }

def create_mt_component(channel_code):
    """
    Create a component for an MT channel given the measurement and orientation
    
    >>> create_mt_component("LQN")
    ex
    
    """
        
    code_dict = read_channel_code(channel_code)
    
    mt_component = mt_components_dict[code_dict["measurement"]]
    mt_orientation = mt_orientation_dict[channel_code[2]]
    
    return f"{mt_component}{mt_orientation}"

