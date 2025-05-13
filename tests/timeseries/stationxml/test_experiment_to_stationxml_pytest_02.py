# -*- coding: utf-8 -*-
"""
Tests for XMLInventoryMTExperiment class

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""
import tempfile
from pathlib import Path

import pytest


try:
    from obspy import read_inventory
    from obspy.core import inventory
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)

from mt_metadata import MT_EXPERIMENT_MULTIPLE_RUNS, MT_EXPERIMENT_MULTIPLE_RUNS_02
from mt_metadata.timeseries import Electric, Experiment, Magnetic, Run, Station, Survey
from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment
from mt_metadata.utils.mttime import MTime


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def translator():
    """Create an XMLInventoryMTExperiment translator"""
    return XMLInventoryMTExperiment()


@pytest.fixture(scope="module")
def experiment_01():
    """Load experiment with multiple runs"""
    experiment = Experiment()
    experiment.from_xml(MT_EXPERIMENT_MULTIPLE_RUNS.as_posix())
    return experiment


@pytest.fixture(scope="module")
def experiment_02():
    """Load experiment with multiple runs (version 2)"""
    experiment = Experiment()
    experiment.from_xml(MT_EXPERIMENT_MULTIPLE_RUNS_02.as_posix())
    return experiment


@pytest.fixture(scope="module")
def inventory_01(translator, experiment_01):
    """Convert experiment_01 to StationXML inventory"""
    return translator.mt_to_xml(experiment_01)


@pytest.fixture(scope="module")
def inventory_02(translator, experiment_02):
    """Convert experiment_02 to StationXML inventory"""
    return translator.mt_to_xml(experiment_02)


@pytest.fixture(scope="module")
def sample_experiment():
    """Create a simple experiment for testing"""
    experiment = Experiment()
    survey = Survey(id="TEST")
    survey.fdsn.network = "ZZ"
    station = Station(id="STA01")
    run1 = Run(id="001")
    run1.time_period.start = "2020-01-01T00:00:00+00:00"
    run1.time_period.end = "2020-01-02T00:00:00+00:00"
    run1.sample_rate = 1.0

    channel_ex = Electric(component="ex")
    channel_ex.time_period.start = "2020-01-01T00:00:00+00:00"
    channel_ex.time_period.end = "2020-01-02T00:00:00+00:00"
    channel_ex.sample_rate = 1.0
    channel_ex.type = "electric"

    channel_hy = Magnetic(component="hy")
    channel_hy.time_period.start = "2020-01-01T00:00:00+00:00"
    channel_hy.time_period.end = "2020-01-02T00:00:00+00:00"
    channel_hy.sample_rate = 1.0
    channel_hy.type = "magnetic"

    run1.add_channel(channel_ex)
    run1.add_channel(channel_hy)

    run2 = Run(id="002")
    run2.time_period.start = "2020-01-02T00:00:00+00:00"
    run2.time_period.end = "2020-01-03T00:00:00+00:00"
    run2.sample_rate = 1.0

    channel_ex2 = Electric(component="ex")
    channel_ex2.time_period.start = "2020-01-02T00:00:00+00:00"
    channel_ex2.time_period.end = "2020-01-03T00:00:00+00:00"
    channel_ex2.sample_rate = 1.0
    channel_ex2.type = "electric"

    channel_hy2 = Magnetic(component="hy")
    channel_hy2.time_period.start = "2020-01-02T00:00:00+00:00"
    channel_hy2.time_period.end = "2020-01-03T00:00:00+00:00"
    channel_hy2.sample_rate = 1.0
    channel_hy2.type = "magnetic"

    run2.add_channel(channel_ex2)
    run2.add_channel(channel_hy2)

    station.add_run(run1)
    station.add_run(run2)
    survey.add_station(station)
    experiment.add_survey(survey)

    return experiment


@pytest.fixture(scope="module")
def sample_inventory(translator, sample_experiment):
    """Convert sample_experiment to inventory"""
    return translator.mt_to_xml(sample_experiment)


@pytest.fixture(scope="module")
def temp_xml_file():
    """Create a temporary file for StationXML output"""
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    yield tmp_path
    tmp_path.unlink(missing_ok=True)


@pytest.fixture(scope="module")
def temp_mt_file():
    """Create a temporary file for MT XML output"""
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    yield tmp_path
    tmp_path.unlink(missing_ok=True)


# =============================================================================
# Test MT to XML Conversion
# =============================================================================


def test_mt_to_xml_basic_structure(sample_inventory, sample_experiment, subtests):
    """Test basic structure of converted inventory"""
    with subtests.test("network count"):
        assert len(sample_inventory.networks) == len(sample_experiment.surveys)

    with subtests.test("station count"):
        assert len(sample_inventory.networks[0].stations) == len(
            sample_experiment.surveys[0].stations
        )

    with subtests.test("channel count"):
        # We should have channels for both runs, but they might be combined if identical
        assert len(sample_inventory.networks[0].stations[0].channels) >= 2


def test_mt_to_xml_network_properties(sample_inventory, subtests):
    """Test properties of the converted network"""
    network = sample_inventory.networks[0]

    with subtests.test("code"):
        assert network.code == "ZZ"

    with subtests.test("time period"):
        assert network.start_date is not None
        assert network.end_date is not None


def test_mt_to_xml_station_properties(sample_inventory, subtests):
    """Test properties of the converted station"""
    station = sample_inventory.networks[0].stations[0]

    with subtests.test("code"):
        assert station.code == "STA01"

    with subtests.test("time period"):
        assert station.start_date is not None
        assert station.end_date is not None


def test_mt_to_xml_channel_properties(sample_inventory, subtests):
    """Test properties of the converted channels"""
    station = sample_inventory.networks[0].stations[0]

    # Find electric and magnetic channels
    electric_channels = station.select(channel="?Q?").channels
    magnetic_channels = station.select(channel="?F?").channels

    with subtests.test("electric channel exists"):
        assert len(electric_channels) > 0

    with subtests.test("magnetic channel exists"):
        assert len(magnetic_channels) > 0

    with subtests.test("electric channel code"):
        assert "Q" in electric_channels[0].code

    with subtests.test("magnetic channel code"):
        assert "F" in magnetic_channels[0].code


def test_mt_to_xml_run_comments(sample_inventory, subtests):
    """Test that run IDs are stored in channel comments"""
    station = sample_inventory.networks[0].stations[0]

    for channel in station.channels:
        with subtests.test(f"run comments in {channel.code}"):
            run_comments = [c for c in channel.comments if c.subject == "mt.run.id"]
            assert len(run_comments) > 0


def test_mt_to_xml_file_output(translator, sample_experiment, temp_xml_file):
    """Test writing inventory to file"""
    translator.mt_to_xml(sample_experiment, stationxml_fn=temp_xml_file)
    assert temp_xml_file.exists()

    # Verify we can read it back
    inventory = read_inventory(temp_xml_file)
    assert len(inventory.networks) == len(sample_experiment.surveys)


# =============================================================================
# Test XML to MT Conversion
# =============================================================================


def test_xml_to_mt_basic_structure(translator, sample_inventory, subtests):
    """Test converting inventory back to MT experiment"""
    experiment = translator.xml_to_mt(sample_inventory)

    with subtests.test("survey count"):
        assert len(experiment.surveys) == len(sample_inventory.networks)

    with subtests.test("station count"):
        assert len(experiment.surveys[0].stations) == len(
            sample_inventory.networks[0].stations
        )


def test_xml_to_mt_survey_properties(translator, sample_inventory, subtests):
    """Test properties of the converted survey"""
    experiment = translator.xml_to_mt(sample_inventory)
    survey = experiment.surveys[0]

    with subtests.test("id"):
        assert survey.id == "TEST"

    with subtests.test("time period"):
        assert survey.time_period.start_date is not None
        assert survey.time_period.end_date is not None


def test_xml_to_mt_station_properties(translator, sample_inventory, subtests):
    """Test properties of the converted station"""
    experiment = translator.xml_to_mt(sample_inventory)
    station = experiment.surveys[0].stations[0]

    with subtests.test("id"):
        assert station.id == "STA01"

    with subtests.test("time period"):
        assert station.time_period.start is not None
        assert station.time_period.end is not None


def test_xml_to_mt_run_creation(translator, sample_inventory, subtests):
    """Test run creation from channels"""
    experiment = translator.xml_to_mt(sample_inventory)
    station = experiment.surveys[0].stations[0]

    with subtests.test("run exists"):
        assert len(station.runs) > 0

    with subtests.test("run has channels"):
        for run in station.runs:
            assert len(run.channels) > 0


def test_xml_to_mt_channel_properties(translator, sample_inventory, subtests):
    """Test channel properties after conversion"""
    experiment = translator.xml_to_mt(sample_inventory)
    station = experiment.surveys[0].stations[0]

    for run in station.runs:
        for channel in run.channels:
            with subtests.test(f"channel {channel.component} type"):
                assert channel.type in ["electric", "magnetic"]

            with subtests.test(f"channel {channel.component} time period"):
                assert channel.time_period.start is not None
                assert channel.time_period.end is not None


def test_xml_to_mt_file_output(translator, sample_inventory, temp_mt_file):
    """Test writing experiment to file"""
    experiment = translator.xml_to_mt(sample_inventory)
    experiment.to_xml(temp_mt_file)
    assert temp_mt_file.exists()

    # Verify we can read it back
    exp2 = Experiment()
    exp2.from_xml(temp_mt_file)
    assert len(exp2.surveys) == len(experiment.surveys)


# =============================================================================
# Test Round Trip Conversion
# =============================================================================


def test_round_trip_basic_structure(translator, sample_experiment, subtests):
    """Test round-trip conversion preserves basic structure"""
    inventory = translator.mt_to_xml(sample_experiment)
    experiment = translator.xml_to_mt(inventory)

    with subtests.test("survey count"):
        assert len(experiment.surveys) == len(sample_experiment.surveys)

    with subtests.test("station count"):
        assert len(experiment.surveys[0].stations) == len(
            sample_experiment.surveys[0].stations
        )


def test_round_trip_survey_properties(translator, sample_experiment, subtests):
    """Test round-trip conversion preserves survey properties"""
    inventory = translator.mt_to_xml(sample_experiment)
    experiment = translator.xml_to_mt(inventory)

    original_survey = sample_experiment.surveys[0]
    converted_survey = experiment.surveys[0]

    with subtests.test("id"):
        assert converted_survey.id == original_survey.id

    with subtests.test("time period"):
        assert MTime(time_stamp=converted_survey.time_period.start_date) == MTime(
            time_stamp=original_survey.time_period.start_date
        )
        assert MTime(time_stamp=converted_survey.time_period.end_date) == MTime(
            time_stamp=original_survey.time_period.end_date
        )


# =============================================================================
# Test Helper Methods
# =============================================================================


def test_compare_xml_channel(translator, subtests):
    """Test compare_xml_channel method"""
    # Create two identical channels
    channel1 = inventory.Channel(
        code="LQE",
        location_code="",
        latitude=40.0,
        longitude=-120.0,
        elevation=100.0,
        depth=0.0,
    )
    channel1.sample_rate = 1.0
    channel1.sensor = inventory.Equipment(type="MT Sensor")
    channel1.azimuth = 90.0
    channel1.dip = 0.0

    channel2 = inventory.Channel(
        code="LQE",
        location_code="",
        latitude=40.0,
        longitude=-120.0,
        elevation=100.0,
        depth=0.0,
    )
    channel2.sample_rate = 1.0
    channel2.sensor = inventory.Equipment(type="MT Sensor")
    channel2.azimuth = 90.0
    channel2.dip = 0.0

    with subtests.test("identical channels"):
        assert translator.compare_xml_channel(channel1, channel2) is True

    # Test different attributes
    tests = [
        ("code", "LQN", False),
        ("sample_rate", 2.0, False),
        ("latitude", 41.0, False),
        ("longitude", -119.0, False),
        ("azimuth", 0.0, False),
        ("dip", 90.0, False),
    ]

    for attr, value, expected in tests:
        with subtests.test(f"different {attr}"):
            channel2_mod = inventory.Channel(
                code="LQE",
                location_code="",
                latitude=40.0,
                longitude=-120.0,
                elevation=100.0,
                depth=0.0,
            )
            channel2_mod.sample_rate = 1.0
            channel2_mod.sensor = inventory.Equipment(type="MT Sensor")
            channel2_mod.azimuth = 90.0
            channel2_mod.dip = 0.0

            # Modify the attribute
            setattr(channel2_mod, attr, value)

            result = translator.compare_xml_channel(channel1, channel2_mod)
            assert result is expected


def test_add_run(translator, subtests):
    """Test add_run method"""
    # Create a station and run
    xml_station = inventory.Station(
        code="STA01",
        latitude=40.0,
        longitude=-120.0,
        elevation=100.0,
        site=inventory.Site(name="Test Site"),
    )

    mt_run = Run(id="001")
    mt_run.time_period.start = "2020-01-01T00:00:00+00:00"
    mt_run.time_period.end = "2020-01-02T00:00:00+00:00"
    mt_run.sample_rate = 1.0

    # Add a channel
    channel = Electric(component="ex")
    channel.time_period.start = "2020-01-01T00:00:00+00:00"
    channel.time_period.end = "2020-01-02T00:00:00+00:00"
    channel.sample_rate = 1.0
    channel.type = "electric"
    channel.positive.latitude = 40.0
    channel.positive.longitude = -120.0

    mt_run.add_channel(channel)

    # Create filters dictionary
    filters_dict = {}

    # Add the run to the station
    result = translator.add_run(xml_station, mt_run, filters_dict)

    with subtests.test("channel added"):
        assert len(result.channels) == 1

    with subtests.test("channel code"):
        assert "Q" in result.channels[0].code

    # Test adding the same run again
    result = translator.add_run(result, mt_run, filters_dict)

    with subtests.test("no duplicate channel"):
        assert len(result.channels) == 1

    # Test adding a different channel
    channel2 = Magnetic(component="hy")
    channel2.time_period.start = "2020-01-01T00:00:00+00:00"
    channel2.time_period.end = "2020-01-02T00:00:00+00:00"
    channel2.sample_rate = 1.0
    channel2.type = "magnetic"
    channel2.location.latitude = 40.0
    channel2.location.longitude = -120.0

    mt_run.add_channel(channel2)

    result = translator.add_run(result, mt_run, filters_dict)

    with subtests.test("second channel added"):
        assert len(result.channels) == 2

    with subtests.test("channel code"):
        assert "F" in result.channels[1].code


# =============================================================================
# Test Complex Scenarios
# =============================================================================


def test_multiple_runs_time_periods(inventory_01, subtests):
    """Test channel time periods across multiple runs"""
    for code in ["LFN", "LFE", "LFZ", "LQN", "LQE"]:
        channels = inventory_01.networks[0].stations[0].select(channel=code).channels

        if len(channels) > 1:
            for ii, channel in enumerate(channels[1:], 0):
                with subtests.test(f"{code} test start"):
                    assert channels[ii].start_date < channel.start_date

                with subtests.test(f"{code} test end"):
                    assert channels[ii].end_date < channel.end_date

                with subtests.test(f"{code} continuity"):
                    assert channels[ii].end_date < channel.start_date


def test_country_is_string(inventory_02):
    """Test country property is properly formatted as string"""
    assert isinstance(inventory_02.networks[0].stations[0].site.country, str)
    assert inventory_02.networks[0].stations[0].site.country == "USA"


if __name__ == "__main__":
    pytest.main([__file__])
