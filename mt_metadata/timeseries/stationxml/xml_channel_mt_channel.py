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
    release_dict,
    read_channel_code,
    make_channel_code,
    units_names,
    create_mt_component,
)

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
                "calibration_units": None,
                "clock_drift": None,
                "comments": None,
                "description": None,
                "dip": "measurement_tilt",
                "end_date": "time_period.end",
                "equipments": None,
                "pre_amplifier": None,
                "response": None,
                "sample_rate": "sample_rate",
                "sensor": None,
                "start_date": "time_period.start",
                "types": "special",
                "water_level": None,
                "alternate_code": "component",
                "latitude": None,
                "longitude": None,
                "elevation": None,
            }
        )

        # StationXML to MT Survey
        self.mt_translator = self.flip_dict(self.xml_translator)
        self.mt_translator["units"] = "calibration_units_description"

        self.mt_comments_list = ["run.id"]
        self.run_list = None

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

        mt_channel = self._get_mt_position(xml_channel, mt_channel)
        mt_channel = self._parse_xml_comments(xml_channel.comments, mt_channel)
        mt_channel = self._sensor_to_mt(xml_channel.sensor, mt_channel)
        mt_channel = self._get_mt_units(xml_channel, mt_channel)

        for xml_key, mt_key in self.xml_translator.items():
            if mt_key:
                value = getattr(xml_channel, xml_key)
                if value:
                    mt_channel.set_attr_from_name(mt_key, value)

        if mt_channel.component is None:
            mt_channel.component = create_mt_component(xml_channel.code)

        return mt_channel

    def mt_to_xml(self, mt_channel):
        """
        Translate :class:`mt_metadata.timeseries.Channel` to 
        :class:`obspy.core.inventory.Channel`


        :param xml_channel: MT Channel object
        :type xml_channel: :class:`mt_metadata.timeseries.Channel`
        :returns: MT Channel
        :rtype: :class:`obspy.core.inventory.Channel`

        """

        if not isinstance(
            mt_channel, (metadata.Electric, metadata.Magnetic,
                         metadata.Auxiliary)
        ):
            msg = f"Input must be mt_metadata.timeseries.Channel object not {type(mt_channel)}"
            self.logger.error(msg)
            raise TypeError(msg)

        # location_code = get_location_code(mt_channel)
        alignement = "horizontal"
        if "z" in mt_channel.component.lower():
            alignement = "vertical"

        channel_code = make_channel_code(
            mt_channel.sample_rate, mt_channel.type, mt_channel.measurement_azimuth,
            orientation=alignement,
        )

        is_electric = mt_channel.type in ["electric"]
        if is_electric:
            xml_channel = inventory.Channel(
                channel_code,
                "",
                mt_channel.positive.latitude,
                mt_channel.positive.longitude,
                mt_channel.positive.elevation,
                0,
            )
        else:
            xml_channel = inventory.Channel(
                channel_code,
                "",
                mt_channel.location.latitude,
                mt_channel.location.longitude,
                mt_channel.location.elevation,
                0,
            )

        xml_channel.types = ["geophysical".upper()]
        xml_channel.sensor = self._mt_to_sensor(mt_channel)
        xml_channel.comments = self._make_xml_comments(mt_channel.comments)
        xml_channel.restricted_status = release_dict[xml_channel.restricted_status]

        for mt_key, xml_key in self.mt_translator.items():
            if xml_key is None:
                msg = f"Cannot currently map {mt_key} to inventory.station.{xml_key}"
                self.logger.debug(msg)
                continue

            # obspy only allows angles (0, 360)
            if xml_key in ["azimuth"]:
                xml_channel.azimuth = mt_channel.measurement_azimuth % 360

            elif xml_key in ["dip"]:
                xml_channel.dip = mt_channel.measurement_tilt % 360

            else:
                setattr(xml_channel, xml_key,
                        mt_channel.get_attr_from_name(mt_key))
                if mt_key == "units":
                    setattr(
                        xml_channel,
                        "calibration_units",
                        units_names[mt_channel.get_attr_from_name(mt_key)],
                    )

        return xml_channel

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
                msg = (
                    f"Cannot put sensor of type {sensor.type} into an "
                    f"MT Channel of {type(mt_channel)}."
                )
                self.logger.error(msg)
                raise ValueError(msg)
            mt_channel.sensor.id = sensor.serial_number
            mt_channel.sensor.manufacturer = sensor.manufacturer
            mt_channel.sensor.model = f"{sensor.model} {sensor.description}"
            mt_channel.sensor.type = sensor.type
            return mt_channel

        elif sensor.type.lower() in ["dipole", "electrode"]:
            if not isinstance(mt_channel, metadata.Electric):
                msg = (
                    f"Cannot put sensor of type {sensor.type} into an "
                    f"MT Channel of {type(mt_channel)}."
                )
                self.logger.error(msg)
                raise ValueError(msg)
            if sensor.serial_number:
                pid, nid = self._parse_electrode_ids(sensor.serial_number)
                mt_channel.positive.id = pid
                mt_channel.negative.id = nid

            mt_channel.positive.manufacturer = sensor.manufacturer
            mt_channel.positive.model = sensor.model
            mt_channel.positive.type = "electrode"

            mt_channel.negative.manufacturer = sensor.manufacturer
            mt_channel.negative.model = sensor.model
            mt_channel.negative.type = "electrode"

            mt_channel.dipole_length = self._parse_dipole_length(
                sensor.description)

            return mt_channel

        else:
            if not isinstance(mt_channel, metadata.Auxiliary):
                msg = (
                    f"Cannot put sensor of type {sensor.type} into an "
                    f"MT Channel of {type(mt_channel)}."
                )
                self.logger.error(msg)
                raise ValueError(msg)

            mt_channel.sensor.type = sensor.type
            mt_channel.sensor.manufacturer = sensor.manufacturer
            mt_channel.sensor.model = f"{sensor.model} {sensor.description}"
            mt_channel.sensor.id = sensor.serial_number

            return mt_channel

    def _mt_to_sensor(self, mt_channel):
        """
        Create an xml sensor from an MT channel
        """
        s = inventory.Equipment()
        if mt_channel.type in ["electric"]:

            s.type = "dipole"
            s.description = f"{mt_channel.dipole_length} meters"
            if mt_channel.positive.manufacturer:
                s.manufacturer = mt_channel.positive.manufacturer
            elif mt_channel.positive.manufacturer:
                s.manufacturer = mt_channel.negative.manufacturer

            if mt_channel.positive.model:
                s.model = mt_channel.positive.model
            elif mt_channel.positive.model:
                s.model = mt_channel.negative.model

            s.serial_number = (
                f"positive: {mt_channel.positive.id}, "
                f"negative: {mt_channel.negative.id}"
            )

        elif mt_channel.type in ["magnetic"]:
            s.type = mt_channel.sensor.type
            s.model = mt_channel.sensor.model.split()[0]
            s.serial_number = mt_channel.sensor.id
            s.manufacturer = mt_channel.sensor.manufacturer
            s.description = mt_channel.sensor.model.split()[1]

        else:
            s.type = mt_channel.sensor.type
            s.model = mt_channel.sensor.model
            s.serial_number = mt_channel.sensor.id
            s.manufacturer = mt_channel.sensor.manufacturer
            s.description = mt_channel.sensor.model

        return s

    def _parse_electrode_ids(self, serial_numbers):
        """
        parse electrode ids from a string formated 'positive: pid, negative: nid'
        """

        if ":" in serial_numbers and "," in serial_numbers:
            serial_list = serial_numbers.split(",")
            if len(serial_list) != 2:
                msg = (
                    f"Cannot parse electrode ids from {serial_numbers}. Must "
                    "have format 'positive: pid, negative: nid'"
                )
                self.logger.error(msg)
                raise ValueError(msg)

            pid, nid = [ss.split(":")[1].strip() for ss in serial_list]
            return pid, nid

        elif ":" not in serial_numbers and "," in serial_numbers:
            serial_list = serial_numbers.split(",")
            if len(serial_list) != 2:
                msg = (
                    f"Cannot parse electrode ids from {serial_numbers}. Must "
                    "have format 'positive: pid, negative: nid'"
                )
                self.logger.error(msg)
                raise ValueError(msg)

            pid, nid = [ss.strip() for ss in serial_list]
            return pid, nid
        else:
            self.logger.warning(
                "Electrod IDs are not properly formatted assigning"
                f" {serial_numbers} to both positive and negative. "
                "Accepted format is 'positive: pid, negative: nid'"
            )
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

    def _parse_xml_comments(self, xml_comments, mt_channel):
        """
        Read xml comments into an MT comment

        :param xml_comments: DESCRIPTION
        :type xml_comments: TYPE
        :param mt_channel: DESCRIPTION
        :type mt_channel: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        runs = []
        for comment in xml_comments:
            k, v = self.read_xml_comment(comment)
            if k == "mt.run.id":
                runs.append(v)
            else:
                if mt_channel.comments:
                    mt_channel.comments += f", {k}: {v}"
                else:
                    mt_channel.comments = f", {k}: {v}"
        if mt_channel.comments:
            mt_channel.comments += f", run_ids: [{','.join(runs)}]"
        else:
            mt_channel.comments = f"run_ids: [{','.join(runs)}]"

        self.run_list = runs

        return mt_channel

    def _make_xml_comments(self, mt_comment):
        """
        make xml comments from an mt comment, namely run ids.

        :param mt_comment: DESCRIPTION
        :type mt_comment: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        comments = []
        clist = mt_comment.split("run_ids:")
        for item in clist:
            if ":" in item:
                k, v = item.split(":")
                comments.append(inventory.Comment(v, subject=k))
            elif "[" in item and "]" in item:
                for run in item.replace("[", "").replace("]", "").split(","):
                    run = run.strip()
                    if run:
                        comments.append(inventory.Comment(
                            run.strip(), subject="mt.run.id"))
        return comments

    def _get_mt_position(self, xml_channel, mt_channel):
        """
        Get the correct locations given the channel type

        :param xml_channel: DESCRIPTION
        :type xml_channel: TYPE
        :param mt_channel: DESCRIPTION
        :type mt_channel: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if mt_channel.type in ["electric"]:
            for direction in ["positive", "negative"]:
                for pos in ["latitude", "longitude", "elevation"]:
                    key = f"{direction}.{pos}"
                    value = getattr(xml_channel, pos)
                    mt_channel.set_attr_from_name(key, value)
        else:
            for pos in ["latitude", "longitude", "elevation"]:
                key = f"location.{pos}"
                value = getattr(xml_channel, pos)
                mt_channel.set_attr_from_name(key, value)

        return mt_channel

    def _get_mt_units(self, xml_channel, mt_channel):
        """

        """
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

        return mt_channel
