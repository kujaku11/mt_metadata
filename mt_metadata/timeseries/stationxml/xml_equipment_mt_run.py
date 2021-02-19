# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 12:49:13 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================

from mt_metadata import timeseries as metadata
from mt_metadata.timeseries.stationxml.utils import BaseTranslator

from obspy.core import inventory

# =============================================================================


class XMLEquipmentMTRun(BaseTranslator):
    """
    translate back and forth between StationXML Station and MT Station
    """

    def __init__(self):
        super().__init__()

        self.xml_translator = {
            "type": "data_type",
            "manufacturer": "data_logger.manufacturer",
            "model": "data_logger.type",
            "serial_number": "data_logger.id",
            "installation_date": "time_period.start",
            "removal_date": "time_period.end",
            "description": "special",
            "resource_id": "id"}

        # StationXML to MT Survey
        self.mt_translator = self.flip_dict(self.xml_translator)
        self.mt_translator["geographic_name"] = "site"
        self.mt_translator["provenance.comments"] = None
        self.mt_translator["time_period.start"] = "start_date"
        self.mt_translator["time_period.end"] = "end_date"
        
    def xml_to_mt(self, equipment):
        """
        Read in an equipment block. 
        
        :param equipment: an Equipment element
        :type equipment: :class:`obspy.core.inventory.Equipment`
        
        """
        
        if not isinstance(equipment, inventory.Equipment):
            msg = f"Input must be obspy.core.inventory.Equipment object not {type(equipment)}"
            self.logger.error(msg)
            raise TypeError(msg)
            
        mt_run = metadata.Run()
        for xml_key, mt_key in self.xml_translator:
            value = getattr(equipment, xml_key)
            if xml_key in ["description"]:
                mt_run = self._parse_description(value, mt_run)
            elif xml_key in ["resource_id"]:
                mt_run.id = value.split(":")[1]
            else:
                mt_run.set_attr_from_name(mt_key, value)
                
        return mt_run
            
        
    def _parse_description(self, description, run_obj):
        """
        Parse a run description into run 
        
        :param description: DESCRIPTION
        :type description: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        for d_str in description.split(','):
            d_key, d_value = d_str.split(":")
            run_obj.set_attr_from_name(f"data_logger.{d_key.strip()}",
                                       d_value.strip())
            
        return run_obj
        
        
        
