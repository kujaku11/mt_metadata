# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:14:41 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.timeseries.stationxml.fdsn_tools import (
    release_dict, read_channel_code, make_channel_code)

from mt_metadata import timeseries as metadata
from mt_metadata.timeseries.stationxml.utils import BaseTranslator

from obspy.core import inventory

# =============================================================================


class XMLChannelMTChannel(BaseTranslator):
    """
    translate back and forth between StationXML Channel and MT Channel
    """

    def __init__(self):
        super().__init__()

        self.xml_translator.update(
            {
                "azimuth": "measurement_azimuth",
                "calibration_units": "units",
                "comments": "special",
                "clock_drift": None,
                "description": None,
                "dip": "measurement_tilt",
                "end_date": "time_period.end",
                "equipments": None,
                "pre_amplifier": None,
                "response": None,
                "latitude": "location.latitude",
                "longitude": "location.longitude",
                "elevation": "location.elevation",
                "sample_rate": "sample_rate",
                "sensor": "special",
                "start_date": "time_period.start",
                "types": "special",
                "water_level": None,
                "alternate_code": "component",
            }
        )

        # StationXML to MT Survey
        self.mt_translator = self.flip_dict(self.xml_translator)

        self.mt_comments_list = [
            "run.id"
        ]

    def xml_to_mt(self, xml_channel):
        """
        Translate :class:`obspy.core.inventory.Channel` to 
        :class:`mt_metadata.timeseries.Channel`

        :param xml_channel: Obspy Channel object
        :type xml_channel: :class:`obspy.core.inventory.Channel`
        :returns: MT Channel
        :rtype: :class:`mt_metadata.timeseries.Channel`

        """

        if not isinstance(xml_channel, inventory.Channel):
            msg = f"Input must be obspy.core.inventory.Channel object not {type(xml_channel)}"
            self.logger.error(msg)
            raise TypeError(msg)
            
        ch_dict = read_channel_code(xml_channel.code)
        if ch_dict["measurement"] in ["electric"]:
            mt_channel = metadata.Electric(type="electric")
        elif ch_dict["measurement"] in ["magnetic"]:
            mt_channel = metadata.Magnetic(type="magnetic")
        else:
            mt_channel = metadata.Auxiliary(type=ch_dict["measurement"])
        
        for xml_key, mt_key in self.xml_translator.items():
            if mt_key:
                if "calibration" in xml_key:
                    name = getattr(xml_channel, "calibration_units")
                    description = getattr(xml_channel, "calibration_units_description")
                    if description and name:
                        if len(description) > len(name):
                            mt_channel.units = description
                        else:
                            mt_channel.units = name
                    elif description:
                        mt_channel.units = description
                    elif name:
                        mt_channel.units = name
                    else:
                        self.logger.debug("Did not find any units descriptions in XML")
                    continue
                if xml_key in ["comments"]:
                    runs = []
                    for comment in xml_channel.comments:
                        k, v = self.read_xml_comment(comment)
                        if k == "mt.run.id":
                            runs.append(v)
                        else:
                            if mt_channel.comments:
                                mt_channel.comments += f", {k}: {v}"
                            else:
                                mt_channel.comments = f", {k}: {v}"
                    if mt_channel.comments:
                        mt_channel.comments += f", run_ids: {','.join(runs)}"
                    else:
                        mt_channel.comments = f", run_ids: {','.join(runs)}"
                value = getattr(xml_channel, xml_key)
                if value:
                    if xml_key in ["sensor"]:
                        mt_channel = self._sensor_to_mt(value, mt_channel)
                        continue
                    
                    mt_channel.set_attr_from_name(mt_key, value)
                    
        return mt_channel

    def mt_to_xml(self, mt_channel):
        """
        Translate :class:`obspy.core.inventory.Channel` to 
        :class:`mt_metadata.timeseries.Channel`

        :param xml_channel: Obspy Channel object
        :type xml_channel: :class:`obspy.core.inventory.Channel`
        :returns: MT Channel
        :rtype: :class:`mt_metadata.timeseries.Channel`

        """

        if not isinstance(mt_channel, (metadata.Electric, metadata.Magnetic, metadata.Auxiliary)):
            msg = f"Input must be mt_metadata.timeseries.Channel object not {type(mt_channel)}"
            self.logger.error(msg)
            raise TypeError(msg)

        location_code = get_location_code(mt_channel)
        channel_code = make_channel_code(mt_channel)

        is_electric = mt_channel.type in ["electric"]
        if is_electric:
            xml_channel = inventory.Channel(
                channel_code,
                location_code,
                mt_channel.positive.latitude,
                mt_channel.positive.longitude,
                mt_channel.positive.elevation,
                mt_channel.positive.elevation,
            )
        else:
            xml_channel = inventory.Channel(
                channel_code,
                location_code,
                mt_channel.location.latitude,
                mt_channel.location.longitude,
                mt_channel.location.elevation,
                mt_channel.location.elevation,
            )

    
        xml_channel.start_date = mt_channel.time_period.start
        xml_channel.end_date = mt_channel.time_period.end
        
    def _sensor_to_mt(self, sensor, mt_channel):
        """
        Fill an MT channel with sensor information.  It is slightly different
        depending on electric or magnetic.
        
        :param sensor: DESCRIPTION
        :type sensor: TYPE
        :param mt_channel: DESCRIPTION
        :type mt_channel: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        if sensor.type.lower() in ["magnetometer", "induction coil", "coil"]:
            if not isinstance(mt_channel, metadata.Magnetic):
                msg = (f"Cannot put sensor of type {sensor.type} into an "
                       f"MT Channel of {type(mt_channel)}.")
                self.logger.error(msg)
                raise ValueError(msg)
            mt_channel.sensor.id = sensor.serial_number
            mt_channel.sensor.manufacturer = sensor.manufacturer
            mt_channel.sensor.model = f"{sensor.model} {sensor.description}"
            mt_channel.sensor.type = sensor.type
            return mt_channel
        
        elif sensor.type.lower() in ["dipole", "electrode"]:
            if not isinstance(mt_channel, metadata.Electric):
                msg = (f"Cannot put sensor of type {sensor.type} into an "
                       f"MT Channel of {type(mt_channel)}.")
                self.logger.error(msg)
                raise ValueError(msg)
            if sensor.serial_number:
                pid, nid = self._parse_electrode_ids(sensor.serial_number)
                mt_channel.positive.id = pid
                mt_channel.negative.id = pid
                
            mt_channel.positive.manufacturer = sensor.manufacturer
            mt_channel.positive.model = sensor.model
            mt_channel.positive.type = sensor.type
            
            mt_channel.negative.manufacturer = sensor.manufacturer
            mt_channel.negative.model = sensor.model
            mt_channel.negative.type = sensor.type
            
            mt_channel.dipole_length = self._parse_dipole_length(sensor.descrption)
            
            return mt_channel
        
        else:
            if not isinstance(mt_channel, metadata.Auxiliary):
                msg = (f"Cannot put sensor of type {sensor.type} into an "
                       f"MT Channel of {type(mt_channel)}.")
                self.logger.error(msg)
                raise ValueError(msg)
                
            mt_channel.sensor.type = sensor.type
            mt_channel.sensor.manufacturer = sensor.manufacturer
            mt_channel.sensor.model = sensor.model
            mt_channel.sensor.id = sensor.serial_number
            
            return mt_channel
            
            
        
    def _parse_electrode_ids(self, serial_numbers):
        """
        parse electrode ids from a string formated 'positive: pid, negative: nid'
        """
        
        if ":" in serial_numbers and "," in serial_numbers:
            serial_list = serial_numbers.split(",")
            if len(serial_list) != 2:
                msg = (f"Cannot parse electrode ids from {serial_numbers}. Must "
                       "have format 'positive: pid, negative: nid'")
                self.logger.error(msg)
                raise ValueError(msg)
                
            pid, nid = [ss.split(':')[1].strip() for ss in serial_list]
            return pid, nid
        
        elif ":" not in serial_numbers and "," in serial_numbers:
            serial_list = serial_numbers.split(",")
            if len(serial_list) != 2:
                msg = (f"Cannot parse electrode ids from {serial_numbers}. Must "
                       "have format 'positive: pid, negative: nid'")
                self.logger.error(msg)
                raise ValueError(msg)
                
            pid, nid = [ss.strip() for ss in serial_list]
            return pid, nid
        else:
            self.logger.warning("Electrod IDs are not properly formatted assigning"
                                f" {serial_numbers} to both positive and negative. "
                                "Accepted format is 'positive: pid, negative: nid'")
            return serial_numbers, serial_numbers
        
    def _parse_dipole_length(self, description):
        """
        Parse the dipole length from the sensor description Assuming a format
        'lenth units' --> '100 meters'
        """
        
        dipole = description.split()
        try:
            return float(dipole[0])
            
        except ValueError as error:
            msg = f"Could not get dipole length from {description} got ValueError({error})"
            self.logger.warning(msg)
            return 0.0
            
            
        
        
        
            
                      

    