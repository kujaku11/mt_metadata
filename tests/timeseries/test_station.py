import pytest
import json
import pandas as pd
from collections import OrderedDict
from mt_metadata.timeseries.station_basemodel import Station
from mt_metadata.timeseries.run_basemodel import Run


@pytest.fixture
def station_object():
    """Fixture to create a fresh Station object."""
    return Station()


@pytest.fixture
def meta_dict():
    """Fixture to provide metadata for testing."""
    return OrderedDict(
        [
            ("acquired_by.author", "name"),
            ("channels_recorded", ["ex", "ey", "hx", "hy", "hz"]),
            ("comments", "comments"),
            ("data_type", "BBMT"),
            ("geographic_name", "here"),
            ("id", "mt01"),
            ("location.declination.epoch", "2019"),
            ("location.declination.model", "WMM"),
            ("location.declination.value", 10.0),
            ("location.elevation", 400.0),
            ("location.latitude", 40.0),
            ("location.longitude", -120.0),
            ("orientation.angle_to_geographic_north", 0.0),
            ("orientation.method", "compass"),
            ("orientation.reference_frame", "geographic"),
            ("provenance.archive.comments", "failed"),
            ("provenance.archive.email", "email@email.com"),
            ("provenance.archive.name", "archive name"),
            ("provenance.archive.organization", "archive org"),
            ("provenance.creation_time", "1980-01-01T00:00:00+00:00"),
            ("provenance.creator.author", "author"),
            ("provenance.creator.comments", "data comments"),
            ("provenance.creator.email", "email@email.com"),
            ("provenance.creator.organization", "org"),
            ("provenance.software.author", "author"),
            ("provenance.software.last_updated", "1980-01-01T00:00:00+00:00"),
            ("provenance.software.name", "mt_metadata"),
            ("provenance.software.version", "0.2.12"),
            ("provenance.submitter.author", "author"),
            ("provenance.submitter.comments", "data comments"),
            ("provenance.submitter.email", "email@email.com"),
            ("release_license", "CC0-1.0"),
            ("run_list", ["001"]),
            ("time_period.end", "2020-01-02T12:20:40.456000+00:00"),
            ("time_period.start", "2020-01-02T12:20:40.456000+00:00"),
        ]
    )


def test_in_out_dict(station_object, meta_dict, subtests):
    """Test Station object with dictionary input and output."""
    station_object.from_dict(meta_dict)
    for key, value_og in meta_dict.items():
        with subtests.test(key):
            value_s = station_object.get_attr_from_name(key)
            assert value_og == value_s


def test_in_out_series(station_object, meta_dict, subtests):
    """Test Station object with pandas Series input and output."""
    station_series = pd.Series(meta_dict)
    station_object.from_series(station_series)
    for key, value_og in meta_dict.items():
        with subtests.test(key):
            value_s = station_object.get_attr_from_name(key)
            assert value_og == value_s


def test_in_out_json(station_object, meta_dict, subtests):
    """Test Station object with JSON input and output."""
    station_json = json.dumps(meta_dict)
    station_object.from_json(station_json)
    for key, value_og in meta_dict.items():
        with subtests.test(key):
            value_s = station_object.get_attr_from_name(key)
            assert value_og == value_s


def test_start(station_object, subtests):
    """Test setting the start time."""
    station_object.time_period.start = "2020/01/02T12:20:40.4560Z"
    with subtests.test("ISO format with Z"):
        assert station_object.time_period.start == "2020-01-02T12:20:40.456000+00:00"

    station_object.time_period.start = "01/02/20T12:20:40.4560"
    with subtests.test("Mixed format"):
        assert station_object.time_period.start == "2020-01-02T12:20:40.456000+00:00"


def test_end_date(station_object, subtests):
    """Test setting the end time."""
    station_object.time_period.end = "2020/01/02T12:20:40.4560Z"
    with subtests.test("ISO format with Z"):
        assert station_object.time_period.end == "2020-01-02T12:20:40.456000+00:00"

    station_object.time_period.end = "01/02/20T12:20:40.4560"
    with subtests.test("Mixed format"):
        assert station_object.time_period.end == "2020-01-02T12:20:40.456000+00:00"


def test_latitude(station_object):
    """Test setting latitude."""
    station_object.location.latitude = "40:10:05.123"
    assert round(station_object.location.latitude, 5) == 40.16809


def test_longitude(station_object):
    """Test setting longitude."""
    station_object.location.longitude = "-115:34:24.9786"
    assert round(station_object.location.longitude, 5) == -115.57361


def test_declination(station_object):
    """Test setting declination."""
    station_object.location.declination.value = "10.980"
    assert station_object.location.declination.value == 10.980


def test_set_runs_from_list(station_object, subtests):
    """Test setting runs from a list."""
    station_object.runs = [Run(id="one")]
    with subtests.test("Length"):
        assert station_object.n_runs == 1
    with subtests.test("Run list"):
        assert station_object.run_list == ["one"]


def test_set_runs_from_dict(station_object, subtests):
    """Test setting runs from a dictionary."""
    station_object.runs = {"one": Run(id="one")}
    with subtests.test("Length"):
        assert station_object.n_runs == 1
    with subtests.test("Run list"):
        assert station_object.run_list == ["one"]


def test_set_runs_fail(station_object, subtests):
    """Test invalid run assignments."""
    with subtests.test("Fail from input int"):
        with pytest.raises(TypeError):
            station_object.runs = 10

    with subtests.test("Fail from input list"):
        with pytest.raises(TypeError):
            station_object.runs = [Run(), Station()]


def test_add_runs(station_object, subtests):
    """Test adding runs to the Station object."""
    station_02 = Station()
    station_02.runs.append(Run(id="two"))
    station_object.runs.append(Run(id="one"))

    station_object.merge(station_02)
    with subtests.test("Length"):
        assert station_object.n_runs == 2
    with subtests.test("Run list"):
        assert station_object.run_list == ["one", "two"]


def test_remove_runs(station_object):
    """Test removing runs from the Station object."""
    station_object.runs.append(Run(id="one"))
    station_object.remove_run("one")
    assert station_object.run_list == []


def test_update_time_period(station_object, subtests):
    """Test updating the time period based on runs."""
    r = Run(id="001")
    r.time_period.start = "2020-01-01T00:00:00"
    r.time_period.end = "2020-12-01T12:12:12"
    station_object.add_run(r)

    with subtests.test("Start time"):
        assert station_object.time_period.start == "2020-01-01T00:00:00+00:00"

    with subtests.test("End time"):
        assert station_object.time_period.end == "2020-12-01T12:12:12+00:00"


def test_channels_recorded(station_object, subtests):
    """Test setting and validating channels recorded."""
    with subtests.test("Full channels"):
        station_object.channels_recorded = ["Ex", "Ey", "Hx", "Hy"]
        assert station_object.channels_recorded == ["Ex", "Ey", "Hx", "Hy"]

    with subtests.test("Comma-separated string"):
        station_object.channels_recorded = "Ex, Ey, Hx, Hy"
        assert station_object.channels_recorded == ["Ex", "Ey", "Hx", "Hy"]

    with subtests.test("Empty list"):
        station_object.channels_recorded = []
        assert station_object.channels_recorded == []
