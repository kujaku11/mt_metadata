# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

from collections import OrderedDict

# =============================================================================
# Imports
# =============================================================================
import pytest

from mt_metadata import TF_EDI_EMPOWER
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io import edi


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture(scope="module")
def edi_object():
    """Create EDI object once for all tests in this module."""
    return edi.EDI(fn=TF_EDI_EMPOWER)


@pytest.fixture(scope="module")
def expected_header():
    """Expected header data for testing."""
    return OrderedDict(
        [
            ("acqdate", "1980-01-01T00:00:00+00:00"),
            ("coordinate_system", "geographic"),
            ("dataid", "701_merged_wrcal"),
            ("datum", "WGS 84"),
            ("elevation", 2489.0),
            ("empty", 1e32),
            ("fileby", "EMTF FCU"),
            ("latitude", 40.64811111111111),
            ("longitude", -106.21241666666667),
            ("stdvers", "SEG 1.0"),
            ("units", "milliVolt per kilometer per nanoTesla"),
        ]
    )


@pytest.fixture(scope="module")
def expected_info():
    """Expected info dictionary for testing."""
    return {
        "maxinfo": "999",
        "project": "",
        "survey": "",
        "survey.time_period.start_date": "2023",
        "processedby": "",
        "transfer_function.software.name": "EMpower v2.9.0.7",
        "processingtag": "",
        "station.geographic_name": "701 Walden South",
        "runlist": "",
        "remoteref": "",
        "remotesite": "",
        "signconvention": "",
        "unique id": "{88290cfe-9200-4cc2-a0dd-5ed7cd7f95ea}",
        "process date": "2023-05-30 16:22",
        "duration": "24h 47m 13s",
        "station.location.declination.value": "0",
        "coordinates": "40 38' 53.2\", -106 12' 44.7\"",
        "gps (min - max)": "8 - 13",
        "temperature (min - max)": "18 - 48",
        "comb filter": "60 HZ",
        "fine robust": "NONE",
        "editing_workbench.totoal rejected crosspowers": "0.0000%",
        "run.id": "10647_2023-05-18-202538",
        "run.data_logger.model": "MTU-5C",
        "run.acquired_by.author": "",
        "run.ex.component": "ex",
        "run.ex.dipole_length": "95.3",
        "run.ex.ac.end": "2.5",
        "run.ex.dc.end": "0.0537872",
        "run.ex.contact_resistance.start": "1558.69",
        "run.ex.contact_resistance.end": "4222.68",
        "run.ex.comments": "saturation=0.0870754%,min value=-1.25,max value=1.25",
        "run.ey.component": "ey",
        "run.ey.dipole_length": "99.1",
        "run.ey.ac.end": "2.5",
        "run.ey.dc.end": "0.0120163",
        "run.ey.contact_resistance.start": "2199.7",
        "run.ey.contact_resistance.end": "2230.26",
        "run.ey.comments": "saturation=0.0379904%,min value=-1.25,max value=1.25",
        "run.ey.measured_azimuth": "0",
        "run.hx.component": "hx",
        "run.hx.sensor.model": "MTC-155",
        "run.hx.comments.end": "ac=0.00976562,dc=-0.0160217",
        "run.hx.comments": "cal name=57507_646504D8.scal,saturation=0.000280165 %,min value=-0.00488281,max value=0.00488281",
        "run.hx.sensor.id": "57507",
        "run.hy.component": "hy",
        "run.hy.sensor.model": "MTC-155",
        "run.hy.comments.end": "ac=0.00913765,dc=-0.00793457",
        "run.hy.comments": "cal name=57513_646504D8.scal,saturation=5.60331e-5 %,min value=-0.00488281,max value=0.00425484",
        "run.hy.sensor.id": "57513",
        "run.hz.component": "hz",
        "run.hz.sensor.model": "MTC-185",
        "run.hz.comments.end": "ac=0.000317973,dc=-0.0448608",
        "run.hz.comments": "cal name=53408_646504D8.scal,saturation=0 %,min value=-0.000170265,max value=0.000147708",
        "run.hz.sensor.id": "53408",
        "run.measured_azimuth": "0",
        "transfer_function.remote_references.geographic_name": "706 Red Canyon",
        "transfer_function.remote_references.hz.measured_azimuth": "0",
        "transfer_function.remote_references.rrhx.component": "rx",
        "transfer_function.remote_references.rrhx.sensor.model": "MTC-155",
        "transfer_function.remote_references.rrhx.comments.end": "ac=0.00976562,dc=0.0205994",
        "transfer_function.remote_references.rrhx.comments": "cal name=57454_6466657B.scal,saturation=0.00229736 %,min value=-0.00488281,max value=0.00488281",
        "transfer_function.remote_references.rrhx.sensor.id": "57454",
        "transfer_function.remote_references.rrhy.component": "ry",
        "transfer_function.remote_references.rrhy.sensor.model": "MTC-155",
        "transfer_function.remote_references.rrhy.comments.end": "ac=0.00976562,dc=0.00549316",
        "transfer_function.remote_references.rrhy.comments": "cal name=57458_6466657B.scal,saturation=0.00207322 %,min value=-0.00488281,max value=0.00488281",
        "transfer_function.remote_references.rrhy.sensor.id": "57458",
    }


@pytest.fixture(scope="module")
def expected_measurement_channels():
    """Expected measurement channel data for testing."""
    return {
        "ex": OrderedDict(
            [
                ("acqchan", ""),
                ("azm", 90.0),
                ("chtype", "EX"),
                ("id", 1004.001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", -48.8),
                ("y2", 46.5),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        ),
        "ey": OrderedDict(
            [
                ("acqchan", ""),
                ("azm", 90.0),
                ("chtype", "EY"),
                ("id", 1005.001),
                ("x", -50.6),
                ("x2", 48.5),
                ("y", 0.0),
                ("y2", 0.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        ),
        "hx": OrderedDict(
            [
                ("acqchan", ""),
                ("azm", 0.0),
                ("chtype", "HX"),
                ("dip", 0.0),
                ("id", 1001.001),
                ("x", 8.5),
                ("y", 8.5),
                ("z", 0.0),
            ]
        ),
        "hy": OrderedDict(
            [
                ("acqchan", ""),
                ("azm", 90.0),
                ("chtype", "HY"),
                ("dip", 0.0),
                ("id", 1002.001),
                ("x", -8.5),
                ("y", 8.5),
                ("z", 0.0),
            ]
        ),
        "hz": OrderedDict(
            [
                ("acqchan", ""),
                ("azm", 0.0),
                ("chtype", "HZ"),
                ("dip", 0.0),
                ("id", 1003.001),
                ("x", 21.2),
                ("y", -21.2),
                ("z", 0.0),
            ]
        ),
    }


@pytest.fixture(scope="module")
def expected_measurement_output():
    """Expected measurement output list for testing."""
    return [
        "\n>=DEFINEMEAS\n",
        "    MAXCHAN=7\n",
        "    MAXRUN=999\n",
        "    MAXMEAS=9999\n",
        "    REFLAT=40:38:53.200000\n",
        "    REFLON=-106:12:44.700000\n",
        "    REFELEV=2489.0\n",
        "    REFTYPE=CART\n",
        "    UNITS=meter\n",
        "\n",
        ">HMEAS ID=1001.001 CHTYPE=HX X=8.50 Y=8.50 Z=0.00 AZM=0.00 DIP=0.00 ACQCHAN=\n",
        ">HMEAS ID=1002.001 CHTYPE=HY X=-8.50 Y=8.50 Z=0.00 AZM=90.00 DIP=0.00 ACQCHAN=\n",
        ">HMEAS ID=1003.001 CHTYPE=HZ X=21.20 Y=-21.20 Z=0.00 AZM=0.00 DIP=0.00 ACQCHAN=\n",
        ">EMEAS ID=1004.001 CHTYPE=EX X=0.00 Y=-48.80 Z=0.00 X2=0.00 Y2=46.50 Z2=0.00 AZM=90.00 ACQCHAN=\n",
        ">EMEAS ID=1005.001 CHTYPE=EY X=-50.60 Y=0.00 Z=0.00 X2=48.50 Y2=0.00 Z2=0.00 AZM=90.00 ACQCHAN=\n",
    ]


@pytest.fixture(scope="module")
def expected_data_section():
    """Expected data section output for testing."""
    return [
        "\n>=MTSECT\n",
        "    NFREQ=98\n",
        "    SECTID=701_merged_wrcal\n",
        "    NCHAN=0\n",
        "    MAXBLOCKS=999\n",
        "    HX=1001.001\n",
        "    HY=1002.001\n",
        "    HZ=1003.001\n",
        "    EX=1004.001\n",
        "    EY=1005.001\n",
        "\n",
    ]


# =============================================================================
# Test Classes
# =============================================================================
class TestEMPOWEREDI:
    """Test class for EMpower EDI functionality."""

    def test_header(self, edi_object, expected_header):
        """Test header values using parametrized subtests."""
        # Test main header attributes
        for key, expected_value in expected_header.items():
            actual_value = getattr(edi_object.Header, key.lower())
            assert actual_value == expected_value, f"Header {key} mismatch"

        # Test declination attributes
        assert edi_object.Header.declination.model == "IGRF"
        assert edi_object.Header.declination.value == 0.0

    def test_info(self, edi_object, expected_info):
        """Test info dictionary."""
        assert edi_object.Info.info_dict == expected_info

    @pytest.mark.parametrize("channel", ["ex", "ey", "hx", "hy", "hz"])
    def test_measurement_channels(
        self, edi_object, expected_measurement_channels, channel
    ):
        """Test individual measurement channels using parametrization."""
        expected = expected_measurement_channels[channel]
        actual = edi_object.Measurement.measurements[channel].to_dict(single=True)
        assert actual == expected

    def test_measurement_output(self, edi_object, expected_measurement_output):
        """Test measurement write output."""
        actual_output = edi_object.Measurement.write_measurement()
        assert actual_output == expected_measurement_output

    @pytest.mark.parametrize(
        "attr,expected,precision",
        [
            ("reflat", 40.64811111111111, 5),
            ("reflon", -106.21241666666667, 5),
            ("refelev", 2489.0, 2),
        ],
    )
    def test_measurement_reference_values(self, edi_object, attr, expected, precision):
        """Test measurement reference values with specified precision."""
        actual = getattr(edi_object.Measurement, attr)
        assert abs(actual - expected) < 10 ** (-precision)

    def test_data_section(self, edi_object, expected_data_section):
        """Test data section output."""
        actual_output = edi_object.Data.write_data()
        assert actual_output == expected_data_section

    @pytest.mark.parametrize(
        "array_name,expected_shape",
        [
            ("z", (98, 2, 2)),
            ("z_err", (98, 2, 2)),
        ],
    )
    def test_impedance_shapes(self, edi_object, array_name, expected_shape):
        """Test impedance array shapes."""
        array = getattr(edi_object, array_name)
        assert array.shape == expected_shape

    @pytest.mark.parametrize(
        "array_name,indices,expected_value",
        [
            ("z", (0, 0, 0), 19.91471 + 63.25052j),
            ("z", (-1, 1, 1), -0.005189691 - 0.0085249j),
            ("z_err", (0, 0, 0), 1.1270665463937788),
            ("z_err", (-1, 1, 1), 0.00031013205251956787),
        ],
    )
    def test_impedance_values(self, edi_object, array_name, indices, expected_value):
        """Test specific impedance values."""
        array = getattr(edi_object, array_name)
        actual_value = array[indices]

        if isinstance(expected_value, complex):
            assert abs(actual_value - expected_value) < 1e-5
        else:
            assert abs(actual_value - expected_value) < 1e-10

    @pytest.mark.parametrize(
        "array_name,expected_shape",
        [
            ("t", (98, 1, 2)),
            ("t_err", (98, 1, 2)),
        ],
    )
    def test_tipper_shapes(self, edi_object, array_name, expected_shape):
        """Test tipper array shapes."""
        array = getattr(edi_object, array_name)
        assert array.shape == expected_shape

    @pytest.mark.parametrize(
        "array_name,indices,expected_value",
        [
            ("t", (0, 0, 0), 0.01175011 - 0.006787284j),
            ("t", (-1, 0, 1), 0.2252638 + 0.1047829j),
            ("t_err", (0, 0, 0), 0.0006966629744718747),
            ("t_err", (-1, 0, 1), 0.01090868461364614),
        ],
    )
    def test_tipper_values(self, edi_object, array_name, indices, expected_value):
        """Test specific tipper values."""
        array = getattr(edi_object, array_name)
        actual_value = array[indices]

        if isinstance(expected_value, complex):
            assert abs(actual_value - expected_value) < 1e-8
        else:
            assert abs(actual_value - expected_value) < 1e-15

    def test_rotation_angle(self, edi_object):
        """Test rotation angle properties."""
        rotation_angle = edi_object.rotation_angle

        # Test that all values are zero
        assert (rotation_angle == 0).all()

        # Test shape
        assert rotation_angle.shape == (98,)


# =============================================================================
# TestEMpowerTF pytest class
# =============================================================================


@pytest.fixture(scope="module")
def tf_edi_object():
    """Fixture to create TF object and convert to EDI once for all tests."""
    tf_obj = TF(TF_EDI_EMPOWER)
    tf_obj.read()
    return tf_obj.to_edi()


@pytest.fixture(scope="module")
def tf_expected_header():
    """Fixture for expected TF header values."""
    return OrderedDict(
        [
            ("acqdate", "1980-01-01T00:00:00+00:00"),
            ("coordinate_system", "geographic"),
            ("dataid", "701_merged_wrcal"),
            ("datum", "WGS 84"),
            ("elevation", 2489.0),
            ("empty", 1e32),
            ("fileby", "EMTF FCU"),
            ("latitude", 40.64811111111111),
            ("longitude", -106.21241666666667),
            ("stdvers", "SEG 1.0"),
            ("units", "milliVolt per kilometer per nanoTesla"),
        ]
    )


@pytest.fixture(scope="module")
def expected_info_dict():
    """Fixture for expected info dictionary."""
    return {
        "survey.datum": "WGS 84",
        "survey.id": "0",
        "survey.release_license": "CC-BY-4.0",
        "transfer_function.coordinate_system": "geographic",
        "transfer_function.id": "701_merged_wrcal",
        "transfer_function.processed_date": "2023-05-30T00:00:00+00:00",
        "transfer_function.remote_references": ["706 Red Canyon"],
        "transfer_function.runs_processed": ["701_merged_wrcala"],
        "transfer_function.sign_convention": "+",
        "transfer_function.software.name": "EMpower v2.9.0.7",
        "transfer_function.units": "milliVolt per kilometer per nanoTesla",
        "provenance.creation_time": "2023-05-30T00:00:00+00:00",
        "provenance.software.name": "EMTF FCU",
        "provenance.software.version": "4.0",
        "provenance.submitter.author": "EMTF FCU",
        "701_merged_wrcala.channels_recorded_auxiliary": [],
        "701_merged_wrcala.channels_recorded_electric": ["ex", "ey"],
        "701_merged_wrcala.channels_recorded_magnetic": ["hx", "hy", "hz"],
        "701_merged_wrcala.data_logger.model": "MTU-5C",
        "701_merged_wrcala.data_logger.power_source.voltage.end": 0.0,
        "701_merged_wrcala.data_logger.power_source.voltage.start": 0.0,
        "701_merged_wrcala.data_logger.timing_system.drift": 0.0,
        "701_merged_wrcala.data_logger.timing_system.type": "GPS",
        "701_merged_wrcala.data_logger.timing_system.uncertainty": 0.0,
        "701_merged_wrcala.data_type": "BBMT",
        "701_merged_wrcala.id": "701_merged_wrcala",
        "701_merged_wrcala.sample_rate": 0.0,
        "701_merged_wrcala.hx.channel_id": "1001.001",
        "701_merged_wrcala.hx.channel_number": 0,
        "701_merged_wrcala.hx.component": "hx",
        "701_merged_wrcala.hx.filters": [],
        "701_merged_wrcala.hx.h_field_max.end": 0.0,
        "701_merged_wrcala.hx.h_field_max.start": 0.0,
        "701_merged_wrcala.hx.h_field_min.end": 0.0,
        "701_merged_wrcala.hx.h_field_min.start": 0.0,
        "701_merged_wrcala.hx.location.datum": "WGS 84",
        "701_merged_wrcala.hx.measurement_azimuth": 0.0,
        "701_merged_wrcala.hx.measurement_tilt": 0.0,
        "701_merged_wrcala.hx.sensor.id": "57454",
        "701_merged_wrcala.hx.sensor.model": "MTC-155",
        "701_merged_wrcala.hx.sensor.type": "magnetic",
        "701_merged_wrcala.hx.type": "magnetic",
        "701_merged_wrcala.hy.channel_id": "1002.001",
        "701_merged_wrcala.hy.channel_number": 0,
        "701_merged_wrcala.hy.component": "hy",
        "701_merged_wrcala.hy.filters": [],
        "701_merged_wrcala.hy.h_field_max.end": 0.0,
        "701_merged_wrcala.hy.h_field_max.start": 0.0,
        "701_merged_wrcala.hy.h_field_min.end": 0.0,
        "701_merged_wrcala.hy.h_field_min.start": 0.0,
        "701_merged_wrcala.hy.location.datum": "WGS 84",
        "701_merged_wrcala.hy.measurement_azimuth": 90.0,
        "701_merged_wrcala.hy.measurement_tilt": 0.0,
        "701_merged_wrcala.hy.sensor.id": "57458",
        "701_merged_wrcala.hy.sensor.model": "MTC-155",
        "701_merged_wrcala.hy.sensor.type": "magnetic",
        "701_merged_wrcala.hy.translated_azimuth": 90.0,
        "701_merged_wrcala.hy.type": "magnetic",
        "701_merged_wrcala.hz.channel_id": "1003.001",
        "701_merged_wrcala.hz.channel_number": 0,
        "701_merged_wrcala.hz.component": "hz",
        "701_merged_wrcala.hz.filters": [],
        "701_merged_wrcala.hz.h_field_max.end": 0.0,
        "701_merged_wrcala.hz.h_field_max.start": 0.0,
        "701_merged_wrcala.hz.h_field_min.end": 0.0,
        "701_merged_wrcala.hz.h_field_min.start": 0.0,
        "701_merged_wrcala.hz.location.datum": "WGS 84",
        "701_merged_wrcala.hz.measurement_azimuth": 0.0,
        "701_merged_wrcala.hz.measurement_tilt": 0.0,
        "701_merged_wrcala.hz.sensor.id": "53408",
        "701_merged_wrcala.hz.sensor.model": "MTC-185",
        "701_merged_wrcala.hz.sensor.type": "magnetic",
        "701_merged_wrcala.hz.type": "magnetic",
        "701_merged_wrcala.ex.ac.end": 2.5,
        "701_merged_wrcala.ex.ac.start": 0.0,
        "701_merged_wrcala.ex.channel_id": "1004.001",
        "701_merged_wrcala.ex.channel_number": 0,
        "701_merged_wrcala.ex.comments": "saturation=0.0870754%,min value=-1.25,max value=1.25",
        "701_merged_wrcala.ex.component": "ex",
        "701_merged_wrcala.ex.contact_resistance.end": 4222.68,
        "701_merged_wrcala.ex.contact_resistance.start": 1558.69,
        "701_merged_wrcala.ex.dc.end": 0.0537872,
        "701_merged_wrcala.ex.dc.start": 0.0,
        "701_merged_wrcala.ex.dipole_length": 95.3,
        "701_merged_wrcala.ex.filters": [],
        "701_merged_wrcala.ex.measurement_azimuth": 90.0,
        "701_merged_wrcala.ex.measurement_tilt": 0.0,
        "701_merged_wrcala.ex.negative.datum": "WGS 84",
        "701_merged_wrcala.ex.negative.type": "electric",
        "701_merged_wrcala.ex.positive.datum": "WGS 84",
        "701_merged_wrcala.ex.positive.type": "electric",
        "701_merged_wrcala.ex.translated_azimuth": 90.0,
        "701_merged_wrcala.ex.type": "electric",
        "701_merged_wrcala.ey.ac.end": 2.5,
        "701_merged_wrcala.ey.ac.start": 0.0,
        "701_merged_wrcala.ey.channel_id": "1005.001",
        "701_merged_wrcala.ey.channel_number": 0,
        "701_merged_wrcala.ey.comments": "saturation=0.0379904%,min value=-1.25,max value=1.25",
        "701_merged_wrcala.ey.component": "ey",
        "701_merged_wrcala.ey.contact_resistance.end": 2230.26,
        "701_merged_wrcala.ey.contact_resistance.start": 2199.7,
        "701_merged_wrcala.ey.dc.end": 0.0120163,
        "701_merged_wrcala.ey.dc.start": 0.0,
        "701_merged_wrcala.ey.dipole_length": 99.1,
        "701_merged_wrcala.ey.filters": [],
        "701_merged_wrcala.ey.measurement_azimuth": 0.0,
        "701_merged_wrcala.ey.measurement_tilt": 0.0,
        "701_merged_wrcala.ey.negative.datum": "WGS 84",
        "701_merged_wrcala.ey.negative.type": "electric",
        "701_merged_wrcala.ey.positive.datum": "WGS 84",
        "701_merged_wrcala.ey.positive.type": "electric",
        "701_merged_wrcala.ey.type": "electric",
    }


@pytest.fixture(scope="module")
def expected_measurement_data():
    """Fixture for expected measurement data by channel."""
    return {
        "ex": OrderedDict(
            [
                ("acqchan", "1004.001"),
                ("azm", 90.0),
                ("chtype", "ex"),
                ("id", 1004.001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", -48.8),
                ("y2", 46.5),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        ),
        "ey": OrderedDict(
            [
                ("acqchan", "1005.001"),
                ("azm", 0.0),
                ("chtype", "ey"),
                ("id", 1005.001),
                ("x", -50.6),
                ("x2", 48.5),
                ("y", 0.0),
                ("y2", 0.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        ),
        "hx": OrderedDict(
            [
                ("acqchan", "1001.001"),
                ("azm", 0.0),
                ("chtype", "hx"),
                ("dip", 0.0),
                ("id", 1001.001),
                ("x", 8.5),
                ("y", 8.5),
                ("z", 0.0),
            ]
        ),
        "hy": OrderedDict(
            [
                ("acqchan", "1002.001"),
                ("azm", 90.0),
                ("chtype", "hy"),
                ("dip", 0.0),
                ("id", 1002.001),
                ("x", -8.5),
                ("y", 8.5),
                ("z", 0.0),
            ]
        ),
        "hz": OrderedDict(
            [
                ("acqchan", "1003.001"),
                ("azm", 0.0),
                ("chtype", "hz"),
                ("dip", 0.0),
                ("id", 1003.001),
                ("x", 21.2),
                ("y", -21.2),
                ("z", 0.0),
            ]
        ),
    }


@pytest.fixture(scope="module")
def expected_measurement_attributes():
    """Fixture for expected measurement attributes."""
    return OrderedDict(
        [
            ("maxchan", 5),
            ("maxmeas", 7),
            ("maxrun", 999),
            ("refelev", 2489.0),
            ("reflat", 40.648111),
            ("refloc", "701_merged_wrcal"),
            ("reflon", -106.212417),
            ("reftype", "cartesian"),
            ("units", "meter"),
        ]
    )


@pytest.fixture(scope="module")
def tf_expected_data_section():
    """Fixture for expected TF data section."""
    return OrderedDict(
        [
            ("ex", "1004.001"),
            ("ey", "1005.001"),
            ("hx", "1001.001"),
            ("hy", "1002.001"),
            ("hz", "1003.001"),
            ("maxblocks", 999),
            ("nchan", 5),
            ("nfreq", 98),
            ("rrhx", None),
            ("rrhy", None),
            ("sectid", "701_merged_wrcal"),
        ]
    )


class TestEMpowerTF:
    """Pytest class for EMpower TF tests using fixtures and parametrization."""

    @pytest.mark.parametrize(
        "key,expected_value",
        [
            ("acqdate", "1980-01-01T00:00:00+00:00"),
            ("coordinate_system", "geographic"),
            ("dataid", "701_merged_wrcal"),
            ("datum", "WGS 84"),
            ("elevation", 2489.0),
            ("empty", 1e32),
            ("fileby", "EMTF FCU"),
            ("latitude", 40.64811111111111),
            ("longitude", -106.21241666666667),
            ("stdvers", "SEG 1.0"),
            ("units", "milliVolt per kilometer per nanoTesla"),
        ],
    )
    def test_header_attributes(self, tf_edi_object, key, expected_value):
        """Test individual header attributes."""
        h_value = getattr(tf_edi_object.Header, key.lower())
        assert h_value == expected_value

    def test_header_declination(self, tf_edi_object):
        """Test header declination properties."""
        assert tf_edi_object.Header.declination.model == "IGRF"
        assert tf_edi_object.Header.declination.value == 0.0

    def test_info_dict(self, tf_edi_object, expected_info_dict):
        """Test info dictionary matches expected values."""
        assert tf_edi_object.Info.info_dict == expected_info_dict

    @pytest.mark.parametrize("channel", ["ex", "ey", "hx", "hy", "hz"])
    def test_measurement_channels(
        self, tf_edi_object, expected_measurement_data, channel
    ):
        """Test measurement data for each channel."""
        expected = expected_measurement_data[channel]
        actual = tf_edi_object.Measurement.measurements[channel].to_dict(single=True)
        assert actual == expected

    @pytest.mark.parametrize(
        "key,expected_value,is_float",
        [
            ("maxchan", 5, False),
            ("maxmeas", 7, False),
            ("maxrun", 999, False),
            ("refelev", 2489.0, True),
            ("reflat", 40.648111, True),
            ("refloc", "701_merged_wrcal", False),
            ("reflon", -106.212417, True),
            ("reftype", "cartesian", False),
            ("units", "meter", False),
        ],
    )
    def test_measurement_attributes(self, tf_edi_object, key, expected_value, is_float):
        """Test measurement attributes with appropriate precision for floats."""
        actual_value = getattr(tf_edi_object.Measurement, key)
        if is_float:
            assert abs(actual_value - expected_value) < 1e-5
        else:
            assert actual_value == expected_value

    def test_data_section(self, tf_edi_object, tf_expected_data_section):
        """Test data section properties."""
        assert tf_edi_object.Data.to_dict(single=True) == tf_expected_data_section

    @pytest.mark.parametrize(
        "array_name,expected_shape",
        [
            ("z", (98, 2, 2)),
            ("z_err", (98, 2, 2)),
        ],
    )
    def test_tf_impedance_shapes(self, tf_edi_object, array_name, expected_shape):
        """Test impedance array shapes."""
        array = getattr(tf_edi_object, array_name)
        assert array.shape == expected_shape

    @pytest.mark.parametrize(
        "array_name,indices,expected_value",
        [
            ("z", (0, 0, 0), 19.91471 + 63.25052j),
            ("z", (-1, 1, 1), -0.005189691 - 0.0085249j),
            ("z_err", (0, 0, 0), 1.1270665463937788),
            ("z_err", (-1, 1, 1), 0.00031013205251956787),
        ],
    )
    def test_tf_impedance_values(
        self, tf_edi_object, array_name, indices, expected_value
    ):
        """Test specific impedance values."""
        array = getattr(tf_edi_object, array_name)
        actual_value = array[indices]

        if isinstance(expected_value, complex):
            assert abs(actual_value - expected_value) < 1e-5
        else:
            assert abs(actual_value - expected_value) < 1e-10

    @pytest.mark.parametrize(
        "array_name,expected_shape",
        [
            ("t", (98, 1, 2)),
            ("t_err", (98, 1, 2)),
        ],
    )
    def test_tf_tipper_shapes(self, tf_edi_object, array_name, expected_shape):
        """Test tipper array shapes."""
        array = getattr(tf_edi_object, array_name)
        assert array.shape == expected_shape

    @pytest.mark.parametrize(
        "array_name,indices,expected_value",
        [
            ("t", (0, 0, 0), 0.01175011 - 0.006787284j),
            ("t", (-1, 0, 1), 0.2252638 + 0.1047829j),
            ("t_err", (0, 0, 0), 0.0006966629744718747),
            ("t_err", (-1, 0, 1), 0.01090868461364614),
        ],
    )
    def test_tf_tipper_values(self, tf_edi_object, array_name, indices, expected_value):
        """Test specific tipper values."""
        array = getattr(tf_edi_object, array_name)
        actual_value = array[indices]

        if isinstance(expected_value, complex):
            assert abs(actual_value - expected_value) < 1e-8
        else:
            assert abs(actual_value - expected_value) < 1e-15

    def test_tf_rotation_angle(self, tf_edi_object):
        """Test rotation angle properties."""
        rotation_angle = tf_edi_object.rotation_angle

        # Test that all values are zero
        assert (rotation_angle == 0).all()

        # Test shape
        assert rotation_angle.shape == (98,)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__])
