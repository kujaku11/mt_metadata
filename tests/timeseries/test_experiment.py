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
        
    def test_set_surveys(self):
        self.experiment.surveys = [Survey()]
        self.assertEqual(len(self.experiment.surveys), 1)
        
    def test_set_surveys_fail(self):
        def set_surveys(value):
            self.experiment.surveys = value
            
        self.assertRaises(TypeError, set_surveys, 10)
        self.assertRaises(TypeError, set_surveys, [Survey(), Station()])
        
    def test_add_experiments(self):
        ex2 = Experiment([Survey(survey_id="two")])
        self.experiment.surveys.append(Survey(survey_id="one"))
        self.experiment += ex2
        self.assertEqual(len(self.experiment), 2)
        self.assertListEqual(["one", "two"], self.experiment.survey_names)
        
        
# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()