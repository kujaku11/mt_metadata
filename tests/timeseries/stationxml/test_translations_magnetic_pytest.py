# -*- coding: utf-8 -*-
"""
Test translation from XML to MTML back to XML for magnetic data.

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""

import numpy as np
import pytest


try:
    from obspy.core import inventory

    from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)

from mt_metadata import STATIONXML_MAGNETIC


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def translator():
    """Create a translator instance."""
    return XMLInventoryMTExperiment()


@pytest.fixture(scope="module")
def original_xml():
    """Load the original StationXML."""
    return inventory.read_inventory(STATIONXML_MAGNETIC.as_posix())


@pytest.fixture(scope="module")
def mtml(translator, original_xml):
    """Convert XML to MT metadata."""
    return translator.xml_to_mt(original_xml)


@pytest.fixture(scope="module")
def new_xml(translator, mtml):
    """Convert MT metadata back to XML."""
    return translator.mt_to_xml(mtml)


@pytest.fixture(scope="module")
def network_pair(original_xml, new_xml):
    """Get the network pair for comparison."""
    return (original_xml.networks[0], new_xml.networks[0])


@pytest.fixture(scope="module")
def station_pair(network_pair):
    """Get the station pair for comparison."""
    return (network_pair[0].stations[0], network_pair[1].stations[0])


@pytest.fixture(scope="module")
def channel_pair(station_pair):
    """Get the channel pair for comparison."""
    return (station_pair[0].channels[0], station_pair[1].channels[0])


@pytest.fixture(scope="module")
def response_pair(channel_pair):
    """Get the response pair for comparison."""
    return (channel_pair[0].response, channel_pair[1].response)


# =============================================================================
# Test Classes
# =============================================================================


class TestNetworkTranslation:
    """Test network-level attributes during translation."""

    def test_basic_attributes(self, network_pair, subtests):
        """Test basic network attributes."""
        network_0, network_1 = network_pair

        with subtests.test("start date"):
            assert network_0.start_date == network_1.start_date

        with subtests.test("code"):
            assert network_0.code == network_1.code

        with subtests.test("restricted status"):
            assert network_0.restricted_status == network_1.restricted_status

        with subtests.test("identifiers"):
            assert (
                network_0.identifiers[0].replace("DOI:", "DOI:https://doi.org/")
                == network_1.identifiers[0]
            )

    def test_end_date(self, network_pair):
        """Test network end date (original doesn't have an end date)."""
        network_0, network_1 = network_pair

        # Original does not have an end date, so they should not be equal
        assert network_0.end_date.isoformat() != network_1.end_date

    def test_comments(self, network_pair):
        """Test network comments."""
        network_0, network_1 = network_pair

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

    def test_operator(self, network_pair, subtests):
        """Test network operator attributes."""
        network_0, network_1 = network_pair

        with subtests.test("agency"):
            assert network_0.operators[0].agency == network_1.operators[0].agency

        with subtests.test("names"):
            assert (
                network_0.operators[0].contacts[0].names
                == network_1.operators[0].contacts[0].names
            )

        with subtests.test("emails"):
            assert (
                network_0.operators[0].contacts[0].emails
                == network_1.operators[0].contacts[0].emails
            )


class TestStationTranslation:
    """Test station-level attributes during translation."""

    def test_basic_attributes(self, station_pair, subtests):
        """Test basic station attributes."""
        station_0, station_1 = station_pair

        with subtests.test("start date"):
            assert station_0.start_date == station_1.start_date

        with subtests.test("code"):
            assert station_0.code == station_1.code

        with subtests.test("alternate code"):
            assert station_0.alternate_code == station_1.alternate_code

        with subtests.test("restricted status"):
            assert station_0.restricted_status == station_1.restricted_status

        with subtests.test("site name"):
            assert station_0.site.name == station_1.site.name

    def test_end_date(self, station_pair):
        """Test station end date (original doesn't have an end date)."""
        station_0, station_1 = station_pair

        # Original does not have correct end date
        assert station_0.end_date.isoformat() != station_1.end_date

    def test_comments(self, station_pair):
        """Test station comments."""
        station_0, station_1 = station_pair

        original_comment_dict = {
            c.subject: c.value for c in station_0.comments if c.value not in [None, ""]
        }

        new_comment_dict = {
            c.subject: c.value for c in station_1.comments if c.value not in [None, ""]
        }

        # Just check the keys are the same
        assert sorted(original_comment_dict.keys()) == sorted(new_comment_dict.keys())

    def test_location(self, station_pair, subtests):
        """Test station location attributes."""
        station_0, station_1 = station_pair

        with subtests.test("latitude"):
            assert np.isclose(station_0.latitude, station_1.latitude, rtol=1e-4)

        with subtests.test("longitude"):
            assert np.isclose(station_0.longitude, station_1.longitude, rtol=1e-4)

        with subtests.test("elevation"):
            assert np.isclose(station_0.elevation, station_1.elevation, rtol=1e-4)

    def test_equipment(self, station_pair, subtests):
        """Test station equipment attributes."""
        station_0, station_1 = station_pair

        for eq_idx, (eq_0, eq_1) in enumerate(
            zip(station_0.equipments, station_1.equipments)
        ):
            attrs = [
                "resource_id",
                "type",
                "manufacturer",
                "model",
                "serial_number",
                "installation_date",
                "removal_date",
            ]

            for attr in attrs:
                with subtests.test(f"equipment {eq_idx} {attr}"):
                    assert getattr(eq_0, attr) == getattr(eq_1, attr)


class TestChannelTranslation:
    """Test channel-level attributes during translation."""

    def test_basic_attributes(self, channel_pair, subtests):
        """Test basic channel attributes."""
        channel_0, channel_1 = channel_pair

        with subtests.test("start date"):
            assert channel_0.start_date == channel_1.start_date

        with subtests.test("code"):
            assert channel_0.code == channel_1.code

        with subtests.test("alternate code"):
            assert channel_0.alternate_code.lower() == channel_1.alternate_code.lower()

        with subtests.test("restricted status"):
            assert channel_0.restricted_status == channel_1.restricted_status

        with subtests.test("sample rate"):
            assert channel_0.sample_rate == channel_1.sample_rate

        with subtests.test("calibration units"):
            assert channel_0.calibration_units == channel_1.calibration_units

    def test_end_date(self, channel_pair):
        """Test channel end date (original doesn't have the correct end date)."""
        channel_0, channel_1 = channel_pair

        # Original does not have correct end date
        assert channel_0.end_date.isoformat() != channel_1.end_date

    def test_comments(self, channel_pair):
        """Test channel comments."""
        channel_0, channel_1 = channel_pair

        original_comment_dict = {
            c.subject: c.value for c in channel_0.comments if c.value not in [None, ""]
        }

        new_comment_dict = {
            c.subject: c.value for c in channel_1.comments if c.value not in [None, ""]
        }

        assert original_comment_dict == new_comment_dict

    def test_location(self, channel_pair, subtests):
        """Test channel location attributes."""
        channel_0, channel_1 = channel_pair

        with subtests.test("latitude"):
            assert np.isclose(channel_0.latitude, channel_1.latitude, rtol=1e-4)

        with subtests.test("longitude"):
            assert np.isclose(channel_0.longitude, channel_1.longitude, rtol=1e-4)

        with subtests.test("elevation"):
            assert np.isclose(channel_0.elevation, channel_1.elevation, rtol=1e-4)

    def test_orientation(self, channel_pair, subtests):
        """Test channel orientation attributes."""
        channel_0, channel_1 = channel_pair

        with subtests.test("azimuth"):
            assert np.isclose(channel_0.azimuth, channel_1.azimuth, rtol=1e-4)

        with subtests.test("dip"):
            assert np.isclose(channel_0.dip, channel_1.dip, rtol=1e-4)

        with subtests.test("depth"):
            assert np.isclose(channel_0.depth, channel_1.depth, rtol=1e-4)

    def test_sensor(self, channel_pair, subtests):
        """Test channel sensor attributes."""
        channel_0, channel_1 = channel_pair

        attrs = ["type", "description", "manufacturer", "model", "serial_number"]

        for attr in attrs:
            with subtests.test(f"sensor {attr}"):
                assert getattr(channel_0.sensor, attr) == getattr(
                    channel_1.sensor, attr
                )


class TestResponseTranslation:
    """Test response-level attributes during translation."""

    def test_sensitivity(self, response_pair, subtests):
        """Test response sensitivity attributes."""
        response_0, response_1 = response_pair

        with subtests.test("sensitivity value"):
            assert np.isclose(
                response_0.instrument_sensitivity.value,
                response_1.instrument_sensitivity.value,
                rtol=1e-3,
            )

        with subtests.test("input units"):
            assert (
                response_0.instrument_sensitivity.input_units
                == response_1.instrument_sensitivity.input_units
            )

        with subtests.test("output units"):
            assert (
                response_0.instrument_sensitivity.output_units
                == response_1.instrument_sensitivity.output_units
            )

    def test_zpk_filter(self, response_pair, subtests):
        """Test ZPK filter attributes."""
        response_0, response_1 = response_pair

        zpk_0 = response_0.response_stages[0]
        zpk_1 = response_1.response_stages[0]

        keys = [
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
        ]

        for key in keys:
            with subtests.test(f"zpk {key}"):
                attr_0 = getattr(zpk_0, key)
                attr_1 = getattr(zpk_1, key)

                assert attr_0 == attr_1

    def test_coefficient_filter(self, response_pair, subtests):
        """Test coefficient filter attributes."""
        response_0, response_1 = response_pair

        f_0 = response_0.response_stages[1]
        f_1 = response_1.response_stages[1]

        keys = [
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
        ]

        for key in keys:
            with subtests.test(f"coefficient {key}"):
                attr_0 = getattr(f_0, key)
                attr_1 = getattr(f_1, key)

                assert attr_0 == attr_1

    def test_time_delay(self, response_pair, subtests):
        """Test time delay filter attributes."""
        response_0, response_1 = response_pair

        f_0 = response_0.response_stages[2]
        f_1 = response_1.response_stages[2]

        keys = [
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
        ]

        for key in keys:
            with subtests.test(f"time delay {key}"):
                attr_0 = getattr(f_0, key)
                attr_1 = getattr(f_1, key)

                assert attr_0 == attr_1


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
