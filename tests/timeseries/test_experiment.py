# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 21:49:13 2021

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
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

from mt_metadata.utils.mttime import MTime, MDate

# =============================================================================


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

    def test_add_survey(self):
        survey_input = Survey(id="one")
        self.experiment.add_survey(survey_input)

        with self.subTest("length"):
            self.assertEqual(len(self.experiment.surveys), 1)

        with self.subTest("staiton names"):
            self.assertListEqual(["one"], self.experiment.survey_names)

        with self.subTest("has station"):
            self.assertTrue(self.experiment.has_survey("one"))

        with self.subTest("index"):
            self.assertEqual(0, self.experiment.survey_index("one"))

    def test_add_survey_fail(self):
        self.assertRaises(TypeError, self.experiment.add_survey, 10)

    def test_get_survey(self):
        input_survey = Survey(id="one")
        self.experiment.add_survey(input_survey)
        s = self.experiment.get_survey("one")
        self.assertTrue(input_survey == s)

    def test_add_experiments(self):
        ex2 = Experiment(surveys=[Survey(id="two")])
        self.experiment.surveys.append(Survey(id="one"))
        self.experiment.merge(ex2)
        with self.subTest(name="length"):
            self.assertEqual(self.experiment.n_surveys, 2)
        with self.subTest(name="name equal"):
            self.assertListEqual(["one", "two"], self.experiment.survey_names)


class TestBuildExperiment(unittest.TestCase):
    """
    build and read an experiment
    """

    @classmethod
    def setUpClass(self):
        self.maxDiff = None
        self.experiment = Experiment()
        self.start = "2020-01-01T00:00:00+00:00"
        self.end = "2021-01-01T12:00:00+00:00"

        kwargs = {"time_period.start": self.start, "time_period.end": self.end}

        for survey in ["One", "Two"]:
            survey_obj = Survey(id=survey, country="USA")
            survey_obj.filters = {}
            for station in ["mt01", "mt02"]:
                station_obj = Station(id=station, **kwargs)
                for run in ["mt01a", "mt01b"]:
                    run_obj = Run(id=run, **kwargs)
                    for ch in ["ex", "ey"]:
                        ch_obj = Electric(component=ch, **kwargs)
                        run_obj.add_channel(ch_obj)
                    for ch in ["hx", "hy", "hz"]:
                        ch_obj = Magnetic(component=ch, **kwargs)
                        run_obj.add_channel(ch_obj)
                    for ch in ["temperature", "voltage"]:
                        ch_obj = Auxiliary(component=ch, **kwargs)
                        run_obj.add_channel(ch_obj)
                    run_obj.update_time_period()
                    station_obj.runs.append(run_obj)
                    station_obj.update_time_period()
                survey_obj.stations.append(station_obj)
                survey_obj.update_time_period()
            self.experiment.surveys.append(survey_obj)

    def test_write_xml(self):
        experiment_xml = self.experiment.to_xml(required=True)
        experiment_02 = Experiment()
        experiment_02.from_xml(element=experiment_xml)

        self.assertDictEqual(self.experiment.to_dict(), experiment_02.to_dict())

    def test_survey_time_period(self):
        with self.subTest("start"):
            self.assertEqual(
                MDate(self.start), self.experiment.surveys[0].time_period.start_date
            )
        with self.subTest("end"):
            self.assertEqual(
                MDate(self.end), self.experiment.surveys[0].time_period.end_date
            )

    def test_station_time_period(self):
        with self.subTest("start"):
            self.assertEqual(
                self.start,
                self.experiment.surveys[0].stations[0].time_period.start,
            )
        with self.subTest("end"):
            self.assertEqual(
                self.end,
                self.experiment.surveys[0].stations[0].time_period.end,
            )

    def test_run_time_period(self):
        with self.subTest("start"):
            self.assertEqual(
                self.start,
                self.experiment.surveys[0].stations[0].runs[0].time_period.start,
            )
        with self.subTest("end"):
            self.assertEqual(
                self.end,
                self.experiment.surveys[0].stations[0].runs[0].time_period.end,
            )

    def test_to_dict(self):
        d = self.experiment.to_dict()

        with self.subTest("keys"):
            self.assertEqual(["experiment"], list(d.keys()))

        with self.subTest("surveys/stations"):
            self.assertIn("stations", d["experiment"]["surveys"][0].keys())

        with self.subTest("surveys/filters"):
            self.assertIn("filters", d["experiment"]["surveys"][0].keys())

        with self.subTest("n_surveys"):
            self.assertEqual(2, len(d["experiment"]["surveys"]))

        with self.subTest("runs"):
            self.assertIn("runs", d["experiment"]["surveys"][0]["stations"][0].keys())
        with self.subTest("n_stations"):
            self.assertEqual(2, len(d["experiment"]["surveys"][0]["stations"]))

        with self.subTest("n_runs"):
            self.assertEqual(
                2, len(d["experiment"]["surveys"][0]["stations"][0]["runs"])
            )

        with self.subTest("n_channels"):
            self.assertEqual(
                7,
                len(
                    d["experiment"]["surveys"][0]["stations"][0]["runs"][0]["channels"]
                ),
            )

    def test_from_dict(self):
        d = self.experiment.to_dict()
        ex = Experiment()
        ex.from_dict(d, skip_none=False)

        self.assertDictEqual(ex.to_dict(), self.experiment.to_dict())

    def test_from_dict_fail(self):
        self.assertRaises(TypeError, self.experiment.from_dict, 10)

    def test_from_empty_dict(self):
        self.assertEqual(None, self.experiment.from_dict({}))


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
