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
        ex2 = Experiment([Survey(id="two")])
        self.experiment.surveys.append(Survey(id="one"))
        self.experiment += ex2
        with self.subTest(name="length"):
            self.assertEqual(len(self.experiment), 2)
        with self.subTest(name="name equal"):
            self.assertListEqual(["one", "two"], self.experiment.survey_names)


class TestBuildExperiment(unittest.TestCase):
    """
    build and read an experiment
    """

    def setUp(self):
        self.experiment = Experiment()
        self.start = "2020-01-01T00:00:00+00:00"
        self.end = "2021-01-01T12:00:00+00:00"
        
        kwargs = {"time_period.start": self.start,
                  "time_period.end": self.end}

        for survey in ["One", "Two"]:
            survey_obj = Survey(survey_id=survey)
            survey_obj.filters = {}
            for station in ["mt01", "mt02"]:
                station_obj = Station(id=station, **kwargs)
                for run in ["mt01a", "mt01b"]:
                    run_obj = Run(id=run, **kwargs)
                    for ch in ["ex", "ey"]:
                        ch_obj = Electric(component=ch, **kwargs)
                        run_obj.channels.append(ch_obj)
                    for ch in ["hx", "hy", "hz"]:
                        ch_obj = Magnetic(component=ch, **kwargs)
                        run_obj.channels.append(ch_obj)
                    for ch in ["temperature", "voltage"]:
                        ch_obj = Auxiliary(component=ch, **kwargs)
                        run_obj.channels.append(ch_obj)

                    run_obj.update_time_period()
                    station_obj.runs.append(run_obj)
                    station_obj.update_time_period()
                survey_obj.stations.append(station_obj)
                survey_obj.update_time_period()

            self.experiment.surveys.append(survey_obj)

    def test_write_xml(self):
        experiment_xml = self.experiment.to_xml(required=False)
        experiment_02 = Experiment()
        experiment_02.from_xml(element=experiment_xml)
        self.assertEqual(self.experiment, experiment_02)
        
    def test_survey_time_period(self):
        with self.subTest("start"):
            self.assertEqual(self.start, self.experiment.surveys[0].time_period.start)
        with self.subTest("end"):
            self.assertEqual(self.end, self.experiment.surveys[0].time_period.end) 
            
    def test_station_time_period(self):
        with self.subTest("start"):
            self.assertEqual(self.start, self.experiment.surveys[0].stations[0].time_period.start)
        with self.subTest("end"):
            self.assertEqual(self.end, self.experiment.surveys[0].stations[0].time_period.end)

    def test_run_time_period(self):
        with self.subTest("start"):
            self.assertEqual(self.start, self.experiment.surveys[0].stations[0].runs[0].time_period.start)
        with self.subTest("end"):
            self.assertEqual(self.end, self.experiment.surveys[0].stations[0].runs[0].time_period.end)

# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
