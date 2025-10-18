# -*- coding: utf-8 -*-
"""
Tests for StationXML to MT Experiment conversion.

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""

import pytest


try:
    from obspy import read_inventory
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)

from mt_metadata import STATIONXML_01, STATIONXML_02, STATIONXML_MULTIPLE_NETWORKS
from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def translator():
    """Create a translator instance to be used across all tests."""
    return XMLInventoryMTExperiment()


@pytest.fixture(scope="module")
def inventory_01():
    """Load inventory from STATIONXML_01."""
    return read_inventory(STATIONXML_01.as_posix())


@pytest.fixture(scope="module")
def inventory_02():
    """Load inventory from STATIONXML_02."""
    return read_inventory(STATIONXML_02.as_posix())


@pytest.fixture(scope="module")
def inventory_multiple():
    """Load inventory from STATIONXML_MULTIPLE_NETWORKS."""
    return read_inventory(STATIONXML_MULTIPLE_NETWORKS.as_posix())


@pytest.fixture(scope="module")
def experiment_01(inventory_01, translator):
    """Convert inventory_01 to MT experiment."""
    return translator.xml_to_mt(inventory_01)


@pytest.fixture(scope="module")
def experiment_02(inventory_02, translator):
    """Convert inventory_02 to MT experiment."""
    return translator.xml_to_mt(inventory_02)


@pytest.fixture(scope="module")
def experiment_multiple(inventory_multiple, translator):
    """Convert inventory_multiple to MT experiment."""
    return translator.xml_to_mt(inventory_multiple)


# =============================================================================
# Tests for Inventory 01
# =============================================================================


class TestInventory01:
    """Tests for the first inventory."""

    def test_structure(self, inventory_01, experiment_01, subtests):
        """Test the structure of converted experiment."""
        with subtests.test("number of networks equals number of surveys"):
            assert len(inventory_01.networks) == len(experiment_01.surveys)

        with subtests.test("number of stations matches"):
            assert len(inventory_01.networks[0].stations) == len(
                experiment_01.surveys[0].stations
            )

        with subtests.test("number of channels matches"):
            assert len(inventory_01.networks[0].stations[0].channels) == len(
                experiment_01.surveys[0].stations[0].runs[0].channels
            )


# =============================================================================
# Tests for Inventory 02
# =============================================================================


class TestInventory02:
    """Tests for the second inventory."""

    def test_structure(self, inventory_02, experiment_02, subtests):
        """Test the structure of converted experiment."""
        with subtests.test("number of networks equals number of surveys"):
            assert len(inventory_02.networks) == len(experiment_02.surveys)

        with subtests.test("number of stations matches"):
            assert len(inventory_02.networks[0].stations) == len(
                experiment_02.surveys[0].stations
            )


# =============================================================================
# Tests for Multiple Networks Inventory
# =============================================================================


class TestInventoryMultipleNetworks:
    """Tests for multiple networks inventory."""

    def test_surveys(self, experiment_multiple):
        """Test that all networks with same alternate_code are combined into one survey."""
        assert list(experiment_multiple.surveys.keys()) == ["Kansas 2017 Long Period"]

    def test_stations(self, experiment_multiple):
        """Test that stations from multiple networks are included in the survey."""
        expected_stations = ["MTF20", "WYYS2", "MTC20", "WYYS3"]
        actual_stations = list(
            experiment_multiple.surveys["Kansas 2017 Long Period"].stations.keys()
        )

        # Sort both lists to ensure order doesn't affect comparison
        assert sorted(actual_stations) == sorted(expected_stations)

    def test_station_count(self, inventory_multiple, experiment_multiple, subtests):
        """Test that station counts are correct across multiple networks."""
        # Calculate total stations from inventory
        total_inventory_stations = sum(
            len(net.stations) for net in inventory_multiple.networks
        )

        # Calculate total stations in experiment
        total_experiment_stations = len(
            experiment_multiple.surveys["Kansas 2017 Long Period"].stations
        )

        with subtests.test("total station count matches"):
            assert total_inventory_stations == total_experiment_stations

        with subtests.test("inventory networks count"):
            assert len(inventory_multiple.networks) == 2

        with subtests.test("experiment surveys count"):
            assert len(experiment_multiple.surveys) == 1


# =============================================================================
# Advanced Tests
# =============================================================================


class TestAdvancedFeatures:
    """Tests for advanced features of the converter."""

    def test_channel_distribution(self, experiment_multiple, subtests):
        """Test that channels are distributed correctly to runs."""
        stations = experiment_multiple.surveys["Kansas 2017 Long Period"].stations

        for station_key, station in stations.items():
            with subtests.test(f"station {station_key} has runs"):
                assert len(station.runs) > 0

            with subtests.test(f"station {station_key} has channels in run"):
                assert len(station.runs[0].channels) > 0


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
