# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 18:36:41 2021

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

import unittest
import pytest

try:
    from obspy import read_inventory
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)
from mt_metadata.timeseries.stationxml import XMLEquipmentMTRun
from mt_metadata import STATIONXML_02


class TestRunFromXML(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.xml_equipment = (
            self.inventory.networks[0].stations[0].equipments[0]
        )

        self.converter = XMLEquipmentMTRun()
        self.mt_run = self.converter.xml_to_mt(self.xml_equipment)

    def test_id(self):
        self.assertEqual(self.mt_run.id, "a")

    def test_data_type(self):
        self.assertEqual(self.mt_run.data_type, "LP")

    def test_data_logger(self):
        with self.subTest("gps"):
            self.assertEqual(self.mt_run.data_logger.timing_system.type, "GPS")
        with self.subTest("firmware author"):
            self.assertEqual(
                self.mt_run.data_logger.firmware.author, "Barry Narod"
            )
        with self.subTest("firmware version"):
            self.assertEqual(self.mt_run.data_logger.firmware.version, None)
        with self.subTest("power source"):
            self.assertEqual(
                self.mt_run.data_logger.power_source.type, "battery"
            )
        with self.subTest("data logger model"):
            self.assertEqual(self.mt_run.data_logger.model, "NIMS")
        with self.subTest("data logger id"):
            self.assertEqual(self.mt_run.data_logger.id, "2612-09")

    def test_time_period(self):
        with self.subTest("start"):
            self.assertEqual(
                self.mt_run.time_period.start, "2020-06-08T22:57:13+00:00"
            )
        with self.subTest("end"):
            self.assertEqual(
                self.mt_run.time_period.end, "2020-06-08T23:54:50+00:00"
            )


class TestEquipmemtXMLFromMT(unittest.TestCase):
    """
    test making equipment from MT Run
    """

    @classmethod
    def setUpClass(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.base_xml_equipment = (
            self.inventory.networks[0].stations[0].equipments[0]
        )

        self.converter = XMLEquipmentMTRun()
        self.mt_run = self.converter.xml_to_mt(self.base_xml_equipment)
        self.test_xml_equipment = self.converter.mt_to_xml(self.mt_run)

    def test_resource_id(self):
        self.assertEqual(
            self.base_xml_equipment.resource_id,
            self.test_xml_equipment.resource_id,
        )

    def test_type(self):
        self.assertEqual(
            self.base_xml_equipment.type, self.test_xml_equipment.type
        )

    def test_description(self):
        self.assertNotEqual(
            self.base_xml_equipment.description,
            self.test_xml_equipment.description,
        )
        self.assertEqual(
            (
                "firmware.author: Barry Narod, "
                "power_source.type: battery, "
                "timing_system.type: GPS"
            ),
            self.test_xml_equipment.description,
        )

    def test_manufacturer(self):
        self.assertEqual(
            self.base_xml_equipment.manufacturer,
            self.test_xml_equipment.manufacturer,
        )

    def test_model(self):
        self.assertEqual(
            self.base_xml_equipment.model, self.test_xml_equipment.model
        )

    def test_serial_number(self):
        self.assertEqual(
            self.base_xml_equipment.serial_number,
            self.test_xml_equipment.serial_number,
        )

    def test_installation_date(self):
        self.assertEqual(
            self.base_xml_equipment.installation_date,
            self.test_xml_equipment.installation_date,
        )

    def test_removal_date(self):
        self.assertEqual(
            self.base_xml_equipment.removal_date,
            self.test_xml_equipment.removal_date,
        )


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
