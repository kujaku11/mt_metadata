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
import enum

from mt_metadata import timeseries as metadata
from mt_metadata.base.helpers import requires
from mt_metadata.timeseries.stationxml.utils import BaseTranslator


try:
    from obspy.core import inventory
except ImportError:
    inventory = None

# =============================================================================


@requires(obspy=inventory)
class XMLEquipmentMTRun(BaseTranslator):
    """
    translate back and forth between StationXML Station and MT Station
    """

    def __init__(self):
        super().__init__()

        self.xml_translator = {
            "type": "data_type",
            "manufacturer": "data_logger.manufacturer",
            "model": "data_logger.model",
            "serial_number": "data_logger.id",
            "installation_date": "time_period.start",
            "removal_date": "time_period.end",
            "description": "special",
            "resource_id": "id",
        }

        # StationXML to MT Survey
        self.mt_translator = self.flip_dict(self.xml_translator)
        self.mt_translator["notes"] = "description"

        self.mt_comments_list = [
            {"acquired_by": ["acquired_by.author", "acquired_by.comments"]},
            {"metadata_by": ["metadata_by.author", "metadata_by.comments"]},
            "comments",
        ]

        self.mt_description_list = [
            "data_logger.firmware.author",
            "data_logger.firmware.name",
            "data_logger.firmware.version",
            "data_logger.power_source.comments.value",
            "data_logger.power_source.id",
            "data_logger.power_source.type",
            "data_logger.power_source.voltage.end",
            "data_logger.power_source.voltage.start",
            "data_logger.timing_system.comments.value",
            "data_logger.timing_system.drift",
            "data_logger.timing_system.type",
            "data_logger.timing_system.uncertainty",
            "data_logger.type",
        ]

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
        for xml_key, mt_key in self.xml_translator.items():
            value = getattr(equipment, xml_key)
            if xml_key in ["description"]:
                mt_run = self._parse_description(value, mt_run)
            elif xml_key in ["resource_id"]:
                mt_run.id = value.split(":")[1]
            elif xml_key in ["installation_date", "removal_date"]:
                # Handle time fields - convert from ObsPy UTCDateTime to string
                if value is not None:
                    # Convert ObsPy UTCDateTime to ISO format string for MTime objects
                    value = str(value)
                mt_run.update_attribute(mt_key, value)
            else:
                mt_run.update_attribute(mt_key, value)

        return mt_run

    def mt_to_xml(self, mt_run):
        """
        Convert an :class:mt_metadata.timeseries.Run` to XML equipment and comments

        :param mt_run: DESCRIPTION
        :type mt_run: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        equipment = inventory.Equipment()
        for mt_key, xml_key in self.mt_translator.items():
            if mt_key == "notes":
                value = self._make_description(mt_run)
            elif mt_key == "id":
                value = f"mt.run.id:{mt_run.id}"
            elif "date" in xml_key:
                time_obj = mt_run.get_attr_from_name(mt_key)
                # Convert MTime object to ISO format string for ObsPy UTCDateTime
                value = (
                    time_obj.isoformat()
                    if hasattr(time_obj, "isoformat")
                    else time_obj.time_stamp
                )
            else:
                value = mt_run.get_attr_from_name(mt_key)
                # Handle enum values by getting their actual value instead of string representation
                if isinstance(value, enum.Enum):
                    value = value.value
            setattr(equipment, xml_key, value)

        return equipment

    def _parse_description(self, description, run_obj):
        """
        Parse a run description into run

        :param description: DESCRIPTION
        :type description: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        for d_str in description.split(","):
            d_key, d_value = d_str.split(":")
            d_value = d_value.strip()
            if not d_value in ["", "None", "null"]:
                run_obj.update_attribute(
                    f"data_logger.{d_key.strip()}", d_value.strip()
                )

        return run_obj

    def _make_description(self, run_obj):
        """
        Make an Equipment description from a run object

        :param run_obj: DESCRIPTION
        :type run_obj: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if not isinstance(run_obj, metadata.Run):
            msg = (
                f"Input must be a mt_metadta.timeseries.Run object not {type(run_obj)}"
            )
            self.logger.error(msg)
            raise TypeError(msg)

        lines = []
        for key in self.mt_description_list:
            value = run_obj.get_attr_from_name(key)
            if value:
                lines.append(f"{key.split('data_logger.')[1]}: {value}")

        return ", ".join(lines)
