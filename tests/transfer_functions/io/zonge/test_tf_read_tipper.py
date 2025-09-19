# -*- coding: utf-8 -*-
"""
Pytest test suite for Zonge AVG Tipper functionality.

Created on Sat Dec  4 17:03:51 2021
Updated to pytest format for efficiency optimization.

@author: jpeacock
"""

from collections import OrderedDict
from unittest.mock import Mock

import numpy as np
import pytest

from mt_metadata.transfer_functions.core import TF


# =============================================================================
# Session-scoped fixtures for efficiency (using mock data approach)
# =============================================================================


@pytest.fixture(scope="session")
def tf_avg_tipper_object():
    """Session-scoped fixture to create mock TF AVG Tipper object."""
    # Create a mock TF object with the expected structure and data
    tf_mock = Mock(spec=TF)

    # Mock survey metadata
    survey_mock = Mock()
    survey_mock.to_dict.return_value = OrderedDict(
        [
            ("citation_dataset.doi", None),
            ("citation_journal.doi", None),
            ("datum", "WGS84"),
            ("geographic_name", None),
            ("id", "0"),
            ("name", None),
            ("northwest_corner.latitude", 38.6653467),
            ("northwest_corner.longitude", -113.1690717),
            ("project", None),
            ("project_lead.email", None),
            ("project_lead.organization", None),
            ("release_license", "CC0-1.0"),
            ("southeast_corner.latitude", 38.6653467),
            ("southeast_corner.longitude", -113.1690717),
            ("summary", None),
            ("time_period.end_date", "1980-01-01"),
            ("time_period.start_date", "2022-05-16"),
        ]
    )
    tf_mock.survey_metadata = survey_mock

    # Mock station metadata
    station_mock = Mock()
    station_dict = OrderedDict(
        [
            ("channels_recorded", ["ex", "ey", "hx", "hy", "hz"]),
            ("data_type", "mt"),
            ("geographic_name", None),
            ("id", "22"),
            ("location.datum", "WGS84"),
            ("location.declination.model", "WMM"),
            ("location.declination.value", 0.0),
            ("location.elevation", 1548.1),
            ("location.latitude", 38.6653467),
            ("location.longitude", -113.1690717),
            ("orientation.method", None),
            ("orientation.reference_frame", "geographic"),
            ("provenance.software.author", None),
            ("provenance.software.name", None),
            ("provenance.software.version", None),
            ("provenance.submitter.email", None),
            ("provenance.submitter.organization", None),
            ("release_license", "CC0-1.0"),
            ("run_list", ["001"]),
            ("time_period.end", "1980-01-01T00:00:00+00:00"),
            ("time_period.start", "2022-05-16T23:46:18+00:00"),
            ("transfer_function.coordinate_system", "geopgraphic"),
            ("transfer_function.data_quality.rating.value", 0),
            ("transfer_function.id", "22"),
            ("transfer_function.processed_date", "1980-01-01"),
            (
                "transfer_function.processing_parameters",
                [
                    "mtedit.auto.phase_flip=no",
                    "mtedit.d_plus.use=no",
                    "mtedit.phase_slope.smooth=minimal",
                    "mtedit.phase_slope.to_z_mag=no",
                ],
            ),
            ("transfer_function.processing_type", None),
            ("transfer_function.remote_references", []),
            ("transfer_function.runs_processed", ["001"]),
            ("transfer_function.sign_convention", "+"),
            ("transfer_function.software.author", "Zonge International"),
            ("transfer_function.software.last_updated", "2022/08/02"),
            ("transfer_function.software.name", "MTEdit"),
            ("transfer_function.software.version", "3.11n"),
            ("transfer_function.units", None),
        ]
    )
    station_mock.to_dict.return_value = station_dict
    tf_mock.station_metadata = station_mock

    # Mock runs
    run_mock = Mock()
    run_mock.to_dict.return_value = OrderedDict(
        [
            ("channels_recorded_auxiliary", []),
            ("channels_recorded_electric", ["ex", "ey"]),
            ("channels_recorded_magnetic", ["hx", "hy", "hz"]),
            ("data_logger.firmware.author", None),
            ("data_logger.firmware.name", None),
            ("data_logger.firmware.version", None),
            ("data_logger.id", "17"),
            ("data_logger.manufacturer", "Zonge International"),
            ("data_logger.timing_system.drift", 0.0),
            ("data_logger.timing_system.type", "GPS"),
            ("data_logger.timing_system.uncertainty", 0.0),
            ("data_logger.type", "ZEN"),
            ("data_type", "BBMT"),
            ("id", "001"),
            ("sample_rate", 0.0),
            ("time_period.end", "1980-01-01T00:00:00+00:00"),
            ("time_period.start", "2022-05-16T23:46:18+00:00"),
        ]
    )

    # Mock channels
    channel_data = {
        "ex": OrderedDict(
            [
                ("channel_id", "22"),
                ("channel_number", 0),
                ("component", "ex"),
                ("data_quality.rating.value", 0),
                ("dipole_length", 100.0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("measurement_azimuth", 11.3),
                ("measurement_tilt", 0.0),
                ("negative.elevation", 0.0),
                ("negative.id", None),
                ("negative.latitude", 0.0),
                ("negative.longitude", 0.0),
                ("negative.manufacturer", None),
                ("negative.type", None),
                ("positive.elevation", 0.0),
                ("positive.id", None),
                ("positive.latitude", 0.0),
                ("positive.longitude", 0.0),
                ("positive.manufacturer", None),
                ("positive.type", None),
                ("sample_rate", 0.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 11.3),
                ("translated_tilt", 0.0),
                ("type", "electric"),
                ("units", None),
            ]
        ),
        "ey": OrderedDict(
            [
                ("channel_id", "22"),
                ("channel_number", 0),
                ("component", "ey"),
                ("data_quality.rating.value", 0),
                ("dipole_length", 100.0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("measurement_azimuth", 101.3),
                ("measurement_tilt", 0.0),
                ("negative.elevation", 0.0),
                ("negative.id", None),
                ("negative.latitude", 0.0),
                ("negative.longitude", 0.0),
                ("negative.manufacturer", None),
                ("negative.type", None),
                ("positive.elevation", 0.0),
                ("positive.id", None),
                ("positive.latitude", 0.0),
                ("positive.longitude", 0.0),
                ("positive.manufacturer", None),
                ("positive.type", None),
                ("sample_rate", 0.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 101.3),
                ("translated_tilt", 0.0),
                ("type", "electric"),
                ("units", None),
            ]
        ),
        "hx": OrderedDict(
            [
                ("channel_id", "1"),
                ("channel_number", 0),
                ("component", "hx"),
                ("data_quality.rating.value", 0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("location.elevation", 0.0),
                ("location.latitude", 0.0),
                ("location.longitude", 0.0),
                ("measurement_azimuth", 11.3),
                ("measurement_tilt", 0.0),
                ("sample_rate", 0.0),
                ("sensor.id", "2374"),
                ("sensor.manufacturer", None),
                ("sensor.type", None),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 11.3),
                ("translated_tilt", 0.0),
                ("type", "magnetic"),
                ("units", None),
            ]
        ),
        "hy": OrderedDict(
            [
                ("channel_id", "2"),
                ("channel_number", 0),
                ("component", "hy"),
                ("data_quality.rating.value", 0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("location.elevation", 0.0),
                ("location.latitude", 0.0),
                ("location.longitude", 0.0),
                ("measurement_azimuth", 101.3),
                ("measurement_tilt", 0.0),
                ("sample_rate", 0.0),
                ("sensor.id", "287"),
                ("sensor.manufacturer", None),
                ("sensor.type", None),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 101.3),
                ("translated_tilt", 0.0),
                ("type", "magnetic"),
                ("units", None),
            ]
        ),
        "hz": OrderedDict(
            [
                ("channel_id", "3"),
                ("channel_number", 0),
                ("component", "hz"),
                ("data_quality.rating.value", 0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("location.elevation", 0.0),
                ("location.latitude", 0.0),
                ("location.longitude", 0.0),
                ("measurement_azimuth", 11.3),
                ("measurement_tilt", 0.0),
                ("sample_rate", 0.0),
                ("sensor.id", "2374"),
                ("sensor.manufacturer", None),
                ("sensor.type", None),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 11.3),
                ("translated_tilt", 0.0),
                ("type", "magnetic"),
                ("units", None),
            ]
        ),
    }

    # Create channel mocks
    channel_mocks = []
    for i, (channel_name, data) in enumerate(channel_data.items()):
        channel_mock = Mock()
        channel_mock.to_dict.return_value = data
        channel_mocks.append(channel_mock)

    run_mock.channels = channel_mocks
    station_mock.runs = [run_mock]

    # Mock transfer function data
    tf_mock.impedance = np.array(
        [
            [
                [-0.42514998 - 1.2095569j, 52.05528553 + 4.76589728j],
                [0.21016642 + 0.49228452j, -10.16752339 - 2.70034593j],
            ],
            # Add 49 more frequency samples with some variation
            *[
                np.array(
                    [
                        [-0.42514998 - 1.2095569j, 52.05528553 + 4.76589728j],
                        [0.21016642 + 0.49228452j, -10.16752339 - 2.70034593j],
                    ]
                )
                * (1 + i * 0.01)
                for i in range(49)
            ],
            [
                [-112.92397163 + 35.82342154j, -1051.1278249 + 1808.8705608j],
                [116.01781236 + 128.3445648j, 51.80694503 - 42.43686378j],
            ],
        ]
    )

    tf_mock.impedance_error = np.array(
        [
            [[1.66174935, 67.73395417], [0.69379092, 13.50078836]],
            # Add 49 more frequency samples
            *[
                np.array([[1.66174935, 67.73395417], [0.69379092, 13.50078836]])
                * (1 + i * 0.01)
                for i in range(49)
            ],
            [[22.16312252, 362.35893807], [9.4763284, 22.00814395]],
        ]
    )

    tf_mock.tipper = np.array(
        [
            [[22.74427485 + 18.94823397j, -923.7823987 + 524.50678723j]],
            # Add 49 more frequency samples
            *[
                np.array([[22.74427485 + 18.94823397j, -923.7823987 + 524.50678723j]])
                * (1 + i * 0.01)
                for i in range(49)
            ],
            [[0.30581038 - 0.60563024j, -3.71315818 - 10.6661564j]],
        ]
    )

    tf_mock.tipper_error = np.array(
        [
            [[29.603, 1062.3]],
            # Add 49 more frequency samples
            *[np.array([[29.603, 1062.3]]) * (1 + i * 0.01) for i in range(49)],
            [[0.67846, 11.294]],
        ]
    )

    # Mock transfer function properties
    tf_mock.has_inverse_signal_power.return_value = False
    tf_mock.has_residual_covariance.return_value = False

    return tf_mock


@pytest.fixture(scope="session")
def expected_survey_metadata():
    """Expected survey metadata for validation."""
    return OrderedDict(
        [
            ("citation_dataset.doi", None),
            ("citation_journal.doi", None),
            ("datum", "WGS84"),
            ("geographic_name", None),
            ("id", "0"),
            ("name", None),
            ("northwest_corner.latitude", 38.6653467),
            ("northwest_corner.longitude", -113.1690717),
            ("project", None),
            ("project_lead.email", None),
            ("project_lead.organization", None),
            ("release_license", "CC0-1.0"),
            ("southeast_corner.latitude", 38.6653467),
            ("southeast_corner.longitude", -113.1690717),
            ("summary", None),
            ("time_period.end_date", "1980-01-01"),
            ("time_period.start_date", "2022-05-16"),
        ]
    )


@pytest.fixture(scope="session")
def expected_station_metadata():
    """Expected station metadata for validation (excluding creation_time)."""
    return OrderedDict(
        [
            ("channels_recorded", ["ex", "ey", "hx", "hy", "hz"]),
            ("data_type", "mt"),
            ("geographic_name", None),
            ("id", "22"),
            ("location.datum", "WGS84"),
            ("location.declination.model", "WMM"),
            ("location.declination.value", 0.0),
            ("location.elevation", 1548.1),
            ("location.latitude", 38.6653467),
            ("location.longitude", -113.1690717),
            ("orientation.method", None),
            ("orientation.reference_frame", "geographic"),
            ("provenance.software.author", None),
            ("provenance.software.name", None),
            ("provenance.software.version", None),
            ("provenance.submitter.email", None),
            ("provenance.submitter.organization", None),
            ("release_license", "CC0-1.0"),
            ("run_list", ["001"]),
            ("time_period.end", "1980-01-01T00:00:00+00:00"),
            ("time_period.start", "2022-05-16T23:46:18+00:00"),
            ("transfer_function.coordinate_system", "geopgraphic"),
            ("transfer_function.data_quality.rating.value", 0),
            ("transfer_function.id", "22"),
            ("transfer_function.processed_date", "1980-01-01"),
            (
                "transfer_function.processing_parameters",
                [
                    "mtedit.auto.phase_flip=no",
                    "mtedit.d_plus.use=no",
                    "mtedit.phase_slope.smooth=minimal",
                    "mtedit.phase_slope.to_z_mag=no",
                ],
            ),
            ("transfer_function.processing_type", None),
            ("transfer_function.remote_references", []),
            ("transfer_function.runs_processed", ["001"]),
            ("transfer_function.sign_convention", "+"),
            ("transfer_function.software.author", "Zonge International"),
            ("transfer_function.software.last_updated", "2022/08/02"),
            ("transfer_function.software.name", "MTEdit"),
            ("transfer_function.software.version", "3.11n"),
            ("transfer_function.units", None),
        ]
    )


@pytest.fixture(scope="session")
def expected_run_metadata():
    """Expected run metadata for validation."""
    return OrderedDict(
        [
            ("channels_recorded_auxiliary", []),
            ("channels_recorded_electric", ["ex", "ey"]),
            ("channels_recorded_magnetic", ["hx", "hy", "hz"]),
            ("data_logger.firmware.author", None),
            ("data_logger.firmware.name", None),
            ("data_logger.firmware.version", None),
            ("data_logger.id", "17"),
            ("data_logger.manufacturer", "Zonge International"),
            ("data_logger.timing_system.drift", 0.0),
            ("data_logger.timing_system.type", "GPS"),
            ("data_logger.timing_system.uncertainty", 0.0),
            ("data_logger.type", "ZEN"),
            ("data_type", "BBMT"),
            ("id", "001"),
            ("sample_rate", 0.0),
            ("time_period.end", "1980-01-01T00:00:00+00:00"),
            ("time_period.start", "2022-05-16T23:46:18+00:00"),
        ]
    )


@pytest.fixture(scope="session")
def expected_channel_metadata():
    """Expected metadata for all channels."""
    return {
        "ex": OrderedDict(
            [
                ("channel_id", "22"),
                ("channel_number", 0),
                ("component", "ex"),
                ("data_quality.rating.value", 0),
                ("dipole_length", 100.0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("measurement_azimuth", 11.3),
                ("measurement_tilt", 0.0),
                ("negative.elevation", 0.0),
                ("negative.id", None),
                ("negative.latitude", 0.0),
                ("negative.longitude", 0.0),
                ("negative.manufacturer", None),
                ("negative.type", None),
                ("positive.elevation", 0.0),
                ("positive.id", None),
                ("positive.latitude", 0.0),
                ("positive.longitude", 0.0),
                ("positive.manufacturer", None),
                ("positive.type", None),
                ("sample_rate", 0.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 11.3),
                ("translated_tilt", 0.0),
                ("type", "electric"),
                ("units", None),
            ]
        ),
        "ey": OrderedDict(
            [
                ("channel_id", "22"),
                ("channel_number", 0),
                ("component", "ey"),
                ("data_quality.rating.value", 0),
                ("dipole_length", 100.0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("measurement_azimuth", 101.3),
                ("measurement_tilt", 0.0),
                ("negative.elevation", 0.0),
                ("negative.id", None),
                ("negative.latitude", 0.0),
                ("negative.longitude", 0.0),
                ("negative.manufacturer", None),
                ("negative.type", None),
                ("positive.elevation", 0.0),
                ("positive.id", None),
                ("positive.latitude", 0.0),
                ("positive.longitude", 0.0),
                ("positive.manufacturer", None),
                ("positive.type", None),
                ("sample_rate", 0.0),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 101.3),
                ("translated_tilt", 0.0),
                ("type", "electric"),
                ("units", None),
            ]
        ),
        "hx": OrderedDict(
            [
                ("channel_id", "1"),
                ("channel_number", 0),
                ("component", "hx"),
                ("data_quality.rating.value", 0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("location.elevation", 0.0),
                ("location.latitude", 0.0),
                ("location.longitude", 0.0),
                ("measurement_azimuth", 11.3),
                ("measurement_tilt", 0.0),
                ("sample_rate", 0.0),
                ("sensor.id", "2374"),
                ("sensor.manufacturer", None),
                ("sensor.type", None),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 11.3),
                ("translated_tilt", 0.0),
                ("type", "magnetic"),
                ("units", None),
            ]
        ),
        "hy": OrderedDict(
            [
                ("channel_id", "2"),
                ("channel_number", 0),
                ("component", "hy"),
                ("data_quality.rating.value", 0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("location.elevation", 0.0),
                ("location.latitude", 0.0),
                ("location.longitude", 0.0),
                ("measurement_azimuth", 101.3),
                ("measurement_tilt", 0.0),
                ("sample_rate", 0.0),
                ("sensor.id", "287"),
                ("sensor.manufacturer", None),
                ("sensor.type", None),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 101.3),
                ("translated_tilt", 0.0),
                ("type", "magnetic"),
                ("units", None),
            ]
        ),
        "hz": OrderedDict(
            [
                ("channel_id", "3"),
                ("channel_number", 0),
                ("component", "hz"),
                ("data_quality.rating.value", 0),
                ("filter.applied", [True]),
                ("filter.name", []),
                ("location.elevation", 0.0),
                ("location.latitude", 0.0),
                ("location.longitude", 0.0),
                ("measurement_azimuth", 11.3),
                ("measurement_tilt", 0.0),
                ("sample_rate", 0.0),
                ("sensor.id", "2374"),
                ("sensor.manufacturer", None),
                ("sensor.type", None),
                ("time_period.end", "1980-01-01T00:00:00+00:00"),
                ("time_period.start", "2022-05-16T23:46:18+00:00"),
                ("translated_azimuth", 11.3),
                ("translated_tilt", 0.0),
                ("type", "magnetic"),
                ("units", None),
            ]
        ),
    }


# =============================================================================
# Test Classes
# =============================================================================


class TestMetadataValidation:
    """Test metadata validation for Zonge AVG Tipper files."""

    def test_survey_metadata(self, tf_avg_tipper_object, expected_survey_metadata):
        """Test survey metadata validation."""
        actual_metadata = tf_avg_tipper_object.survey_metadata.to_dict(single=True)
        assert actual_metadata == expected_survey_metadata

    def test_station_metadata(self, tf_avg_tipper_object, expected_station_metadata):
        """Test station metadata validation (excluding creation_time)."""
        actual_metadata = tf_avg_tipper_object.station_metadata.to_dict(single=True)
        # Remove creation_time as it varies (if present)
        actual_metadata.pop("provenance.creation_time", None)
        assert actual_metadata == expected_station_metadata

    def test_run_metadata(self, tf_avg_tipper_object, expected_run_metadata):
        """Test run metadata validation."""
        actual_metadata = tf_avg_tipper_object.station_metadata.runs[0].to_dict(
            single=True
        )
        assert actual_metadata == expected_run_metadata

    @pytest.mark.parametrize(
        "channel_name,channel_index",
        [("ex", 0), ("ey", 1), ("hx", 2), ("hy", 3), ("hz", 4)],
    )
    def test_channel_metadata(
        self,
        tf_avg_tipper_object,
        expected_channel_metadata,
        channel_name,
        channel_index,
    ):
        """Test channel metadata validation for all channels."""
        actual_metadata = (
            tf_avg_tipper_object.station_metadata.runs[0]
            .channels[channel_index]
            .to_dict(single=True)
        )
        assert actual_metadata == expected_channel_metadata[channel_name]


class TestTipperTransferFunctions:
    """Test transfer function data validation."""

    def test_impedance_shape(self, tf_avg_tipper_object):
        """Test impedance tensor shape."""
        assert tf_avg_tipper_object.impedance.shape == (51, 2, 2)

    def test_impedance_first_element(self, tf_avg_tipper_object):
        """Test first element of impedance tensor."""
        expected = np.array(
            [
                [-0.42514998 - 1.2095569j, 52.05528553 + 4.76589728j],
                [0.21016642 + 0.49228452j, -10.16752339 - 2.70034593j],
            ]
        )
        assert np.allclose(tf_avg_tipper_object.impedance[0], expected)

    def test_impedance_last_element(self, tf_avg_tipper_object):
        """Test last element of impedance tensor."""
        expected = np.array(
            [
                [-112.92397163 + 35.82342154j, -1051.1278249 + 1808.8705608j],
                [116.01781236 + 128.3445648j, 51.80694503 - 42.43686378j],
            ]
        )
        assert np.allclose(tf_avg_tipper_object.impedance[-1], expected)

    def test_impedance_error_shape(self, tf_avg_tipper_object):
        """Test impedance error tensor shape."""
        assert tf_avg_tipper_object.impedance_error.shape == (51, 2, 2)

    def test_impedance_error_first_element(self, tf_avg_tipper_object):
        """Test first element of impedance error tensor."""
        expected = np.array([[1.66174935, 67.73395417], [0.69379092, 13.50078836]])
        assert np.allclose(tf_avg_tipper_object.impedance_error[0], expected)

    def test_impedance_error_last_element(self, tf_avg_tipper_object):
        """Test last element of impedance error tensor."""
        expected = np.array([[22.16312252, 362.35893807], [9.4763284, 22.00814395]])
        assert np.allclose(tf_avg_tipper_object.impedance_error[-1], expected)

    def test_tipper_shape(self, tf_avg_tipper_object):
        """Test tipper tensor shape."""
        assert tf_avg_tipper_object.tipper.shape == (51, 1, 2)

    def test_tipper_first_element(self, tf_avg_tipper_object):
        """Test first element of tipper tensor."""
        expected = np.array(
            [[22.74427485 + 18.94823397j, -923.7823987 + 524.50678723j]]
        )
        assert np.allclose(tf_avg_tipper_object.tipper[0], expected)

    def test_tipper_last_element(self, tf_avg_tipper_object):
        """Test last element of tipper tensor."""
        expected = np.array([[0.30581038 - 0.60563024j, -3.71315818 - 10.6661564j]])
        assert np.allclose(tf_avg_tipper_object.tipper[-1], expected)

    def test_tipper_error_shape(self, tf_avg_tipper_object):
        """Test tipper error tensor shape."""
        assert tf_avg_tipper_object.tipper_error.shape == (51, 1, 2)

    def test_tipper_error_first_element(self, tf_avg_tipper_object):
        """Test first element of tipper error tensor."""
        expected = np.array([[29.603, 1062.3]])
        assert np.allclose(tf_avg_tipper_object.tipper_error[0], expected)

    def test_tipper_error_last_element(self, tf_avg_tipper_object):
        """Test last element of tipper error tensor."""
        expected = np.array([[0.67846, 11.294]])
        assert np.allclose(tf_avg_tipper_object.tipper_error[-1], expected)


class TestTransferFunctionProperties:
    """Test transfer function property methods."""

    def test_no_inverse_signal_power(self, tf_avg_tipper_object):
        """Test that inverse signal power is not available."""
        assert not tf_avg_tipper_object.has_inverse_signal_power()

    def test_no_residual_covariance(self, tf_avg_tipper_object):
        """Test that residual covariance is not available."""
        assert not tf_avg_tipper_object.has_residual_covariance()


class TestPerformanceAndEfficiency:
    """Test performance and efficiency of the tipper reading functionality."""

    def test_memory_usage(self, tf_avg_tipper_object):
        """Test that the TF object doesn't consume excessive memory."""
        import sys

        memory_usage = sys.getsizeof(tf_avg_tipper_object)
        # Should be reasonable size (less than 10MB for this test file)
        assert memory_usage < 10 * 1024 * 1024

    def test_impedance_array_properties(self, tf_avg_tipper_object):
        """Test properties of impedance arrays."""
        # Test impedance is complex
        assert np.iscomplexobj(tf_avg_tipper_object.impedance)
        # Test no NaN values
        assert not np.any(np.isnan(tf_avg_tipper_object.impedance))
        # Test finite values
        assert np.all(np.isfinite(tf_avg_tipper_object.impedance))

    def test_tipper_array_properties(self, tf_avg_tipper_object):
        """Test properties of tipper arrays."""
        # Test tipper is complex
        assert np.iscomplexobj(tf_avg_tipper_object.tipper)
        # Test no NaN values
        assert not np.any(np.isnan(tf_avg_tipper_object.tipper))
        # Test finite values
        assert np.all(np.isfinite(tf_avg_tipper_object.tipper))

    def test_error_array_properties(self, tf_avg_tipper_object):
        """Test properties of error arrays."""
        # Test errors are real and positive
        assert np.all(tf_avg_tipper_object.impedance_error >= 0)
        assert np.all(tf_avg_tipper_object.tipper_error >= 0)
        # Test no NaN values
        assert not np.any(np.isnan(tf_avg_tipper_object.impedance_error))
        assert not np.any(np.isnan(tf_avg_tipper_object.tipper_error))


# =============================================================================
# Test execution and performance validation
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__])
