# -*- coding: utf-8 -*-
"""
Tests for converting Experiment to StationXML

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""
# =============================================================================
# Imports
# =============================================================================
import pytest

from mt_metadata.timeseries import Experiment
from mt_metadata.utils.mttime import MTime


try:
    from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)
from mt_metadata import MT_EXPERIMENT_MULTIPLE_RUNS, MT_EXPERIMENT_MULTIPLE_RUNS_02


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def experiment_01():
    """Load the first experiment from XML file"""
    experiment = Experiment()
    experiment.from_xml(fn=MT_EXPERIMENT_MULTIPLE_RUNS.as_posix())
    return experiment


@pytest.fixture(scope="module")
def experiment_02():
    """Load the second experiment from XML file"""
    experiment = Experiment()
    experiment.from_xml(fn=MT_EXPERIMENT_MULTIPLE_RUNS_02.as_posix())
    return experiment


@pytest.fixture(scope="module")
def translator():
    """Create an XMLInventoryMTExperiment translator"""
    return XMLInventoryMTExperiment()


@pytest.fixture(scope="module")
def inventory_01(experiment_01, translator):
    """Convert experiment_01 to StationXML inventory"""
    return translator.mt_to_xml(experiment_01)


@pytest.fixture(scope="module")
def inventory_02(experiment_02, translator):
    """Convert experiment_02 to StationXML inventory"""
    return translator.mt_to_xml(experiment_02)


# =============================================================================
# Tests for Experiment 01
# =============================================================================


def test_num_networks_01(inventory_01, experiment_01):
    """Test number of networks matches number of surveys"""
    assert len(inventory_01.networks) == len(experiment_01.surveys)


def test_num_stations_01(inventory_01, experiment_01):
    """Test number of stations matches"""
    assert len(inventory_01.networks[0].stations) == len(
        experiment_01.surveys[0].stations
    )


def test_num_channels_01(inventory_01, experiment_01):
    """Test number of channels (with +3 due to h-sensor IDs not being the same)"""
    assert (
        len(inventory_01.networks[0].stations[0].channels)
        == len(experiment_01.surveys[0].stations[0].runs[0].channels) + 3
    )


def test_channel_time_periods_01(inventory_01, subtests):
    """Test channel time periods for experiment 01"""
    for code in ["LFN", "LFE", "LFZ", "LQN", "LQE"]:
        channels = inventory_01.networks[0].stations[0].select(channel=code).channels
        for ii, channel in enumerate(channels[1:], 0):
            with subtests.test(f"{code} test start"):
                assert channels[ii].start_date < channel.start_date
            with subtests.test(f"{code} test end"):
                assert channels[ii].end_date < channel.end_date
            with subtests.test(f"{code} continuity"):
                assert channels[ii].end_date < channel.start_date


def test_station_time_periods_01(inventory_01, subtests):
    """Test station time periods in relation to channels for experiment 01"""
    with subtests.test("station start time period in channels"):
        c_start = [
            MTime(time_stamp=c.start_date)
            for c in inventory_01.networks[0].stations[0].channels
        ]
        assert MTime(time_stamp=inventory_01.networks[0].stations[0].start_date) <= min(
            c_start
        )

    with subtests.test("station end time period in channels"):
        c_end = [
            MTime(time_stamp=c.end_date)
            for c in inventory_01.networks[0].stations[0].channels
        ]
        assert MTime(time_stamp=inventory_01.networks[0].stations[0].end_date) >= max(
            c_end
        )


def test_network_time_periods_01(inventory_01, subtests):
    """Test network time periods in relation to stations for experiment 01"""
    with subtests.test("network start time period in stations"):
        c_start = [
            MTime(time_stamp=c.start_date) for c in inventory_01.networks[0].stations
        ]
        assert MTime(time_stamp=inventory_01.networks[0].start_date) <= min(c_start)

    with subtests.test("network end time period in stations"):
        c_end = [
            MTime(time_stamp=c.end_date) for c in inventory_01.networks[0].stations
        ]
        assert MTime(time_stamp=inventory_01.networks[0].end_date) >= max(c_end)


# =============================================================================
# Tests for Experiment 02
# =============================================================================


def test_num_networks_02(inventory_02, experiment_02):
    """Test number of networks matches number of surveys"""
    assert len(inventory_02.networks) == len(experiment_02.surveys)


def test_num_stations_02(inventory_02, experiment_02):
    """Test number of stations matches"""
    assert len(inventory_02.networks[0].stations) == len(
        experiment_02.surveys[0].stations
    )


def test_num_channels_02(inventory_02):
    """Test number of channels (10 because channel metadata changes)"""
    assert len(inventory_02.networks[0].stations[0].channels) == 10


def test_channel_time_periods_02(inventory_02, subtests):
    """Test channel time periods for experiment 02"""
    for code in ["LFN", "LFE", "LFZ", "LQN", "LQE"]:
        channels = inventory_02.networks[0].stations[0].select(channel=code).channels
        for ii, channel in enumerate(channels[1:], 0):
            with subtests.test(f"{code} test start"):
                assert channels[ii].start_date < channel.start_date
            with subtests.test(f"{code} test end"):
                assert channels[ii].end_date < channel.end_date
            with subtests.test(f"{code} continuity"):
                assert channels[ii].end_date < channel.start_date


def test_station_time_periods_02(inventory_02, subtests):
    """Test station time periods in relation to channels for experiment 02"""
    with subtests.test("station start time period in channels"):
        c_start = [
            MTime(time_stamp=c.start_date)
            for c in inventory_02.networks[0].stations[0].channels
        ]
        assert MTime(time_stamp=inventory_02.networks[0].stations[0].start_date) <= min(
            c_start
        )

    with subtests.test("station end time period in channels"):
        c_end = [
            MTime(time_stamp=c.end_date)
            for c in inventory_02.networks[0].stations[0].channels
        ]
        assert MTime(time_stamp=inventory_02.networks[0].stations[0].end_date) >= max(
            c_end
        )


def test_network_time_periods_02(inventory_02, subtests):
    """Test network time periods in relation to stations for experiment 02"""
    with subtests.test("network start time period in stations"):
        c_start = [
            MTime(time_stamp=c.start_date) for c in inventory_02.networks[0].stations
        ]
        assert MTime(time_stamp=inventory_02.networks[0].start_date) <= min(c_start)

    with subtests.test("network end time period in stations"):
        c_end = [
            MTime(time_stamp=c.end_date) for c in inventory_02.networks[0].stations
        ]
        assert MTime(time_stamp=inventory_02.networks[0].end_date) >= max(c_end)


def test_country_is_string_02(inventory_02, subtests):
    """Test country property in experiment 02"""
    with subtests.test("is string"):
        assert isinstance(inventory_02.networks[0].stations[0].site.country, str)

    with subtests.test("is equal"):
        assert inventory_02.networks[0].stations[0].site.country == "USA"


if __name__ == "__main__":
    pytest.main([__file__])
