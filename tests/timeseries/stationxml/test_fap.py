# -*- coding: utf-8 -*-
"""

Test FAP tables

"""
import unittest
import numpy as np
from obspy.core import inventory

from mt_metadata.timeseries.filters import FrequencyResponseTableFilter
from mt_metadata.timeseries.stationxml import XMLInventoryMTExperiment
from mt_metadata.utils import STATIONXML_FAP
from mt_metadata.timeseries.filters.obspy_stages import create_filter_from_stage


class TestFAPFilter(unittest.TestCase):
    """
    Test filter translation from :class:`obspy.inventory.Network
    """

    def setUp(self):
        self.inventory = inventory.read_inventory(STATIONXML_FAP.as_posix())
        self.fir_stage = (
            self.inventory.networks[0].stations[0].channels[0].response.response_stages[0]
        )
        self.instrument_sensitivity = (
            self.inventory.networks[0]
            .stations[0]
            .channels[0]
            .response.instrument_sensitivity
        )
        self.fir = create_filter_from_stage(self.fir_stage)
        
    def test_is_fap_instance(self):
        self.assertIsInstance(self.fir, FrequencyResponseTableFilter)
        
    def test_amplitudes(self):
        self.assertTrue(np.all(np.isclose(self.fir_stage.amplitudes, 
                                   self.fir.amplitudes) == True))
        
    def test_phases(self):
        self.assertTrue(np.all(np.isclose(self.fir_stage.phases, 
                                   self.fir.phases) == True))
        
    def test_frequencies(self):
        self.assertTrue(np.all(np.isclose(self.fir_stage.frequencies, 
                                   self.fir.frequencies) == True))
        
    def test_units_in(self):
        self.assertTrue(self.fir_stage.input_units, self.fir.units_in)
        
    def test_units_out(self):
        self.assertTrue(self.fir_stage.output_units, self.fir.units_out)
        
    def test_comments(self):
        self.assertTrue(self.fir_stage.description, self.fir.comments)
        
    def test_gain(self):
        self.assertTrue(self.fir_stage.stage_gain, self.fir.gain)
        

class TestFAPTranslation(unittest.TestCase):
    """
    Test the translation of a FAP table from stationXML -> MTXML -> StationXML
    """
    
    def setUp(self):
        self.translator = XMLInventoryMTExperiment()
        
        self.inventory = inventory.read_inventory(STATIONXML_FAP.as_posix())
        
        self.experiment = self.translator.xml_to_mt(self.inventory)
        
    def test_has_surveys(self):
        self.assertEqual(len(self.inventory.networks), len(self.experiment.surveys))
        self.assertEqual(self.inventory.networks[0].code, 
                         self.experiment.surveys[0].fdsn.network)
        
    def test_has_stations(self):
        self.assertEqual(len(self.inventory.networks[0].stations),
                         len(self.experiment.surveys[0].stations))
        self.assertEqual(self.inventory.networks[0].stations[0].code, 
                         self.experiment.surveys[0].stations[0].fdsn.id)
        
        
    def test_has_channels(self):
        self.assertEqual(len(self.inventory.networks[0].stations[0].channels),
                         len(self.experiment.surveys[0].stations[0].runs[0].channels))
        
    def test_has_filters(self):
        self.assertIn("frequency response table_00", 
                      self.experiment.surveys[0].filters.keys())
        
        self.assertIn("v to counts (electric)", 
                      self.experiment.surveys[0].filters.keys())
    
        
        
    
        
        

        
        
    
    

