# -*- coding: utf-8 -*-
"""
Tests for converting between StationXML Network and MT Survey objects using pytest.

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""

import datetime

import pytest

try:
    from obspy import read_inventory
    from obspy.core import inventory
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)

from mt_metadata import STATIONXML_01, STATIONXML_02
from mt_metadata.timeseries import Survey
from mt_metadata.timeseries.stationxml import xml_network_mt_survey

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def inventories():
    """Load both StationXML inventories."""
    return {
        "inventory_01": read_inventory(STATIONXML_01.as_posix()),
        "inventory_02": read_inventory(STATIONXML_02.as_posix()),
    }


@pytest.fixture(scope="module")
def networks(inventories):
    """Extract networks from inventories."""
    return {
        "network_01": inventories["inventory_01"].networks[0],
        "network_02": inventories["inventory_02"].networks[0],
    }


@pytest.fixture(scope="module")
def converter():
    """Create an XMLNetworkMTSurvey converter."""
    return xml_network_mt_survey.XMLNetworkMTSurvey()


@pytest.fixture(scope="module")
def surveys(networks, converter):
    """Convert networks to MT surveys."""
    return {
        "survey_01": converter.xml_to_mt(networks["network_01"]),
        "survey_02": converter.xml_to_mt(networks["network_02"]),
    }


@pytest.fixture(scope="module")
def reconverted_networks(surveys, converter):
    """Convert surveys back to networks for round-trip testing."""
    return {
        "reconverted_01": converter.mt_to_xml(surveys["survey_01"]),
        "reconverted_02": converter.mt_to_xml(surveys["survey_02"]),
    }


@pytest.fixture(scope="module")
def expected_surveys():
    """Create expected survey objects for comparison."""
    survey_01 = Survey()
    survey_01.summary = (
        "USMTArray South Magnetotelluric Time Series (USMTArray CONUS South-USGS)"
    )
    survey_01.time_period.start_date = "2020-01-01"
    survey_01.time_period.end_date = "2023-12-31"
    survey_01.fdsn.network = "ZU"
    survey_01.citation_dataset.doi = "https://doi.org/10.7914/SN/ZU_2020"

    survey_02 = Survey(id="CONUS South-USGS")
    survey_02.summary = "USMTArray South Magnetotelluric Time Series"
    survey_02.time_period.start_date = "2020-06-01"
    survey_02.time_period.end_date = "2023-12-31"
    survey_02.fdsn.network = "ZU"
    survey_02.project = "USMTArray"
    survey_02.geographic_name = "Southern USA"
    survey_02.comments.value = (
        "Long-period EarthScope-style coverage of southern United States, "
    )
    survey_02.acquired_by.name = "Pellerin, L."
    survey_02.citation_dataset.doi = "https://doi.org/10.17611/DP/EMTF/USMTARRAY/SOUTH"
    survey_02.citation_journal.doi = "https://doi.org/10.666/test.doi"
    survey_02.project_lead.name = "Schultz, A."
    survey_02.project_lead.email = "Adam.Schultz@oregonstate.edu"
    survey_02.project_lead.organization = "Oregon State University"

    return {"survey_01": survey_01, "survey_02": survey_02}


@pytest.fixture(scope="module")
def sample_survey():
    """Create a sample survey for testing mt_to_xml."""
    survey = Survey(id="Test Survey")
    survey.summary = "Test magnetotelluric survey"
    survey.time_period.start_date = "2020-01-01"
    survey.time_period.end_date = "2021-01-01"
    survey.fdsn.network = "ZZ"
    survey.project = "Test Project"
    survey.geographic_name = "Test Area"
    survey.comments.value = "This is a test survey"
    survey.acquired_by.author = "Test Person"
    survey.acquired_by.comments.value = "Test comments"
    survey.citation_dataset.doi = "https://doi.org/10.1234/test.doi"
    survey.citation_journal.doi = "https://doi.org/10.5678/journal.doi"
    survey.project_lead.author = "Lead Person"
    survey.project_lead.email = "lead@example.com"
    survey.project_lead.organization = "Test Organization"
    survey.release_license = "CC BY 4.0"
    survey.update_all()
    return survey


@pytest.fixture(scope="module")
def network_from_sample(converter, sample_survey):
    """Convert sample_survey to Network."""
    return converter.mt_to_xml(sample_survey)


# =============================================================================
# Tests for Network01 to Survey Conversion
# =============================================================================


class TestNetwork01ToSurvey:
    """Test conversion of first StationXML network to MT survey."""

    def test_basic_attributes(self, surveys, subtests):
        """Test basic attributes from network_01 conversion."""
        survey = surveys["survey_01"]

        with subtests.test("network code"):
            assert survey.fdsn.network == "ZU"

        with subtests.test("id"):
            assert survey.id == "ZU"

        with subtests.test("summary"):
            assert (
                survey.summary
                == "USMTArray South Magnetotelluric Time Series (USMTArray CONUS South-USGS)"
            )

    def test_time_period(self, surveys, subtests):
        """Test time period attributes."""
        survey = surveys["survey_01"]

        with subtests.test("start_date"):
            assert survey.time_period.start_date == "2020-01-01"

        with subtests.test("end_date"):
            assert survey.time_period.end_date == "2023-12-31"

    def test_dataset_doi(self, surveys):
        """Test dataset DOI value."""
        survey = surveys["survey_01"]
        assert (
            survey.citation_dataset.doi.unicode_string()
            == "https://doi.org/10.7914/SN/ZU_2020"
        )


# =============================================================================
# Tests for Network02 to Survey Conversion
# =============================================================================


class TestNetwork02ToSurvey:
    """Test conversion of second StationXML network to MT survey."""

    def test_basic_attributes(self, surveys, subtests):
        """Test basic attributes from network_02 conversion."""
        survey = surveys["survey_02"]

        with subtests.test("network code"):
            assert survey.fdsn.network == "ZU"

        with subtests.test("id"):
            assert survey.id == "CONUS South-USGS"

        with subtests.test("summary"):
            assert survey.summary == "USMTArray South Magnetotelluric Time Series"

        with subtests.test("project"):
            assert survey.project == "USMTArray"

        with subtests.test("geographic_name"):
            assert survey.geographic_name == "Southern USA"

    def test_time_period(self, surveys, subtests):
        """Test time period attributes."""
        survey = surveys["survey_02"]

        with subtests.test("start_date"):
            assert survey.time_period.start_date == "2020-06-01"

        with subtests.test("end_date"):
            assert survey.time_period.end_date == "2023-12-31"

    def test_comments(self, surveys):
        """Test comments attribute."""
        survey = surveys["survey_02"]
        assert (
            survey.comments
            == "Long-period EarthScope-style coverage of southern United States, "
        )

    def test_acquired_by(self, surveys):
        """Test acquired by attribute."""
        survey = surveys["survey_02"]
        assert survey.acquired_by.name == "Pellerin, L."

    def test_project_lead(self, surveys, subtests):
        """Test project lead attributes."""
        survey = surveys["survey_02"]

        with subtests.test("name"):
            assert survey.project_lead.author == "Schultz, A."

        with subtests.test("email"):
            assert survey.project_lead.email == "Adam.Schultz@oregonstate.edu"

        with subtests.test("organization"):
            assert survey.project_lead.organization == "Oregon State University"

    def test_doi_values(self, surveys, subtests):
        """Test DOI values."""
        survey = surveys["survey_02"]

        with subtests.test("dataset doi"):
            assert (
                survey.citation_dataset.doi.unicode_string()
                == "https://doi.org/10.17611/DP/EMTF/USMTARRAY/SOUTH"
            )

        with subtests.test("journal doi"):
            assert (
                survey.citation_journal.doi.unicode_string()
                == "https://doi.org/10.666/test.doi"
            )


# =============================================================================
# Tests for Round-Trip Conversion
# =============================================================================


class TestRoundTripConversion:
    """Test round-trip conversion from Network -> Survey -> Network."""

    def test_time_period(self, networks, reconverted_networks, subtests):
        """Test time period preservation."""
        for idx in ["01", "02"]:
            net_key = f"network_{idx}"
            reconv_key = f"reconverted_{idx}"

            with subtests.test(f"network {idx} start date"):
                assert (
                    reconverted_networks[reconv_key].start_date
                    == networks[net_key].start_date.date.isoformat()
                )

            with subtests.test(f"network {idx} end date"):
                assert (
                    reconverted_networks[reconv_key].end_date
                    == networks[net_key].end_date.date.isoformat()
                )

    def test_comment_preservation(
        self, networks, reconverted_networks, converter, subtests
    ):
        """Test comment preservation for both networks."""
        comment_types = [
            "mt.survey.id",
            "mt.survey.project",
            "mt.survey.geographic_name",
            "mt.survey.acquired_by.author",
            "mt.survey.acquired_by.comments",
        ]

        for idx in ["02"]:  # Network 01 doesn't have these comments
            net_key = f"network_{idx}"
            reconv_key = f"reconverted_{idx}"

            for comment_type in comment_types:
                # Skip if comment doesn't exist in original network
                try:
                    orig = converter.get_comment(
                        networks[net_key].comments, comment_type
                    )
                    if orig is None:
                        continue
                except (AttributeError, IndexError):
                    continue

                with subtests.test(f"network {idx} comment {comment_type}"):
                    c1 = converter.get_comment(
                        networks[net_key].comments, comment_type
                    ).value

                    # Handle special case for acquired_by.comments
                    if comment_type == "mt.survey.acquired_by.comments":
                        c2 = converter.get_comment(
                            reconverted_networks[reconv_key].comments,
                            "mt.survey.acquired_by.comments.value",
                        ).value
                    else:
                        c2 = converter.get_comment(
                            reconverted_networks[reconv_key].comments, comment_type
                        ).value

                    assert c1 == c2

    def test_journal_doi_preservation(
        self, networks, reconverted_networks, converter, subtests
    ):
        """Test journal DOI preservation."""
        for idx in ["02"]:  # Only network 02 has journal DOI
            net_key = f"network_{idx}"
            reconv_key = f"reconverted_{idx}"

            with subtests.test(f"network {idx} journal DOI"):
                c1 = (
                    "https://doi.org/"
                    + converter.get_comment(
                        networks[net_key].comments, "mt.survey.citation_journal.doi"
                    ).value
                )
                c2 = converter.get_comment(
                    reconverted_networks[reconv_key].comments,
                    "mt.survey.citation_journal.doi",
                ).value
                assert c1 == c2

    def test_description_preservation(self, networks, reconverted_networks, subtests):
        """Test description preservation."""
        for idx in ["01", "02"]:
            net_key = f"network_{idx}"
            reconv_key = f"reconverted_{idx}"

            with subtests.test(f"network {idx} description"):
                assert (
                    networks[net_key].description
                    == reconverted_networks[reconv_key].description
                )

    def test_restricted_status_preservation(
        self, networks, reconverted_networks, subtests
    ):
        """Test restricted status preservation."""
        for idx in ["01", "02"]:
            net_key = f"network_{idx}"
            reconv_key = f"reconverted_{idx}"

            with subtests.test(f"network {idx} restricted status"):
                assert (
                    networks[net_key].restricted_status
                    == reconverted_networks[reconv_key].restricted_status
                )


# =============================================================================
# Tests for Survey to Network Conversion (from sample survey)
# =============================================================================


class TestSurveyToNetwork:
    """Test conversion of MT survey to StationXML network."""

    def test_validation(self, converter):
        """Test validation of input objects."""
        with pytest.raises(
            ValueError, match="Input must be mt_metadata.timeseries.Survey object"
        ):
            converter.mt_to_xml("not a survey")

        with pytest.raises(
            ValueError, match="Input must be obspy.core.inventory.Network object"
        ):
            converter.xml_to_mt("not a network")

    def test_basic_attributes(self, sample_survey, network_from_sample, subtests):
        """Test basic attributes of network converted from survey."""
        with subtests.test("code"):
            assert network_from_sample.code == "ZZ"

        with subtests.test("description"):
            assert network_from_sample.description == "Test magnetotelluric survey"

        with subtests.test("start_date"):
            expected = datetime.datetime.strptime("2020-01-01", "%Y-%m-%d")
            assert network_from_sample.start_date == expected.date().isoformat()

        with subtests.test("end_date"):
            expected = datetime.datetime.strptime("2021-01-01", "%Y-%m-%d")
            assert network_from_sample.end_date == expected.date().isoformat()

    def test_comments(self, converter, network_from_sample, subtests):
        """Test comments in network converted from survey."""
        # Main comment
        with subtests.test("main comment"):
            main_comment = None
            for comment in network_from_sample.comments:
                if "test" in comment.value.lower():
                    main_comment = comment.value
                    break
            assert main_comment is not None

        # Test specific comments
        comment_checks = [
            ("mt.survey.project", "Test Project"),
            ("mt.survey.geographic_name", "Test Area"),
            ("mt.survey.acquired_by.author", "Test Person"),
            ("mt.survey.acquired_by.comments.value", "Test comments"),
            ("mt.survey.citation_journal.doi", "https://doi.org/10.5678/journal.doi"),
        ]

        for subject, expected_value in comment_checks:
            with subtests.test(f"comment {subject}"):
                found = False
                for comment in network_from_sample.comments:
                    if comment.subject == subject:
                        assert comment.value == expected_value
                        found = True
                        break
                assert found, f"Comment with subject '{subject}' not found"

    def test_operators(self, network_from_sample, subtests):
        """Test operators in network converted from survey."""
        with subtests.test("operator exists"):
            assert len(network_from_sample.operators) == 1

        operator = network_from_sample.operators[0]

        with subtests.test("agency"):
            assert operator.agency == "Test Organization"

        with subtests.test("contact exists"):
            assert len(operator.contacts) == 1

        contact = operator.contacts[0]

        with subtests.test("contact name"):
            assert contact.names == ["Lead Person"]

        with subtests.test("contact email"):
            assert contact.emails == ["lead@example.com"]

    def test_doi(self, network_from_sample, subtests):
        """Test DOI in network converted from survey."""
        with subtests.test("identifiers exist"):
            assert len(network_from_sample.identifiers) == 1

        with subtests.test("doi value"):
            assert (
                network_from_sample.identifiers[0]
                == "DOI:https://doi.org/10.1234/test.doi"
            )

    def test_restricted_status(self, sample_survey, converter, subtests):
        """Test restricted status in network converted from survey."""
        # Test CC-0
        with subtests.test("CC-0"):
            network = converter.mt_to_xml(sample_survey)
            assert network.restricted_status == "open"

        # Test other license types
        license_tests = [
            ("CC-BY-1.0", "open"),
            ("CC-BY-SA-1.0", "partial"),
            ("CC-BY-NC-1.0", "partial"),
            ("CC-BY-NC-ND-1.0", "closed"),
        ]

        for license_type, expected_status in license_tests:
            with subtests.test(license_type):
                sample_survey.release_license = license_type
                network = converter.mt_to_xml(sample_survey)
                assert network.restricted_status == expected_status


# =============================================================================
# Tests for Helper Methods
# =============================================================================


class TestHelperMethods:
    """Test helper methods of the converter class."""

    def test_make_mt_comments(self, converter, sample_survey, subtests):
        """Test make_mt_comments method."""
        comments = converter.make_mt_comments(sample_survey, mt_key_base="mt.survey")

        # Check expected comment subjects
        expected_subjects = [
            "mt.survey.project",
            "mt.survey.geographic_name",
            "mt.survey.citation_journal.doi",
            "mt.survey.id",
            "mt.survey.acquired_by.author",
            "mt.survey.acquired_by.comments.value",
        ]

        for subject in expected_subjects:
            with subtests.test(f"comment {subject}"):
                found = False
                for comment in comments:
                    if comment.subject == subject:
                        found = True
                        break
                assert found, f"Comment with subject '{subject}' not found"

    def test_read_xml_identifier(self, converter, subtests):
        """Test read_xml_identifier method."""
        test_cases = [
            (["DOI:10.1234/test"], "https://doi.org/10.1234/test"),
            (
                ["something:else", "DOI:10.5678/test"],
                "something:else, https://doi.org/10.5678/test",
            ),
            (["empty_here"], "empty_here"),
        ]

        for identifiers, expected in test_cases:
            with subtests.test(f"identifiers: {identifiers}"):
                result = converter.read_xml_identifier(identifiers)
                assert result == expected

    def test_read_xml_comment(self, converter, subtests):
        """Test read_xml_comment method."""
        # Create some test comments
        comment_tests = [
            (
                inventory.Comment("Test Value", subject="mt.survey.test"),
                "mt.survey.test",
                "Test Value",
            ),
            (
                inventory.Comment("Test Value", subject="other.subject"),
                "other.subject",
                "Test Value",
            ),
            (inventory.Comment("Test Value"), "mt", "Test Value"),
        ]

        for comment, expected_key, expected_value in comment_tests:
            with subtests.test(f"comment: {comment.subject}"):
                key, value = converter.read_xml_comment(comment)
                assert key == expected_key
                assert value == expected_value

    def test_get_comment(self, converter, network_from_sample, subtests):
        """Test get_comment method."""
        # Add some test comments
        test_comments = [
            inventory.Comment("Value 1", subject="test.subject.1"),
            inventory.Comment("Value 2", subject="test.subject.2"),
            inventory.Comment("Value 3"),
        ]

        # Save original comments and restore after test
        original_comments = network_from_sample.comments
        network_from_sample.comments = test_comments

        test_cases = [
            ("test.subject.1", "Value 1"),
            ("test.subject.2", "Value 2"),
            ("nonexistent.subject", None),
        ]

        for subject, expected_value in test_cases:
            with subtests.test(f"subject: {subject}"):
                comment = converter.get_comment(network_from_sample.comments, subject)
                if expected_value is None:
                    assert comment is None
                else:
                    assert comment.value == expected_value

        # Restore original comments
        network_from_sample.comments = original_comments


if __name__ == "__main__":
    pytest.main([__file__])
