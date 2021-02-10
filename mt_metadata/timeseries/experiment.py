# -*- coding: utf-8 -*-
"""
Containers for the full metadata tree

Experiment
   |--> Surveys
   -------------
       |--> Stations
       --------------
           |--> Runs
           -----------
               |--> Channels
               ---------------
                   |--> Responses
                   
Each level has a list attribute 
    
Created on Mon Feb  8 21:25:40 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
from .survey import Survey
from mt_metadata.utils.mt_logger import setup_logger


class Experiment:
    """
    Top level of the metadata
    """

    def __init__(self, survey_list=[]):
        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")
        self.survey_list = survey_list
        
    def __str__(self):
        lines = ["Experiment Contents", "-" * 20]
        if len(self.survey_list) > 0:
            lines.append(f"Number of Surveys: {len(self.survey_list)}")
            for survey in self.survey_list:
                lines.append(f"\tSurvey ID: {survey.survey_id}")
                lines.append(f"\tNumber of Stations: {len(survey)}")
                lines.append(f"\t{'-' * 20}")
                for station in survey.station_list:
                    lines.append(f"\t\tStation ID: {station.id}")
                    lines.append(f"\t\tNumber of Runs: {len(station)}")
                    lines.append(f"\t\t{'-' * 20}")
                    for run in station.run_list:
                        lines.append(f"\t\t\tRun ID: {run.id}")
                        lines.append(f"\t\t\tNumber of Channels: {len(run)}")
                        lines.append("\t\t\tRecorded Channels: " 
                                     +", ".join(run.channels_recorded_all))
                        lines.append(f"\t\t\t{'-' * 20}")
                
        return "\n".join(lines)
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __add__(self, other):
        if isinstance(other, Experiment): 
            self.survey_list.extend(other.survey_list)

            return self
        else:
            msg = f"Can only merge Experiment objects, not {type(other)}"
            self.logger.error(msg)
            raise TypeError(msg)
            
    def __len__(self):
        return len(self.survey_list)
            
    @property
    def survey_list(self):
        """ Return survey list """
        return self._survey_list
    
    @survey_list.setter
    def survey_list(self, value):
        """ set the survey list """
        if not hasattr(value, "__iter__"):
            msg = ("input survey_list must be an iterable, should be a list "
                   f"not {type(value)}")
            self.logger.error(msg)
            raise TypeError(msg)
        surveys = []
        fails = []
        for ii, survey in enumerate(value):
            if not isinstance(survey, Survey):
                msg = f"Item {ii} is not type(Survey); type={type(survey)}"
                fails.append(msg)
                self.logger.error(msg)
            else:
                surveys.append(survey)
        if len(fails) > 0:
            raise TypeError("\n".join(fails))
            
        self._survey_list = surveys
        
    @property
    def survey_names(self):
        """ Return names of surveys in experiment """
        return [ss.survey_id for ss in self.survey_list]
    
    def to_xml(self, fn):
        """
        Write XML version of the experiment
        
        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        pass
    
    def to_json(self, fn):
        """
        Write JSON version of the experiment
        
        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        pass
    
    def to_pickle(self, fn):
        """
        Write a pickle version of the experiment
        
        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        pass
    
    def from_xml(self, fn):
        """
        Read XML version of the experiment
        
        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        pass
    
    def from_json(self, fn):
        """
        Read JSON version of experiment
        
        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        pass
    
    def from_pickle(self, fn):
        """
        Read pickle version of experiment
        
        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        pass
    
    def validate_experiment(self):
        """
        Validate experiment is legal
        
        :return: DESCRIPTION
        :rtype: TYPE

        """
        pass
    
        
    

            
            
        

