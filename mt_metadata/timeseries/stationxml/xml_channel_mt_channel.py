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
import copy
from collections import OrderedDict

from mt_metadata.base.helpers import requires
from mt_metadata.timeseries import AppliedFilter, Auxiliary, Electric, Magnetic
from mt_metadata.timeseries.filters.obspy_stages import create_filter_from_stage
from mt_metadata.timeseries.stationxml.fdsn_tools import (
    create_mt_component,
    make_channel_code,
    read_channel_code,
    release_dict,
)
from mt_metadata.timeseries.stationxml.utils import BaseTranslator
from mt_metadata.utils.units import get_unit_object


try:
    from obspy import UTCDateTime
    from obspy.core import inventory
except ImportError as error:
    inventory = None
    UTCDateTime = None

# =============================================================================


@requires(obspy=inventory)
class XMLChannelMTChannel(BaseTranslator):
    """
    translate back and forth between StationXML Channel and MT Channel
    """

    understood_sensor_types = [
        "logger",
        "magnetometer",
        "induction coil",
        "coil",
        "dipole",
        "electrode",
    ]

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

        self.mt_comments_list = ["run.id"]
        self.run_list = None

    def xml_to_mt(self, xml_channel, existing_filters={}):
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
            mt_channel = Electric()
        elif ch_dict["measurement"] in ["magnetic"]:
            mt_channel = Magnetic()
        else:
            mt_channel = Auxiliary(type=ch_dict["measurement"])

        mt_channel = self._get_mt_position(xml_channel, mt_channel)
        mt_channel = self._parse_xml_comments(xml_channel.comments, mt_channel)
        mt_channel = self._sensor_to_mt(xml_channel.sensor, mt_channel)
        mt_channel = self._get_mt_units(xml_channel, mt_channel)
        mt_filters = self._xml_response_to_mt(xml_channel, existing_filters)

        for xml_key, mt_key in self.xml_translator.items():
            if mt_key:
                value = getattr(xml_channel, xml_key)
                if value:
                    mt_channel.update_attribute(mt_key, value)

        if mt_channel.component in [None, ""]:
            mt_channel.component = create_mt_component(xml_channel.code)

        # fill channel filters
        for filter_name, mt_filter in mt_filters.items():
            mt_channel.filter.filter_list.append(
                AppliedFilter(
                    name=filter_name,
                    applied=True,
                    comments=mt_filter.comments,
                    stage=mt_filter.sequence_number,
                )
            )

        if UTCDateTime(mt_channel.time_period.end.time_stamp) < UTCDateTime(
            mt_channel.time_period.start.time_stamp
        ):
            mt_channel.time_period.end = "2200-01-01T00:00:00+00:00"
        return mt_channel, mt_filters

    def mt_to_xml(self, mt_channel, filters_dict, hard_code=True):
        """
        Translate :class:`mt_metadata.timeseries.Channel` to
        :class:`obspy.core.inventory.Channel`


        :param xml_channel: MT Channel object
        :type xml_channel: :class:`mt_metadata.timeseries.Channel`
        :returns: MT Channel
        :rtype: :class:`obspy.core.inventory.Channel`

        """

        if not isinstance(
            mt_channel,
            (Electric, Magnetic, Auxiliary),
        ):
            msg = f"Input must be mt_metadata.timeseries.Channel object not {type(mt_channel)}"
            self.logger.error(msg)
            raise TypeError(msg)

        # location_code = get_location_code(mt_channel)
        if not hard_code:
            alignement = "horizontal"
            if "z" in mt_channel.component.lower():
                alignement = "vertical"

            channel_code = make_channel_code(
                mt_channel.sample_rate,
                mt_channel.type,
                mt_channel.measurement_azimuth,
                orientation=alignement,
            )
        # this assumes the last character of the component is the orientation
        # direction
        elif hard_code:
            channel_code = make_channel_code(
                mt_channel.sample_rate,
                mt_channel.type,
                mt_channel.component[-1].lower(),
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
        xml_channel = self._mt_to_xml_response(mt_channel, filters_dict, xml_channel)
        xml_channel.restricted_status = release_dict[xml_channel.restricted_status]
        xml_channel = self._mt_to_xml_response(mt_channel, filters_dict, xml_channel)

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

            elif "time_period" in mt_key:
                value = mt_channel.get_attr_from_name(mt_key).time_stamp
                setattr(xml_channel, xml_key, value)

            else:
                setattr(xml_channel, xml_key, mt_channel.get_attr_from_name(mt_key))

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
        sensor.type = self._deduce_sensor_type(sensor)

        if not sensor.type:
            return mt_channel

        if sensor.type.lower() in ["magnetometer", "induction coil", "coil"]:
            if not isinstance(mt_channel, Magnetic):
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
            mt_channel.sensor.name = sensor.description

            return mt_channel

        elif sensor.type.lower() in ["dipole", "electrode"]:
            if not isinstance(mt_channel, Electric):
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

            mt_channel.dipole_length = self._parse_dipole_length(sensor.description)

            return mt_channel

        else:
            if not isinstance(mt_channel, Auxiliary):
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
            if mt_channel.sensor.model:
                s.model = mt_channel.sensor.model.split()[0]
                try:
                    s.description = mt_channel.sensor.model.split()[1]
                except IndexError:
                    pass
            s.serial_number = mt_channel.sensor.id
            s.manufacturer = mt_channel.sensor.manufacturer
            s.description = mt_channel.sensor.name

        else:
            s.type = mt_channel.sensor.type
            s.model = mt_channel.sensor.model
            s.serial_number = mt_channel.sensor.id
            s.manufacturer = mt_channel.sensor.manufacturer
            s.description = mt_channel.sensor.name

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
                if mt_channel.comments.value:
                    mt_channel.comments.value += f", {k}: {v}"
                else:
                    mt_channel.comments.value = f", {k}: {v}"
        if mt_channel.comments.value:
            mt_channel.comments.value += f", run_ids: [{','.join(runs)}]"
        else:
            mt_channel.comments.value = f"run_ids: [{','.join(runs)}]"

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
        if mt_comment.value is None:
            return comments
        clist = mt_comment.value.split("run_ids:")
        for item in clist:
            if ":" in item:
                k, v = item.split(":")
                comments.append(inventory.Comment(v, subject=k))
            elif "[" in item and "]" in item:
                for run in item.replace("[", "").replace("]", "").split(","):
                    run = run.strip()
                    if run:
                        comments.append(
                            inventory.Comment(run.strip(), subject="mt.run.id")
                        )
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
        """ """
        if len(xml_channel.response.response_stages) == 0:
            return mt_channel
        name = xml_channel.response.response_stages[-1].output_units
        description = xml_channel.response.response_stages[-1].output_units_description
        description = xml_channel.response.response_stages[-1].output_units_description
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

    def _xml_response_to_mt(self, xml_channel, existing_filters={}):
        """
        parse the filters from obspy into mt filters
        """
        ch_filter_dict = OrderedDict()
        for i_stage, stage in enumerate(xml_channel.response.response_stages):
            new_and_unnamed = False
            mt_filter = create_filter_from_stage(stage)
            if not mt_filter.name:
                filter_name, new_and_unnamed = self._add_filter_number(
                    existing_filters, mt_filter
                )
                mt_filter.name = filter_name

            if mt_filter.decimation_active:
                # keep filter names unique if same one used more than once
                mt_filter.name += f"_{mt_filter.decimation_input_sample_rate}"

            if new_and_unnamed:
                self.logger.info(
                    f"Found an unnamed filter, named it: '{mt_filter.name}'"
                )
                existing_filters[filter_name] = mt_filter

            ch_filter_dict[mt_filter.name.lower()] = mt_filter

        return ch_filter_dict

    def _add_filter_number(self, existing_filters, mt_filter):
        """
        return the next number the number of filters

        :param keys: DESCRIPTION
        :type keys: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        # check for existing filters
        for f_key, f_obj in existing_filters.items():
            if f_obj.type == mt_filter.type:
                if round(abs(f_obj.complex_response([1])[0])) == round(
                    abs(mt_filter.complex_response([1])[0])
                ):
                    return f_obj.name, False

        try:
            last = sorted([k for k in existing_filters.keys() if mt_filter.type in k])[
                -1
            ]
            last = sorted([k for k in existing_filters.keys() if mt_filter.type in k])[
                -1
            ]
        except IndexError:
            return f"{mt_filter.type}_{0:02}", True
        try:
            return f"{mt_filter.type}_{int(last[-2:]) + 1:02}", True
        except ValueError:
            return f"{mt_filter.type}_{0:02}", True

    def _mt_to_xml_response(self, mt_channel, filters_dict, xml_channel):
        """
        Translate MT filters into Obspy Response

        :param mt_channel: DESCRIPTION
        :type mt_channel: TYPE
        :param filters_dict: DESCRIPTION
        :type filters_dict: TYPE
        :param xml_channel: DESCRIPTION
        :type xml_channel: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        mt_channel_response = mt_channel.channel_response(filters_dict)
        xml_channel.response = mt_channel_response.to_obspy(
            sample_rate=mt_channel.sample_rate
        )

        unit_obj = get_unit_object(mt_channel_response.units_in)

        xml_channel.calibration_units = unit_obj.symbol
        xml_channel.calibration_units_description = unit_obj.name

        return xml_channel

    def _deduce_sensor_type(self, sensor):
        """

        :param sensor: Information about a sensor, usually extractes from FDSN XML
        :type sensor: obspy.core.inventory.util.Equipment

        :return:
        """
        original_sensor_type = sensor.type
        original_sensor_description = sensor.description
        # set sensor_type to be a string if it is None
        if original_sensor_type is None:
            sensor_type = ""  # make a string
            msg = f"Sensor {sensor} does not have field type attr"
            self.logger.debug(msg)
        else:
            sensor_type = copy.deepcopy(original_sensor_type)

        if original_sensor_description is None:
            sensor_description = ""  # make a string
        else:
            sensor_description = copy.deepcopy(original_sensor_type)

        if sensor_type.lower() in self.understood_sensor_types:
            return sensor_type
        else:
            self.logger.warning(
                f" sensor {sensor} type {sensor.type} not in {self.understood_sensor_types}"
            )
            self.logger.warning(
                f" sensor {sensor} type {sensor.type} not in {self.understood_sensor_types}"
            )

        #  Try handling Bartington FGM at Earthscope ... this is a place holder for handling non-standard cases
        if sensor_type.lower() == "bartington":
            sensor_type = "magnetometer"
        if not sensor_type:
            if sensor_description == "Bartington 3-Axis Fluxgate Sensor":
                sensor_type = "magnetometer"
            if sensor_description:
                if ("bf-4" in sensor_description.lower()) & (
                    "schlumberger" in sensor_description.lower()
                ):  # BSL-NCEDC
                    sensor_type = "magnetometer"
                elif ("electric" in sensor_description.lower()) & (
                    "dipole" in sensor_description.lower()
                ):  # BSL-NCEDC
                    sensor_type = "dipole"

        # reset sensor_type to None it it was not handled
        if not sensor_type:
            sensor_type = original_sensor_type
            self.logger.error("sensor type could not be resolved")

        return sensor_type
