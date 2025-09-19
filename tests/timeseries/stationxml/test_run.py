# -*- coding: utf-8 -*-
"""
Tests for converting between StationXML Equipment and MT Run objects using pytest

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""

import pytest


try:
    from obspy import read_inventory
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)

from mt_metadata import STATIONXML_02
from mt_metadata.timeseries.stationxml import XMLEquipmentMTRun


@pytest.fixture(scope="module")
def inventory():
    """Load StationXML inventory."""
    return read_inventory(STATIONXML_02.as_posix())


@pytest.fixture(scope="module")
def xml_equipment(inventory):
    """Get the first equipment from the inventory."""
    return inventory.networks[0].stations[0].equipments[0]


@pytest.fixture(scope="module")
def converter():
    """Create an XMLEquipmentMTRun converter."""
    return XMLEquipmentMTRun()


@pytest.fixture(scope="module")
def mt_run(converter, xml_equipment):
    """Convert XML equipment to MT run."""
    return converter.xml_to_mt(xml_equipment)


@pytest.fixture(scope="module")
def test_xml_equipment(converter, mt_run):
    """Convert MT run back to XML equipment."""
    return converter.mt_to_xml(mt_run)


class TestRunFromXML:
    """
    Test converting StationXML Equipment to MT Run object
    """

    def test_id(self, mt_run, subtests):
        """Test run ID."""
        with subtests.test("id matches expected value"):
            assert mt_run.id == "a"

    def test_data_type(self, mt_run, subtests):
        """Test data type."""
        with subtests.test("data_type matches expected value"):
            assert mt_run.data_type == "LP"

    def test_data_logger(self, mt_run, subtests):
        """Test data logger attributes."""
        with subtests.test("timing system type is GPS"):
            assert mt_run.data_logger.timing_system.type == "GPS"

        with subtests.test("firmware author is Barry Narod"):
            assert mt_run.data_logger.firmware.author == "Barry Narod"

        with subtests.test("firmware version is empty"):
            assert mt_run.data_logger.firmware.version == ""

        with subtests.test("power source type is battery"):
            assert mt_run.data_logger.power_source.type == "battery"

        with subtests.test("data logger model is NIMS"):
            assert mt_run.data_logger.model == "NIMS"

        with subtests.test("data logger id is 2612-09"):
            assert mt_run.data_logger.id == "2612-09"

    def test_time_period(self, mt_run, subtests):
        """Test time period attributes."""
        with subtests.test("start time matches expected value"):
            assert mt_run.time_period.start == "2020-06-08T22:57:13+00:00"

        with subtests.test("end time matches expected value"):
            assert mt_run.time_period.end == "2020-06-08T23:54:50+00:00"


class TestEquipmentXMLFromMT:
    """
    Test converting MT Run back to StationXML Equipment
    """

    def test_resource_id(self, base_xml_equipment, test_xml_equipment, subtests):
        """Test resource ID."""
        with subtests.test("resource_id matches"):
            assert base_xml_equipment.resource_id == test_xml_equipment.resource_id

    def test_type(self, base_xml_equipment, test_xml_equipment, subtests):
        """Test equipment type."""
        with subtests.test("type matches"):
            assert base_xml_equipment.type == test_xml_equipment.type

    def test_description(self, base_xml_equipment, test_xml_equipment, subtests):
        """Test equipment description."""
        with subtests.test("description differs"):
            assert base_xml_equipment.description != test_xml_equipment.description

        expected_description = (
            "firmware.author: Barry Narod, "
            "power_source.type: battery, "
            "timing_system.type: GPS"
        )

        with subtests.test("description has expected format"):
            assert test_xml_equipment.description == expected_description

    def test_manufacturer(self, base_xml_equipment, test_xml_equipment, subtests):
        """Test equipment manufacturer."""
        with subtests.test("manufacturer matches"):
            assert base_xml_equipment.manufacturer == test_xml_equipment.manufacturer

    def test_model(self, base_xml_equipment, test_xml_equipment, subtests):
        """Test equipment model."""
        with subtests.test("model matches"):
            assert base_xml_equipment.model == test_xml_equipment.model

    def test_serial_number(self, base_xml_equipment, test_xml_equipment, subtests):
        """Test equipment serial number."""
        with subtests.test("serial_number matches"):
            assert base_xml_equipment.serial_number == test_xml_equipment.serial_number

    def test_installation_date(self, base_xml_equipment, test_xml_equipment, subtests):
        """Test installation date."""
        with subtests.test("installation_date matches"):
            assert (
                base_xml_equipment.installation_date
                == test_xml_equipment.installation_date
            )

    def test_removal_date(self, base_xml_equipment, test_xml_equipment, subtests):
        """Test removal date."""
        with subtests.test("removal_date matches"):
            assert base_xml_equipment.removal_date == test_xml_equipment.removal_date


# Additional fixture needed for TestEquipmentXMLFromMT
@pytest.fixture(scope="module")
def base_xml_equipment(xml_equipment):
    """Provide the base XML equipment fixture."""
    return xml_equipment
