# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 11:58:11 2021

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

import pytest

try:
    from obspy import read_inventory
except ImportError:
    pytest.skip(reason="obspy is not installed", allow_module_level=True)
from mt_metadata.timeseries.stationxml import xml_network_mt_survey
from mt_metadata import STATIONXML_01, STATIONXML_02


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def network_01():
    """
    Get the first network from STATIONXML_01
    """
    inventory = read_inventory(STATIONXML_01.as_posix())
    return inventory.networks[0]


@pytest.fixture
def network_02():
    """
    Get the first network from STATIONXML_02
    """
    inventory = read_inventory(STATIONXML_02.as_posix())
    return inventory.networks[0]


@pytest.fixture
def converter():
    """
    Create an XMLNetworkMTSurvey converter
    """
    return xml_network_mt_survey.XMLNetworkMTSurvey()


@pytest.fixture
def survey_01(network_01, converter):
    """
    Convert network_01 to MT survey
    """
    return converter.xml_to_mt(network_01)


@pytest.fixture
def survey_02(network_02, converter):
    """
    Convert network_02 to MT survey
    """
    return converter.xml_to_mt(network_02)


@pytest.fixture
def reconverted_network(survey_02, converter):
    """
    Convert survey_02 back to a network for testing round trip conversion
    """
    return converter.mt_to_xml(survey_02)


# =============================================================================
# Tests for Network01
# =============================================================================


def test_network_01_time_period(survey_01, subtests):
    """Test time period from network 01"""
    with subtests.test("start_date"):
        assert survey_01.time_period.start_date == "2020-01-01"
    with subtests.test("end_date"):
        assert survey_01.time_period.end_date == "2023-12-31"


def test_network_01_dataset_doi(survey_01):
    """Test dataset DOI from network 01"""
    assert (
        survey_01.citation_dataset.doi.unicode_string()
        == "https://doi.org/10.7914/SN/ZU_2020"
    )


def test_network_01_network_code(survey_01):
    """Test network code from network 01"""
    assert survey_01.fdsn.network == "ZU"


def test_network_01_description(survey_01):
    """Test description from network 01"""
    assert (
        survey_01.summary
        == "USMTArray South Magnetotelluric Time Series (USMTArray CONUS South-USGS)"
    )


# =============================================================================
# Tests for Network02
# =============================================================================


def test_network_02_comments_acquired_by(survey_02):
    """Test acquired by from network 02"""
    assert survey_02.acquired_by.name == "Pellerin, L."


def test_network_02_comments_id(survey_02):
    """Test id from network 02"""
    assert survey_02.id == "CONUS South-USGS"


def test_network_02_comments_project(survey_02):
    """Test project from network 02"""
    assert survey_02.project == "USMTArray"


def test_network_02_comments_geographic_name(survey_02):
    """Test geographic name from network 02"""
    assert survey_02.geographic_name == "Southern USA"


def test_network_02_comments_comments(survey_02):
    """Test comments from network 02"""
    assert (
        survey_02.comments
        == "Long-period EarthScope-style coverage of southern United States, "
    )


def test_network_02_comments_project_lead(survey_02, subtests):
    """Test project lead from network 02"""
    with subtests.test("name"):
        assert survey_02.project_lead.name == "Schultz, A."
    with subtests.test("email"):
        assert survey_02.project_lead.email == "Adam.Schultz@oregonstate.edu"
    with subtests.test("organization"):
        assert survey_02.project_lead.organization == "Oregon State University"


def test_network_02_time_period(survey_02, subtests):
    """Test time period from network 02"""
    with subtests.test("start_date"):
        assert survey_02.time_period.start_date == "2020-06-01"
    with subtests.test("end_date"):
        assert survey_02.time_period.end_date == "2023-12-31"


def test_network_02_dataset_doi(survey_02):
    """Test dataset DOI from network 02"""
    assert (
        survey_02.citation_dataset.doi.unicode_string()
        == "https://doi.org/10.17611/DP/EMTF/USMTARRAY/SOUTH"
    )


def test_network_02_journal_doi(survey_02):
    """Test journal DOI from network 02"""
    assert (
        survey_02.citation_journal.doi.unicode_string()
        == "https://doi.org/10.666/test.doi"
    )


def test_network_02_network_code(survey_02):
    """Test network code from network 02"""
    assert survey_02.fdsn.network == "ZU"


def test_network_02_description(survey_02):
    """Test description from network 02"""
    assert survey_02.summary == "USMTArray South Magnetotelluric Time Series"


# =============================================================================
# Tests for Survey to Network Conversion
# =============================================================================


def test_reconverted_time_period(network_02, reconverted_network):
    """Test time period from reconverted network"""
    assert (
        reconverted_network.start_date
        == network_02.start_date.isoformat().split("T")[0]
    )
    assert reconverted_network.end_date == network_02.end_date.isoformat().split("T")[0]


def test_reconverted_comment_id(network_02, reconverted_network, converter):
    """Test id comment from reconverted network"""
    c1 = converter.get_comment(network_02.comments, "mt.survey.id").value
    c2 = converter.get_comment(reconverted_network.comments, "mt.survey.id").value
    assert c1 == c2


def test_reconverted_comment_project(network_02, reconverted_network, converter):
    """Test project comment from reconverted network"""
    c1 = converter.get_comment(network_02.comments, "mt.survey.project").value
    c2 = converter.get_comment(reconverted_network.comments, "mt.survey.project").value
    assert c1 == c2


def test_reconverted_comment_journal_doi(network_02, reconverted_network, converter):
    """Test journal DOI comment from reconverted network"""
    c1 = (
        "https://doi.org/"
        + converter.get_comment(
            network_02.comments, "mt.survey.citation_journal.doi"
        ).value
    )
    c2 = converter.get_comment(
        reconverted_network.comments, "mt.survey.citation_journal.doi"
    ).value
    assert c1 == c2


def test_reconverted_comment_acquired_by(
    network_02, reconverted_network, converter, subtests
):
    """Test acquired by comment from reconverted network"""
    with subtests.test("name"):
        c1 = converter.get_comment(
            network_02.comments, "mt.survey.acquired_by.name"
        ).value
        c2 = converter.get_comment(
            reconverted_network.comments, "mt.survey.acquired_by.name"
        ).value
        assert c1 == c2

    with subtests.test("comments"):
        c1 = converter.get_comment(
            network_02.comments, "mt.survey.acquired_by.comments"
        ).value
        c2 = converter.get_comment(
            reconverted_network.comments, "mt.survey.acquired_by.comments.value"
        ).value
        assert c1 == c2


def test_reconverted_comment_geographic_name(
    network_02, reconverted_network, converter
):
    """Test geographic name comment from reconverted network"""
    c1 = converter.get_comment(network_02.comments, "mt.survey.geographic_name").value
    c2 = converter.get_comment(
        reconverted_network.comments, "mt.survey.geographic_name"
    ).value
    assert c1 == c2


def test_reconverted_description(network_02, reconverted_network):
    """Test description from reconverted network"""
    assert network_02.description == reconverted_network.description


def test_reconverted_restricted_access(network_02, reconverted_network):
    """Test restricted status from reconverted network"""
    assert network_02.restricted_status == reconverted_network.restricted_status
