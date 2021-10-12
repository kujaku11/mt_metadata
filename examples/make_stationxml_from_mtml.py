# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 16:31:55 2021

@author: jpeacock
"""

# =============================================================================
# Imports 
# =============================================================================
from pathlib import Path
import pandas as pd
from xml.etree import cElementTree as et

from mt_metadata.timeseries import (Experiment, Survey, Station, Run, 
                                    Electric, Magnetic)
from mt_metadata.timeseries.filters import (PoleZeroFilter, CoefficientFilter,
                                            TimeDelayFilter, FIRFilter)
from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment

# =============================================================================
# Input Parameters
# =============================================================================
xml_path = Path(r"c:\Users\jpeacock\OneDrive - DOI\mt\mt_array_xmls")

output_filename = "example_station_xml"

# =============================================================================
# Useful functions
# =============================================================================
class MTML2StationXML(XMLInventoryMTExperiment):
    """
    A class to convert multiple MTML xml files into a stationXML
    
    """
    
    def __init__(self, xml_path=None):
        self.xml_path = xml_path
        
        super().__init__()
        
        
    @property
    def xml_path(self):
        return self._xml_path
    
    @xml_path.setter
    def xml_path(self, value):
        if value is None:
            self._xml_path = None
        else:
            self._xml_path = Path(value)
            self.make_df()
            
    def has_xml_path(self):
        if self.xml_path is not None and self.xml_path.exists():
            return True
        return False

    @staticmethod
    def is_a_filter_xml(fn):
        return fn.stem in ["filters"]
    
    @staticmethod
    def is_a_survey_xml(fn):
        return fn.stem in ["survey"]
    
    @staticmethod
    def is_a_station_xml(fn):
        if fn.stem not in ["filters", "survey"]:
            return fn.stem.count(".") == 0
        return False
    
    @staticmethod
    def is_a_run_xml(fn):
        return fn.stem.count(".") == 1
    
    @staticmethod
    def is_a_channel_xml(fn):
        return fn.stem.count(".") > 1
    
    def get_xml_files(self) -> list:
        """
        Get all mtml xml files for a given station.
        """
        if self.has_xml_path():
            return list(self.xml_path.rglob("*.xml"))
        raise ValueError("self.xml_path must be set")
        
    def make_df(self):
        """
        Make a pandas data frame for easier querying
        
        :return: DESCRIPTION
        :rtype: TYPE

        """
        df_dict = {
            "fn":[],
            "station": [],
            "run": [],
            "is_station": [],
            "is_run": [],
            "is_channel": [],
            "is_filters": [], 
            "is_survey": []
            }
        for fn in self.get_xml_files():
            df_dict["fn"].append(fn)
            df_dict["station"].append(fn.stem.split('.')[0])
            if self.is_a_run_xml(fn) or self.is_a_channel_xml(fn):
                df_dict["run"].append(fn.stem.split('.')[1])
            else:
                df_dict["run"].append(None)
            df_dict["is_station"].append(self.is_a_station_xml(fn))
            df_dict["is_run"].append(self.is_a_run_xml(fn))
            df_dict["is_channel"].append(self.is_a_channel_xml(fn))
            df_dict["is_filters"].append(self.is_a_filter_xml(fn))
            df_dict["is_survey"].append(self.is_a_survey_xml(fn))

        self.df = pd.DataFrame(df_dict)
       
    @property
    def stations(self):
        if self.has_xml_path():
            return list(self.df[self.df.is_station == True].station)
        return None
    
    @property
    def survey(self):
        if self.has_xml_path():
            return self.df[self.df.is_survey == True].fn.values[0]
        return None
    
    @property
    def filters(self):
        if self.has_xml_path():
            return self.df[self.df.is_filters == True].fn.values[0]
        return None
    
    def _get_runs(self, station):
        """
        Get runs from the dataframe for a given station
        
        :param station: DESCRIPTION
        :type station: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        return self.df[(self.df.station == station) & (self.df.is_run == True)]
        
    
    def _get_channels(self, station, run):
        """
        Get runs from the dataframe for a given station
        
        :param station: DESCRIPTION
        :type station: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        return list(self.df[(self.df.station == station) & (self.df.run == run) & (self.df.is_channel == True)].fn)
        
    def sort_by_station(self, stations=None):
        """
        sort the file into station, runs and channels

        :return: DESCRIPTION
        :rtype: TYPE

        """
        fn_dict = {"survey": self.survey, "filters": self.filters, "stations": []}
        if stations in [None, []]:
            station_iterator = self.stations
        else:
            if isinstance(stations, str):
                stations = [stations]
            if not isinstance(stations, list):
                raise ValueError("stations must be a list of stations")
            station_iterator = stations
        for station in station_iterator:
            station_dict = {"fn": self.df[(self.df.station == station) & (self.df.is_station==True)].fn.values[0],
                            "runs": []}
            for run in self._get_runs(station).itertuples():
                run_dict = {}
                run_dict["fn"] = run.fn
                run_dict["channels"] = self._get_channels(station, run.run)
                station_dict["runs"].append(run_dict)
            fn_dict["stations"].append(station_dict)
            
        return fn_dict
    
    @staticmethod
    def read_xml_file(xml_file):
        """
        read an xml file an return an xml element
        
        :param xml_file: DESCRIPTION
        :type xml_file: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        return et.parse(xml_file).getroot()
    
    def _make_channel(self, channel_fn):
        """
        Make a :class:`mt_metadata.timeseries.Channel` object from an 
        xml file
        
        :param channel_fn: DESCRIPTION
        :type channel_fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        ch_type = channel_fn.stem.split(".")[2].lower()
        if ch_type in ["electric"]:
            ch = Electric()
        
        elif ch_type in ["magnetic"]:
            ch = Magnetic()
            
        ch.from_xml(self.read_xml_file(channel_fn))
        
        return ch
    
    def _make_run(self, run_dict):
        """
        Make a :class:`mt_metadata.timeseries.Run` object from information
        in a run dictionary
        
        run_dict = {'fn': xml_file_name, 'channels': [list of xml file names]}

        :param run_dict: DESCRIPTION
        :type run_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        r = Run()
        r.from_xml(self.read_xml_file(run_dict["fn"]))
        for ch_fn in run_dict["channels"]:
            r.channels.append(self._make_channel(ch_fn))
        
        return r
    
    def _make_station(self, station_dict):
        """
        Make a station object from a station dictionary
        
        station_dict = {
            'fn': xml_file_name,
            'runs': [{'fn': run_xml_file_name,
                     'channels': [list of xml file names]}]
            }
        
        :param station_dict: DESCRIPTION
        :type station_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        s = Station()
        s.from_xml(self.read_xml_file(station_dict["fn"]))
        # < need to reset the runs, otherwise there are empty runs and double
        # the ammount of runs because the run_list is input. > 
        s.runs = []
        for run_dict in station_dict["runs"]:
            s.runs.append(self._make_run(run_dict))
        
        return s
    
    def _make_survey(self, survey_dict):
        """
        Make a :class:`mt_metadata.timeseries.Survey` object 
        
        survey_dict = {
            'survey': survey_xml_file,
            'filters': filter_xml_file,
            'stations': [
                {
                'fn': xml_file_name,
                'runs': [
                    {'fn': run_xml_file_name,
                     'channels': [list of xml file names]}]
                }
                ]
            }
        :param survey_dict: DESCRIPTION
        :type survey_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        s = Survey()
        s.from_xml(self.read_xml_file(survey_dict["survey"]))
        s.stations = []
        for station_dict in survey_dict["stations"]:
            s.stations.append(self._make_station(station_dict))
            
        return s
    
    def _make_filters_dict(self, filters_xml_file):
        """
        Make a filter dictionary from a filter file with all the filters in it
        
        :param filters_xml_file: DESCRIPTION
        :type filters_xml_file: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        element = self.read_xml_file(filters_xml_file)
        
        f_dict = {}
        for f in element.iter(tag="filter"):
            f_type = [y.text for y in f.findall("type")][0]
            if f_type in ["zpk"]:
                mt_filter = PoleZeroFilter()
            elif f_type in ["coefficient"]:
                mt_filter = CoefficientFilter()
            elif f_type in ["time delay"]:
                mt_filter = TimeDelayFilter()
            elif f_type in ["fir"]:
                mt_filter = FIRFilter()
            else:
                raise ValueError(f"No support for {f_type} currently.")
            
            mt_filter.from_xml(f)
            f_dict[mt_filter.name] = mt_filter
            
        return f_dict

    def make_experiment(self, stations=None):
        """
        Create an MTML experiment from the a directory of xml files 
        :return: DESCRIPTION
        :rtype: TYPE

        """
        mtex = Experiment()
        
        mtex.surveys.append(self._make_survey(self.sort_by_station(stations)))
        mtex.surveys[0].filters = self._make_filters_dict(self.filters)
        return mtex
        

a = MTML2StationXML(xml_path)
mtex = a.make_experiment(stations="TTX11")
inv = a.mt_to_xml(mtex, stationxml_fn=r"c:\Users\jpeacock\test_stationxml_TTX11.xml")


    
    
    