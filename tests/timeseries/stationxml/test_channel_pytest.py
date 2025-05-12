# -*- coding: utf-8 -*-
"""
Tests for converting between XML Channel and MT Channel formats using pytest

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""
# =============================================================================
# Imports
# =============================================================================
import pytest
from collections import OrderedDict

try:
    from obspy import read_inventory
    from mt_metadata.timeseries.filters.obspy_stages import (
        create_filter_from_stage,
    )
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)

from mt_metadata.timeseries.stationxml import XMLChannelMTChannel
from mt_metadata import STATIONXML_01, STATIONXML_02


@pytest.fixture
def converter():
    """Create an XMLChannelMTChannel converter."""
    return XMLChannelMTChannel()


@pytest.fixture
def inventory_01():
    """Load first stationxml inventory."""
    return read_inventory(STATIONXML_01.as_posix())


@pytest.fixture
def inventory_02():
    """Load second stationxml inventory."""
    return read_inventory(STATIONXML_02.as_posix())


@pytest.fixture
def hy_channel_01(inventory_01):
    """Get HY channel from first inventory."""
    return inventory_01.networks[0].stations[0].channels[0]


@pytest.fixture
def ey_channel_01(inventory_01):
    """Get EY channel from first inventory."""
    return inventory_01.networks[0].stations[0].channels[1]


@pytest.fixture
def inventory_02_channels(inventory_02):
    """Get all channels from second inventory."""
    station = inventory_02.networks[0].stations[0]
    return {
        "hx": station.channels[0],
        "hy": station.channels[1],
        "hz": station.channels[2],
        "ex": station.channels[3],
        "ey": station.channels[4],
    }


@pytest.fixture
def mt_channel_and_filters(converter, request, inventory_01, inventory_02_channels):
    """Convert an XML channel to MT channel and filters."""
    # Handle different ways the parameter might be passed
    param = request.param

    # Get the appropriate XML channel object based on the parameter
    if param == "hy_channel_01":
        xml_channel = inventory_01.networks[0].stations[0].channels[0]
    elif param == "ey_channel_01":
        xml_channel = inventory_01.networks[0].stations[0].channels[1]
    elif param.startswith("inventory_02_channels"):
        # Extract the channel name from something like: inventory_02_channels["hx"]
        channel_name = param.split('"')[1]
        xml_channel = inventory_02_channels[channel_name]
    else:
        # For direct channel objects
        xml_channel = param

    # Process the channel
    mt_channel, mt_filters = converter.xml_to_mt(xml_channel)
    test_xml_channel = converter.mt_to_xml(mt_channel, mt_filters)

    return {
        "base_xml_channel": xml_channel,
        "mt_channel": mt_channel,
        "mt_filters": mt_filters,
        "test_xml_channel": test_xml_channel,
    }


class TestParseSerialID:
    """Test parsing a string that holds the electrode serial ID numbers."""

    @pytest.fixture
    def setup(self, converter):
        """Set up test data."""
        pid = "2004007"
        nid = "2004008"
        id_str = f"positive: {pid}, negative: {nid}"
        comma_only_str = f"{pid}, {nid}"
        generic_str = "basic"

        return {
            "converter": converter,
            "pid": pid,
            "nid": nid,
            "id_str": id_str,
            "comma_only_str": comma_only_str,
            "generic_str": generic_str,
        }

    def test_parse(self, setup, subtests):
        """Test parsing electrode IDs with full format."""
        test_pid, test_nid = setup["converter"]._parse_electrode_ids(setup["id_str"])

        with subtests.test("positive ID is parsed correctly"):
            assert test_pid == setup["pid"]

        with subtests.test("negative ID is parsed correctly"):
            assert test_nid == setup["nid"]

    def test_parse_comma_only(self, setup, subtests):
        """Test parsing electrode IDs with comma-only format."""
        test_pid, test_nid = setup["converter"]._parse_electrode_ids(
            setup["comma_only_str"]
        )

        with subtests.test("positive ID is parsed correctly"):
            assert test_pid == setup["pid"]

        with subtests.test("negative ID is parsed correctly"):
            assert test_nid == setup["nid"]

    def test_parse_basic(self, setup, subtests):
        """Test parsing basic string format."""
        test_pid, test_nid = setup["converter"]._parse_electrode_ids(
            setup["generic_str"]
        )

        with subtests.test("positive ID is same as input"):
            assert test_pid == "basic"

        with subtests.test("negative ID is same as input"):
            assert test_nid == "basic"


class TestParseDipole:
    """Test parsing a dipole length string."""

    @pytest.fixture
    def setup(self, converter):
        """Set up test data."""
        dipole_length = 100.0
        dipole_str = f"{dipole_length} meters"

        return {
            "converter": converter,
            "dipole_length": dipole_length,
            "dipole_str": dipole_str,
        }

    def test_parse(self, setup, subtests):
        """Test parsing dipole length string."""
        d = setup["converter"]._parse_dipole_length(setup["dipole_str"])

        with subtests.test("dipole length is parsed correctly"):
            assert d == setup["dipole_length"]


class TestXMLChannelTwoChannels:
    """Test reading XML channel to MT Channel."""

    @pytest.fixture
    def setup(self, converter, inventory_01):
        """Set up test data."""
        xml_hy = inventory_01.networks[0].stations[0].channels[0]
        xml_ey = inventory_01.networks[0].stations[0].channels[1]

        filters_dict = dict(
            [
                (c.name, c)
                for c in [
                    create_filter_from_stage(s) for s in xml_hy.response.response_stages
                ]
            ]
        )

        return {
            "converter": converter,
            "xml_hy": xml_hy,
            "xml_ey": xml_ey,
            "filters_dict": filters_dict,
        }

    def test_channel_hy(self, setup, subtests):
        """Test converting HY channel."""
        mt_channel, mt_filters = setup["converter"].xml_to_mt(setup["xml_hy"])
        expected_dict = {
            "magnetic": OrderedDict(
                [
                    ("channel_number", 0),
                    ("comments", "run_ids: []"),
                    ("component", "hy"),
                    ("data_quality.rating.value", None),
                    (
                        "filter.filter_list",
                        [
                            {
                                "applied_filter": OrderedDict(
                                    [
                                        ("applied", True),
                                        (
                                            "name",
                                            "magnetic field 3 pole butterworth low-pass",
                                        ),
                                        ("stage", 1),
                                    ]
                                )
                            },
                            {
                                "applied_filter": OrderedDict(
                                    [
                                        ("applied", True),
                                        ("name", "v to counts (magnetic)"),
                                        ("stage", 2),
                                    ]
                                )
                            },
                            {
                                "applied_filter": OrderedDict(
                                    [
                                        ("applied", True),
                                        ("name", "hy time offset"),
                                        ("stage", 3),
                                    ]
                                )
                            },
                        ],
                    ),
                    ("h_field_max.end", 0.0),
                    ("h_field_max.start", 0.0),
                    ("h_field_min.end", 0.0),
                    ("h_field_min.start", 0.0),
                    ("location.datum", "WGS 84"),
                    ("location.elevation", 329.4),
                    ("location.latitude", 37.633351),
                    ("location.longitude", -121.468382),
                    ("measurement_azimuth", 103.2),
                    ("measurement_tilt", 0.0),
                    ("sample_rate", 1.0),
                    ("sensor.id", "2593"),
                    ("sensor.manufacturer", "Barry Narod"),
                    ("sensor.model", "fluxgate NIMS"),
                    ("sensor.name", "NIMS"),
                    ("sensor.type", "Magnetometer"),
                    ("time_period.end", "2020-07-13T21:46:12+00:00"),
                    ("time_period.start", "2020-06-02T18:41:43+00:00"),
                    ("type", "magnetic"),
                    ("units", "digital counts"),
                ]
            )
        }

        with subtests.test("channel dictionary matches expected"):
            assert mt_channel.to_dict() == expected_dict

    def test_channel_ey(self, setup, subtests):
        """Test converting EY channel."""
        mt_channel, mt_filters = setup["converter"].xml_to_mt(setup["xml_ey"])
        expected_dict = {
            "electric": OrderedDict(
                [
                    ("ac.end", 0.0),
                    ("ac.start", 0.0),
                    ("channel_number", 0),
                    ("comments", "run_ids: []"),
                    ("component", "ey"),
                    ("contact_resistance.end", 0.0),
                    ("contact_resistance.start", 0.0),
                    ("data_quality.rating.value", None),
                    ("dc.end", 0.0),
                    ("dc.start", 0.0),
                    ("dipole_length", 92.0),
                    (
                        "filter.filter_list",
                        [
                            {
                                "applied_filter": OrderedDict(
                                    [
                                        ("applied", True),
                                        (
                                            "name",
                                            "electric field 5 pole butterworth low-pass",
                                        ),
                                        ("stage", 1),
                                    ]
                                )
                            },
                            {
                                "applied_filter": OrderedDict(
                                    [
                                        ("applied", True),
                                        (
                                            "name",
                                            "electric field 1 pole butterworth high-pass",
                                        ),
                                        ("stage", 2),
                                    ]
                                )
                            },
                            {
                                "applied_filter": OrderedDict(
                                    [
                                        ("applied", True),
                                        ("name", "mv/km to v/m"),
                                        ("stage", 3),
                                    ]
                                )
                            },
                            {
                                "applied_filter": OrderedDict(
                                    [
                                        ("applied", True),
                                        ("name", "v/m to v"),
                                        ("stage", 4),
                                    ]
                                )
                            },
                            {
                                "applied_filter": OrderedDict(
                                    [
                                        ("applied", True),
                                        ("name", "v to counts (electric)"),
                                        ("stage", 5),
                                    ]
                                )
                            },
                            {
                                "applied_filter": OrderedDict(
                                    [
                                        ("applied", True),
                                        ("name", "electric time offset"),
                                        ("stage", 6),
                                    ]
                                )
                            },
                        ],
                    ),
                    ("measurement_azimuth", 103.2),
                    ("measurement_tilt", 0.0),
                    ("negative.datum", "WGS 84"),
                    ("negative.elevation", 329.4),
                    ("negative.id", "2004020"),
                    ("negative.latitude", 37.633351),
                    ("negative.longitude", -121.468382),
                    ("negative.manufacturer", "Oregon State University"),
                    ("negative.model", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                    ("negative.type", "electrode"),
                    ("positive.datum", "WGS 84"),
                    ("positive.elevation", 329.4),
                    ("positive.id", "200402F"),
                    ("positive.latitude", 37.633351),
                    ("positive.longitude", -121.468382),
                    ("positive.manufacturer", "Oregon State University"),
                    ("positive.model", "Pb-PbCl2 kaolin gel Petiau 2 chamber type"),
                    ("positive.type", "electrode"),
                    ("sample_rate", 1.0),
                    ("time_period.end", "2020-07-13T21:46:12+00:00"),
                    ("time_period.start", "2020-06-02T18:41:43+00:00"),
                    ("type", "electric"),
                    ("units", "digital counts"),
                ]
            )
        }

        with subtests.test("channel dictionary matches expected"):
            assert mt_channel.to_dict() == expected_dict


@pytest.mark.parametrize("mt_channel_and_filters", ["hy_channel_01"], indirect=True)
class TestMTChannelToXML01HY:
    """Test converting MT channel back to XML channel for HY channel."""

    def test_location(self, mt_channel_and_filters, subtests):
        """Test location attributes."""
        base = mt_channel_and_filters["base_xml_channel"]
        test = mt_channel_and_filters["test_xml_channel"]

        with subtests.test("latitude matches"):
            assert base.latitude == test.latitude

        with subtests.test("longitude matches"):
            assert base.longitude == test.longitude

        with subtests.test("elevation matches"):
            assert base.elevation == test.elevation

        with subtests.test("depth matches"):
            assert base.depth == test.depth

    def test_time_period(self, mt_channel_and_filters, subtests):
        """Test time period attributes."""
        base = mt_channel_and_filters["base_xml_channel"]
        test = mt_channel_and_filters["test_xml_channel"]

        with subtests.test("start_date matches"):
            assert base.start_date == test.start_date

        with subtests.test("end_date matches"):
            assert base.end_date == test.end_date

    def test_code(self, mt_channel_and_filters, subtests):
        """Test code attributes."""
        base = mt_channel_and_filters["base_xml_channel"]
        test = mt_channel_and_filters["test_xml_channel"]

        with subtests.test("code matches"):
            assert base.code == test.code

        with subtests.test("alternate_code differs"):
            assert base.alternate_code != test.alternate_code

    def test_code_unforced(self, mt_channel_and_filters, converter, subtests):
        """Test code attributes with hard_code=False."""
        base = mt_channel_and_filters["base_xml_channel"]
        mt_channel = mt_channel_and_filters["mt_channel"]
        mt_filters = mt_channel_and_filters["mt_filters"]

        # Generate XML channel without forcing hard coding
        xml_channel = converter.mt_to_xml(mt_channel, mt_filters, hard_code=False)

        with subtests.test("code matches"):
            assert base.code == xml_channel.code

        with subtests.test("alternate_code differs"):
            assert base.alternate_code != xml_channel.alternate_code

    def test_sensor(self, mt_channel_and_filters, subtests):
        """Test sensor attributes."""
        base = mt_channel_and_filters["base_xml_channel"]
        test = mt_channel_and_filters["test_xml_channel"]

        with subtests.test("sensor type matches"):
            assert base.sensor.type == test.sensor.type

        with subtests.test("sensor model matches"):
            assert base.sensor.model == test.sensor.model

        with subtests.test("sensor manufacturer matches"):
            assert base.sensor.manufacturer == test.sensor.manufacturer

        with subtests.test("sensor serial_number matches"):
            assert base.sensor.serial_number == test.sensor.serial_number

        with subtests.test("sensor description matches"):
            assert base.sensor.description == test.sensor.description

    def test_units(self, mt_channel_and_filters, subtests):
        """Test units attributes."""
        base = mt_channel_and_filters["base_xml_channel"]
        test = mt_channel_and_filters["test_xml_channel"]

        with subtests.test("calibration_units match"):
            assert base.calibration_units == test.calibration_units

        with subtests.test("calibration_units_description matches"):
            assert (
                base.calibration_units_description == test.calibration_units_description
            )

    def test_sample_rate(self, mt_channel_and_filters, subtests):
        """Test sample rate attribute."""
        base = mt_channel_and_filters["base_xml_channel"]
        test = mt_channel_and_filters["test_xml_channel"]

        with subtests.test("sample_rate matches"):
            assert base.sample_rate == test.sample_rate

    def test_azimuth(self, mt_channel_and_filters, subtests):
        """Test orientation attributes."""
        base = mt_channel_and_filters["base_xml_channel"]
        test = mt_channel_and_filters["test_xml_channel"]

        with subtests.test("azimuth matches"):
            assert base.azimuth == test.azimuth

        with subtests.test("dip matches"):
            assert base.dip == test.dip

    def test_types(self, mt_channel_and_filters, subtests):
        """Test types attribute."""
        base = mt_channel_and_filters["base_xml_channel"]
        test = mt_channel_and_filters["test_xml_channel"]

        with subtests.test("types match"):
            assert base.types == test.types


@pytest.mark.parametrize("mt_channel_and_filters", ["ey_channel_01"], indirect=True)
class TestMTChannelToXML01EY:
    """Test converting MT channel back to XML channel for EY channel."""

    def test_location(self, mt_channel_and_filters, subtests):
        """Test location attributes."""
        base = mt_channel_and_filters["base_xml_channel"]
        test = mt_channel_and_filters["test_xml_channel"]

        with subtests.test("latitude matches"):
            assert base.latitude == test.latitude

        with subtests.test("longitude matches"):
            assert base.longitude == test.longitude

        with subtests.test("elevation matches"):
            assert base.elevation == test.elevation

        with subtests.test("depth matches"):
            assert base.depth == test.depth

    def test_time_period(self, mt_channel_and_filters, subtests):
        """Test time period attributes."""
        base = mt_channel_and_filters["base_xml_channel"]
        test = mt_channel_and_filters["test_xml_channel"]

        with subtests.test("start_date matches"):
            assert base.start_date == test.start_date

        with subtests.test("end_date matches"):
            assert base.end_date == test.end_date

    def test_code(self, mt_channel_and_filters, subtests):
        """Test code attributes."""
        base = mt_channel_and_filters["base_xml_channel"]
        test = mt_channel_and_filters["test_xml_channel"]

        with subtests.test("code matches"):
            assert base.code == test.code

        with subtests.test("alternate_code differs"):
            assert base.alternate_code != test.alternate_code

    def test_code_unforced(self, mt_channel_and_filters, converter, subtests):
        """Test code attributes with hard_code=False."""
        base = mt_channel_and_filters["base_xml_channel"]
        mt_channel = mt_channel_and_filters["mt_channel"]
        mt_filters = mt_channel_and_filters["mt_filters"]

        # Generate XML channel without forcing hard coding
        xml_channel = converter.mt_to_xml(mt_channel, mt_filters, hard_code=False)

        with subtests.test("code matches"):
            assert base.code == xml_channel.code

        with subtests.test("alternate_code differs"):
            assert base.alternate_code != xml_channel.alternate_code

    def test_sensor(self, mt_channel_and_filters, subtests):
        """Test sensor attributes."""
        base = mt_channel_and_filters["base_xml_channel"]
        test = mt_channel_and_filters["test_xml_channel"]

        with subtests.test("sensor type matches"):
            assert base.sensor.type == test.sensor.type

        with subtests.test("sensor model matches"):
            assert base.sensor.model == test.sensor.model

        with subtests.test("sensor manufacturer matches"):
            assert base.sensor.manufacturer == test.sensor.manufacturer

        with subtests.test("sensor serial_number matches"):
            assert base.sensor.serial_number == test.sensor.serial_number

        with subtests.test("sensor description matches"):
            assert base.sensor.description == test.sensor.description


# Function to create parameterized fixtures for inventory_02 channels
def create_channel_test_class(channel_name):
    """Create a test class for a specific channel."""

    @pytest.mark.parametrize(
        "mt_channel_and_filters",
        [f'inventory_02_channels["{channel_name}"]'],
        indirect=True,
    )
    class TestChannelClass:
        """Test class for channel conversion."""

        def test_location(self, mt_channel_and_filters, subtests):
            """Test location attributes."""
            base = mt_channel_and_filters["base_xml_channel"]
            test = mt_channel_and_filters["test_xml_channel"]

            with subtests.test("latitude matches"):
                assert base.latitude == test.latitude

            with subtests.test("longitude matches"):
                assert base.longitude == test.longitude

            with subtests.test("elevation matches"):
                assert base.elevation == test.elevation

            with subtests.test("depth matches"):
                assert base.depth == test.depth

        def test_time_period(self, mt_channel_and_filters, subtests):
            """Test time period attributes."""
            base = mt_channel_and_filters["base_xml_channel"]
            test = mt_channel_and_filters["test_xml_channel"]

            with subtests.test("start_date matches"):
                assert base.start_date == test.start_date

            with subtests.test("end_date matches"):
                assert base.end_date == test.end_date

        def test_code(self, mt_channel_and_filters, subtests):
            """Test code attributes."""
            base = mt_channel_and_filters["base_xml_channel"]
            test = mt_channel_and_filters["test_xml_channel"]

            with subtests.test("code matches"):
                assert base.code == test.code

            with subtests.test("alternate_code matches case-insensitive"):
                assert base.alternate_code.lower() == test.alternate_code.lower()

        def test_code_unforced(self, mt_channel_and_filters, converter, subtests):
            """Test code attributes with hard_code=False."""
            base = mt_channel_and_filters["base_xml_channel"]
            mt_channel = mt_channel_and_filters["mt_channel"]
            mt_filters = mt_channel_and_filters["mt_filters"]

            # Generate XML channel without forcing hard coding
            xml_channel = converter.mt_to_xml(mt_channel, mt_filters, hard_code=False)

            with subtests.test("code matches"):
                assert base.code == xml_channel.code

            with subtests.test("alternate_code matches case-insensitive"):
                assert base.alternate_code.lower() == xml_channel.alternate_code.lower()

        def test_sensor(self, mt_channel_and_filters, subtests):
            """Test sensor attributes."""
            base = mt_channel_and_filters["base_xml_channel"]
            test = mt_channel_and_filters["test_xml_channel"]

            with subtests.test("sensor type matches"):
                assert base.sensor.type == test.sensor.type

            with subtests.test("sensor model matches"):
                assert base.sensor.model == test.sensor.model

            with subtests.test("sensor manufacturer matches"):
                assert base.sensor.manufacturer == test.sensor.manufacturer

            with subtests.test("sensor serial_number matches"):
                assert base.sensor.serial_number == test.sensor.serial_number

            with subtests.test("sensor description matches"):
                assert base.sensor.description == test.sensor.description

        def test_units(self, mt_channel_and_filters, subtests):
            """Test units attributes."""
            base = mt_channel_and_filters["base_xml_channel"]
            test = mt_channel_and_filters["test_xml_channel"]

            with subtests.test("calibration_units match"):
                assert base.calibration_units == test.calibration_units

            with subtests.test("calibration_units_description matches"):
                assert (
                    base.calibration_units_description
                    == test.calibration_units_description
                )

        def test_sample_rate(self, mt_channel_and_filters, subtests):
            """Test sample rate attribute."""
            base = mt_channel_and_filters["base_xml_channel"]
            test = mt_channel_and_filters["test_xml_channel"]

            with subtests.test("sample_rate matches"):
                assert base.sample_rate == test.sample_rate

        def test_azimuth(self, mt_channel_and_filters, subtests):
            """Test orientation attributes."""
            base = mt_channel_and_filters["base_xml_channel"]
            test = mt_channel_and_filters["test_xml_channel"]

            with subtests.test("azimuth matches"):
                assert base.azimuth == test.azimuth

            with subtests.test("dip matches"):
                assert base.dip == test.dip

        def test_types(self, mt_channel_and_filters, subtests):
            """Test types attribute."""
            base = mt_channel_and_filters["base_xml_channel"]
            test = mt_channel_and_filters["test_xml_channel"]

            with subtests.test("types match"):
                assert base.types == test.types

        def test_comments(self, mt_channel_and_filters, subtests):
            """Test comments attribute."""
            base = mt_channel_and_filters["base_xml_channel"]
            test = mt_channel_and_filters["test_xml_channel"]

            with subtests.test("comments length matches"):
                assert len(base.comments) == len(test.comments)

            for i, (comment_base, comment_test) in enumerate(
                zip(base.comments, test.comments)
            ):
                with subtests.test(f"comment {i} value matches"):
                    assert comment_base.value == comment_test.value

                with subtests.test(f"comment {i} subject matches"):
                    assert comment_base.subject == comment_test.subject

    # Set the class name dynamically
    TestChannelClass.__name__ = f"TestMTChannelToXML02{channel_name.upper()}"
    return TestChannelClass


# Create test classes for each channel type in inventory_02
TestMTChannelToXML02HX = create_channel_test_class("hx")
TestMTChannelToXML02HY = create_channel_test_class("hy")
TestMTChannelToXML02HZ = create_channel_test_class("hz")
TestMTChannelToXML02EX = create_channel_test_class("ex")
TestMTChannelToXML02EY = create_channel_test_class("ey")
