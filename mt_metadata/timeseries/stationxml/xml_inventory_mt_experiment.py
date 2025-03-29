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
from copy import deepcopy
from loguru import logger

from mt_metadata import timeseries as metadata
from mt_metadata.timeseries.stationxml import (
    XMLNetworkMTSurvey,
    XMLStationMTStation,
    XMLChannelMTChannel,
)

from obspy.core import inventory
from obspy import read_inventory

# =============================================================================


class XMLInventoryMTExperiment:
    """
    Read the full files and put the elements in the appropriate locations.

    """

    def __init__(self):
        self.logger = logger
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
                    mt_channel, mt_filters = self.channel_translator.xml_to_mt(
                        xml_channel, mt_survey.filters
                    )
                    mt_survey.filters.update(mt_filters)
                    # if there is a run list match channel to runs
                    if self.channel_translator.run_list:
                        for run_id in sorted(self.channel_translator.run_list):
                            # need to make a copy of the channel otherwise
                            # the properties are constantly overwritten as we loop
                            # through the runs
                            run_channel = deepcopy(mt_channel)
                            mt_run = mt_station.get_run(run_id)
                            # need to set the start and end time to the run
                            run_channel.time_period.start = (
                                mt_run.time_period.start
                            )
                            run_channel.time_period.end = mt_run.time_period.end
                            mt_run.add_channel(run_channel)
                    # if there are runs already try to match by start, end, sample_rate
                    # initialized runs have a sample rate of 0.  This could be an
                    # issue in the future.
                    elif mt_station.runs:
                        for mt_run in mt_station.runs:
                            if (
                                mt_run.sample_rate == mt_channel.sample_rate
                                or mt_run.sample_rate == 0
                            ):
                                # match assuming the runs have the correct start
                                # and end times.
                                if (
                                    mt_run.time_period.start
                                    >= mt_channel.time_period.start
                                ) and (
                                    mt_run.time_period.end
                                    <= mt_channel.time_period.end
                                ):
                                    mt_run.channels.append(mt_channel)
                                    mt_run.sample_rate = mt_channel.sample_rate
                    # make a new run with generic information
                    else:
                        mt_run = metadata.Run(
                            id=f"{len(mt_station.runs)+1:03d}"
                        )
                        mt_run.time_period.start = mt_channel.time_period.start
                        mt_run.time_period.end = mt_channel.time_period.end
                        mt_run.sample_rate = mt_channel.sample_rate
                        mt_run.channels.append(mt_channel)
                        mt_station.runs.append(mt_run)
                mt_station.update_time_period()
                mt_survey.stations.append(mt_station)
            if xml_network.stations:
                mt_survey.update_bounding_box()
                mt_survey.update_time_period()
            # need to check if the network/survey already exists, the files
            # from make_mth5_from_iris have multiples of the same network
            if mt_survey.id in mt_experiment.surveys.keys():
                mt_experiment.surveys[mt_survey.id].stations.update(
                    mt_survey.stations
                )
            else:
                mt_experiment.surveys.append(mt_survey)
        if mt_fn:
            mt_experiment.to_xml(fn=mt_fn)
        return mt_experiment

    def mt_to_xml(
        self, mt_experiment, mt_fn=None, stationxml_fn=None, ns_dict=None
    ):
        """
        Convert from MT :class:`mt_metadata.timeseries.Experiment` to
        :class:`obspy.core.inventory.Inventory`

        :param mt_experiment: DESCRIPTION
        :type mt_experiment: TYPE
        :param mt_fn: DESCRIPTION, defaults to None
        :type mt_fn: TYPE, optional
        :param stationxml_fn: DESCRIPTION, defaults to None
        :type stationxml_fn: TYPE, optional
        :param ns_dict: DESCRIPTION, defaults to None
        :type ns_dict: TYPE, optional
        :raises ValueError: DESCRIPTION
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if mt_fn:
            mt_experiment = metadata.Experiment()
            mt_experiment.from_xml(mt_fn)
        if not mt_experiment:
            msg = "Must provide either an experiment object or file path"
            self.logger.error(msg)
            raise ValueError(msg)
        xml_inventory = inventory.Inventory()
        for mt_survey in mt_experiment.surveys:
            xml_network = self.network_translator.mt_to_xml(mt_survey)
            for mt_station in mt_survey.stations:
                xml_station = self.station_translator.mt_to_xml(mt_station)
                if mt_survey.country is not None:
                    xml_station.site.country = ",".join(
                        [str(country) for country in mt_survey.country]
                    )
                # need to sort the runs by time
                for mt_run in mt_station.runs:
                    xml_station = self.add_run(
                        xml_station, mt_run, mt_survey.filters
                    )
                xml_network.stations.append(xml_station)
            xml_inventory.networks.append(xml_network)
        if stationxml_fn:
            if isinstance(stationxml_fn, Path):
                stationxml_fn = stationxml_fn.as_posix()
            xml_inventory.write(stationxml_fn, "stationxml", nsmap=ns_dict)
        return xml_inventory

    def add_run(self, xml_station, mt_run, filters_dict):
        """
        Check to see if channel information already exists in the channel list of
        an xml station.

        .. todo:: Need to make sure the times are updated

        :param xml_station: DESCRIPTION
        :type xml_station: TYPE
        :param xml_channel: DESCRIPTION
        :type xml_channel: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        for mt_channel in mt_run.channels:
            xml_channel = self.channel_translator.mt_to_xml(
                mt_channel, filters_dict
            )
            existing_channels = xml_station.select(
                channel=xml_channel.code
            ).channels

            if existing_channels:
                find = False
                start_list = [c.start_date for c in existing_channels]
                existing_channel = existing_channels[
                    start_list.index(max(start_list))
                ]
                # should only compare the last channel
                # for existing_channel in existing_channels:
                run_list = [c.value for c in existing_channel.comments]
                # Compare channel metadata if matches just add run.id if its
                # not already there.
                self.logger.debug(
                    f"Comparing {xml_channel.code} to {existing_channel.code}"
                )
                if self.compare_xml_channel(xml_channel, existing_channel):
                    find = True
                    self.logger.debug(
                        f"Matched {xml_channel.code}={existing_channel.code}"
                    )
                    if not mt_run.id in run_list:
                        self.logger.debug(
                            f"adding run id {mt_run.id} to {run_list}"
                        )
                        existing_channel.comments.append(
                            inventory.Comment(mt_run.id, subject="mt.run.id")
                        )
                    if xml_channel.start_date < existing_channel.start_date:
                        self.logger.debug("Changed starting time")
                        existing_channel.start_date = xml_channel.start_date
                    if xml_channel.end_date > existing_channel.end_date:
                        self.logger.debug("Changed ending time")
                        existing_channel.end_date = xml_channel.end_date
                    # continue
                if not find:
                    self.logger.debug(
                        f"xxx Unmatched {xml_channel.code}!={existing_channel.code}"
                    )
                    run_list = [c.value for c in xml_channel.comments]
                    if not mt_run.id in run_list:
                        self.logger.debug(
                            f"adding run id {mt_run.id} to {run_list}"
                        )
                        xml_channel.comments.append(
                            inventory.Comment(mt_run.id, subject="mt.run.id")
                        )
                    xml_station.channels.append(xml_channel)
            else:
                self.logger.debug(
                    f"no existing channels for {xml_channel.code}"
                )
                run_list = [c.value for c in xml_channel.comments]
                if not mt_run.id in run_list:
                    self.logger.debug(
                        f"adding run id {mt_run.id} to {run_list}"
                    )
                    xml_channel.comments.append(
                        inventory.Comment(mt_run.id, subject="mt.run.id")
                    )
                xml_station.channels.append(xml_channel)
        return xml_station

    def compare_xml_channel(self, xml_channel_01, xml_channel_02):
        """
        Compare xml channels to see if a new epoch needs to be made or not.

        :param xml_channel_01: DESCRIPTION
        :type xml_channel_01: TYPE
        :param xml_channel_02: DESCRIPTION
        :type xml_channel_02: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if xml_channel_01.code != xml_channel_02.code:
            self.logger.debug(f"{xml_channel_01.code} != {xml_channel_02.code}")
            return False
        if xml_channel_01.sample_rate != xml_channel_02.sample_rate:
            self.logger.debug(
                f"{xml_channel_01.sample_rate} != {xml_channel_02.sample_rate}"
            )
            return False
        if xml_channel_01.sensor != xml_channel_02.sensor:
            self.logger.debug(
                f"{xml_channel_01.sensor} != {xml_channel_02.sensor}"
            )
            return False
        if round(xml_channel_01.latitude, 3) != round(
            xml_channel_02.latitude, 3
        ):
            self.logger.debug(
                f"{round(xml_channel_01.latitude, 3)} != {round(xml_channel_02.latitude, 3)}"
            )
            return False
        if round(xml_channel_01.longitude, 3) != round(
            xml_channel_02.longitude, 3
        ):
            self.logger.debug(
                f"{round(xml_channel_01.longitude, 3)} != {round(xml_channel_02.longitude, 3)}"
            )
            return False
        if round(xml_channel_01.azimuth, 2) != round(xml_channel_02.azimuth, 2):
            self.logger.debug(
                f"{round(xml_channel_01.azimuth, 2)} != {round(xml_channel_02.azimuth, 2)}"
            )
            return False
        if round(xml_channel_01.dip, 2) != round(xml_channel_02.dip, 2):
            self.logger.debug(
                f"{round(xml_channel_01.dip, 2)} != {round(xml_channel_02.dip, 2)}"
            )
            return False
        return True
