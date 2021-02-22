# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 09:27:10 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from pathlib import Path

from mt_metadata.utils.mt_logger import setup_logger
from mt_metadata import timeseries as metadata
from mt_metadata.timeseries.stationxml import (XMLNetworkMTSurvey,
                                               XMLStationMTStation,
                                               XMLChannelMTChannel)

from obspy.core import inventory
from obspy import read_inventory
# =============================================================================

class XMLInventoryMTExperiment():
    """
    Read the full files and put the elements in the appropriate locations.
    
    """
    
    def __init__(self):
        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")
        self.network_translator = XMLNetworkMTSurvey()
        self.station_translator = XMLStationMTStation()
        self.channel_translator = XMLChannelMTChannel()
    
    def xml_to_mt(self, inventory_object=None, stationxml_fn=None, mt_fn=None):
        """
        Read in a StationXML using Obspy :class:`obspy.core.inventory.Inventory` 
        and convert to an MT :class:`mt_metadata.timeseries.Experiment` 
        
        
        :param inventory_object: inventory object or StationXML file name
        :type inventory_object: :class:`obspy.core.inventory.Inventory`
        :param stationxml_fn: full path to StationXML file
        :type stationxml_fn: Path or string
        :param mt_fn: full path to MT file
        :type mt_fn: Path or string
        
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        if stationxml_fn:
            if isinstance(stationxml_fn, Path):
                stationxml_fn = stationxml_fn.as_posix()
            inventory_object = read_inventory(stationxml_fn)
            
        if not inventory_object:
            msg = "Must provide either an inventory object or StationXML file path"
            self.logger.error(msg)
            raise ValueError(msg)
            
        mt_experiment = metadata.Experiment()
        for xml_network in inventory_object.networks:
            mt_survey = self.network_translator.xml_to_mt(xml_network)
            for xml_station in xml_network.stations:
                mt_station = self.station_translator.xml_to_mt(xml_station)
                for xml_channel in xml_station:
                    mt_channel = self.channel_translator.xml_to_mt(xml_channel)
                    # if there is a run list match channel to runs
                    if self.channel_translator.run_list:
                        for run_id in self.channel_translator.run_list:
                            mt_station.get_run(run_id).add_channel(mt_channel)
                    elif mt_station.runs:
                        for mt_run in mt_station.runs:
                            if mt_run.sample_rate == mt_channel.sample_rate:
                                if mt_run.time_period.start == mt_channel.time_period.start:
                                    if mt_run.time_period.end == mt_channel.time_period.end:
                                        mt_run.channels.append(mt_channel)
                    else:
                        mt_run = metadata.Run(id=f"{len(mt_station.runs)+1:02d}")
                        mt_run.time_period.start = mt_channel.time_period.start
                        mt_run.time_period.end = mt_channel.time_period.end
                        mt_run.sample_rate = mt_channel.sample_rate
                        mt_run.channels.append(mt_channel)
                        mt_station.runs.append(mt_run)
                                
                                
                mt_survey.stations.append(mt_station)
            mt_experiment.surveys.append(mt_survey)
            
        if mt_fn:
            mt_experiment.to_xml(fn=mt_fn)

        return mt_experiment                        
                    
        
        
