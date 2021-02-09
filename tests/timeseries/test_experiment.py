# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 21:49:13 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

import unittest
from mt_metadata.timeseries import Survey
from mt_metadata.timeseries import Station
from mt_metadata.timeseries.experiment import Experiment

class TestExperiment(unittest.TestCase):
    """
    test Experiment
    """
    
    def setUp(self):
        self.experiment = Experiment()
        
    def test_set_survey_list(self):
        self.experiment.survey_list = [Survey()]
        self.assertEqual(len(self.experiment.survey_list), 1)
        
    def test_set_survey_list_fail(self):
        def set_survey_list(value):
            self.experiment.survey_list = value
            
        self.assertRaises(TypeError, set_survey_list, 10)
        self.assertRaises(TypeError, set_survey_list, [Survey(), Station()])
        
    def test_add_experiments(self):
        ex2 = Experiment([Survey(survey_id="two")])
        self.experiment.survey_list.append(Survey(survey_id="one"))
        self.experiment += ex2
        self.assertEqual(len(self.experiment), 2)
        self.assertListEqual(["one", "two"], self.experiment.survey_names)
        
        
# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()