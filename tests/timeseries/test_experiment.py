# -*- coding: utf-8 -*-
"""
Tests for the Experiment class in mt_metadata.timeseries using pytest

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""

import copy

import pytest

from mt_metadata.timeseries import (
    Auxiliary,
    Electric,
    Experiment,
    Magnetic,
    Run,
    Station,
    Survey,
)
from mt_metadata.utils.mttime import MDate


@pytest.fixture
def experiment():
    """Create a basic empty experiment object."""
    return Experiment()


@pytest.fixture
def sample_survey():
    """Create a sample survey for testing."""
    return Survey(id="test_survey")


@pytest.fixture
def complex_experiment():
    """
    Create a complex experiment object with multiple surveys, stations, runs and channels.
    """
    experiment = Experiment()
    start = "2020-01-01T00:00:00+00:00"
    end = "2021-01-01T12:00:00+00:00"

    kwargs = {"time_period.start": start, "time_period.end": end}

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
                station_obj.add_run(run_obj)
                station_obj.update_time_period()
            survey_obj.add_station(station_obj)
            survey_obj.update_time_period()
        experiment.add_survey(survey_obj)

    return {"experiment": experiment, "start": start, "end": end}


def test_set_surveys(experiment, sample_survey, subtests):
    """Test setting surveys directly."""
    with subtests.test("setting surveys list works"):
        experiment.surveys = [sample_survey]
        assert experiment.n_surveys == 1


def test_set_surveys_fail(experiment, subtests):
    """Test failures when setting invalid surveys."""
    with subtests.test("integer input raises TypeError"):
        with pytest.raises(TypeError):
            experiment.surveys = 10

    with subtests.test("mixed list raises TypeError"):
        with pytest.raises(TypeError):
            experiment.surveys = [Survey(), Station()]


def test_add_survey(experiment, subtests):
    """Test adding a survey to the experiment."""
    survey_input = Survey(id="one")
    experiment.add_survey(survey_input)

    with subtests.test("length"):
        assert experiment.n_surveys == 1

    with subtests.test("survey names"):
        assert experiment.survey_names == ["one"]

    with subtests.test("has survey"):
        assert experiment.has_survey("one") is True

    with subtests.test("index"):
        assert experiment.survey_index("one") == 0


def test_add_survey_fail(experiment, subtests):
    """Test adding an invalid survey."""
    with subtests.test("adding integer raises TypeError"):
        with pytest.raises(TypeError):
            experiment.add_survey(10)


def test_get_survey(experiment, subtests):
    """Test getting a survey from the experiment."""
    with subtests.test("get added survey works"):
        input_survey = Survey(id="one")
        experiment.add_survey(input_survey)
        s = experiment.get_survey("one")
        assert input_survey == s


def test_add_experiments(experiment, subtests):
    """Test merging experiments."""
    ex2 = Experiment(surveys=[Survey(id="two")])
    experiment.surveys.append(Survey(id="one"))
    experiment.merge(ex2)

    with subtests.test("correct length after merge"):
        assert experiment.n_surveys == 2

    with subtests.test("survey names are correct"):
        assert experiment.survey_names == ["one", "two"]


def test_write_xml(complex_experiment, subtests):
    """Test writing experiment to XML and reading it back."""
    experiment = complex_experiment["experiment"]
    experiment_xml = experiment.to_xml(required=True)
    experiment_02 = Experiment()
    experiment_02.from_xml(element=experiment_xml)

    with subtests.test("XML roundtrip preserves data"):
        assert experiment.to_dict(required=True) == experiment_02.to_dict(required=True)


def test_survey_time_period(complex_experiment, subtests):
    """Test survey time period."""
    experiment = complex_experiment["experiment"]
    start = complex_experiment["start"]
    end = complex_experiment["end"]

    with subtests.test("start"):
        assert MDate(time_stamp=start) == experiment.surveys[0].time_period.start_date

    with subtests.test("end"):
        assert (
            MDate(time_stamp=end.split("T")[0])
            == experiment.surveys[0].time_period.end_date
        )


def test_station_time_period(complex_experiment, subtests):
    """Test station time period."""
    experiment = complex_experiment["experiment"]
    start = complex_experiment["start"]
    end = complex_experiment["end"]

    with subtests.test("start"):
        assert start == experiment.surveys[0].stations[0].time_period.start

    with subtests.test("end"):
        assert end == experiment.surveys[0].stations[0].time_period.end


def test_run_time_period(complex_experiment, subtests):
    """Test run time period."""
    experiment = complex_experiment["experiment"]
    start = complex_experiment["start"]
    end = complex_experiment["end"]

    with subtests.test("start"):
        assert start == experiment.surveys[0].stations[0].runs[0].time_period.start

    with subtests.test("end"):
        assert end == experiment.surveys[0].stations[0].runs[0].time_period.end


def test_to_dict(complex_experiment, subtests):
    """Test the to_dict method."""
    experiment = complex_experiment["experiment"]
    d = experiment.to_dict()

    with subtests.test("keys"):
        assert list(d.keys()) == ["experiment"]

    with subtests.test("surveys/stations"):
        assert "stations" in d["experiment"]["surveys"][0].keys()

    with subtests.test("surveys/filters"):
        assert "filters" in d["experiment"]["surveys"][0].keys()

    with subtests.test("n_surveys"):
        assert len(d["experiment"]["surveys"]) == 2

    with subtests.test("runs"):
        assert "runs" in d["experiment"]["surveys"][0]["stations"][0].keys()

    with subtests.test("n_stations"):
        assert len(d["experiment"]["surveys"][0]["stations"]) == 2

    with subtests.test("n_runs"):
        assert len(d["experiment"]["surveys"][0]["stations"][0]["runs"]) == 2

    with subtests.test("n_channels"):
        assert (
            len(d["experiment"]["surveys"][0]["stations"][0]["runs"][0]["channels"])
            == 7
        )


def test_from_dict(complex_experiment, subtests):
    """Test the from_dict method."""
    experiment = complex_experiment["experiment"]
    d = experiment.to_dict()
    ex = Experiment()

    with subtests.test("from_dict loads correctly"):
        ex.from_dict(d, skip_none=False)
        assert ex.to_dict() == d


def test_from_dict_fail(experiment, subtests):
    """Test from_dict with invalid input."""
    with subtests.test("integer input raises TypeError"):
        with pytest.raises(TypeError):
            experiment.from_dict(10)


def test_from_empty_dict(experiment, subtests):
    """Test from_dict with empty dict."""
    with subtests.test("empty dict returns None"):
        assert experiment.from_dict({}) is None


# Additional pytest tests for Experiment
@pytest.fixture(scope="module")
def example_experiment():
    """Create an example experiment with minimal structure."""
    experiment = Experiment(id="EX01")
    survey = Survey(id="SV01")
    station = Station(id="ST01")
    run = Run(id="RN01")

    # Add electric channels
    run.add_channel(Electric(component="ex"))
    run.add_channel(Electric(component="ey"))

    # Add magnetic channels
    run.add_channel(Magnetic(component="hx"))
    run.add_channel(Magnetic(component="hy"))
    run.add_channel(Magnetic(component="hz"))

    # Build the hierarchy
    station.add_run(run)
    survey.add_station(station)
    experiment.add_survey(survey)

    return experiment


def test_experiment_initialization(subtests):
    """Test different ways to initialize an Experiment."""
    with subtests.test("default initialization"):
        exp = Experiment()
        assert isinstance(exp, Experiment)
        assert len(exp.surveys) == 0

    with subtests.test("initialization with id"):
        exp = Experiment(id="TEST01")
        assert exp.id == "TEST01"

    with subtests.test("initialization with kwargs"):
        exp = Experiment(**{"id": "TEST02", "project": "MT Survey 2023"})
        assert exp.id == "TEST02"
        assert exp.project == "MT Survey 2023"


def test_experiment_survey_management(experiment, subtests):
    """Test survey management methods."""
    # Add surveys
    survey1 = Survey(id="survey1")
    survey2 = Survey(id="survey2")

    with subtests.test("add_survey adds survey"):
        experiment.add_survey(survey1)
        assert len(experiment.surveys) == 1

    with subtests.test("has_survey returns True for existing survey"):
        assert experiment.has_survey("survey1") is True

    with subtests.test("has_survey returns False for non-existent survey"):
        assert experiment.has_survey("non_existent") is False

    with subtests.test("get_survey returns correct survey"):
        retrieved_survey = experiment.get_survey("survey1")
        assert retrieved_survey.id == "survey1"

    with subtests.test("survey_names returns correct list"):
        experiment.add_survey(survey2)
        assert sorted(experiment.survey_names) == ["survey1", "survey2"]

    with subtests.test("remove_survey removes survey"):
        experiment.remove_survey("survey1")
        assert "survey1" not in experiment.survey_names
        assert len(experiment.surveys) == 1


# experiment does not have any attributes yet.
# def test_experiment_time_extent(example_experiment, subtests):
#     """Test experiment time extent calculation."""
#     # Set different time periods for stations
#     example_experiment.surveys[0].stations[0].time_period.start = "2020-01-01T00:00:00"
#     example_experiment.surveys[0].stations[0].time_period.end = "2020-12-31T23:59:59"

#     # Add another survey with different time period
#     survey2 = Survey(id="SV02")
#     station2 = Station(id="ST02")
#     station2.time_period.start = "2019-06-01T00:00:00"
#     station2.time_period.end = "2021-06-30T23:59:59"
#     survey2.add_station(station2)
#     example_experiment.add_survey(survey2)

#     # Update time periods
#     example_experiment.update_time_period()

#     with subtests.test("start time is earliest of all stations"):
#         assert example_experiment.time_period.start_date == "2019-06-01"

#     with subtests.test("end time is latest of all stations"):
#         assert example_experiment.time_period.end_date == "2021-06-30"


def test_experiment_to_from_json(example_experiment, subtests):
    """Test conversion to and from JSON."""
    json_str = example_experiment.to_json(nested=True)

    with subtests.test("to_json produces string"):
        assert isinstance(json_str, str)

    new_experiment = Experiment()
    new_experiment.from_json(json_str)

    with subtests.test("from_json preserves data"):
        assert new_experiment.to_dict() == example_experiment.to_dict()

    with subtests.test("channels are preserved"):
        channel_types = [
            ch.type for ch in new_experiment.surveys[0].stations[0].runs[0].channels
        ]
        assert sorted(channel_types) == [
            "electric",
            "electric",
            "magnetic",
            "magnetic",
            "magnetic",
        ]


def test_experiment_copy(example_experiment, subtests):
    """Test copying an experiment."""
    copied = copy.deepcopy(example_experiment)

    with subtests.test("copy is a different object"):
        assert id(copied) != id(example_experiment)

    with subtests.test("copy has same structure"):
        assert copied.to_dict() == example_experiment.to_dict()

    with subtests.test("modifying copy doesn't affect original"):
        copied.id = "MODIFIED"
        assert example_experiment.id != "MODIFIED"


def test_experiment_validation(example_experiment, subtests):
    """Test experiment validation."""
    with subtests.test("valid experiment passes validation"):
        d = example_experiment.to_dict()["experiment"]
        assert example_experiment.model_validate(d) == example_experiment

    with subtests.test("invalid experiment raises appropriate errors"):
        # Create invalid experiment (no required fields)
        invalid_exp = Experiment()
        # Validation should fail or raise error - depending on implementation
        with pytest.raises(TypeError):
            invalid_exp.model_validate(id=None)
