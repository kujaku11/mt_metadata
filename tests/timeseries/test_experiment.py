# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 21:49:13 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
from pathlib import Path
import unittest

from mt_metadata.timeseries import (
    Auxiliary,
    Electric,
    Magnetic,
    Run,
    Station,
    Survey,
    Experiment,
)


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


class TestBuildExperiment(unittest.TestCase):
    """
    build and read an experiment
    """

    def setUp(self):
        self.experiment = Experiment()

        for survey in ["One", "Two"]:
            survey_obj = Survey(survey_id=survey)
            for station in ["mt01", "mt02"]:
                station_obj = Station(id=station)
                for run in ["mt01a", "mt01b"]:
                    run_obj = Run(id=run)
                    for ch in ["ex", "ey"]:
                        ch_obj = Electric(component=ch)
                        run_obj.channels.append(ch_obj)
                    for ch in ["hx", "hy", "hz"]:
                        ch_obj = Magnetic(component=ch)
                        run_obj.channels.append(ch_obj)
                    for ch in ["temperature", "voltage"]:
                        ch_obj = Auxiliary(component=ch)
                        run_obj.channels.append(ch_obj)

                    station_obj.runs.append(run_obj)
                survey_obj.stations.append(station_obj)

            self.experiment.surveys.append(survey_obj)

    def test_write_xml(self):
        experiment_xml = self.experiment.to_xml(required=False)
        experiment_02 = Experiment()
        experiment_02.from_xml(element=experiment_xml)
        self.assertEqual(self.experiment, experiment_02)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
