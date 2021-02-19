# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 11:58:11 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

import unittest

from obspy import read_inventory
from mt_metadata.timeseries.stationxml import XMLStationMTStation
from tests import STATIONXML_01, STATIONXML_02


class TestNetwork01(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_01.as_posix())
        self.xml_station = self.inventory.networks[0].stations[0]

        self.converter = XMLStationMTStation()
        self.mt_station, self.run_comments = self.converter.xml_to_mt(self.xml_station)

    def test_time_period(self):
        self.assertEqual(self.mt_station.time_period.start, "2020-06-02T18:41:43+00:00")
        self.assertEqual(self.mt_station.time_period.end, "2020-07-13T21:46:12+00:00")

    def test_code(self):
        self.assertEqual(self.mt_station.fdsn.id, "CAS04")
        self.assertEqual(self.mt_station.id, "CAS04")
    
    def test_location(self):
        self.assertEqual(self.mt_station.location.latitude, 37.633351)
        self.assertEqual(self.mt_station.location.longitude, -121.468382)
        self.assertEqual(self.mt_station.location.elevation, 329.3875)
        
    def test_geographic_name(self):
        self.assertEqual(self.mt_station.geographic_name, "Corral Hollow, CA, USA")
        
    def test_run_comments(self):
        self.assertEqual(self.run_comments, [])

class TestNetwork02(unittest.TestCase):
    """
    Test reading network into MT mt_station object
    """

    def setUp(self):
        self.inventory = read_inventory(STATIONXML_02.as_posix())
        self.xml_station = self.inventory.networks[0].stations[0]

        self.converter = XMLStationMTStation()
        self.mt_station, self.run_comments = self.converter.xml_to_mt(self.xml_station)

    def test_time_period(self):
        self.assertEqual(self.mt_station.time_period.start, "2020-06-08T22:57:13+00:00")
        self.assertEqual(self.mt_station.time_period.end, "2020-07-17T21:15:32+00:00")

    def test_code(self):
        self.assertEqual(self.mt_station.fdsn.id, "REW09")
        self.assertEqual(self.mt_station.id, "REW09")
    
    def test_location(self):
        self.assertEqual(self.mt_station.location.latitude, 35.1469128125)
        self.assertEqual(self.mt_station.location.longitude, -117.160798541667)
        self.assertEqual(self.mt_station.location.elevation, 887.775)
        
    def test_geographic_name(self):
        self.assertEqual(self.mt_station.geographic_name, "Opal Mountain, CA, USA")
         
    def test_provenance(self):
        self.assertEqual(self.mt_station.provenance.software.author,
                         "Anna Kelbert, USGS")
        self.assertEqual(self.mt_station.provenance.software.name,
                         "mth5_metadata.m")
        self.assertEqual(self.mt_station.provenance.software.version,
                         "2021-02-01")
        
    def test_declination(self):
        self.assertEqual(self.mt_station.location.declination.value, -666)
        self.assertEqual(self.mt_station.location.declination.model, "IGRF-13")
        self.assertEqual(self.mt_station.location.declination.comments,
                         "igrf.m by Drew Compston")
        
    def test_orientation(self):
        self.assertEqual(self.mt_station.orientation.method, "compass")
        self.assertEqual(self.mt_station.orientation.reference_frame, "geographic")
        
    def test_run_list(self):
        self.assertEqual(self.mt_station.run_list, ["a", "b", "c", "d", "e"])
        
    def test_data_type(self):
        self.assertEqual(self.mt_station.data_type, "MT")
        
    def test_run_comments(self):
        self.assertNotEqual(self.run_comments, [])



# class Testmt_stationToNetwork(unittest.TestCase):
#     """
#     Test converting a network to a mt_station
#     """

#     def setUp(self):
#         self.inventory = read_inventory(STATIONXML_02.as_posix())
#         self.original_network = self.inventory.networks[0]

#         self.converter = xml_network_mt_mt_station.XMLNetworkMTmt_station()
#         self.mt_station = self.converter.xml_to_mt(self.original_network)
#         self.test_network = self.converter.mt_to_xml(self.mt_station)

#     def test_time_period(self):
#         self.assertEqual(self.test_network.start_date, self.original_network.start_date)
#         self.assertEqual(self.test_network.end_date, self.original_network.end_date)

#     def test_comment_mt_station_id(self):
#         c1 = self.converter.get_comment(
#             self.original_network.comments, "mt.mt_station.mt_station_id"
#         ).value
#         c2 = self.converter.get_comment(
#             self.test_network.comments, "mt.mt_station.mt_station_id"
#         ).value
#         self.assertEqual(c1, c2)

#     def test_comment_project(self):
#         c1 = self.converter.get_comment(
#             self.original_network.comments, "mt.mt_station.project"
#         ).value
#         c2 = self.converter.get_comment(
#             self.test_network.comments, "mt.mt_station.project"
#         ).value
#         self.assertEqual(c1, c2)

#     def test_comment_journal_doi(self):
#         c1 = self.converter.get_comment(
#             self.original_network.comments, "mt.mt_station.citation_journal.doi"
#         ).value
#         c2 = self.converter.get_comment(
#             self.test_network.comments, "mt.mt_station.citation_journal.doi"
#         ).value
#         self.assertEqual(c1, c2)

#     def test_comment_acquired_by(self):
#         c1 = self.converter.get_comment(
#             self.original_network.comments, "mt.mt_station.acquired_by.author"
#         ).value
#         c2 = self.converter.get_comment(
#             self.test_network.comments, "mt.mt_station.acquired_by.author"
#         ).value
#         self.assertEqual(c1, c2)

#         c1 = self.converter.get_comment(
#             self.original_network.comments, "mt.mt_station.acquired_by.comments"
#         ).value
#         c2 = self.converter.get_comment(
#             self.test_network.comments, "mt.mt_station.acquired_by.comments"
#         ).value
#         self.assertEqual(c1, c2)

#     def test_comment_geographic_name(self):
#         c1 = self.converter.get_comment(
#             self.original_network.comments, "mt.mt_station.geographic_name"
#         ).value
#         c2 = self.converter.get_comment(
#             self.test_network.comments, "mt.mt_station.geographic_name"
#         ).value
#         self.assertEqual(c1, c2)

#     def test_description(self):
#         self.assertEqual(
#             self.original_network.description, self.test_network.description
#         )

#     def test_restricted_access(self):
#         self.assertEqual(
#             self.original_network.restricted_status, self.test_network.restricted_status
#         )


# =============================================================================
#     Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
