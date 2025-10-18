# -*- coding: utf-8 -*-
"""
Tests for the Survey class in mt_metadata.timeseries

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT
"""

import json
from collections import OrderedDict
from operator import itemgetter

import pandas as pd
import pytest

from mt_metadata.common.mttime import MDate
from mt_metadata.timeseries import Station, Survey


@pytest.fixture(scope="module")
def survey_dict():
    """Create a dictionary with survey metadata."""
    meta_dict = {
        "survey": {
            "acquired_by.comments": "tired",
            "acquired_by.author": "MT",
            "id": "MT001",
            "fdsn.network": "EM",
            "citation_dataset.doi": "https://doi.org/####",
            "comments": "comments",
            "country": ["Canada"],
            "datum": "WGS 84",
            "funding_source.name": ["NSF"],
            "funding_source.organization": ["US governement"],
            "funding_source.grant_id": ["a345"],
            "geographic_name": "earth",
            "name": "entire survey of the earth",
            "northwest_corner.elevation": 0.0,
            "northwest_corner.latitude": 80.0,
            "northwest_corner.longitude": 179.9,
            "project": "EM-EARTH",
            "project_lead.email": "mt@mt.org",
            "project_lead.author": "T. Lurric",
            "project_lead.organization": "mt rules",
            "release_license": "CC-BY-1.0",
            "southeast_corner.elevation": 0.0,
            "southeast_corner.latitude": -80.0,
            "southeast_corner.longitude": -179.9,
            "state": ["Manitoba"],
            "summary": "Summary paragraph",
            "time_period.end_date": "1980-01-01",
            "time_period.start_date": "2080-01-01",
        }
    }

    meta_dict = {
        "survey": OrderedDict(sorted(meta_dict["survey"].items(), key=itemgetter(0)))
    }
    return meta_dict


@pytest.fixture
def survey_object():
    """Create a Survey object for testing."""
    return Survey()


@pytest.fixture(scope="module")
def station_01():
    """Create a first station for testing."""
    station = Station()
    station.location.latitude = 40.0
    station.location.longitude = -120
    station.id = "mt01"
    station.time_period.start = "2023-01-01T00:00:00"
    station.time_period.end = "2023-01-03T00:00:00"
    return station


@pytest.fixture(scope="module")
def station_02():
    """Create a second station for testing."""
    station = Station()
    station.location.latitude = 35.0
    station.location.longitude = -115
    station.id = "mt02"
    station.time_period.start = "2023-01-03T00:00:00"
    station.time_period.end = "2023-01-06T00:00:00"
    return station


@pytest.fixture
def survey_with_stations(station_01, station_02):
    """Create a survey with stations for testing."""
    survey = Survey(id="test")
    survey.add_station(station_01)
    survey.add_station(station_02)
    return survey


def test_in_out_dict(survey_object, survey_dict, subtests):
    """Test conversion from dict to Survey object and back to dict."""
    with subtests.test("dictionary conversion"):
        survey_object.from_dict(survey_dict)
        assert survey_dict == survey_object.to_dict()


def test_in_out_series(survey_object, survey_dict, subtests):
    """Test conversion from pandas Series to Survey object and back to dict."""
    survey_series = pd.Series(survey_dict["survey"])

    with subtests.test("series conversion"):
        survey_object.from_series(survey_series)
        assert survey_dict == survey_object.to_dict()


def test_in_out_json(survey_object, survey_dict, subtests):
    """Test conversion from JSON to Survey object and back."""
    with subtests.test("JSON Dumps"):
        survey_json = json.dumps(survey_dict)
        survey_object.from_json(survey_json)
        assert survey_dict == survey_object.to_dict()

    with subtests.test("json to dict"):
        survey_json = survey_object.to_json(nested=True)
        survey_object.from_json(survey_json)
        assert survey_dict == survey_object.to_dict()


def test_start_date(survey_object, subtests):
    """Test start date handling."""
    with subtests.test("input date"):
        survey_object.time_period.start_date = "2020/01/02"
        assert survey_object.time_period.start_date == "2020-01-02"

    with subtests.test("Input datetime"):
        survey_object.start_date = "01-02-2020T12:20:30.450000+00:00"
        assert survey_object.time_period.start_date == "2020-01-02"


def test_end_date(survey_object, subtests):
    """Test end date handling."""
    with subtests.test("input date"):
        survey_object.time_period.end_date = "2020/01/02"
        assert survey_object.time_period.end_date == "2020-01-02"

    with subtests.test("Input datetime"):
        survey_object.end_date = "01-02-2020T12:20:30.45Z"
        assert survey_object.time_period.end_date == "2020-01-02"


def test_latitude(survey_object, subtests):
    """Test latitude conversion."""
    with subtests.test("string to decimal degrees"):
        survey_object.southeast_corner.latitude = "40:10:05.123"
        assert (
            pytest.approx(survey_object.southeast_corner.latitude, abs=1e-5)
            == 40.1680897
        )


def test_longitude(survey_object, subtests):
    """Test longitude conversion."""
    with subtests.test("string to decimal degrees"):
        survey_object.southeast_corner.longitude = "-115:34:24.9786"
        assert (
            pytest.approx(survey_object.southeast_corner.longitude, abs=1e-5)
            == -115.57361
        )


def test_funding_source(survey_object, subtests):
    """Test funding source handling."""
    with subtests.test("name"):
        survey_object.funding_source.name = "NSF"
        assert survey_object.funding_source.name == ["NSF"]

    with subtests.test("organization"):
        survey_object.funding_source.organization = "US governement, DOE"
        assert survey_object.funding_source.organization == ["US governement", "DOE"]

    with subtests.test("grant_id"):
        survey_object.funding_source.grant_id = "a345"
        assert survey_object.funding_source.grant_id == ["a345"]


def test_geographic_location(survey_object, subtests):
    """Test geographic location handling."""
    with subtests.test("country"):
        survey_object.country = "Canada"
        assert survey_object.country == ["Canada"]

    with subtests.test("state"):
        survey_object.state = "Manitoba, Saskatchewan"
        assert survey_object.state == ["Manitoba", "Saskatchewan"]


def test_acquired_by(survey_object, survey_dict, subtests):
    """Test acquired_by handling."""
    with subtests.test("name is set correctly"):
        survey_object.from_dict(survey_dict)
        assert survey_object.acquired_by.author == "MT"


def test_add_station(survey_object, subtests):
    """Test adding a station to the survey."""
    survey_object.add_station(Station(id="one"))

    with subtests.test("length"):
        assert len(survey_object.stations) == 1

    with subtests.test("station names"):
        assert survey_object.station_names == ["one"]

    with subtests.test("has station"):
        assert survey_object.has_station("one") is True

    with subtests.test("index"):
        assert survey_object.station_index("one") == 0


def test_add_stations_fail(survey_object, subtests):
    """Test adding invalid stations."""
    with subtests.test("adding non-Station raises TypeError"):
        with pytest.raises(TypeError):
            survey_object.add_station(10)


def test_get_station(survey_object, subtests):
    """Test getting a station from the survey."""
    with subtests.test("get existing station"):
        input_station = Station(id="one")
        survey_object.add_station(input_station)
        s = survey_object.get_station("one")
        assert input_station == s


def test_set_stations_fail(survey_object, subtests):
    """Test setting invalid stations."""
    with subtests.test("integer input"):
        with pytest.raises(TypeError):
            survey_object.stations = 10

    with subtests.test("bad object"):
        with pytest.raises(TypeError):
            survey_object.stations = [Station(), Survey()]


def test_add_surveys(survey_object, subtests):
    """Test merging surveys."""
    survey_02 = Survey()
    survey_02.stations.append(Station(id="two"))
    survey_object.stations.append(Station(id="one"))
    survey_object.merge(survey_02)

    with subtests.test("length"):
        assert survey_object.n_stations == 2

    with subtests.test("compare list"):
        assert survey_object.station_names == ["one", "two"]


def test_remove_station(survey_object, subtests):
    """Test removing a station from the survey."""
    with subtests.test("remove existing station"):
        survey_object.stations.append(Station(id="one"))
        survey_object.remove_station("one")
        assert survey_object.station_names == []


def test_update_time_period(survey_object, subtests):
    """Test updating the time period from stations."""
    s = Station(id="001")
    s.time_period.start = "2020-01-01T00:00:00"
    s.time_period.end = "2020-12-01T12:12:12"
    survey_object.add_station(s)
    survey_object.update_time_period()

    with subtests.test("Test new start"):
        assert survey_object.time_period.start_date == "2020-01-01"

    with subtests.test("Test new end"):
        assert survey_object.time_period.end_date == "2020-12-01"


def test_time_period_with_stations(
    survey_with_stations, station_01, station_02, subtests
):
    """Test time period with multiple stations."""
    with subtests.test("start"):
        assert MDate(time_stamp=survey_with_stations.time_period.start_date) == MDate(
            time_stamp=station_01.time_period.start
        )

    with subtests.test("end"):
        assert MDate(time_stamp=survey_with_stations.time_period.end_date) == MDate(
            time_stamp=station_02.time_period.end
        )


def test_bounding_box_with_stations(
    survey_with_stations, station_01, station_02, subtests
):
    """Test bounding box with multiple stations."""
    with subtests.test("northwest corner latitude"):
        assert (
            station_01.location.latitude
            == survey_with_stations.northwest_corner.latitude
        )

    with subtests.test("northwest corner longitude"):
        assert (
            station_01.location.longitude
            == survey_with_stations.northwest_corner.longitude
        )

    with subtests.test("southeast corner latitude"):
        assert (
            station_02.location.latitude
            == survey_with_stations.southeast_corner.latitude
        )

    with subtests.test("southeast corner longitude"):
        assert (
            station_02.location.longitude
            == survey_with_stations.southeast_corner.longitude
        )


def test_station_list_with_stations(
    survey_with_stations, station_01, station_02, subtests
):
    """Test station list with multiple stations."""
    with subtests.test("station names"):
        assert survey_with_stations.station_names == [station_01.id, station_02.id]


def test_remove_station_with_stations(survey_with_stations, station_01, subtests):
    """Test removing a station from a survey with multiple stations."""
    with subtests.test("remove station"):
        survey_with_stations.remove_station("mt02")
        assert survey_with_stations.station_names == [station_01.id]


def test_in_out_dict(survey_object, survey_dict, subtests):
    """Test conversion from dict to Survey object and back to dict."""
    with subtests.test("dict round trip"):
        survey_object.from_dict(survey_dict)
        assert survey_dict == survey_object.to_dict()


def test_in_out_series(survey_object, survey_dict, subtests):
    """Test conversion from pandas Series to Survey object and back to dict."""
    with subtests.test("series round trip"):
        survey_series = pd.Series(survey_dict["survey"])
        survey_object.from_series(survey_series)
        assert survey_dict == survey_object.to_dict()


def test_in_out_json(survey_object, survey_dict, subtests):
    """Test conversion from JSON to Survey object and back."""
    with subtests.test("JSON dumps"):
        survey_json = json.dumps(survey_dict)
        survey_object.from_json(survey_json)
        assert survey_dict == survey_object.to_dict()

    with subtests.test("JSON to dict"):
        survey_json = survey_object.to_json(nested=True)
        survey_object.from_json(survey_json)
        assert survey_dict == survey_object.to_dict()


def test_initialization(subtests):
    """Test initialization of Survey object."""
    with subtests.test("default initialization"):
        survey = Survey()
        assert isinstance(survey, Survey)

    with subtests.test("initialization with id"):
        survey = Survey(id="TEST")
        assert survey.id == "TEST"


def test_in_out_dict(survey_object, survey_dict, subtests):
    """Test conversion from dict to Survey object and back to dict."""
    survey_object.from_dict(survey_dict)

    with subtests.test("dict conversion matches input"):
        assert survey_dict == survey_object.to_dict()

    with subtests.test("id value is set correctly"):
        assert survey_object.id == survey_dict["survey"]["id"]

    with subtests.test("name is set correctly"):
        assert survey_object.name == survey_dict["survey"]["name"]


def test_in_out_series(survey_object, survey_dict, subtests):
    """Test conversion from pandas Series to Survey object and back to dict."""
    survey_series = pd.Series(survey_dict["survey"])
    survey_object.from_series(survey_series)

    with subtests.test("series conversion matches original dict"):
        assert survey_dict == survey_object.to_dict()

    with subtests.test("to_series produces correct output"):
        output_series = survey_object.to_series()
        assert isinstance(output_series, pd.Series)

        # Compare series values individually for better test diagnostics
        for key in survey_series.index:
            with subtests.test(f"series key: {key}"):
                # Handle np.nan values which don't compare equal with ==
                if pd.isna(survey_series[key]) and pd.isna(output_series[key]):
                    assert True
                else:
                    assert survey_series[key] == output_series[key]


def test_in_out_json(survey_object, survey_dict, subtests):
    """Test conversion from JSON to Survey object and back."""
    survey_json = json.dumps(survey_dict)
    survey_object.from_json(survey_json)

    with subtests.test("JSON imports correctly"):
        assert survey_dict == survey_object.to_dict()

    with subtests.test("to_json produces valid JSON"):
        json_output = survey_object.to_json(nested=True)
        assert isinstance(json_output, str)

    with subtests.test("JSON roundtrip preserves data"):
        json_output = survey_object.to_json(nested=True)
        test_survey = Survey()
        test_survey.from_json(json_output)
        assert test_survey.to_dict() == survey_object.to_dict()


def test_time_period(survey_object, survey_dict, subtests):
    """Test the time period properties."""
    survey_object.from_dict(survey_dict)

    with subtests.test("start_date is set correctly"):
        assert (
            survey_object.time_period.start_date
            == survey_dict["survey"]["time_period.start_date"]
        )

    with subtests.test("end_date is set correctly"):
        assert (
            survey_object.time_period.end_date
            == survey_dict["survey"]["time_period.end_date"]
        )


def test_station_management(survey_with_stations, station_01, station_02, subtests):
    """Test station management methods."""
    with subtests.test("stations list contains both stations"):
        assert len(survey_with_stations.stations) == 2

    with subtests.test("station IDs are correct"):
        station_ids = [station.id for station in survey_with_stations.stations]
        assert "mt01" in station_ids
        assert "mt02" in station_ids

    with subtests.test("get_station returns correct station"):
        retrieved_station = survey_with_stations.get_station("mt01")
        assert retrieved_station.id == "mt01"

    with subtests.test("get_station returns None for non-existent station"):
        retrieved_station = survey_with_stations.get_station("non_existent")
        assert retrieved_station is None

    with subtests.test("has_station returns True for existing station"):
        assert survey_with_stations.has_station("mt01") is True

    with subtests.test("has_station returns False for non-existent station"):
        assert survey_with_stations.has_station("non_existent") is False

    # Test station removal
    survey_with_stations.remove_station("mt01")

    with subtests.test("station is removed correctly"):
        assert len(survey_with_stations.stations) == 1
        assert survey_with_stations.has_station("mt01") is False
        assert survey_with_stations.has_station("mt02") is True


def test_geographic_extent(survey_with_stations, subtests):
    """Test geographic extent methods."""
    with subtests.test("survey_extent returns correct bounds"):
        extent = survey_with_stations.survey_extent
        assert extent["longitude"]["min"] == -120  # min longitude
        assert extent["latitude"]["min"] == 35.0  # min latitude
        assert extent["longitude"]["max"] == -115  # max longitude
        assert extent["latitude"]["max"] == 40.0  # max latitude

    with subtests.test("northwest_corner correct values"):
        assert survey_with_stations.northwest_corner.latitude == 40.0
        assert survey_with_stations.northwest_corner.longitude == -120

    with subtests.test("southeast_corner correct values"):
        assert survey_with_stations.southeast_corner.latitude == 35.0
        assert survey_with_stations.southeast_corner.longitude == -115


def test_time_extent(survey_with_stations, subtests):
    """Test time extent methods."""
    with subtests.test("time_period start is earliest station"):
        # time_period should be set from stations
        assert survey_with_stations.time_period.start_date == "2023-01-01"

    with subtests.test("time_period end is latest station"):
        assert survey_with_stations.time_period.end_date == "2023-01-06"


def test_repr_and_str(survey_with_stations, subtests):
    """Test string representation methods."""
    with subtests.test("__repr__ returns non-empty string"):
        repr_str = repr(survey_with_stations)
        assert isinstance(repr_str, str)
        assert len(repr_str) > 0

    with subtests.test("__str__ returns non-empty string"):
        str_output = str(survey_with_stations)
        assert isinstance(str_output, str)
        assert len(str_output) > 0


def test_survey_update(survey_object, survey_dict, subtests):
    """Test updating survey with new values."""
    survey_object.from_dict(survey_dict)

    with subtests.test("update_attribute changes value"):
        survey_object.update_attribute("name", "New Survey Name")
        assert survey_object.name == "New Survey Name"

    with subtests.test("update_attribute works with nested attributes"):
        survey_object.update_attribute("project_lead.author", "New Lead Name")
        assert survey_object.project_lead.author == "New Lead Name"


# TODO: Uncomment figure out if this is the correct test.
# def test_validation(survey_object, subtests):
#     """Test validation methods."""
#     # Set required fields
#     with subtests.test("valid survey passes validation"):
#         # For Pydantic v2
#         result = survey_object.model_validate(survey_object.model_dump())
#         assert isinstance(result, Survey)
