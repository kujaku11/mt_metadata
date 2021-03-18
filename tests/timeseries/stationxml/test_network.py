# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 11:58:11 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

import unittest

from obspy import read_inventory
from mt_metadata.timeseries.stationxml import xml_network_mt_survey
from tests import STATIONXML_01, STATIONXML_02


class TestNetwork01(unittest.TestCase):
    """
    Test reading network into MT Survey object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        self.network = self.inventory.networks[0]

        self.converter = xml_network_mt_survey.XMLNetworkMTSurvey()
        self.survey = self.converter.xml_to_mt(self.network)

    def test_time_period(self):
        self.assertEqual(self.survey.time_period.start_date, "2020-01-01")
        self.assertEqual(self.survey.time_period.end_date, "2023-12-31")
        self.assertEqual(self.survey.time_period.start, "2020-01-01T00:00:00+00:00")
        self.assertEqual(self.survey.time_period.end, "2023-12-31T23:59:59+00:00")

    def test_dataset_doi(self):
        self.assertEqual(self.survey.citation_dataset.doi, "10.7914/SN/ZU_2020")

    def test_networkd_code(self):
        self.assertEqual(self.survey.fdsn.network, "ZU")

    def test_description(self):
        self.assertEqual(
            self.survey.summary,
            "USMTArray South Magnetotelluric Time Series (USMTArray CONUS South-USGS)",
        )


class TestNetwork02(unittest.TestCase):
    """
    Test reading network into MT Survey object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.network = self.inventory.networks[0]

        self.converter = xml_network_mt_survey.XMLNetworkMTSurvey()
        self.survey = self.converter.xml_to_mt(self.network)

    def test_comments_acquired_by(self):
        self.assertEqual(self.survey.acquired_by.author, "Pellerin, L.")

    def test_comments_survey_id(self):
        self.assertEqual(self.survey.survey_id, "CONUS South-USGS")

    def test_comments_project(self):
        self.assertEqual(self.survey.project, "USMTArray")

    def test_comments_geographic_name(self):
        self.assertEqual(self.survey.geographic_name, "Southern USA")

    def test_comments_comments(self):
        self.assertEqual(
            self.survey.comments,
            "Long-period EarthScope-style coverage of southern United States",
        )

    def test_comments_project_lead(self):
        self.assertEqual(self.survey.project_lead.author, "Schultz, A.")
        self.assertEqual(self.survey.project_lead.email, "Adam.Schultz@oregonstate.edu")
        self.assertEqual(
            self.survey.project_lead.organization, "Oregon State University"
        )

    def test_time_period(self):
        self.assertEqual(self.survey.time_period.start_date, "2020-06-01")
        self.assertEqual(self.survey.time_period.end_date, "2023-12-31")
        self.assertEqual(self.survey.time_period.start, "2020-06-01T00:00:00+00:00")
        self.assertEqual(self.survey.time_period.end, "2023-12-31T23:59:59+00:00")

    def test_dataset_doi(self):
        self.assertEqual(
            self.survey.citation_dataset.doi, "10.17611/DP/EMTF/USMTARRAY/SOUTH"
        )

    def test_journal_doi(self):
        self.assertEqual(self.survey.citation_journal.doi, "10.666/test.doi")

    def test_networkd_code(self):
        self.assertEqual(self.survey.fdsn.network, "ZU")

    def test_description(self):
        self.assertEqual(
            self.survey.summary, "USMTArray South Magnetotelluric Time Series"
        )


class TestSurveyToNetwork(unittest.TestCase):
    """
    Test converting a network to a survey
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.original_network = self.inventory.networks[0]

        self.converter = xml_network_mt_survey.XMLNetworkMTSurvey()
        self.survey = self.converter.xml_to_mt(self.original_network)
        self.test_network = self.converter.mt_to_xml(self.survey)

    def test_time_period(self):
        self.assertEqual(self.test_network.start_date, self.original_network.start_date)
        self.assertEqual(self.test_network.end_date, self.original_network.end_date)

    def test_comment_survey_id(self):
        c1 = self.converter.get_comment(
            self.original_network.comments, "mt.survey.survey_id"
        ).value
        c2 = self.converter.get_comment(
            self.test_network.comments, "mt.survey.survey_id"
        ).value
        self.assertEqual(c1, c2)

    def test_comment_project(self):
        c1 = self.converter.get_comment(
            self.original_network.comments, "mt.survey.project"
        ).value
        c2 = self.converter.get_comment(
            self.test_network.comments, "mt.survey.project"
        ).value
        self.assertEqual(c1, c2)

    def test_comment_journal_doi(self):
        c1 = self.converter.get_comment(
            self.original_network.comments, "mt.survey.citation_journal.doi"
        ).value
        c2 = self.converter.get_comment(
            self.test_network.comments, "mt.survey.citation_journal.doi"
        ).value
        self.assertEqual(c1, c2)

    def test_comment_acquired_by(self):
        c1 = self.converter.get_comment(
            self.original_network.comments, "mt.survey.acquired_by.author"
        ).value
        c2 = self.converter.get_comment(
            self.test_network.comments, "mt.survey.acquired_by.author"
        ).value
        self.assertEqual(c1, c2)

        c1 = self.converter.get_comment(
            self.original_network.comments, "mt.survey.acquired_by.comments"
        ).value
        c2 = self.converter.get_comment(
            self.test_network.comments, "mt.survey.acquired_by.comments"
        ).value
        self.assertEqual(c1, c2)

    def test_comment_geographic_name(self):
        c1 = self.converter.get_comment(
            self.original_network.comments, "mt.survey.geographic_name"
        ).value
        c2 = self.converter.get_comment(
            self.test_network.comments, "mt.survey.geographic_name"
        ).value
        self.assertEqual(c1, c2)

    def test_description(self):
        self.assertEqual(
            self.original_network.description, self.test_network.description
        )

    def test_restricted_access(self):
        self.assertEqual(
            self.original_network.restricted_status, self.test_network.restricted_status
        )


# =============================================================================
#     Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
