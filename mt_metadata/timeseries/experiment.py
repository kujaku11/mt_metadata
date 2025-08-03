# -*- coding: utf-8 -*-
"""
Containers for the full metadata tree

Experiment --> Survey --> Station --> Run --> Channel

Each level has a list attribute

Created on Mon Feb  8 21:25:40 2021

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
import json

# =============================================================================
# Imports
# =============================================================================
from collections import OrderedDict
from pathlib import Path
from typing import Annotated
from xml.etree import cElementTree as et

from loguru import logger
from pydantic import computed_field, Field, field_validator

from mt_metadata.base import helpers, MetadataBase
from mt_metadata.common.list_dict import ListDict

from . import Auxiliary, Electric, Magnetic, Run, Station, Survey
from .filters import (
    CoefficientFilter,
    FIRFilter,
    FrequencyResponseTableFilter,
    PoleZeroFilter,
    TimeDelayFilter,
)


# =============================================================================


class Experiment(MetadataBase):
    """
    Top level of the metadata
    """

    surveys: Annotated[
        ListDict | list | dict | OrderedDict,
        Field(
            default_factory=ListDict,
            description="List of surveys in the experiment",
            title="List of Surveys",
            example=[{"id": "survey_1"}, {"id": "survey_2"}],
            json_schema_extra={
                "required": False,
                "units": None,
            },
        ),
    ]

    def __str__(self) -> str:
        lines = ["Experiment Contents", "-" * 20]
        if len(self.surveys) > 0:
            lines.append(f"Number of Surveys: {len(self.surveys)}")
            for survey in self.surveys:
                lines.append(f"  Survey ID: {survey.id}")
                lines.append(f"  Number of Stations: {survey.n_stations}")
                lines.append(f"  Number of Filters: {len(survey.filters.keys())}")
                lines.append(f"  {'-' * 20}")
                for f_key, f_object in survey.filters.items():
                    lines.append(f"    Filter Name: {f_key}")
                    lines.append(f"    Filter Type: {f_object.type}")
                    lines.append(f"    {'-' * 20}")
                for station in survey.stations:
                    lines.append(f"    Station ID: {station.id}")
                    lines.append(f"    Number of Runs: {station.n_runs}")
                    lines.append(f"    {'-' * 20}")
                    for run in station.runs:
                        lines.append(f"      Run ID: {run.id}")
                        lines.append(f"      Number of Channels: {run.n_channels}")
                        lines.append(
                            "      Recorded Channels: "
                            + ", ".join(run.channels_recorded_all)
                        )
                        lines.append(f"      Start: {run.time_period.start}")
                        lines.append(f"      End:   {run.time_period.end}")

                        lines.append(f"      {'-' * 20}")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def merge(self, other: "Experiment") -> "Experiment":
        """
        Merge two Experiment objects
        """
        if isinstance(other, Experiment):
            self.surveys.extend(other.surveys)

            return self
        else:
            msg = f"Can only merge Experiment objects, not {type(other)}"
            logger.error(msg)
            raise TypeError(msg)

    @computed_field
    @property
    def n_surveys(self) -> int:
        return len(self.surveys)

    @field_validator("surveys", mode="before")
    @classmethod
    def validate_surveys(cls, value) -> ListDict:
        """set the survey list"""

        if not isinstance(value, (list, tuple, dict, ListDict, OrderedDict)):
            msg = (
                "input station_list must be an iterable, should be a list or dict "
                f"not {type(value)}"
            )
            logger.error(msg)
            raise TypeError(msg)

        fails = []
        surveys = ListDict()
        if isinstance(value, (dict, ListDict, OrderedDict)):
            value_list = value.values()

        elif isinstance(value, (list, tuple)):
            value_list = value

        for ii, survey in enumerate(value_list):
            if isinstance(survey, (dict, OrderedDict)):
                s = Survey()
                s.from_dict(survey)
                surveys.append(s)
            elif not isinstance(survey, Survey):
                msg = f"Item {ii} is not type(Survey); type={type(survey)}"
                fails.append(msg)
                logger.error(msg)
            else:
                surveys.append(survey)
        if len(fails) > 0:
            raise TypeError("\n".join(fails))
        return surveys

    @property
    def survey_names(self) -> list[str]:
        """Return names of surveys in experiment"""
        return self.surveys.keys()

    def has_survey(self, survey_id: str) -> bool:
        """
        Has survey id

        :param survey_id: DESCRIPTION
        :type survey_id: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if survey_id in self.survey_names:
            return True
        return False

    def survey_index(self, survey_id: str) -> int | None:
        """
        Get survey index

        :param survey_id: DESCRIPTION
        :type survey_id: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if self.has_survey(survey_id):
            return self.survey_names.index(survey_id)
        return None

    def add_survey(self, survey_obj: "Survey") -> None:
        """
        Add a survey, if has the same name update that object.

        :param survey_obj: DESCRIPTION
        :type survey_obj: `:class:`mt_metadata.timeseries.Survey`
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if not isinstance(survey_obj, Survey):
            raise TypeError(
                f"Input must be a mt_metadata.timeseries.Survey object not {type(survey_obj)}"
            )

        if self.has_survey(survey_obj.id):
            self.surveys[survey_obj.id].update(survey_obj)
            logger.debug(f"survey {survey_obj.id} already exists, updating metadata")
        else:
            self.surveys.append(survey_obj)

    def get_survey(self, survey_id: str) -> "Survey":
        """
        Get a survey from the survey id

        :param survey_id: DESCRIPTION
        :type survey_id: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if self.has_survey(survey_id):
            return self.surveys[survey_id]
        else:
            logger.warning(f"Could not find survey {survey_id}")
            return None

    def remove_survey(self, survey_id: str, update: bool = True) -> None:
        """
        Remove a survey from the experiment

        :param survey_id: DESCRIPTION
        :type survey_id: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if self.has_survey(survey_id):
            self.surveys.remove(survey_id)
            logger.debug(f"Removed survey {survey_id} from experiment")

        else:
            logger.warning(f"Could not find survey {survey_id} to remove")

    def to_dict(self, nested: bool = False, required: bool = True) -> dict:
        """
        create a dictionary for the experiment object.

        :param nested: DESCRIPTION, defaults to False
        :type nested: TYPE, optional
        :param single: DESCRIPTION, defaults to False
        :type single: TYPE, optional
        :param required: DESCRIPTION, defaults to True
        :type required: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        kwargs = {"nested": nested, "single": True, "required": required}

        ex_dict = {"experiment": {"surveys": []}}
        for survey in self.surveys:
            survey_dict = survey.to_dict(**kwargs)
            survey_dict["stations"] = []
            survey_dict["filters"] = []
            for station in survey.stations:
                station_dict = station.to_dict(**kwargs)
                station_dict["runs"] = []
                for run in station.runs:
                    run_dict = run.to_dict(**kwargs)
                    run_dict["channels"] = []
                    for channel in run.channels:
                        run_dict["channels"].append(channel.to_dict(**kwargs))
                    station_dict["runs"].append(run_dict)
                survey_dict["stations"].append(station_dict)
            for f_key, f_object in survey.filters.items():
                survey_dict["filters"].append(f_object.to_dict(**kwargs))
            ex_dict["experiment"]["surveys"].append(survey_dict)

        return ex_dict

    def from_dict(self, ex_dict: dict | OrderedDict, skip_none: bool = True) -> None:
        """
        fill from an input dictionary

        :param ex_dict: DESCRIPTION
        :type ex_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if not isinstance(ex_dict, dict):
            msg = f"experiemnt input must be a dictionary not {type(ex_dict)}"
            logger.debug(msg)
            raise TypeError(msg)
        if "experiment" not in ex_dict.keys():
            return

        for survey_dict in ex_dict["experiment"]["surveys"]:
            survey_object = Survey()
            survey_object.from_dict(survey_dict, skip_none=skip_none)
            self.add_survey(survey_object)

    def to_json(
        self,
        fn: str | Path = None,
        nested: bool = False,
        indent: str = " " * 4,
        required: bool = True,
    ) -> str | None:
        """
        Write a json string from a given object, taking into account other
        class objects contained within the given object.

        :param nested: make the returned json nested
        :type nested: [ True | False ] , default is False

        """

        if fn is not None:
            with open(fn, "w") as fid:
                json.dump(
                    self.to_dict(nested=nested, required=required),
                    fid,
                    cls=helpers.NumpyEncoder,
                    indent=indent,
                )

        else:
            return json.dumps(
                self.to_dict(nested=nested, required=required),
                cls=helpers.NumpyEncoder,
                indent=indent,
            )

    def from_json(self, json_str: str, skip_none: bool = True) -> None:
        """
        read in a json string and update attributes of an object

        :param json_str: json string or file path
        :type json_str: string or :class:`pathlib.Path`

        """
        if isinstance(json_str, str):
            try:
                json_path = Path(json_str)
                if json_path.exists():
                    with open(json_path, "r") as fid:
                        json_dict = json.load(fid)
            except OSError:
                pass
            json_dict = json.loads(json_str)
        elif isinstance(json_str, Path):
            if json_str.exists():
                with open(json_str, "r") as fid:
                    json_dict = json.load(fid)
        elif not isinstance(json_str, (str, Path)):
            msg = "Input must be valid JSON string not %"
            logger.error(msg, type(json_str))
            raise TypeError(msg % type(json_str))
        self.from_dict(json_dict, skip_none=skip_none)

    def to_xml(
        self, fn: str | Path = None, required: bool = True, sort: bool = True
    ) -> et.Element:
        """
        Write XML version of the experiment

        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        experiment_element = et.Element(self.__class__.__name__)
        if sort:
            self.surveys.sort()
        for survey in self.surveys:
            survey.update_bounding_box()
            survey.update_time_period()
            survey_element = survey.to_xml(required=required)
            filter_element = et.SubElement(survey_element, "filters")
            for key, value in survey.filters.items():
                filter_element.append(value.to_xml(required=required))
            if sort:
                survey.stations.sort()
            for station in survey.stations:
                station.update_time_period()
                station_element = station.to_xml(required=required)
                if sort:
                    station.runs.sort()
                for run in station.runs:
                    run.update_time_period()
                    run_element = run.to_xml(required=required)
                    if sort:
                        run.channels.sort()
                    for channel in run.channels:
                        if channel.type in ["electric"]:
                            if (
                                channel.positive.latitude == 0
                                and channel.positive.longitude == 0
                                and channel.positive.elevation == 0
                            ):
                                channel.positive.latitude = station.location.latitude
                                channel.positive.longitude = station.location.longitude
                                channel.positive.elevation = station.location.elevation
                        else:
                            if (
                                channel.location.latitude == 0
                                and channel.location.longitude == 0
                                and channel.location.elevation == 0
                            ):
                                channel.location.latitude = station.location.latitude
                                channel.location.longitude = station.location.longitude
                                channel.location.elevation = station.location.elevation

                        run_element.append(channel.to_xml(required=required))
                    station_element.append(run_element)
                survey_element.append(station_element)
            experiment_element.append(survey_element)

        if fn:
            with open(fn, "w") as fid:
                fid.write(helpers.element_to_string(experiment_element))
        return experiment_element

    def from_xml(
        self,
        fn: str | Path = None,
        element: et.Element | None = None,
        sort: bool = True,
        skip_none: bool = True,
    ) -> None:
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
            stations = self._pop_dictionary(survey_dict["survey"], "station")
            survey_obj = Survey()
            survey_obj.from_dict(survey_dict, skip_none=skip_none)
            fd = survey_dict["survey"].pop("filters")
            filter_dict = self._read_filter_dict(fd)
            survey_obj.filters.update(filter_dict)

            for station_dict in stations:
                station_obj = Station()
                runs = self._pop_dictionary(station_dict, "run")
                station_obj.from_dict(station_dict, skip_none=skip_none)
                for run_dict in runs:
                    run_obj = Run()

                    for ch in ["electric", "magnetic", "auxiliary"]:
                        try:
                            for ch_dict in self._pop_dictionary(run_dict, ch):
                                if ch == "electric":
                                    channel = Electric()
                                elif ch == "magnetic":
                                    channel = Magnetic()
                                elif ch == "auxiliary":
                                    channel = Auxiliary()
                                channel.from_dict(ch_dict, skip_none=skip_none)
                                run_obj.add_channel(channel)
                        except KeyError:
                            logger.debug(f"Could not find channel {ch}")
                    run_obj.from_dict(run_dict, skip_none=skip_none)
                    station_obj.add_run(run_obj)
                survey_obj.add_station(station_obj)
            self.add_survey(survey_obj)

            if sort:
                self.sort()

    def _pop_dictionary(self, in_dict: dict, element: str) -> list:
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

    def to_pickle(self, fn: str | Path = None) -> None:
        """
        Write a pickle version of the experiment

        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

    def from_pickle(self, fn: str | Path = None) -> None:
        """
        Read pickle version of experiment

        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

    # def validate_experiment(self):
    #     """
    #     Validate experiment is legal

    #     :return: DESCRIPTION
    #     :rtype: TYPE

    #     """
    #     pass

    def _read_filter_dict(self, filters_dict: dict | None) -> ListDict:
        """
        Read in filter element an put it in the correct object

        :param filter_element: DESCRIPTION
        :type filter_element: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        return_dict = ListDict()
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

    def sort(self, inplace: bool = True) -> "Experiment":
        """
        sort surveys, stations, runs, channels alphabetically/numerically

        :param inplace: DESCRIPTION, defaults to True
        :type inplace: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if inplace:
            self.surveys.sort()
            for survey in self.surveys:
                survey.stations.sort()
                for station in survey.stations:
                    station.runs.sort()
                    for run in station.runs:
                        run.channels.sort()

        else:
            ex = Experiment()
            ex.from_dict(self.to_dict())
            ex.sort()
            return ex
