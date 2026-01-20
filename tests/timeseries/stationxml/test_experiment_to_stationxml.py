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
import tempfile
from pathlib import Path

import pytest

try:
    from obspy import read_inventory
    from obspy.core import inventory
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)

from mt_metadata import MT_EXPERIMENT_MULTIPLE_RUNS, MT_EXPERIMENT_MULTIPLE_RUNS_02
from mt_metadata.common.mttime import MTime
from mt_metadata.timeseries import Electric, Experiment, Magnetic, Run, Station, Survey
from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def translator():
    """Create an XMLInventoryMTExperiment translator"""
    return XMLInventoryMTExperiment()


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
def inventory_01(experiment_01, translator):
    """Convert experiment_01 to StationXML inventory"""
    return translator.mt_to_xml(experiment_01)


@pytest.fixture(scope="module")
def inventory_02(experiment_02, translator):
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
def temp_files():
    """Create temporary files for testing file I/O operations"""
    xml_file = tempfile.NamedTemporaryFile(suffix=".xml", delete=False).name
    mt_file = tempfile.NamedTemporaryFile(suffix=".xml", delete=False).name

    yield Path(xml_file), Path(mt_file)

    # Clean up
    Path(xml_file).unlink(missing_ok=True)
    Path(mt_file).unlink(missing_ok=True)


# =============================================================================
# Helper Functions
# =============================================================================


def get_channel_codes(station):
    """Get unique channel codes from a station with caching"""
    return sorted(set(c.code[:3] for c in station.channels))


def get_channels_by_code(station, code):
    """Get channels with specific code from a station with caching"""
    return station.select(channel=code).channels


# =============================================================================
# Test Classes - Original Experiment Tests
# =============================================================================


class TestExperiment01:
    """Tests for experiment 01"""

    def test_structure(self, inventory_01, experiment_01):
        """Test basic structure matches between inventory and experiment"""
        # Test network/survey count
        assert len(inventory_01.networks) == len(experiment_01.surveys)

        # Test station count
        assert len(inventory_01.networks[0].stations) == len(
            experiment_01.surveys[0].stations
        )

        # Test channel count (with +3 due to h-sensor IDs not being the same)
        assert (
            len(inventory_01.networks[0].stations[0].channels)
            == len(experiment_01.surveys[0].stations[0].runs[0].channels) + 3
        )

    def test_channel_time_periods(self, inventory_01, subtests):
        """Test channel time periods for experiment 01"""
        station = inventory_01.networks[0].stations[0]

        for code in get_channel_codes(station):
            channels = get_channels_by_code(station, code)
            if len(channels) <= 1:
                continue

            for ii, channel in enumerate(channels[1:], 0):
                with subtests.test(f"{code} start order"):
                    assert channels[ii].start_date < channel.start_date

                with subtests.test(f"{code} end order"):
                    assert channels[ii].end_date < channel.end_date

                with subtests.test(f"{code} continuity"):
                    assert channels[ii].end_date < channel.start_date

    def test_time_period_nesting(self, inventory_01, subtests):
        """Test time period nesting (station contains channels, network contains stations)"""
        # Station contains all channels
        station = inventory_01.networks[0].stations[0]

        with subtests.test("station contains channel start times"):
            c_start = [MTime(time_stamp=c.start_date) for c in station.channels]
            assert MTime(time_stamp=station.start_date) <= min(c_start)

        with subtests.test("station contains channel end times"):
            c_end = [MTime(time_stamp=c.end_date) for c in station.channels]
            assert MTime(time_stamp=station.end_date) >= max(c_end)

        # Network contains all stations
        network = inventory_01.networks[0]

        with subtests.test("network contains station start times"):
            s_start = [MTime(time_stamp=s.start_date) for s in network.stations]
            assert MTime(time_stamp=network.start_date) <= min(s_start)

        with subtests.test("network contains station end times"):
            s_end = [MTime(time_stamp=s.end_date) for s in network.stations]
            assert MTime(time_stamp=network.end_date) >= max(s_end)


class TestExperiment02:
    """Tests for experiment 02"""

    def test_structure(self, inventory_02, experiment_02):
        """Test basic structure matches between inventory and experiment"""
        # Test network/survey count
        assert len(inventory_02.networks) == len(experiment_02.surveys)

        # Test station count
        assert len(inventory_02.networks[0].stations) == len(
            experiment_02.surveys[0].stations
        )

        # Test channel count (10 because channel metadata changes)
        assert len(inventory_02.networks[0].stations[0].channels) == 10

    def test_channel_time_periods(self, inventory_02, subtests):
        """Test channel time periods for experiment 02"""
        station = inventory_02.networks[0].stations[0]

        for code in get_channel_codes(station):
            channels = get_channels_by_code(station, code)
            if len(channels) <= 1:
                continue

            for ii, channel in enumerate(channels[1:], 0):
                with subtests.test(f"{code} start order"):
                    assert channels[ii].start_date < channel.start_date

                with subtests.test(f"{code} end order"):
                    assert channels[ii].end_date < channel.end_date

                with subtests.test(f"{code} continuity"):
                    assert channels[ii].end_date < channel.start_date

    def test_time_period_nesting(self, inventory_02, subtests):
        """Test time period nesting (station contains channels, network contains stations)"""
        # Station contains all channels
        station = inventory_02.networks[0].stations[0]

        with subtests.test("station contains channel start times"):
            c_start = [MTime(time_stamp=c.start_date) for c in station.channels]
            assert MTime(time_stamp=station.start_date) <= min(c_start)

        with subtests.test("station contains channel end times"):
            c_end = [MTime(time_stamp=c.end_date) for c in station.channels]
            assert MTime(time_stamp=station.end_date) >= max(c_end)

        # Network contains all stations
        network = inventory_02.networks[0]

        with subtests.test("network contains station start times"):
            s_start = [MTime(time_stamp=s.start_date) for s in network.stations]
            assert MTime(time_stamp=network.start_date) <= min(s_start)

        with subtests.test("network contains station end times"):
            s_end = [MTime(time_stamp=s.end_date) for s in network.stations]
            assert MTime(time_stamp=network.end_date) >= max(s_end)

    def test_country_property(self, inventory_02, subtests):
        """Test country property in experiment 02"""
        country = inventory_02.networks[0].stations[0].site.country

        with subtests.test("is string"):
            assert isinstance(country, str)

        with subtests.test("correct value"):
            assert country == "USA"


# =============================================================================
# Test Classes - Conversion Tests
# =============================================================================


class TestMTToXMLConversion:
    """Tests for MT to XML conversion using sample experiment"""

    def test_basic_structure(self, sample_inventory, sample_experiment, subtests):
        """Test basic structure of converted inventory"""
        with subtests.test("network count"):
            assert len(sample_inventory.networks) == len(sample_experiment.surveys)

        with subtests.test("station count"):
            assert len(sample_inventory.networks[0].stations) == len(
                sample_experiment.surveys[0].stations
            )

        with subtests.test("channel count"):
            # At least the electric and magnetic channels should be present
            assert len(sample_inventory.networks[0].stations[0].channels) >= 2

    def test_network_properties(self, sample_inventory, subtests):
        """Test properties of the converted network"""
        network = sample_inventory.networks[0]

        properties = {
            "code": lambda n: n.code == "ZZ",
            "start_date": lambda n: n.start_date is not None,
            "end_date": lambda n: n.end_date is not None,
        }

        for name, check in properties.items():
            with subtests.test(name):
                assert check(network)

    def test_station_properties(self, sample_inventory, subtests):
        """Test properties of the converted station"""
        station = sample_inventory.networks[0].stations[0]

        properties = {
            "code": lambda s: s.code == "STA01",
            "start_date": lambda s: s.start_date is not None,
            "end_date": lambda s: s.end_date is not None,
        }

        for name, check in properties.items():
            with subtests.test(name):
                assert check(station)

    def test_channel_properties(self, sample_inventory):
        """Test properties of the converted channels"""
        station = sample_inventory.networks[0].stations[0]

        # Find electric and magnetic channels
        electric_channels = get_channels_by_code(station, "?Q?")
        magnetic_channels = get_channels_by_code(station, "?F?")

        assert len(electric_channels) > 0
        assert len(magnetic_channels) > 0
        assert "Q" in electric_channels[0].code
        assert "F" in magnetic_channels[0].code

    def test_run_comments(self, sample_inventory):
        """Test that run IDs are stored in channel comments"""
        station = sample_inventory.networks[0].stations[0]

        for channel in station.channels:
            run_comments = [c for c in channel.comments if c.subject == "mt.run.id"]
            assert len(run_comments) > 0

    def test_file_output(self, translator, sample_experiment, temp_files):
        """Test writing inventory to file and reading it back"""
        xml_file, _ = temp_files

        # Write to file
        translator.mt_to_xml(sample_experiment, stationxml_fn=xml_file)
        assert xml_file.exists()

        # Read back
        inventory = read_inventory(xml_file)
        assert len(inventory.networks) == len(sample_experiment.surveys)


class TestXMLToMTConversion:
    """Tests for XML to MT conversion using sample inventory"""

    def test_basic_structure(self, translator, sample_inventory, subtests):
        """Test converting inventory back to MT experiment"""
        experiment = translator.xml_to_mt(sample_inventory)

        with subtests.test("survey count"):
            assert len(experiment.surveys) == len(sample_inventory.networks)

        with subtests.test("station count"):
            assert len(experiment.surveys[0].stations) == len(
                sample_inventory.networks[0].stations
            )

    def test_survey_properties(self, translator, sample_inventory, subtests):
        """Test properties of the converted survey"""
        experiment = translator.xml_to_mt(sample_inventory)
        survey = experiment.surveys[0]

        properties = {
            "id": lambda s: s.id == "TEST",
            "start_date": lambda s: s.time_period.start_date is not None,
            "end_date": lambda s: s.time_period.end_date is not None,
        }

        for name, check in properties.items():
            with subtests.test(name):
                assert check(survey)

    def test_station_properties(self, translator, sample_inventory, subtests):
        """Test properties of the converted station"""
        experiment = translator.xml_to_mt(sample_inventory)
        station = experiment.surveys[0].stations[0]

        properties = {
            "id": lambda s: s.id == "STA01",
            "start_date": lambda s: s.time_period.start is not None,
            "end_date": lambda s: s.time_period.end is not None,
        }

        for name, check in properties.items():
            with subtests.test(name):
                assert check(station)

    def test_run_creation(self, translator, sample_inventory):
        """Test run creation from channels"""
        experiment = translator.xml_to_mt(sample_inventory)
        station = experiment.surveys[0].stations[0]

        # Runs should be created from channels
        assert len(station.runs) > 0

        # Each run should have channels
        for run in station.runs:
            assert len(run.channels) > 0

    def test_channel_properties(self, translator, sample_inventory, subtests):
        """Test channel properties after conversion"""
        experiment = translator.xml_to_mt(sample_inventory)
        station = experiment.surveys[0].stations[0]

        for run in station.runs:
            for channel in run.channels:
                # Channel type should be either electric or magnetic
                with subtests.test(f"channel {channel.component} type"):
                    assert channel.type in ["electric", "magnetic"]

                # Channel should have time period
                with subtests.test(f"channel {channel.component} time period"):
                    assert channel.time_period.start is not None
                    assert channel.time_period.end is not None

    def test_file_output(self, translator, sample_inventory, temp_files):
        """Test writing experiment to file and reading it back"""
        _, mt_file = temp_files

        # Convert to experiment
        experiment = translator.xml_to_mt(sample_inventory)

        # Write to file
        experiment.to_xml(mt_file)
        assert mt_file.exists()

        # Read back
        exp2 = Experiment()
        exp2.from_xml(mt_file)
        assert len(exp2.surveys) == len(experiment.surveys)


class TestRoundTripConversion:
    """Tests for round-trip conversion (MT->XML->MT)"""

    def test_basic_structure(self, translator, sample_experiment, subtests):
        """Test round-trip conversion preserves basic structure"""
        # Convert to XML then back to MT
        inventory = translator.mt_to_xml(sample_experiment)
        experiment = translator.xml_to_mt(inventory)

        with subtests.test("survey count"):
            assert len(experiment.surveys) == len(sample_experiment.surveys)

        with subtests.test("station count"):
            assert len(experiment.surveys[0].stations) == len(
                sample_experiment.surveys[0].stations
            )

    def test_survey_properties(self, translator, sample_experiment, subtests):
        """Test round-trip conversion preserves survey properties"""
        # Convert to XML then back to MT
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


class TestHelperMethods:
    """Tests for XMLInventoryMTExperiment helper methods"""

    def test_compare_xml_channel(self, translator, subtests):
        """Test compare_xml_channel method"""
        # Create two identical channels
        channel1 = self._create_test_channel("LQE", 40.0, -120.0)
        channel2 = self._create_test_channel("LQE", 40.0, -120.0)

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
                # Create a fresh channel and modify the attribute
                channel_mod = self._create_test_channel("LQE", 40.0, -120.0)
                setattr(channel_mod, attr, value)

                result = translator.compare_xml_channel(channel1, channel_mod)
                assert result is expected

    def test_add_run(self, translator, subtests):
        """Test add_run method"""
        # Create a station
        xml_station = inventory.Station(
            code="STA01",
            latitude=40.0,
            longitude=-120.0,
            elevation=100.0,
            site=inventory.Site(name="Test Site"),
        )

        # Create a run with an electric channel
        mt_run, electric_channel = self._create_test_run_with_channel("ex", "electric")
        filters_dict = {}

        # Add the run to the station
        result = translator.add_run(xml_station, mt_run, filters_dict)

        with subtests.test("electric channel added"):
            assert len(result.channels) == 1

        with subtests.test("electric channel code"):
            assert "Q" in result.channels[0].code

        # Add a magnetic channel to the run
        magnetic_channel = Magnetic(component="hy")
        magnetic_channel.time_period.start = "2020-01-01T00:00:00+00:00"
        magnetic_channel.time_period.end = "2020-01-02T00:00:00+00:00"
        magnetic_channel.sample_rate = 1.0
        magnetic_channel.type = "magnetic"
        magnetic_channel.location.latitude = 40.0
        magnetic_channel.location.longitude = -120.0

        mt_run.add_channel(magnetic_channel)

        # Add the updated run to the station
        result = translator.add_run(result, mt_run, filters_dict)

        with subtests.test("magnetic channel added"):
            assert len(result.channels) == 2

        with subtests.test("magnetic channel code"):
            assert "F" in result.channels[1].code

    @staticmethod
    def _create_test_channel(code, lat, lon):
        """Helper to create a test channel"""
        channel = inventory.Channel(
            code=code,
            location_code="",
            latitude=lat,
            longitude=lon,
            elevation=100.0,
            depth=0.0,
        )
        channel.sample_rate = 1.0
        channel.sensor = inventory.Equipment(type="MT Sensor")
        channel.azimuth = 90.0
        channel.dip = 0.0
        return channel

    @staticmethod
    def _create_test_run_with_channel(component, channel_type):
        """Helper to create a test run with a channel"""
        mt_run = Run(id="001")
        mt_run.time_period.start = "2020-01-01T00:00:00+00:00"
        mt_run.time_period.end = "2020-01-02T00:00:00+00:00"
        mt_run.sample_rate = 1.0

        if channel_type == "electric":
            channel = Electric(component=component)
            channel.positive.latitude = 40.0
            channel.positive.longitude = -120.0
        else:
            channel = Magnetic(component=component)
            channel.location.latitude = 40.0
            channel.location.longitude = -120.0

        channel.time_period.start = "2020-01-01T00:00:00+00:00"
        channel.time_period.end = "2020-01-02T00:00:00+00:00"
        channel.sample_rate = 1.0
        channel.type = channel_type

        mt_run.add_channel(channel)
        return mt_run, channel


if __name__ == "__main__":
    pytest.main([__file__])
