# -*- coding: utf-8 -*-
"""
Tests for mt_metadata.transfer_functions.tf.Station basemodel
===========================================================

This module contains comprehensive pytest tests for the transfer function Station class.
The Station class inherits from the timeseries Station but adds transfer function metadata.
Tests cover data serialization, time period handling, coordinate validation, and transfer function integration.

"""

import json
from collections import OrderedDict

import pandas as pd
import pytest

from mt_metadata.timeseries import Run
from mt_metadata.transfer_functions.tf import Station
from mt_metadata.transfer_functions.tf.transfer_function import TransferFunction


class TestStationBasic:
    """Basic Station functionality tests."""

    @classmethod
    def setup_class(cls):
        """Set up class-level test data."""
        cls.base_meta_dict = OrderedDict(
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
                # Transfer function specific fields
                ("transfer_function.coordinate_system", "geographic"),
                ("transfer_function.data_quality.comments", "crushed it"),
                ("transfer_function.data_quality.flag", None),
                ("transfer_function.data_quality.good_from_period", 0.01),
                ("transfer_function.data_quality.good_to_period", 1000),
                ("transfer_function.data_quality.rating.author", "author"),
                ("transfer_function.data_quality.rating.method", "eye ball"),
                ("transfer_function.data_quality.rating.value", 5),
                ("transfer_function.data_quality.warnings", "60 hz"),
                ("transfer_function.id", "mt01_sr100"),
                ("transfer_function.processed_by.author", "name"),
                ("transfer_function.processed_by.comments", "took time"),
                ("transfer_function.processed_by.email", "email@email.com"),
                ("transfer_function.processed_date", "2023-01-01"),
                ("transfer_function.processing_parameters", ["aurora.id=tf_01"]),
                ("transfer_function.processing_type", "robust remote reference"),
                ("transfer_function.remote_references", ["mtrr"]),
                ("transfer_function.runs_processed", ["001"]),
                ("transfer_function.sign_convention", "exp(+ i\\omega t)"),
            ]
        )

    @pytest.fixture
    def station_object(self):
        """Fixture to create a fresh Station object."""
        return Station()

    @pytest.fixture
    def meta_dict(self):
        """Fixture to provide metadata for testing."""
        return self.base_meta_dict.copy()

    def test_station_creation(self, station_object):
        """Test basic Station object creation."""
        assert isinstance(station_object, Station)
        assert hasattr(station_object, "transfer_function")
        assert isinstance(station_object.transfer_function, TransferFunction)

    def test_transfer_function_default(self, station_object):
        """Test that transfer function has proper default value."""
        assert station_object.transfer_function is not None
        assert isinstance(station_object.transfer_function, TransferFunction)

    def test_inheritance_from_timeseries_station(self, station_object):
        """Test that Station properly inherits from timeseries Station."""
        # Should have timeseries Station attributes
        assert hasattr(station_object, "id")
        assert hasattr(station_object, "location")
        assert hasattr(station_object, "time_period")
        assert hasattr(station_object, "runs")

        # Plus the additional transfer_function attribute
        assert hasattr(station_object, "transfer_function")


class TestStationSerialization:
    """Test Station serialization and deserialization."""

    @classmethod
    def setup_class(cls):
        """Set up class-level test data."""
        cls.base_meta_dict = OrderedDict(
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
                # Transfer function specific fields
                ("transfer_function.coordinate_system", "geographic"),
                ("transfer_function.data_quality.comments", "crushed it"),
                ("transfer_function.data_quality.flag", None),
                ("transfer_function.data_quality.good_from_period", 0.01),
                ("transfer_function.data_quality.good_to_period", 1000),
                ("transfer_function.data_quality.rating.author", "author"),
                ("transfer_function.data_quality.rating.method", "eye ball"),
                ("transfer_function.data_quality.rating.value", 5),
                ("transfer_function.data_quality.warnings", "60 hz"),
                ("transfer_function.id", "mt01_sr100"),
                ("transfer_function.processed_by.author", "name"),
                ("transfer_function.processed_by.comments", "took time"),
                ("transfer_function.processed_by.email", "email@email.com"),
                ("transfer_function.processed_date", "2023-01-01"),
                ("transfer_function.processing_parameters", ["aurora.id=tf_01"]),
                ("transfer_function.processing_type", "robust remote reference"),
                ("transfer_function.remote_references", ["mtrr"]),
                ("transfer_function.runs_processed", ["001"]),
                ("transfer_function.sign_convention", "exp(+ i\\omega t)"),
            ]
        )

    @pytest.fixture
    def station_object(self):
        """Fixture to create a fresh Station object."""
        return Station()

    @pytest.fixture
    def meta_dict(self):
        """Fixture to provide metadata for testing."""
        return self.base_meta_dict.copy()

    def test_in_out_dict(self, station_object, meta_dict, subtests):
        """Test Station object with dictionary input and output."""
        station_object.from_dict(meta_dict)
        for key, value_og in meta_dict.items():
            with subtests.test(key=key):
                value_s = station_object.get_attr_from_name(key)
                assert value_og == value_s

    def test_in_out_series(self, station_object, meta_dict, subtests):
        """Test Station object with pandas Series input and output."""
        station_series = pd.Series(meta_dict)
        station_object.from_series(station_series)
        for key, value_og in meta_dict.items():
            with subtests.test(key=key):
                value_s = station_object.get_attr_from_name(key)
                assert value_og == value_s

    def test_in_out_json(self, station_object, meta_dict, subtests):
        """Test Station object with JSON input and output."""
        station_json = json.dumps(meta_dict)
        station_object.from_json(station_json)
        for key, value_og in meta_dict.items():
            with subtests.test(key=key):
                value_s = station_object.get_attr_from_name(key)
                assert value_og == value_s

    def test_to_dict_round_trip(self, station_object, meta_dict):
        """Test that to_dict and from_dict are symmetric."""
        station_object.from_dict(meta_dict)
        output_dict = station_object.to_dict(single=True)

        # Create new station and load from output
        station_2 = Station()
        station_2.from_dict(output_dict)

        # Compare key attributes
        assert station_object.id == station_2.id
        assert station_object.transfer_function.id == station_2.transfer_function.id
        assert station_object.location.latitude == station_2.location.latitude


class TestStationTimePeriod:
    """Test Station time period handling."""

    @pytest.fixture
    def station_object(self):
        """Fixture to create a fresh Station object."""
        return Station()

    def test_start_time_formats(self, station_object, subtests):
        """Test setting the start time in various formats."""
        with subtests.test("ISO format with Z"):
            station_object.time_period.start = "2020/01/02T12:20:40.4560Z"
            assert (
                station_object.time_period.start == "2020-01-02T12:20:40.456000+00:00"
            )

        with subtests.test("Mixed format"):
            station_object.time_period.start = "01/02/20T12:20:40.4560"
            assert (
                station_object.time_period.start == "2020-01-02T12:20:40.456000+00:00"
            )

    def test_end_time_formats(self, station_object, subtests):
        """Test setting the end time in various formats."""
        with subtests.test("ISO format with Z"):
            station_object.time_period.end = "2020/01/02T12:20:40.4560Z"
            assert station_object.time_period.end == "2020-01-02T12:20:40.456000+00:00"

        with subtests.test("Mixed format"):
            station_object.time_period.end = "01/02/20T12:20:40.4560"
            assert station_object.time_period.end == "2020-01-02T12:20:40.456000+00:00"

    def test_update_time_period_from_runs(self, station_object, subtests):
        """Test updating the time period based on runs."""
        run = Run(id="001")
        run.time_period.start = "2020-01-01T00:00:00"
        run.time_period.end = "2020-12-01T12:12:12"
        station_object.add_run(run)

        with subtests.test("Start time"):
            assert station_object.time_period.start == "2020-01-01T00:00:00+00:00"

        with subtests.test("End time"):
            assert station_object.time_period.end == "2020-12-01T12:12:12+00:00"


class TestStationLocation:
    """Test Station location and coordinate handling."""

    @pytest.fixture
    def station_object(self):
        """Fixture to create a fresh Station object."""
        return Station()

    def test_latitude_formats(self, station_object, subtests):
        """Test setting latitude in various formats."""
        with subtests.test("Decimal degrees"):
            station_object.location.latitude = 40.16809
            assert round(station_object.location.latitude, 5) == 40.16809

        with subtests.test("Degrees:minutes:seconds"):
            station_object.location.latitude = "40:10:05.123"
            assert round(station_object.location.latitude, 5) == 40.16809

    def test_longitude_formats(self, station_object, subtests):
        """Test setting longitude in various formats."""
        with subtests.test("Decimal degrees"):
            station_object.location.longitude = -115.57361
            assert round(station_object.location.longitude, 5) == -115.57361

        with subtests.test("Degrees:minutes:seconds"):
            station_object.location.longitude = "-115:34:24.9786"
            assert round(station_object.location.longitude, 5) == -115.57361

    def test_declination_setting(self, station_object):
        """Test setting declination value."""
        station_object.location.declination.value = "10.980"
        assert station_object.location.declination.value == 10.980

    def test_elevation_setting(self, station_object):
        """Test setting elevation."""
        station_object.location.elevation = 1500.0
        assert station_object.location.elevation == 1500.0


class TestStationRuns:
    """Test Station run management."""

    @pytest.fixture
    def station_object(self):
        """Fixture to create a fresh Station object."""
        return Station()

    @pytest.fixture
    def populated_station(self):
        """Fixture to create a Station object with pre-populated runs."""
        station = Station()
        station.add_run(Run(id="001"))
        station.add_run(Run(id="002"))
        return station

    def test_add_run(self, station_object, subtests):
        """Test adding runs to the Station object."""
        run = Run(id="001")
        station_object.add_run(run)

        with subtests.test("Run added"):
            assert station_object.run_list == ["001"]

        with subtests.test("Number of runs"):
            assert station_object.n_runs == 1

    def test_set_runs_from_list(self, station_object, subtests):
        """Test setting runs from a list."""
        station_object.runs = [Run(id="one")]
        with subtests.test("Length"):
            assert station_object.n_runs == 1
        with subtests.test("Run list"):
            assert station_object.run_list == ["one"]

    def test_set_runs_from_dict(self, station_object, subtests):
        """Test setting runs from a dictionary."""
        station_object.runs = {"one": Run(id="one")}
        with subtests.test("Length"):
            assert station_object.n_runs == 1
        with subtests.test("Run list"):
            assert station_object.run_list == ["one"]

    def test_remove_run(self, populated_station, subtests):
        """Test removing runs from the Station object."""
        populated_station.remove_run("001")

        with subtests.test("Run removed"):
            assert "001" not in populated_station.run_list

        with subtests.test("Remaining runs"):
            assert populated_station.run_list == ["002"]

    def test_set_runs_fail(self, station_object, subtests):
        """Test invalid run assignments."""
        with subtests.test("Invalid input type (int)"):
            with pytest.raises(TypeError):
                station_object.runs = 10

        with subtests.test("Invalid input type (mixed list)"):
            with pytest.raises(TypeError):
                station_object.runs = [Run(), Station()]


class TestStationChannels:
    """Test Station channel handling."""

    @pytest.fixture
    def station_object(self):
        """Fixture to create a fresh Station object."""
        return Station()

    def test_channels_recorded_list(self, station_object, subtests):
        """Test setting channels recorded from list."""
        with subtests.test("Valid list of channels"):
            station_object.channels_recorded = ["Ex", "Ey", "Hx", "Hy"]
            assert station_object.channels_recorded == ["Ex", "Ey", "Hx", "Hy"]

        with subtests.test("Empty list"):
            station_object.channels_recorded = []
            assert station_object.channels_recorded == []

    def test_channels_recorded_string(self, station_object):
        """Test setting channels recorded from comma-separated string."""
        station_object.channels_recorded = "Ex, Ey, Hx, Hy"
        assert station_object.channels_recorded == ["Ex", "Ey", "Hx", "Hy"]

    def test_channels_recorded_validation(self, station_object):
        """Test validation of channels recorded."""
        with pytest.raises(TypeError):
            station_object.channels_recorded = True


class TestStationTransferFunction:
    """Test Station transfer function specific functionality."""

    @pytest.fixture
    def station_object(self):
        """Fixture to create a fresh Station object."""
        return Station()

    def test_transfer_function_access(self, station_object):
        """Test that transfer function is accessible."""
        assert hasattr(station_object, "transfer_function")
        assert isinstance(station_object.transfer_function, TransferFunction)

    def test_transfer_function_id_setting(self, station_object):
        """Test setting transfer function ID."""
        station_object.transfer_function.id = "mt01_sr100"
        assert station_object.transfer_function.id == "mt01_sr100"

    def test_transfer_function_coordinate_system(self, station_object, subtests):
        """Test setting coordinate system."""
        with subtests.test("Geographic coordinate system"):
            station_object.transfer_function.coordinate_system = "geographic"
            assert station_object.transfer_function.coordinate_system == "geographic"

        with subtests.test("Geomagnetic coordinate system"):
            station_object.transfer_function.coordinate_system = "geomagnetic"
            assert station_object.transfer_function.coordinate_system == "geomagnetic"

    def test_transfer_function_processing_info(self, station_object, subtests):
        """Test transfer function processing information."""
        with subtests.test("Processing type"):
            station_object.transfer_function.processing_type = "robust remote reference"
            assert (
                station_object.transfer_function.processing_type
                == "robust remote reference"
            )

        with subtests.test("Processed by"):
            station_object.transfer_function.processed_by.author = "test_author"
            assert station_object.transfer_function.processed_by.author == "test_author"

        with subtests.test("Processing date"):
            station_object.transfer_function.processed_date = "2023-01-01"
            assert station_object.transfer_function.processed_date == "2023-01-01"

    def test_transfer_function_data_quality(self, station_object, subtests):
        """Test transfer function data quality parameters."""
        with subtests.test("Good period range"):
            station_object.transfer_function.data_quality.good_from_period = 0.01
            station_object.transfer_function.data_quality.good_to_period = 1000
            assert (
                station_object.transfer_function.data_quality.good_from_period == 0.01
            )
            assert station_object.transfer_function.data_quality.good_to_period == 1000

        with subtests.test("Quality rating"):
            station_object.transfer_function.data_quality.rating.value = 5
            station_object.transfer_function.data_quality.rating.method = "eye ball"
            assert station_object.transfer_function.data_quality.rating.value == 5
            assert (
                station_object.transfer_function.data_quality.rating.method
                == "eye ball"
            )

        with subtests.test("Comments and warnings"):
            station_object.transfer_function.data_quality.comments = "excellent data"
            station_object.transfer_function.data_quality.warnings = "60 hz noise"
            assert (
                station_object.transfer_function.data_quality.comments
                == "excellent data"
            )
            assert (
                station_object.transfer_function.data_quality.warnings == "60 hz noise"
            )

    def test_runs_processed(self, station_object):
        """Test setting runs processed in transfer function."""
        station_object.transfer_function.runs_processed = ["001", "002"]
        assert station_object.transfer_function.runs_processed == ["001", "002"]

    def test_remote_references(self, station_object):
        """Test setting remote references."""
        station_object.transfer_function.remote_references = ["ref1", "ref2"]
        assert station_object.transfer_function.remote_references == ["ref1", "ref2"]

    def test_sign_convention(self, station_object):
        """Test setting sign convention."""
        station_object.transfer_function.sign_convention = "exp(+ i\\omega t)"
        assert station_object.transfer_function.sign_convention == "exp(+ i\\omega t)"


class TestStationMerge:
    """Test Station merge functionality."""

    @pytest.fixture
    def station_object(self):
        """Fixture to create a fresh Station object."""
        return Station()

    @pytest.fixture
    def populated_station(self):
        """Fixture to create a Station object with pre-populated runs."""
        station = Station()
        station.add_run(Run(id="001"))
        station.add_run(Run(id="002"))
        return station

    def test_merge_stations(self, station_object, populated_station, subtests):
        """Test merging two Station objects."""
        station_object.add_run(Run(id="003"))
        station_object.merge(populated_station)

        with subtests.test("Number of runs after merge"):
            assert station_object.n_runs == 3

        with subtests.test("Run list after merge"):
            assert sorted(station_object.run_list) == ["001", "002", "003"]


class TestStationValidation:
    """Test Station validation and error handling."""

    @pytest.fixture
    def station_object(self):
        """Fixture to create a fresh Station object."""
        return Station()

    def test_invalid_data_types(self, station_object, subtests):
        """Test that invalid data types are properly rejected."""
        with subtests.test("Invalid elevation type"):
            with pytest.raises((TypeError, ValueError)):
                station_object.location.elevation = "not_a_number"

        with subtests.test("Invalid coordinates"):
            with pytest.raises((TypeError, ValueError)):
                station_object.location.latitude = "invalid_coord"

    def test_required_fields(self, station_object):
        """Test that station can be created with minimal required fields."""
        station_object.id = "test_station"
        assert station_object.id == "test_station"

        # Transfer function should have default
        assert station_object.transfer_function is not None


if __name__ == "__main__":
    pytest.main([__file__])
