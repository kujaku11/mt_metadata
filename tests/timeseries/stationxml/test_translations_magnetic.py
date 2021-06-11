# -*- coding: utf-8 -*-
"""
Test translation from xml to mtml back to xml

Created on Fri Mar 26 08:15:49 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
import unittest
from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment
from mt_metadata.utils import STATIONXML_MAGNETIC
from obspy.core import inventory

# =============================================================================


class TestTranslationXML2MTML2XML(unittest.TestCase):
    def setUp(self):
        self.translator = XMLInventoryMTExperiment()
        self.mtml = self.translator.xml_to_mt(stationxml_fn=STATIONXML_MAGNETIC)
        self.original_xml = inventory.read_inventory(STATIONXML_MAGNETIC.as_posix())
        self.new_xml = self.translator.mt_to_xml(self.mtml)
        self.maxDiff = None

        self.network_0 = self.original_xml.networks[0]
        self.network_1 = self.new_xml.networks[0]

        self.station_0 = self.network_0.stations[0]
        self.station_1 = self.network_1.stations[0]

        self.channel_0 = self.network_0.stations[0].channels[0]
        self.channel_1 = self.network_1.stations[0].channels[0]

        self.response_0 = self.channel_0.response
        self.response_1 = self.channel_1.response

    def test_network_start(self):
        self.assertEqual(self.network_0.start_date, self.network_1.start_date)

    def test_network_end(self):
        # original does not have an end date
        self.assertNotEqual(
            self.network_0.end_date.isoformat(), self.network_1.end_date
        )

    def test_network_comments(self):
        original_comment_dict = dict(
            [
                (c.subject, c.value)
                for c in self.network_0.comments
                if c.value not in [None, ""]
            ]
        )
        new_comment_dict = dict(
            [
                (c.subject, c.value)
                for c in self.network_1.comments
                if c.value not in [None, ""]
            ]
        )

        self.assertDictEqual(original_comment_dict, new_comment_dict)

    def test_network_identifier(self):
        self.assertListEqual(self.network_0.identifiers, self.network_1.identifiers)

    def test_network_code(self):
        self.assertEqual(self.network_0.code, self.network_1.code)

    def test_network_restricted_status(self):
        self.assertEqual(
            self.network_0.restricted_status, self.network_1.restricted_status
        )

    def test_network_operator(self):
        self.assertEqual(
            self.network_0.operators[0].agency, self.network_1.operators[0].agency
        )

        self.assertListEqual(
            self.network_0.operators[0].contacts[0].names,
            self.network_1.operators[0].contacts[0].names,
        )

        self.assertListEqual(
            self.network_0.operators[0].contacts[0].emails,
            self.network_1.operators[0].contacts[0].emails,
        )

    def test_station_start(self):
        self.assertEqual(self.station_0.start_date, self.station_1.start_date)

    def test_station_end(self):
        # original file does not have an end date
        self.assertNotEqual(
            self.station_0.end_date.isoformat(), self.station_1.end_date
        )

    def test_station_code(self):
        self.assertEqual(self.station_0.code, self.station_1.code)

    def test_station_alternate_code(self):
        self.assertEqual(self.station_0.alternate_code, self.station_1.alternate_code)

    def test_station_restricted(self):
        self.assertEqual(
            self.station_0.restricted_status, self.station_1.restricted_status
        )

    def test_station_comments(self):
        original_comment_dict = dict(
            [
                (c.subject, c.value)
                for c in self.station_0.comments
                if c.value not in [None, ""]
            ]
        )
        new_comment_dict = dict(
            [
                (c.subject, c.value)
                for c in self.station_1.comments
                if c.value not in [None, ""]
            ]
        )

        # for now just make sure the right keys are there.  The values are slightly
        # different because of how they are parsed.
        self.assertListEqual(
            sorted(list(original_comment_dict.keys())),
            sorted(list(new_comment_dict.keys())),
        )

    def test_station_location(self):
        self.assertAlmostEqual(self.station_0.latitude, self.station_1.latitude, 4)
        self.assertAlmostEqual(self.station_0.longitude, self.station_1.longitude, 4)
        self.assertAlmostEqual(self.station_0.elevation, self.station_1.elevation, 4)

    def test_station_site(self):
        self.assertEqual(self.station_0.site.name, self.station_1.site.name)

    def test_station_equipment(self):
        for eq_0, eq_1 in zip(self.station_0.equipments, self.station_1.equipments):
            self.assertEqual(eq_0.resource_id, eq_1.resource_id)
            self.assertEqual(eq_0.type, eq_1.type)
            self.assertEqual(eq_0.manufacturer, eq_1.manufacturer)
            self.assertEqual(eq_0.model, eq_1.model)
            self.assertEqual(eq_0.serial_number, eq_1.serial_number)
            self.assertEqual(eq_0.installation_date, eq_1.installation_date)
            self.assertEqual(eq_0.removal_date, eq_1.removal_date)

    def test_channel_start(self):
        self.assertEqual(self.channel_0.start_date, self.channel_1.start_date)

    def test_channel_end(self):
        # original file does not have the correct end date
        self.assertNotEqual(
            self.channel_0.end_date.isoformat(), self.channel_1.end_date
        )

    def test_channel_code(self):
        self.assertEqual(self.channel_0.code, self.channel_1.code)

    def test_channel_alternate_code(self):
        self.assertEqual(
            self.channel_0.alternate_code.lower(), self.channel_1.alternate_code.lower()
        )

    def test_channel_restricted(self):
        self.assertEqual(
            self.channel_0.restricted_status, self.channel_1.restricted_status
        )

    def test_channel_comments(self):
        original_comment_dict = dict(
            [
                (c.subject, c.value)
                for c in self.channel_0.comments
                if c.value not in [None, ""]
            ]
        )
        new_comment_dict = dict(
            [
                (c.subject, c.value)
                for c in self.channel_1.comments
                if c.value not in [None, ""]
            ]
        )

        self.assertDictEqual(original_comment_dict, new_comment_dict)

    def test_channel_location(self):
        self.assertAlmostEqual(self.channel_0.latitude, self.channel_1.latitude, 4)
        self.assertAlmostEqual(self.channel_0.longitude, self.channel_1.longitude, 4)
        self.assertAlmostEqual(self.channel_0.elevation, self.channel_1.elevation, 4)

    def test_channel_orientation(self):
        self.assertAlmostEqual(self.channel_0.azimuth, self.channel_1.azimuth, 4)
        self.assertAlmostEqual(self.channel_0.dip, self.channel_1.dip, 4)
        self.assertAlmostEqual(self.channel_0.depth, self.channel_1.depth, 4)

    def test_channel_sample_rate(self):
        self.assertEqual(self.channel_0.sample_rate, self.channel_1.sample_rate)

    def test_channel_calibration_units(self):
        self.assertEqual(
            self.channel_0.calibration_units, self.channel_1.calibration_units
        )

    def test_channel_sensor(self):
        self.assertEqual(self.channel_0.sensor.type, self.channel_1.sensor.type)
        self.assertEqual(
            self.channel_0.sensor.description, self.channel_1.sensor.description
        )
        self.assertEqual(
            self.channel_0.sensor.manufacturer, self.channel_1.sensor.manufacturer
        )
        self.assertEqual(self.channel_0.sensor.model, self.channel_1.sensor.model)
        self.assertEqual(
            self.channel_0.sensor.serial_number, self.channel_1.sensor.serial_number
        )

    def test_response_sensitivity(self):
        self.assertAlmostEqual(
            self.response_0.instrument_sensitivity.value,
            self.response_1.instrument_sensitivity.value,
        )

        self.assertEqual(
            self.response_0.instrument_sensitivity.input_units,
            self.response_1.instrument_sensitivity.input_units,
        )

        self.assertEqual(
            self.response_0.instrument_sensitivity.output_units,
            self.response_1.instrument_sensitivity.output_units,
        )

    def test_response_zpk(self):
        zpk_0 = self.response_0.response_stages[0]
        zpk_1 = self.response_1.response_stages[0]

        # test all but the normalization and gain frequency.
        for key in [
            "pz_transfer_function_type",
            "normalization_factor",
            "zeros",
            "poles",
            "stage_sequence_number",
            "input_units",
            "output_units",
            "input_units_description",
            "output_units_description",
            "resource_id",
            "resource_id2",
            "stage_gain",
            "name",
            "description",
            "decimation_input_sample_rate",
            "decimation_factor",
            "decimation_offset",
            "decimation_delay",
            "decimation_correction",
        ]:
            attr_0 = getattr(zpk_0, key)
            attr_1 = getattr(zpk_1, key)
            if isinstance(attr_0, str):
                attr_0 = attr_0.lower()
                attr_1 = attr_1.lower()
            self.assertEqual(attr_0, attr_1)

    def test_response_coefficient_filter(self):
        f_0 = self.response_0.response_stages[1]
        f_1 = self.response_1.response_stages[1]

        # test all but the normalization and gain frequency.
        for key in [
            "cf_transfer_function_type",
            "numerator",
            "denominator",
            "stage_sequence_number",
            "input_units",
            "output_units",
            "input_units_description",
            "output_units_description",
            "resource_id",
            "resource_id2",
            "stage_gain",
            "name",
            "description",
            "decimation_input_sample_rate",
            "decimation_factor",
            "decimation_offset",
            "decimation_delay",
            "decimation_correction",
        ]:
            attr_0 = getattr(f_0, key)
            attr_1 = getattr(f_1, key)
            if isinstance(attr_0, str):
                attr_0 = attr_0.lower()
                attr_1 = attr_1.lower()
            self.assertEqual(attr_0, attr_1)

    def test_response_time_delay(self):
        f_0 = self.response_0.response_stages[2]
        f_1 = self.response_1.response_stages[2]

        # test all but the normalization and gain frequency.
        for key in [
            "cf_transfer_function_type",
            "numerator",
            "denominator",
            "stage_sequence_number",
            "input_units",
            "output_units",
            "input_units_description",
            "output_units_description",
            "resource_id",
            "resource_id2",
            "stage_gain",
            "name",
            "description",
            "decimation_input_sample_rate",
            "decimation_factor",
            "decimation_offset",
            "decimation_delay",
            "decimation_correction",
        ]:
            attr_0 = getattr(f_0, key)
            attr_1 = getattr(f_1, key)
            if isinstance(attr_0, str):
                attr_0 = attr_0.lower()
                attr_1 = attr_1.lower()
            self.assertEqual(attr_0, attr_1)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
