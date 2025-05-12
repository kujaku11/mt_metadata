# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 12:49:13 2021

:copyright:
:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.timeseries.stationxml.fdsn_tools import release_dict

from mt_metadata import timeseries as metadata
from mt_metadata.timeseries.stationxml.utils import BaseTranslator
from mt_metadata.timeseries.stationxml import XMLEquipmentMTRun
from mt_metadata.base.helpers import requires

try:
    from obspy.core import inventory
except ImportError:
    inventory = None

# =============================================================================


@requires(obspy=inventory)
class XMLStationMTStation(BaseTranslator):
    """
    translate back and forth between StationXML Station and MT Station
    """

    def __init__(self):
        """
        Initialize the XMLStationMTStation converter.

        Sets up translation dictionaries between StationXML and MT metadata
        attributes, and defines which MT attributes should be stored as comments.
        """
        super().__init__()

        self.xml_translator.update(
            {
                "alternate_code": "id",
                "channels": None,
                "code": "fdsn.id",
                "comments": "provenance.comments",
                "creation_date": "time_period.start",
                "data_availability": None,
                "description": "comments",
                "elevation": "location.elevation",
                "end_date": "time_period.end",
                "equipments": None,
                "external_references": None,
                "geology": None,
                "identifiers": None,
                "latitude": "location.latitude",
                "longitude": "location.longitude",
                "operators": "special",
                "site": "special",
                "start_date": "time_period.start",
                "termination_date": "time_period.end",
                "vault": None,
                "water_level": None,
                "restricted_status": "special",
            }
        )

        # StationXML to MT Survey
        self.mt_translator = self.flip_dict(self.xml_translator)
        self.mt_translator["geographic_name"] = "site"
        self.mt_translator["provenance.comments"] = None
        self.mt_translator["time_period.start"] = "start_date"
        self.mt_translator["time_period.end"] = "end_date"

        self.mt_comments_list = [
            "run_list",
            "orientation.method",
            "orientation.reference_frame",
            "location.declination.value",
            "location.declination.model",
            "location.declination.comments.value",
            "provenance.software.author",
            "provenance.software.name",
            "provenance.software.version",
            "provenance.comments.value",
            "data_type",
        ]

    def xml_to_mt(self, xml_station) -> metadata.Station:
        """
        Translate a StationXML station object to MT Station object.

        Parameters
        ----------
        xml_station : obspy.core.inventory.Station
            StationXML station element to convert.

        Returns
        -------
        mt_metadata.timeseries.Station
            MT Station object with attributes populated from the XML station.

        Raises
        ------
        ValueError
            If input is not an obspy.core.inventory.Station object.
        """

        if not isinstance(xml_station, inventory.Station):
            msg = f"Input must be obspy.core.inventory.station object not {type(xml_station)}"
            self.logger.error(msg)
            raise ValueError(msg)

        mt_station = metadata.Station()
        run_comments = []

        for mt_key, xml_key in self.mt_translator.items():
            if xml_key is None:
                continue
            if xml_key in ["site"]:
                site = xml_station.site
                mt_station.geographic_name = site.name

            elif mt_key in ["comments"]:
                for comment in xml_station.comments:
                    key, value = self.read_xml_comment(comment)
                    if "mt.run" in key:
                        run_comments.append({key: value})
                        continue

                    try:
                        key = key.split("mt.station.")[1]
                    except IndexError:
                        pass

                    if "summary" in key:
                        key = key.replace("summary", "comments")
                    if key in ["comments"]:
                        if mt_station.comments:
                            mt_station.comments.value += value
                        else:
                            mt_station.comments.value = value
                    else:
                        mt_station.update_attribute(key, value)

            else:
                value = getattr(xml_station, xml_key)
                if value is None:
                    continue
                if isinstance(value, (list, tuple)):
                    for k, v in zip(mt_key, value):
                        mt_station.update_attribute(k, v)
                else:
                    if xml_key == "restricted_status":
                        value = self.flip_dict(release_dict)[value]

                mt_station.update_attribute(mt_key, value)

        if mt_station.id is None:
            if mt_station.fdsn.id is not None:
                mt_station.id = mt_station.fdsn.id

        # read in equipment information
        mt_station = self._equipments_to_runs(xml_station.equipments, mt_station)
        mt_station = self._equipments_to_runs(xml_station.equipments, mt_station)
        mt_station = self._add_run_comments(run_comments, mt_station)

        return mt_station

    def mt_to_xml(self, mt_station: metadata.Station):
        """
        Convert MT Station to ObsPy StationXML Station object.

        Parameters
        ----------
        mt_station : mt_metadata.timeseries.Station
            MT Station object to convert.

        Returns
        -------
        obspy.core.inventory.Station
            StationXML Station object with attributes populated from MT Station.

        Raises
        ------
        ValueError
            If input is not an mt_metadata.timeseries.Station object,
            or if both id and fdsn.id attributes are None.

        Notes
        -----
        Station code is set to uppercase in the resulting StationXML object.
        """

        if not isinstance(mt_station, metadata.Station):
            msg = f"Input must be mt_metadata.timeseries.Station object not {type(mt_station)}"
            self.logger.error(msg)
            raise ValueError(msg)

        if mt_station.id is None:
            if mt_station.fdsn.id is None:
                msg = "Need to input id or fdsn.id, both cannot be None"
                self.logger.error(msg)
                raise ValueError(msg)
            else:
                code = mt_station.fdsn.id
        else:
            code = mt_station.id

        if mt_station.fdsn.id is None:
            mt_station.fdsn.id = mt_station.id

        xml_station = inventory.Station(
            code.upper(),
            mt_station.location.latitude,
            mt_station.location.longitude,
            mt_station.location.elevation,
        )

        for xml_key, mt_key in self.xml_translator.items():
            # need to skip code because we just set it above and it needs to be upper.

            if mt_key is None:
                self.logger.debug(
                    f"Cannot currently map mt_key.station to inventory.station.{xml_key}"
                )
                continue

            if xml_key in ["code"]:
                continue
            elif xml_key in ["alternate_code"]:
                xml_station.alternate_code = mt_station.id.upper()

            elif xml_key == "operators":
                if mt_station.acquired_by.author:
                    if mt_station.acquired_by.organization is None:
                        mt_station.acquired_by.organization = " "
                    operator = inventory.Operator(
                        agency=mt_station.acquired_by.organization
                    )
                    person = inventory.Person(names=[mt_station.acquired_by.author])
                    person = inventory.Person(names=[mt_station.acquired_by.author])
                    operator.contacts = [person]
                    xml_station.operators = [operator]

            elif xml_key == "site":
                if mt_station.geographic_name is None:
                    xml_station.site.name = mt_station.id.upper()
                    self.logger.warning(
                        f"Station.geographic_name is None, using Station.id = {mt_station.id}."
                        "Check StationXML site.name."
                    )
                else:
                    xml_station.site.name = mt_station.geographic_name

            elif xml_key == "comments":
                if mt_station.comments is not None:
                    comment = inventory.Comment(mt_station.comments.value)
                    xml_station.comments.append(comment)
            elif xml_key == "restricted_status":
                xml_station.restricted_status = release_dict[
                    xml_station.restricted_status
                ]
            elif "time_period" in mt_key:
                value = mt_station.get_attr_from_name(mt_key).time_stamp
                setattr(xml_station, xml_key, value)
            else:
                setattr(xml_station, xml_key, mt_station.get_attr_from_name(mt_key))
                setattr(xml_station, xml_key, mt_station.get_attr_from_name(mt_key))

        # add mt comments
        xml_station.comments = self.make_mt_comments(mt_station, "mt.station")

        # add run information
        for mt_run in mt_station.runs:
            run_converter = XMLEquipmentMTRun()
            xml_station.equipments.append(run_converter.mt_to_xml(mt_run))
            xml_station.comments += run_converter.make_mt_comments(
                mt_run, f"mt.run:{mt_run.id}"
            )

        return xml_station

    def _equipments_to_runs(
        self, equipments, station_obj: metadata.Station
    ) -> metadata.Station:
        """
        Convert equipment list to station runs.

        Parameters
        ----------
        equipments : list
            List of StationXML Equipment objects. (inventory.Equipement)
        station_obj : mt_metadata.timeseries.Station
            MT Station object to add runs to.

        Returns
        -------
        mt_metadata.timeseries.Station
            Updated MT Station object with runs added.

        Raises
        ------
        TypeError
            If equipments parameter is not a list.
        """
        if not isinstance(equipments, list):
            msg = f"Input must be a list not {type(equipments)}"
            self.logger.error(msg)
            raise TypeError(msg)

        for equipment in equipments:
            run_translator = XMLEquipmentMTRun()
            run_item = run_translator.xml_to_mt(equipment)
            run_index = station_obj.run_index(run_item.id)
            if run_index:
                station_obj.runs[run_index].from_dict(run_item.to_dict())
            else:
                station_obj.add_run(run_item)

        return station_obj

    def _add_run_comments(
        self, run_comments: list[dict], station_obj: metadata.Station
    ) -> metadata.Station:
        """
        Add StationXML comments to MT Station run objects.

        Parameters
        ----------
        run_comments : list of dict
            List of dictionaries containing run comments.
            Each dict should be in the format {key: value} where key
            includes the run ID and attribute name.
        station_obj : mt_metadata.timeseries.Station
            MT Station object with runs to update.

        Returns
        -------
        mt_metadata.timeseries.Station
            Updated MT Station object with comments added to runs.

        Notes
        -----
        Comment keys should be in the format "mt.run:run_id" or
        "mt.run:run_id.attribute" to specify which run and attribute
        to update.
        """
        for comment in run_comments:

            for rkey, rvalue in comment.items():
                run_id = rkey.split(":", 1)[1]
                run_attr = None
                if run_id.count(".") > 0:
                    run_id, run_attr = run_id.split(".", 1)
                run_index = station_obj.run_index(run_id)
                if run_index is None:
                    continue
                if isinstance(rvalue, dict):
                    for ckey, cvalue in rvalue.items():
                        if run_attr:
                            if run_attr == "comments":
                                value = f"{ckey}: {cvalue}"
                                try:
                                    station_obj.runs[
                                        run_index
                                    ].comments.value += f", {value}"
                                except TypeError:
                                    station_obj.runs[run_index].comments.value = value
                            else:
                                c_attr = f"{run_attr}.{ckey}"

                                station_obj.runs[run_index].update_attribute(
                                    c_attr, cvalue
                                )
                        else:
                            station_obj.runs[run_index].update_attribute(ckey, cvalue)

        return station_obj
