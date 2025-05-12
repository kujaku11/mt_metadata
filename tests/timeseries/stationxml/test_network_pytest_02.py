# -*- coding: utf-8 -*-
"""
Tests for XMLNetworkMTSurvey class

:copyright:
    Jared Peacock (jpeacock@usgs.gov)
:license: MIT
"""
import pytest
from pathlib import Path
import datetime

try:
    from obspy.core import inventory
    from obspy import read_inventory
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)

from mt_metadata.timeseries.stationxml import xml_network_mt_survey
from mt_metadata.timeseries import Survey
from mt_metadata import STATIONXML_01, STATIONXML_02
from mt_metadata.timeseries.stationxml.fdsn_tools import release_dict


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def converter():
    """Create an XMLNetworkMTSurvey converter"""
    return xml_network_mt_survey.XMLNetworkMTSurvey()


@pytest.fixture
def sample_inventory_01():
    """Read sample inventory file 01"""
    return read_inventory(STATIONXML_01.as_posix())


@pytest.fixture
def sample_inventory_02():
    """Read sample inventory file 02"""
    return read_inventory(STATIONXML_02.as_posix())


@pytest.fixture
def network_01(sample_inventory_01):
    """Get network from sample inventory 01"""
    return sample_inventory_01.networks[0]


@pytest.fixture
def network_02(sample_inventory_02):
    """Get network from sample inventory 02"""
    return sample_inventory_02.networks[0]


@pytest.fixture
def survey_01_expected():
    """Create expected survey object from network_01"""
    survey = Survey()
    survey.summary = (
        "USMTArray South Magnetotelluric Time Series (USMTArray CONUS South-USGS)"
    )
    survey.time_period.start_date = "2020-01-01"
    survey.time_period.end_date = "2023-12-31"
    survey.fdsn.network = "ZU"
    survey.citation_dataset.doi = "https://doi.org/10.7914/SN/ZU_2020"
    return survey


@pytest.fixture
def survey_02_expected():
    """Create expected survey object from network_02"""
    survey = Survey(id="CONUS South-USGS")
    survey.summary = "USMTArray South Magnetotelluric Time Series"
    survey.time_period.start_date = "2020-06-01"
    survey.time_period.end_date = "2023-12-31"
    survey.fdsn.network = "ZU"
    survey.project = "USMTArray"
    survey.geographic_name = "Southern USA"
    survey.comments.value = (
        "Long-period EarthScope-style coverage of southern United States, "
    )
    survey.acquired_by.name = "Pellerin, L."
    survey.citation_dataset.doi = "https://doi.org/10.17611/DP/EMTF/USMTARRAY/SOUTH"
    survey.citation_journal.doi = "https://doi.org/10.666/test.doi"
    survey.project_lead.name = "Schultz, A."
    survey.project_lead.email = "Adam.Schultz@oregonstate.edu"
    survey.project_lead.organization = "Oregon State University"
    return survey


@pytest.fixture
def survey_01_converted(converter, network_01):
    """Convert network_01 to Survey"""
    return converter.xml_to_mt(network_01)


@pytest.fixture
def survey_02_converted(converter, network_02):
    """Convert network_02 to Survey"""
    return converter.xml_to_mt(network_02)


@pytest.fixture
def sample_survey():
    """Create a sample survey for testing mt_to_xml"""
    survey = Survey(id="Test Survey")
    survey.summary = "Test magnetotelluric survey"
    survey.time_period.start_date = "2020-01-01"
    survey.time_period.end_date = "2021-01-01"
    survey.fdsn.network = "ZZ"
    survey.project = "Test Project"
    survey.geographic_name = "Test Area"
    survey.comments.value = "This is a test survey"
    survey.acquired_by.name = "Test Person"
    survey.acquired_by.comments.value = "Test comments"
    survey.citation_dataset.doi = "https://doi.org/10.1234/test.doi"
    survey.citation_journal.doi = "https://doi.org/10.5678/journal.doi"
    survey.project_lead.name = "Lead Person"
    survey.project_lead.email = "lead@example.com"
    survey.project_lead.organization = "Test Organization"
    survey.release_license = "CC BY 4.0"
    survey.update_all()
    return survey


@pytest.fixture
def network_from_survey(converter, sample_survey):
    """Convert sample_survey to Network"""
    return converter.mt_to_xml(sample_survey)


# =============================================================================
# Test Network to Survey Conversion
# =============================================================================


def test_network_01_to_survey_basic(survey_01_converted, subtests):
    """Test basic attributes from network_01 conversion"""
    with subtests.test("network code"):
        assert survey_01_converted.fdsn.network == "ZU"

    with subtests.test("id"):
        assert survey_01_converted.id == ""

    with subtests.test("summary"):
        assert (
            survey_01_converted.summary
            == "USMTArray South Magnetotelluric Time Series (USMTArray CONUS South-USGS)"
        )


def test_network_01_to_survey_time_period(survey_01_converted, subtests):
    """Test time period from network_01 conversion"""
    with subtests.test("start_date"):
        assert survey_01_converted.time_period.start_date == "2020-01-01"

    with subtests.test("end_date"):
        assert survey_01_converted.time_period.end_date == "2023-12-31"


def test_network_01_to_survey_doi(survey_01_converted):
    """Test DOI from network_01 conversion"""
    assert (
        survey_01_converted.citation_dataset.doi.unicode_string()
        == "https://doi.org/10.7914/SN/ZU_2020"
    )


def test_network_02_to_survey_basic(survey_02_converted, subtests):
    """Test basic attributes from network_02 conversion"""
    with subtests.test("network code"):
        assert survey_02_converted.fdsn.network == "ZU"

    with subtests.test("id"):
        assert survey_02_converted.id == "CONUS South-USGS"

    with subtests.test("summary"):
        assert (
            survey_02_converted.summary == "USMTArray South Magnetotelluric Time Series"
        )

    with subtests.test("project"):
        assert survey_02_converted.project == "USMTArray"

    with subtests.test("geographic_name"):
        assert survey_02_converted.geographic_name == "Southern USA"


def test_network_02_to_survey_comments(survey_02_converted):
    """Test comments from network_02 conversion"""
    assert (
        "Long-period EarthScope-style coverage of southern United States"
        in survey_02_converted.comments.value
    )


def test_network_02_to_survey_acquired_by(survey_02_converted):
    """Test acquired_by from network_02 conversion"""
    assert survey_02_converted.acquired_by.name == "Pellerin, L."


def test_network_02_to_survey_project_lead(survey_02_converted, subtests):
    """Test project_lead from network_02 conversion"""
    with subtests.test("name"):
        assert survey_02_converted.project_lead.name == "Schultz, A."

    with subtests.test("email"):
        assert survey_02_converted.project_lead.email == "Adam.Schultz@oregonstate.edu"

    with subtests.test("organization"):
        assert (
            survey_02_converted.project_lead.organization == "Oregon State University"
        )


def test_network_02_to_survey_doi(survey_02_converted, subtests):
    """Test DOIs from network_02 conversion"""
    with subtests.test("dataset doi"):
        assert (
            survey_02_converted.citation_dataset.doi.unicode_string()
            == "https://doi.org/10.17611/DP/EMTF/USMTARRAY/SOUTH"
        )

    with subtests.test("journal doi"):
        assert (
            survey_02_converted.citation_journal.doi.unicode_string()
            == "https://doi.org/10.666/test.doi"
        )


# =============================================================================
# Test Survey to Network Conversion
# =============================================================================


def test_survey_to_network_validation(converter):
    """Test validation of input to mt_to_xml"""
    with pytest.raises(
        ValueError, match="Input must be mt_metadata.timeseries.Survey object"
    ):
        converter.mt_to_xml("not a survey")


def test_network_validation(converter):
    """Test validation of input to xml_to_mt"""
    with pytest.raises(
        ValueError, match="Input must be obspy.core.inventory.Network object"
    ):
        converter.xml_to_mt("not a network")


def test_survey_to_network_basic(sample_survey, network_from_survey, subtests):
    """Test basic attributes of network converted from survey"""
    with subtests.test("code"):
        assert network_from_survey.code == "ZZ"

    with subtests.test("description"):
        assert network_from_survey.description == "Test magnetotelluric survey"

    with subtests.test("start_date"):
        expected = datetime.datetime.strptime("2020-01-01", "%Y-%m-%d")
        assert network_from_survey.start_date == expected.date().isoformat()

    with subtests.test("end_date"):
        expected = datetime.datetime.strptime("2021-01-01", "%Y-%m-%d")
        assert network_from_survey.end_date == expected.date().isoformat()


def test_survey_to_network_comments(converter, network_from_survey, subtests):
    """Test comments in network converted from survey"""
    # Main comment
    with subtests.test("main comment"):
        main_comment = None
        for comment in network_from_survey.comments:
            if "test" in comment.value.lower():
                main_comment = comment.value
                break
        assert main_comment is not None

    # Test specific comments
    comment_checks = [
        ("mt.survey.project", "Test Project"),
        ("mt.survey.geographic_name", "Test Area"),
        ("mt.survey.acquired_by.name", "Test Person"),
        ("mt.survey.acquired_by.comments.value", "Test comments"),
        ("mt.survey.citation_journal.doi", "https://doi.org/10.5678/journal.doi"),
    ]

    for subject, expected_value in comment_checks:
        with subtests.test(f"comment {subject}"):
            found = False
            for comment in network_from_survey.comments:
                if comment.subject == subject:
                    assert comment.value == expected_value
                    found = True
                    break
            assert found, f"Comment with subject '{subject}' not found"


def test_survey_to_network_operators(network_from_survey, subtests):
    """Test operators in network converted from survey"""
    with subtests.test("operator exists"):
        assert len(network_from_survey.operators) == 1

    operator = network_from_survey.operators[0]

    with subtests.test("agency"):
        assert operator.agency == "Test Organization"

    with subtests.test("contact exists"):
        assert len(operator.contacts) == 1

    contact = operator.contacts[0]

    with subtests.test("contact name"):
        assert contact.names == ["Lead Person"]

    with subtests.test("contact email"):
        assert contact.emails == ["lead@example.com"]


def test_survey_to_network_doi(network_from_survey, subtests):
    """Test DOI in network converted from survey"""
    with subtests.test("identifiers exist"):
        assert len(network_from_survey.identifiers) == 1

    with subtests.test("doi value"):
        assert (
            network_from_survey.identifiers[0] == "DOI:https://doi.org/10.1234/test.doi"
        )


def test_survey_to_network_restricted_status(sample_survey, converter, subtests):
    """Test restricted status in network converted from survey"""
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
# Test Helper Methods
# =============================================================================


def test_make_mt_comments(converter, sample_survey, subtests):
    """Test make_mt_comments method"""
    comments = converter.make_mt_comments(sample_survey, mt_key_base="mt.survey")

    # Check expected comment subjects
    expected_subjects = [
        "mt.survey.project",
        "mt.survey.geographic_name",
        "mt.survey.citation_journal.doi",
        "mt.survey.id",
        "mt.survey.acquired_by.name",
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


def test_read_xml_identifier(converter, subtests):
    """Test read_xml_identifier method"""
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


def test_read_xml_comment(converter, subtests):
    """Test read_xml_comment method"""
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


def test_get_comment(converter, network_from_survey, subtests):
    """Test get_comment method"""
    # Add some test comments
    network_from_survey.comments = [
        inventory.Comment("Value 1", subject="test.subject.1"),
        inventory.Comment("Value 2", subject="test.subject.2"),
        inventory.Comment("Value 3"),
    ]

    test_cases = [
        ("test.subject.1", "Value 1"),
        ("test.subject.2", "Value 2"),
        ("nonexistent.subject", None),
    ]

    for subject, expected_value in test_cases:
        with subtests.test(f"subject: {subject}"):
            comment = converter.get_comment(network_from_survey.comments, subject)
            if expected_value is None:
                assert comment is None
            else:
                assert comment.value == expected_value


if __name__ == "__main__":
    pytest.main([__file__])
