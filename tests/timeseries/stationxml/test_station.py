# -*- coding: utf-8 -*-
"""
Tests for converting between StationXML Station and MT Station objects using pytest

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""
from collections import OrderedDict

# =============================================================================
# Imports
# =============================================================================
import pytest


try:
    from obspy import read_inventory
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)

from mt_metadata import STATIONXML_01, STATIONXML_02
from mt_metadata.timeseries import Station
from mt_metadata.timeseries.stationxml import XMLStationMTStation


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def inventory_01():
    """Load first StationXML inventory."""
    return read_inventory(STATIONXML_01.as_posix())


@pytest.fixture(scope="module")
def inventory_02():
    """Load second StationXML inventory."""
    return read_inventory(STATIONXML_02.as_posix())


@pytest.fixture(scope="module")
def xml_station_01(inventory_01):
    """Get station from first inventory."""
    return inventory_01.networks[0].stations[0]


@pytest.fixture(scope="module")
def xml_station_02(inventory_02):
    """Get station from second inventory."""
    return inventory_02.networks[0].stations[0]


@pytest.fixture(scope="module")
def converter():
    """Create an XMLStationMTStation converter."""
    return XMLStationMTStation()


@pytest.fixture(scope="module")
def mt_station_01(converter, xml_station_01):
    """Convert first XML station to MT station."""
    return converter.xml_to_mt(xml_station_01)


@pytest.fixture(scope="module")
def mt_station_02(converter, xml_station_02):
    """Convert second XML station to MT station."""
    return converter.xml_to_mt(xml_station_02)


@pytest.fixture(scope="module")
def test_xml_station_01(converter, mt_station_01):
    """Convert first MT station back to XML station."""
    return converter.mt_to_xml(mt_station_01)


@pytest.fixture(scope="module")
def test_xml_station_02(converter, mt_station_02):
    """Convert second MT station back to XML station."""
    return converter.mt_to_xml(mt_station_02)


# =============================================================================
# Tests
# =============================================================================


class TestReadXMLStation01:
    """
    Test reading first StationXML station into MT station object
    """

    def test_time_period(self, mt_station_01, subtests):
        """Test time period attributes."""
        with subtests.test("start time matches expected value"):
            assert mt_station_01.time_period.start == "2020-06-02T18:41:43+00:00"

        with subtests.test("end time matches expected value"):
            assert mt_station_01.time_period.end == "2020-07-13T21:46:12+00:00"

    def test_code(self, mt_station_01, subtests):
        """Test station code attributes."""
        with subtests.test("station fdsn id"):
            assert mt_station_01.fdsn.id == "CAS04"

        with subtests.test("station id"):
            assert mt_station_01.id == "CAS04"

    def test_location(self, mt_station_01, subtests):
        """Test location attributes."""
        with subtests.test("latitude"):
            assert mt_station_01.location.latitude == 37.633351

        with subtests.test("longitude"):
            assert mt_station_01.location.longitude == -121.468382

        with subtests.test("elevation"):
            assert mt_station_01.location.elevation == 329.3875

    def test_geographic_name(self, mt_station_01, subtests):
        """Test geographic name."""
        with subtests.test("geographic name matches expected"):
            assert mt_station_01.geographic_name == "Corral Hollow, CA, USA"

    def test_run_list(self, mt_station_01, subtests):
        """Test run list."""
        with subtests.test("run list is empty"):
            assert mt_station_01.run_list == []


class TestMTStationToXML01:
    """
    Test converting first MT station back to StationXML station
    """

    def test_time_period(self, xml_station_01, test_xml_station_01, subtests):
        """Test time period attributes."""
        with subtests.test("start_date matches"):
            assert xml_station_01.start_date == test_xml_station_01.start_date

        with subtests.test("end_date matches"):
            assert xml_station_01.end_date == test_xml_station_01.end_date

    def test_code(self, xml_station_01, test_xml_station_01, subtests):
        """Test code attributes."""
        with subtests.test("station code matches"):
            assert xml_station_01.code == test_xml_station_01.code

        with subtests.test("alternate code differs"):
            # the original file does not have an alternate code
            assert xml_station_01.alternate_code != test_xml_station_01.alternate_code

    def test_location(self, xml_station_01, test_xml_station_01, subtests):
        """Test location attributes."""
        with subtests.test("latitude matches"):
            assert xml_station_01.latitude == test_xml_station_01.latitude

        with subtests.test("longitude matches"):
            assert xml_station_01.longitude == test_xml_station_01.longitude

        with subtests.test("elevation matches"):
            assert xml_station_01.elevation == test_xml_station_01.elevation

    def test_site(self, xml_station_01, test_xml_station_01, subtests):
        """Test site attributes."""
        with subtests.test("site name matches"):
            assert xml_station_01.site.name == test_xml_station_01.site.name


class TestReadXMLStation02:
    """
    Test reading second StationXML station into MT station object
    """

    def test_time_period(self, mt_station_02, subtests):
        """Test time period attributes."""
        with subtests.test("start time matches expected value"):
            assert mt_station_02.time_period.start == "2020-06-08T22:57:13+00:00"

        with subtests.test("end time matches expected value"):
            assert mt_station_02.time_period.end == "2020-07-17T21:15:32+00:00"

    def test_code(self, mt_station_02, subtests):
        """Test code attributes."""
        with subtests.test("fdsn code matches expected"):
            assert mt_station_02.fdsn.id == "REW09"

        with subtests.test("station id matches expected"):
            assert mt_station_02.id == "REW09"

    def test_location(self, mt_station_02, subtests):
        """Test location attributes."""
        with subtests.test("latitude matches expected"):
            assert mt_station_02.location.latitude == 35.1469128125

        with subtests.test("longitude matches expected"):
            assert mt_station_02.location.longitude == -117.160798541667

        with subtests.test("elevation matches expected"):
            assert mt_station_02.location.elevation == 887.775

    def test_geographic_name(self, mt_station_02, subtests):
        """Test geographic name."""
        with subtests.test("geographic name matches expected"):
            assert mt_station_02.geographic_name == "Opal Mountain, CA, USA"

    def test_provenance(self, mt_station_02, subtests):
        """Test provenance attributes."""
        with subtests.test("author matches expected"):
            assert mt_station_02.provenance.software.author == "Anna Kelbert, USGS"

        with subtests.test("software name matches expected"):
            assert mt_station_02.provenance.software.name == "mth5_metadata.m"

        with subtests.test("software version matches expected"):
            assert mt_station_02.provenance.software.version == "2021-02-01"

    def test_declination(self, mt_station_02, subtests):
        """Test declination attributes."""
        with subtests.test("value matches expected"):
            assert mt_station_02.location.declination.value == -666

        with subtests.test("model matches expected"):
            assert mt_station_02.location.declination.model == "IGRF-13"

        with subtests.test("comments match expected"):
            assert (
                mt_station_02.location.declination.comments.value
                == "igrf.m by Drew Compston"
            )

    def test_orientation(self, mt_station_02, subtests):
        """Test orientation attributes."""
        with subtests.test("method matches expected"):
            assert mt_station_02.orientation.method == "compass"

        with subtests.test("reference frame matches expected"):
            assert mt_station_02.orientation.reference_frame == "geographic"

    def test_run_list(self, mt_station_02, subtests):
        """Test run list."""
        with subtests.test("run list matches expected"):
            assert mt_station_02.run_list == ["a", "b", "c", "d", "e"]

    def test_data_type(self, mt_station_02, subtests):
        """Test data type."""
        with subtests.test("data type matches expected"):
            assert mt_station_02.data_type == "MT"


@pytest.fixture(scope="module")
def run_test_data():
    """Fixture providing expected run data dictionaries."""

    base_run_a = {
        "run": OrderedDict(
            [
                ("acquired_by.author", "Kristin Pratscher"),
                (
                    "acquired_by.comments.value",
                    "X array at 0 and 90 degrees. Site i rocky drainage basin proximal to basalt lava flows. Ln",
                ),
                ("channels_recorded_auxiliary", []),
                ("channels_recorded_electric", []),
                ("channels_recorded_magnetic", []),
                ("comments.value", "author: machine generated, comments: "),
                ("data_logger.firmware.author", "Barry Narod"),
                ("data_logger.firmware.name", ""),
                ("data_logger.firmware.version", ""),
                ("data_logger.id", "2612-09"),
                ("data_logger.manufacturer", "Barry Narod"),
                ("data_logger.model", "NIMS"),
                ("data_logger.power_source.type", "battery"),
                ("data_logger.power_source.voltage.end", 0.0),
                ("data_logger.power_source.voltage.start", 0.0),
                ("data_logger.timing_system.drift", 0.0),
                ("data_logger.timing_system.type", "GPS"),
                ("data_logger.timing_system.uncertainty", 0.0),
                ("data_type", "LP"),
                ("id", "a"),
                ("metadata_by.author", "Jade Crosbie"),
                ("provenance.archive.name", ""),
                ("provenance.creation_time", "1980-01-01T00:00:00+00:00"),
                ("provenance.creator.author", ""),
                ("provenance.software.author", ""),
                ("provenance.software.name", ""),
                ("provenance.software.version", ""),
                ("provenance.submitter.author", ""),
                ("sample_rate", 0.0),
                ("time_period.end", "2020-06-08T23:54:50+00:00"),
                ("time_period.start", "2020-06-08T22:57:13+00:00"),
            ]
        )
    }

    base_run_b = {
        "run": OrderedDict(
            [
                ("acquired_by.author", "Kristin Pratscher"),
                (
                    "acquired_by.comments.value",
                    "X array a 0 and 90 degreest. Site in rocky drainage basin proximal to basalt lava flows. L",
                ),
                ("channels_recorded_auxiliary", []),
                ("channels_recorded_electric", []),
                ("channels_recorded_magnetic", []),
                (
                    "comments.value",
                    "author: machine generated, comments: A.Kelbert:Gap and a spike 726 secs into the run. Poor quality data after this event. However, timing before and after the gap verified against CAV09.",
                ),
                ("data_logger.firmware.author", "Barry Narod"),
                ("data_logger.firmware.name", ""),
                ("data_logger.firmware.version", ""),
                ("data_logger.id", "2612-09"),
                ("data_logger.manufacturer", "Barry Narod"),
                ("data_logger.model", "NIMS"),
                ("data_logger.power_source.type", "battery"),
                ("data_logger.power_source.voltage.end", 0.0),
                ("data_logger.power_source.voltage.start", 0.0),
                ("data_logger.timing_system.drift", 0.0),
                ("data_logger.timing_system.type", "GPS"),
                ("data_logger.timing_system.uncertainty", 0.0),
                ("data_type", "LP"),
                ("id", "b"),
                ("metadata_by.author", "Jade Crosbie; Anna Kelbert"),
                (
                    "metadata_by.comments.value",
                    "A.Kelbert- Gap and a spike 726 secs into the run. Poor quality data after this event. However, timing before and after the gap verified against CAV09.",
                ),
                ("provenance.archive.name", ""),
                ("provenance.creation_time", "1980-01-01T00:00:00+00:00"),
                ("provenance.creator.author", ""),
                ("provenance.software.author", ""),
                ("provenance.software.name", ""),
                ("provenance.software.version", ""),
                ("provenance.submitter.author", ""),
                ("sample_rate", 0.0),
                ("time_period.end", "2020-06-25T17:57:40+00:00"),
                ("time_period.start", "2020-06-09T00:08:03+00:00"),
            ]
        )
    }

    base_run_c = {
        "run": OrderedDict(
            [
                ("acquired_by.author", "Kristin Pratscher"),
                (
                    "acquired_by.comments.value",
                    "X array at 0 and 90 degrees. Site in rocky drainage basin proximal to basalt lava flows. Li",
                ),
                ("channels_recorded_auxiliary", []),
                ("channels_recorded_electric", []),
                ("channels_recorded_magnetic", []),
                ("comments.value", "author: machine generated, comments: "),
                ("data_logger.firmware.author", "Barry Narod"),
                ("data_logger.firmware.name", ""),
                ("data_logger.firmware.version", ""),
                ("data_logger.id", "2612-09"),
                ("data_logger.manufacturer", "Barry Narod"),
                ("data_logger.model", "NIMS"),
                ("data_logger.power_source.type", "battery"),
                ("data_logger.power_source.voltage.end", 0.0),
                ("data_logger.power_source.voltage.start", 0.0),
                ("data_logger.timing_system.drift", 0.0),
                ("data_logger.timing_system.type", "GPS"),
                ("data_logger.timing_system.uncertainty", 0.0),
                ("data_type", "LP"),
                ("id", "c"),
                ("metadata_by.author", "Jade Crosbie"),
                ("provenance.archive.name", ""),
                ("provenance.creation_time", "1980-01-01T00:00:00+00:00"),
                ("provenance.creator.author", ""),
                ("provenance.software.author", ""),
                ("provenance.software.name", ""),
                ("provenance.software.version", ""),
                ("provenance.submitter.author", ""),
                ("sample_rate", 0.0),
                ("time_period.end", "2020-07-04T01:16:15+00:00"),
                ("time_period.start", "2020-06-25T19:57:57+00:00"),
            ]
        )
    }

    base_run_d = {
        "run": OrderedDict(
            [
                ("acquired_by.author", "Kristin Pratscher"),
                (
                    "acquired_by.comments.value",
                    "Replaced mag cable & NIMS. X array at 0 and 90 degrees. Site in rocky drainage basin proxim",
                ),
                ("channels_recorded_auxiliary", []),
                ("channels_recorded_electric", []),
                ("channels_recorded_magnetic", []),
                ("comments.value", "author: machine generated, comments: "),
                ("data_logger.firmware.author", "Barry Narod"),
                ("data_logger.firmware.name", ""),
                ("data_logger.firmware.version", ""),
                ("data_logger.id", "2485"),
                ("data_logger.manufacturer", "Barry Narod"),
                ("data_logger.model", "NIMS"),
                ("data_logger.power_source.type", "battery"),
                ("data_logger.power_source.voltage.end", 0.0),
                ("data_logger.power_source.voltage.start", 0.0),
                ("data_logger.timing_system.drift", 0.0),
                ("data_logger.timing_system.type", "GPS"),
                ("data_logger.timing_system.uncertainty", 0.0),
                ("data_type", "LP"),
                ("id", "d"),
                ("metadata_by.author", "Jade Crosbie"),
                ("provenance.archive.name", ""),
                ("provenance.creation_time", "1980-01-01T00:00:00+00:00"),
                ("provenance.creator.author", ""),
                ("provenance.software.author", ""),
                ("provenance.software.name", ""),
                ("provenance.software.version", ""),
                ("provenance.submitter.author", ""),
                ("sample_rate", 0.0),
                ("time_period.end", "2020-07-04T03:07:30+00:00"),
                ("time_period.start", "2020-07-04T02:59:02+00:00"),
            ]
        )
    }

    base_run_e = {
        "run": OrderedDict(
            [
                ("acquired_by.author", "Kristin Pratscher"),
                (
                    "acquired_by.comments.value",
                    "Replaced mag cable & NIMS. MX array at 0 and 90 degrees. Site in rocky drainage basin proxim",
                ),
                ("channels_recorded_auxiliary", []),
                ("channels_recorded_electric", []),
                ("channels_recorded_magnetic", []),
                ("comments.value", "author: machine generated, comments: "),
                ("data_logger.firmware.author", "Barry Narod"),
                ("data_logger.firmware.name", ""),
                ("data_logger.firmware.version", ""),
                ("data_logger.id", "2485"),
                ("data_logger.manufacturer", "Barry Narod"),
                ("data_logger.model", "NIMS"),
                ("data_logger.power_source.type", "battery"),
                ("data_logger.power_source.voltage.end", 0.0),
                ("data_logger.power_source.voltage.start", 0.0),
                ("data_logger.timing_system.drift", 0.0),
                ("data_logger.timing_system.type", "GPS"),
                ("data_logger.timing_system.uncertainty", 0.0),
                ("data_type", "LP"),
                ("id", "e"),
                ("metadata_by.author", "Jade Crosbie"),
                ("provenance.archive.name", ""),
                ("provenance.creation_time", "1980-01-01T00:00:00+00:00"),
                ("provenance.creator.author", ""),
                ("provenance.software.author", ""),
                ("provenance.software.name", ""),
                ("provenance.software.version", ""),
                ("provenance.submitter.author", ""),
                ("sample_rate", 0.0),
                ("time_period.end", "2020-07-17T21:15:32+00:00"),
                ("time_period.start", "2020-07-04T03:28:45+00:00"),
            ]
        )
    }

    return {
        "a": base_run_a,
        "b": base_run_b,
        "c": base_run_c,
        "d": base_run_d,
        "e": base_run_e,
    }


@pytest.mark.parametrize("run_id", ["a", "b", "c", "d", "e"])
def test_run_data(mt_station_02, run_test_data, run_id, subtests):
    """Test run data for each run."""
    run = mt_station_02.get_run(run_id)
    expected_dict = run_test_data[run_id]

    with subtests.test(f"run {run_id} data matches expected"):
        assert run.to_dict() == expected_dict


class TestMTStationToXML02:
    """
    Test converting second MT station back to StationXML station
    """

    @pytest.fixture(autouse=True)
    def setup(self, xml_station_02, converter, mt_station_02):
        """Set up test data."""
        # Create test_xml_station directly in the test class to ensure it's recreated for each test
        self.base_xml_station = xml_station_02
        self.test_xml_station = converter.mt_to_xml(mt_station_02)
        self.converter = converter

    def test_time_period(self, subtests):
        """Test time period attributes."""
        with subtests.test("start date matches"):
            assert self.base_xml_station.start_date == self.test_xml_station.start_date

        with subtests.test("end date matches"):
            assert self.base_xml_station.end_date == self.test_xml_station.end_date

    def test_code(self, subtests):
        """Test code attributes."""
        with subtests.test("fdsn code matches"):
            assert self.base_xml_station.code == self.test_xml_station.code

        with subtests.test("alternate code matches"):
            assert (
                self.base_xml_station.alternate_code
                == self.test_xml_station.alternate_code
            )

    def test_location(self, subtests):
        """Test location attributes."""
        with subtests.test("latitude matches"):
            assert self.base_xml_station.latitude == self.test_xml_station.latitude

        with subtests.test("longitude matches"):
            assert self.base_xml_station.longitude == self.test_xml_station.longitude

        with subtests.test("elevation matches"):
            assert self.base_xml_station.elevation == self.test_xml_station.elevation

    def test_site(self, subtests):
        """Test site attributes."""
        with subtests.test("site name matches"):
            assert self.base_xml_station.site.name == self.test_xml_station.site.name

    def test_equipments(self, subtests):
        """Test equipment attributes."""
        with subtests.test("equipment count matches"):
            assert len(self.base_xml_station.equipments) == len(
                self.test_xml_station.equipments
            )

        for be, te in zip(
            self.base_xml_station.equipments, self.test_xml_station.equipments
        ):
            with subtests.test("equipment resource_id matches"):
                assert be.resource_id == te.resource_id

            with subtests.test("equipment manufacturer matches"):
                assert be.manufacturer == te.manufacturer

            with subtests.test("equipment serial number matches"):
                assert be.serial_number == te.serial_number

            with subtests.test("equipment installation date matches"):
                assert be.installation_date == te.installation_date

            with subtests.test("equipment removal date matches"):
                assert be.removal_date == te.removal_date

    def test_comments(self, subtests):
        """Test comments attributes."""
        for bc in self.base_xml_station.comments:
            for tc in self.test_xml_station.comments:
                if bc.subject == tc.subject:
                    if bc.value:
                        bk, bv = self.converter.read_xml_comment(bc)
                        tk, tv = self.converter.read_xml_comment(tc)

                        with subtests.test("comment key matches"):
                            assert bk == tk

                        if isinstance(bv, dict):
                            for kk, vv in bv.items():
                                if vv not in ["", None]:
                                    with subtests.test(
                                        f"comment dict value for {kk} matches"
                                    ):
                                        assert tv[kk] == vv
                        else:
                            with subtests.test("comment string value matches"):
                                assert bv == tv


@pytest.fixture(scope="module")
def example_inventories():
    """Load both example StationXML inventories."""
    return {
        "inventory_01": read_inventory(STATIONXML_01.as_posix()),
        "inventory_02": read_inventory(STATIONXML_02.as_posix()),
    }


@pytest.fixture(scope="module")
def example_xml_stations(example_inventories):
    """Extract stations from example inventories."""
    return {
        "station_01": example_inventories["inventory_01"].networks[0].stations[0],
        "station_02": example_inventories["inventory_02"].networks[0].stations[0],
    }


@pytest.fixture(scope="module")
def example_mt_station():
    """Create a sample MT station with basic attributes."""
    station = Station(
        id="TEST01",
        time_period={"start": "2020-01-01T00:00:00", "end": "2020-01-31T23:59:59"},
        location={"latitude": 42.5, "longitude": -122.5, "elevation": 1500.0},
        geographic_name="Test Mountain, CA, USA",
    )
    return station


class TestXMLStationMTStationInitialization:
    """Test initialization and basic properties of the converter."""

    def test_initialization(self, converter, subtests):
        """Test basic initialization of the converter."""
        with subtests.test("converter initializes without error"):
            assert converter is not None

        with subtests.test("converter has correct class"):
            assert isinstance(converter, XMLStationMTStation)

        with subtests.test("converter has necessary attributes/methods"):
            assert hasattr(converter, "xml_to_mt")
            assert hasattr(converter, "mt_to_xml")
            assert hasattr(converter, "read_xml_comment")


class TestXMLToMTConversion:
    """Test conversion from XML to MT station."""

    def test_station_basic_attributes(self, converter, example_xml_stations, subtests):
        """Test conversion of basic station attributes."""
        xml_station = example_xml_stations["station_01"]
        mt_station = converter.xml_to_mt(xml_station)

        with subtests.test("id is correctly converted"):
            assert mt_station.id == xml_station.code

        with subtests.test("fdsn.id is correctly set"):
            assert mt_station.fdsn.id == xml_station.code

        with subtests.test("time_period.start is correctly set"):
            assert mt_station.time_period.start == "2020-06-02T18:41:43+00:00"

        with subtests.test("time_period.end is correctly set"):
            assert mt_station.time_period.end == "2020-07-13T21:46:12+00:00"

    def test_location_conversion(self, converter, example_xml_stations, subtests):
        """Test conversion of location attributes."""
        xml_station = example_xml_stations["station_01"]
        mt_station = converter.xml_to_mt(xml_station)

        with subtests.test("latitude is correctly converted"):
            assert mt_station.location.latitude == xml_station.latitude

        with subtests.test("longitude is correctly converted"):
            assert mt_station.location.longitude == xml_station.longitude

        with subtests.test("elevation is correctly converted"):
            assert mt_station.location.elevation == xml_station.elevation

    def test_site_name_conversion(self, converter, example_xml_stations, subtests):
        """Test conversion of site name."""
        xml_station = example_xml_stations["station_01"]
        mt_station = converter.xml_to_mt(xml_station)

        with subtests.test("geographic_name is correctly set"):
            assert mt_station.geographic_name == "Corral Hollow, CA, USA"

    def test_complex_station_conversion(
        self, converter, example_xml_stations, subtests
    ):
        """Test conversion of more complex station from STATIONXML_02."""
        xml_station = example_xml_stations["station_02"]
        mt_station = converter.xml_to_mt(xml_station)

        with subtests.test("run_list is correctly extracted"):
            assert mt_station.run_list == ["a", "b", "c", "d", "e"]

        with subtests.test("data_type is correctly set"):
            assert mt_station.data_type == "MT"

        with subtests.test("orientation.reference_frame is correctly set"):
            assert mt_station.orientation.reference_frame == "geographic"

        with subtests.test("provenance.software.author is correctly set"):
            assert mt_station.provenance.software.author == "Anna Kelbert, USGS"

    def test_run_extraction(self, converter, example_xml_stations, subtests):
        """Test extraction of run objects from equipment elements."""
        xml_station = example_xml_stations["station_02"]
        mt_station = converter.xml_to_mt(xml_station)

        # Get a sample run
        run_a = mt_station.get_run("a")

        with subtests.test("run id is correctly set"):
            assert run_a.id == "a"

        with subtests.test("data_type is correctly set"):
            assert run_a.data_type == "LP"

        with subtests.test("data_logger.id is correctly set"):
            assert run_a.data_logger.id == "2612-09"

        with subtests.test("time_period is correctly set for run"):
            assert run_a.time_period.start == "2020-06-08T22:57:13+00:00"
            assert run_a.time_period.end == "2020-06-08T23:54:50+00:00"

        with subtests.test("acquired_by.author is correctly set"):
            assert run_a.acquired_by.author == "Kristin Pratscher"


class TestMTToXMLConversion:
    """Test conversion from MT station to XML."""

    def test_basic_attributes_conversion(self, converter, example_mt_station, subtests):
        """Test conversion of basic MT station attributes to XML."""
        xml_station = converter.mt_to_xml(example_mt_station)

        with subtests.test("station code is correctly set"):
            assert xml_station.code == example_mt_station.id

        with subtests.test("start_date is correctly set"):
            assert xml_station.start_date.isoformat() == "2020-01-01T00:00:00+00:00"

        with subtests.test("end_date is correctly set"):
            assert xml_station.end_date.isoformat() == "2020-01-31T23:59:59+00:00"

    def test_location_conversion(self, converter, example_mt_station, subtests):
        """Test conversion of location attributes."""
        xml_station = converter.mt_to_xml(example_mt_station)

        with subtests.test("latitude is correctly converted"):
            assert xml_station.latitude == example_mt_station.location.latitude

        with subtests.test("longitude is correctly converted"):
            assert xml_station.longitude == example_mt_station.location.longitude

        with subtests.test("elevation is correctly converted"):
            assert xml_station.elevation == example_mt_station.location.elevation

    def test_site_name_conversion(self, converter, example_mt_station, subtests):
        """Test conversion of geographic name to site name."""
        xml_station = converter.mt_to_xml(example_mt_station)

        with subtests.test("site name is correctly set"):
            assert xml_station.site.name == example_mt_station.geographic_name

    def test_roundtrip_conversion(self, converter, example_xml_stations, subtests):
        """Test round-trip conversion (XML → MT → XML)."""
        original_xml = example_xml_stations["station_01"]
        mt_station = converter.xml_to_mt(original_xml)
        new_xml = converter.mt_to_xml(mt_station)

        with subtests.test("code is preserved"):
            assert original_xml.code == new_xml.code

        with subtests.test("site name is preserved"):
            assert original_xml.site.name == new_xml.site.name

        with subtests.test("location is preserved"):
            assert original_xml.latitude == new_xml.latitude
            assert original_xml.longitude == new_xml.longitude
            assert original_xml.elevation == new_xml.elevation

        with subtests.test("time period is preserved"):
            assert original_xml.start_date == new_xml.start_date
            assert original_xml.end_date == new_xml.end_date


class TestXMLCommentHandling:
    """Test reading and writing XML comments."""

    @pytest.fixture(scope="module")
    def sample_comment(self):
        """Create a sample ObsPy Comment object with metadata."""
        from obspy.core.inventory import Comment

        return Comment(
            value="declination.value: -13.5, declination.model: WMM-2020",
            subject="Magnetic Declination",
        )

    def test_read_xml_comment(self, converter, sample_comment, subtests):
        """Test parsing XML comment into key-value pairs."""
        key, value = converter.read_xml_comment(sample_comment)

        with subtests.test("comment subject becomes key"):
            assert key == "magnetic_declination"

        with subtests.test("comment value is parsed into dictionary"):
            assert isinstance(value, dict)
            assert value["declination.value"] == "-13.5"
            assert value["declination.model"] == "WMM-2020"

    # def test_make_mt_comment(self, converter, subtests):
    #     """Test creating XML comment from key-value pairs."""
    #     key = "Station Info"
    #     value = {"id": "MT01", "operator": "USGS", "location": "California"}

    #     comment = converter.make_mt_comment(key, value)

    #     with subtests.test("comment subject is set correctly"):
    #         assert comment.subject == key

    #     with subtests.test("comment value contains all key-value pairs"):
    #         for k, v in value.items():
    #             assert f"{k}: {v}" in comment.value

    # def test_comment_roundtrip(self, converter, subtests):
    #     """Test round-trip conversion of comments."""
    #     original_key = "Data Quality"
    #     original_value = {
    #         "rating.value": "4",
    #         "rating.author": "J. Smith",
    #         "issues": "minor noise at 60Hz",
    #     }

    #     # Create XML comment
    #     comment = converter.make_mt_comments(original_key, original_value)

    #     # Read it back
    #     parsed_key, parsed_value = converter.read_xml_comment(comment)

    #     with subtests.test("key is preserved"):
    #         assert parsed_key == original_key

    #     with subtests.test("values are preserved"):
    #         for k, v in original_value.items():
    #             assert parsed_value[k] == v


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_station(self, converter, subtests):
        """Test conversion with minimal station information."""
        empty_station = Station()
        xml_station = converter.mt_to_xml(empty_station)

        with subtests.test("code is set to empty string if id is None"):
            assert xml_station.code == ""

        with subtests.test("station still has valid structure"):
            assert hasattr(xml_station, "site")
            assert hasattr(xml_station, "latitude")
            assert hasattr(xml_station, "longitude")

    def test_missing_dates(self, converter, subtests):
        """Test conversion with missing time period."""
        station = Station(id="TEST01")
        xml_station = converter.mt_to_xml(station)

        with subtests.test("start_date is None with missing time period"):
            assert xml_station.start_date.isoformat() == "1980-01-01T00:00:00+00:00"
        # Assuming the default value for start_date is "1980-01-01T00:00:00+00:00"

        with subtests.test("end_date is None with missing time period"):
            assert xml_station.end_date.isoformat() == "1980-01-01T00:00:00+00:00"
