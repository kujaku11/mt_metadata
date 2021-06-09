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
# =============================================================================
# Imports
# =============================================================================
from xml.etree import cElementTree as et

from . import Auxiliary, Electric, Magnetic, Run, Station, Survey
from .filters import (
    PoleZeroFilter,
    CoefficientFilter,
    TimeDelayFilter,
    FIRFilter,
    FrequencyResponseTableFilter,
)
from mt_metadata.utils.mt_logger import setup_logger
from mt_metadata.base import helpers

# =============================================================================


class Experiment:
    """
    Top level of the metadata
    """

    def __init__(self, surveys=[]):
        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")
        self.surveys = surveys

    def __str__(self):
        lines = ["Experiment Contents", "-" * 20]
        if len(self.surveys) > 0:
            lines.append(f"Number of Surveys: {len(self.surveys)}")
            for survey in self.surveys:
                lines.append(f"\tSurvey ID: {survey.survey_id}")
                lines.append(f"\tNumber of Stations: {len(survey)}")
                lines.append(f"\t{'-' * 20}")
                for station in survey.stations:
                    lines.append(f"\t\tStation ID: {station.id}")
                    lines.append(f"\t\tNumber of Runs: {len(station)}")
                    lines.append(f"\t\t{'-' * 20}")
                    for run in station.runs:
                        lines.append(f"\t\t\tRun ID: {run.id}")
                        lines.append(f"\t\t\tNumber of Channels: {len(run)}")
                        lines.append(
                            "\t\t\tRecorded Channels: "
                            + ", ".join(run.channels_recorded_all)
                        )
                        lines.append(f"\t\t\tStart: {run.time_period.start}")
                        lines.append(f"\t\t\tEnd:   {run.time_period.end}")

                        lines.append(f"\t\t\t{'-' * 20}")

        return "\n".join(lines)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, Experiment):
            self.surveys.extend(other.surveys)

            return self
        else:
            msg = f"Can only merge Experiment objects, not {type(other)}"
            self.logger.error(msg)
            raise TypeError(msg)

    def __len__(self):
        return len(self.surveys)

    @property
    def surveys(self):
        """ Return survey list """
        return self._surveys

    @surveys.setter
    def surveys(self, value):
        """ set the survey list """
        if not hasattr(value, "__iter__"):
            msg = (
                "input surveys must be an iterable, should be a list "
                f"not {type(value)}"
            )
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

        self._surveys = surveys

    @property
    def survey_names(self):
        """ Return names of surveys in experiment """
        return [ss.survey_id for ss in self.surveys]

    def to_xml(self, fn=None, required=True):
        """
        Write XML version of the experiment
        
        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        experiment_element = et.Element(self.__class__.__name__)
        for survey in self.surveys:
            survey.update_bounding_box()
            survey.update_time_period()
            survey_element = survey.to_xml(required=required)
            filter_element = et.SubElement(survey_element, "filters")
            for key, value in survey.filters.items():
                filter_element.append(value.to_xml(required=required))
            for station in survey.stations:
                station.update_time_period()
                station_element = station.to_xml(required=required)
                for run in station.runs:
                    run.update_time_period()
                    run_element = run.to_xml(required=required)
                    for channel in run.channels:
                        run_element.append(channel.to_xml(required=required))
                    station_element.append(run_element)
                survey_element.append(station_element)
            experiment_element.append(survey_element)

        if fn:
            with open(fn, "w") as fid:
                fid.write(helpers.element_to_string(experiment_element))
        return experiment_element

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

    def from_xml(self, fn=None, element=None):
        """
        
        :param fn: DESCRIPTION, defaults to None
        :type fn: TYPE, optional
        :param element: DESCRIPTION, defaults to None
        :type element: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE
        
        

        """
        if fn:
            experiment_element = et.parse(fn).getroot()
        if element:
            experiment_element = element

        # need to set the lists for each layer, otherwise you get duplicates.
        for survey_element in list(experiment_element):
            survey_dict = helpers.element_to_dict(survey_element)
            survey_obj = Survey()
            fd = survey_dict["survey"].pop("filters")
            filter_dict = self._read_filter_dict(fd)
            survey_obj.filters.update(filter_dict)

            stations = self._pop_dictionary(survey_dict["survey"], "station")
            for station_dict in stations:
                station_obj = Station()
                run_list = []
                runs = self._pop_dictionary(station_dict, "run")
                for run_dict in runs:
                    run_obj = Run()
                    channel_list = []
                    for ch in ["electric", "magnetic", "auxiliary"]:
                        try:
                            for ch_dict in self._pop_dictionary(run_dict, ch):
                                if ch == "electric":
                                    channel = Electric()
                                elif ch == "magnetic":
                                    channel = Magnetic()
                                elif ch == "auxiliary":
                                    channel = Auxiliary()
                                channel.from_dict(ch_dict)
                                channel_list.append(channel)
                        except KeyError:
                            self.logger.debug(f"Could not find channel {ch}")
                    run_obj.from_dict(run_dict)
                    run_obj.channels = channel_list
                    run_list.append(run_obj)

                station_obj.from_dict(station_dict)
                station_obj.runs = run_list
                survey_obj.stations.append(station_obj)
            survey_obj.from_dict(survey_dict)
            self.surveys.append(survey_obj)

    def _pop_dictionary(self, in_dict, element):
        """
        Pop off a key from an input dictionary, make sure output is a list
        
        :param in_dict: DESCRIPTION
        :type in_dict: TYPE
        :param element: DESCRIPTION
        :type element: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        elements = in_dict.pop(element)
        if not isinstance(elements, list):
            elements = [elements]

        return elements

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

    def _read_filter_dict(self, filters_dict):
        """
        Read in filter element an put it in the correct object
        
        :param filter_element: DESCRIPTION
        :type filter_element: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        return_dict = {}
        if filters_dict is None:
            return return_dict

        for key, value in filters_dict.items():
            if key in ["pole_zero_filter"]:
                if isinstance(value, list):
                    for v in value:
                        mt_filter = PoleZeroFilter(**v)
                        return_dict[mt_filter.name] = mt_filter
                else:
                    mt_filter = PoleZeroFilter(value)
                    return_dict[mt_filter.name] = mt_filter

            elif key in ["coefficient_filter"]:
                if isinstance(value, list):
                    for v in value:
                        mt_filter = CoefficientFilter(**v)
                        return_dict[mt_filter.name] = mt_filter
                else:
                    mt_filter = CoefficientFilter(value)
                    return_dict[mt_filter.name] = mt_filter

            elif key in ["time_delay_filter"]:
                if isinstance(value, list):
                    for v in value:
                        mt_filter = TimeDelayFilter(**v)
                        return_dict[mt_filter.name] = mt_filter
                else:
                    mt_filter = TimeDelayFilter(value)
                    return_dict[mt_filter.name] = mt_filter

            elif key in ["frequency_response_table_filter"]:
                if isinstance(value, list):
                    for v in value:
                        mt_filter = FrequencyResponseTableFilter(**v)
                        return_dict[mt_filter.name] = mt_filter
                else:
                    mt_filter = FrequencyResponseTableFilter(value)
                    return_dict[mt_filter.name] = mt_filter

            elif key in ["fir_filter"]:
                if isinstance(value, list):
                    for v in value:
                        mt_filter = FIRFilter(**v)
                        return_dict[mt_filter.name] = mt_filter
                else:
                    mt_filter = FIRFilter(value)
                    return_dict[mt_filter.name] = mt_filter

        return return_dict
