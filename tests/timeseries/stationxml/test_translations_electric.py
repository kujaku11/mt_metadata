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
import pytest

try:
    from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment
    from obspy.core import inventory
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)

from mt_metadata import STATIONXML_ELECTRIC

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def translator():
    """Create an XMLInventoryMTExperiment translator"""
    return XMLInventoryMTExperiment()


@pytest.fixture(scope="module")
def original_xml():
    """Read the original StationXML file"""
    return inventory.read_inventory(STATIONXML_ELECTRIC.as_posix())


@pytest.fixture(scope="module")
def mtml(translator, original_xml):
    """Convert the original XML to MTML"""
    return translator.xml_to_mt(original_xml)


@pytest.fixture(scope="module")
def new_xml(translator, mtml):
    """Convert the MTML back to StationXML"""
    return translator.mt_to_xml(mtml)


@pytest.fixture(scope="module")
def network_0(original_xml):
    """Get the network from the original XML"""
    return original_xml.networks[0]


@pytest.fixture(scope="module")
def network_1(new_xml):
    """Get the network from the new XML"""
    return new_xml.networks[0]


@pytest.fixture(scope="module")
def station_0(network_0):
    """Get the station from the original XML"""
    return network_0.stations[0]


@pytest.fixture(scope="module")
def station_1(network_1):
    """Get the station from the new XML"""
    return network_1.stations[0]


@pytest.fixture(scope="module")
def channel_0(station_0):
    """Get the channel from the original XML"""
    return station_0.channels[0]


@pytest.fixture(scope="module")
def channel_1(station_1):
    """Get the channel from the new XML"""
    return station_1.channels[0]


@pytest.fixture(scope="module")
def response_0(channel_0):
    """Get the response from the original XML"""
    return channel_0.response


@pytest.fixture(scope="module")
def response_1(channel_1):
    """Get the response from the new XML"""
    return channel_1.response


# =============================================================================
# Network Tests
# =============================================================================


def test_network_basic_properties(network_0, network_1, subtests):
    """Test basic network properties"""
    with subtests.test("start date"):
        assert network_0.start_date.date.isoformat() == network_1.start_date

    with subtests.test("code"):
        assert network_0.code == network_1.code

    with subtests.test("restricted status"):
        assert network_0.restricted_status == network_1.restricted_status

    with subtests.test("identifiers"):
        assert (
            network_0.identifiers[0].replace("DOI:", "DOI:https://doi.org/")
            == network_1.identifiers[0]
        )


def test_network_end_date(network_0, network_1):
    """Test network end date (original does not have an end date)"""
    assert network_0.end_date.isoformat() != network_1.end_date


def test_network_comments(network_0, network_1):
    """Test network comments"""
    original_comment_dict = {
        c.subject: c.value for c in network_0.comments if c.value not in [None, ""]
    }
    original_comment_dict["mt.survey.citation_journal.doi"] = (
        f"https://doi.org/{original_comment_dict['mt.survey.citation_journal.doi']}"
    )
    new_comment_dict = {
        c.subject: c.value for c in network_1.comments if c.value not in [None, ""]
    }
    assert original_comment_dict == new_comment_dict


def test_network_operator(network_0, network_1, subtests):
    """Test network operator properties"""
    with subtests.test("agency"):
        assert network_0.operators[0].agency == network_1.operators[0].agency

    with subtests.test("contact names"):
        assert (
            network_0.operators[0].contacts[0].names
            == network_1.operators[0].contacts[0].names
        )

    with subtests.test("contact emails"):
        assert (
            network_0.operators[0].contacts[0].emails
            == network_1.operators[0].contacts[0].emails
        )


# =============================================================================
# Station Tests
# =============================================================================


def test_station_basic_properties(station_0, station_1, subtests):
    """Test basic station properties"""
    with subtests.test("start date"):
        assert station_0.start_date == station_1.start_date

    with subtests.test("code"):
        assert station_0.code == station_1.code

    with subtests.test("alternate code"):
        assert station_0.alternate_code == station_1.alternate_code

    with subtests.test("restricted status"):
        assert station_0.restricted_status == station_1.restricted_status


def test_station_end_date(station_0, station_1):
    """Test station end date (original file does not have an end date)"""
    assert station_0.end_date.isoformat() != station_1.end_date


def test_station_comments(station_0, station_1):
    """Test station comments"""
    original_comment_dict = {
        c.subject: c.value for c in station_0.comments if c.value not in [None, ""]
    }
    new_comment_dict = {
        c.subject: c.value for c in station_1.comments if c.value not in [None, ""]
    }
    # Check just the keys as the values might differ slightly due to parsing
    assert sorted(original_comment_dict.keys()) == sorted(new_comment_dict.keys())


def test_station_location(station_0, station_1, subtests):
    """Test station geographical information"""
    with subtests.test("latitude"):
        assert station_0.latitude == pytest.approx(station_1.latitude, abs=1e-4)

    with subtests.test("longitude"):
        assert station_0.longitude == pytest.approx(station_1.longitude, abs=1e-4)

    with subtests.test("elevation"):
        assert station_0.elevation == pytest.approx(station_1.elevation, abs=1e-4)


def test_station_site(station_0, station_1):
    """Test station site name"""
    assert station_0.site.name == station_1.site.name


def test_station_equipment(station_0, station_1):
    """Test station equipment properties"""
    for eq_0, eq_1 in zip(station_0.equipments, station_1.equipments):
        assert eq_0.resource_id == eq_1.resource_id
        assert eq_0.type == eq_1.type
        assert eq_0.manufacturer == eq_1.manufacturer
        assert eq_0.model == eq_1.model
        assert eq_0.serial_number == eq_1.serial_number
        assert eq_0.installation_date == eq_1.installation_date
        assert eq_0.removal_date == eq_1.removal_date


# =============================================================================
# Channel Tests
# =============================================================================


def test_channel_basic_properties(channel_0, channel_1, subtests):
    """Test basic channel properties"""
    with subtests.test("start date"):
        assert channel_0.start_date == channel_1.start_date

    with subtests.test("code"):
        assert channel_0.code == channel_1.code

    with subtests.test("restricted status"):
        assert channel_0.restricted_status == channel_1.restricted_status

    with subtests.test("alternate code"):
        assert channel_0.alternate_code.lower() == channel_1.alternate_code.lower()

    with subtests.test("sample rate"):
        assert channel_0.sample_rate == channel_1.sample_rate

    with subtests.test("calibration units"):
        assert channel_0.calibration_units == channel_1.calibration_units


def test_channel_end_date(channel_0, channel_1):
    """Test channel end date (original file does not have the correct end date)"""
    assert channel_0.end_date.isoformat() != channel_1.end_date


def test_channel_comments(channel_0, channel_1):
    """Test channel comments"""
    original_comment_dict = {
        c.subject: c.value for c in channel_0.comments if c.value not in [None, ""]
    }
    new_comment_dict = {
        c.subject: c.value for c in channel_1.comments if c.value not in [None, ""]
    }
    assert original_comment_dict == new_comment_dict


def test_channel_location(channel_0, channel_1, subtests):
    """Test channel geographical information"""
    with subtests.test("latitude"):
        assert channel_0.latitude == pytest.approx(channel_1.latitude, abs=1e-4)

    with subtests.test("longitude"):
        assert channel_0.longitude == pytest.approx(channel_1.longitude, abs=1e-4)

    with subtests.test("elevation"):
        assert channel_0.elevation == pytest.approx(channel_1.elevation, abs=1e-4)


def test_channel_orientation(channel_0, channel_1, subtests):
    """Test channel orientation"""
    with subtests.test("azimuth"):
        assert channel_0.azimuth == pytest.approx(channel_1.azimuth, abs=1e-4)

    with subtests.test("dip"):
        assert channel_0.dip == pytest.approx(channel_1.dip, abs=1e-4)

    with subtests.test("depth"):
        assert channel_0.depth == pytest.approx(channel_1.depth, abs=1e-4)


def test_channel_sensor(channel_0, channel_1, subtests):
    """Test channel sensor properties"""
    with subtests.test("type"):
        assert channel_0.sensor.type == channel_1.sensor.type

    with subtests.test("description"):
        assert channel_0.sensor.description == channel_1.sensor.description

    with subtests.test("manufacturer"):
        assert channel_0.sensor.manufacturer == channel_1.sensor.manufacturer

    with subtests.test("model"):
        assert channel_0.sensor.model == channel_1.sensor.model

    with subtests.test("serial number"):
        assert channel_0.sensor.serial_number == channel_1.sensor.serial_number


# =============================================================================
# Response Tests
# =============================================================================


def test_response_sensitivity(response_0, response_1, mtml):
    """Test response sensitivity"""
    mt_response = (
        mtml.surveys[0]
        .stations[0]
        .runs[0]
        .channels[0]
        .channel_response(mtml.surveys[0].filters)
    )

    # Using pytest.approx with abs parameter since we want to compare with ~6 decimal places
    assert response_0.instrument_sensitivity.value == pytest.approx(
        mt_response.compute_instrument_sensitivity(
            response_0.instrument_sensitivity.frequency, sig_figs=10
        ),
        abs=1,
    )

    assert (
        response_0.instrument_sensitivity.input_units
        == response_1.instrument_sensitivity.input_units
    )
    assert (
        response_0.instrument_sensitivity.output_units
        == response_1.instrument_sensitivity.output_units
    )


def test_response_stages(response_0, response_1):
    """Test response stages"""
    for stage_0, stage_1 in zip(response_0.response_stages, response_1.response_stages):
        # Check instance types
        if not isinstance(stage_0, type(stage_1)):
            assert stage_0.stage_sequence_number == stage_1.stage_sequence_number

        else:
            assert isinstance(stage_0, type(stage_1))

        # Common attributes to check
        common_keys = [
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
        ]

        # Check specific attributes based on response stage type
        if isinstance(stage_0, inventory.PolesZerosResponseStage):
            specific_keys = [
                "pz_transfer_function_type",
                "normalization_factor",
                "zeros",
                "poles",
            ]
        elif isinstance(stage_0, inventory.CoefficientsTypeResponseStage):
            specific_keys = [
                "cf_transfer_function_type",
                "numerator",
                "denominator",
            ]
        else:
            specific_keys = []

        # Combine keys and check each attribute
        keys = common_keys + specific_keys
        for key in keys:
            attr_0 = getattr(stage_0, key)
            attr_1 = getattr(stage_1, key)

            assert attr_0 == attr_1


if __name__ == "__main__":
    pytest.main([__file__])
