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

from mt_metadata import TF_EDI_PHOENIX
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io import edi


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture(scope="module")
def phoenix_edi_object():
    """Create Phoenix EDI object once for all tests in this module."""
    return edi.EDI(fn=TF_EDI_PHOENIX)


@pytest.fixture(scope="module")
def phoenix_tf_object():
    """Create Phoenix TF object once for all tests in this module."""
    tf_obj = TF(fn=TF_EDI_PHOENIX)
    tf_obj.read()
    return tf_obj


@pytest.fixture(scope="module")
def phoenix_tf_to_edi_object(phoenix_tf_object):
    """Create EDI object from TF object for testing."""
    return phoenix_tf_object.to_edi()


@pytest.fixture(scope="module")
def expected_header():
    """Expected header data for Phoenix EDI testing."""
    return {
        "acqby": "Phoenix",
        "acqdate": "2014-07-28T00:00:00+00:00",
        "coordinate_system": "geographic",
        "dataid": "14_IEB0537A",
        "datum": "WGS 84",
        "elevation": 158.0,
        "fileby": "Phoenix",
        "filedate": "2014-08-01",
        "latitude": -22.823722222222223,
        "longitude": 139.29469444444445,
        "progdate": "2010-03-09",
        "progname": "mt_metadata",
        "progvers": "MT-Editor Ver 0.99.2.106",
        "stdvers": "SEG 1.0",
    }


@pytest.fixture(scope="module")
def expected_info():
    """Expected info dictionary for Phoenix EDI testing."""
    return {
        "phoenix_attribute": "MTU5A",
        "survey.id": "BOULIA",
        "station.acquired_by.organization": "GA",
        "survey.project": "IEB",
        "run.data_logger.model": "MTU5A MTU5A",
        "station.time_period.start": "2014/07/28 - 02:57:00",
        "station.time_period.end": "2014/07/28",
        "run.data_logger.id": "U-2189",
        "run.data_logger.firmware.version": "3112F6",
        "processing_parameter": "RHO",
        "run.ex.contact_resistance.start": "1.085",
        "run.ex.ac.start": "25.7",
        "run.ex.dc.start": "+1.30",
        "run.ey.contact_resistance.start": "0.532",
        "run.hx.sensor.id": "COIL2318",
        "hx.sensor.manufacturer": "Phoenix Geophysics",
        "hx.sensor.type": "Induction Coil",
        "run.ey.ac.start": "13.8",
        "run.ey.dc.start": "+1.50",
        "run.hy.sensor.id": "COIL2319",
        "hy.sensor.manufacturer": "Phoenix Geophysics",
        "hy.sensor.type": "Induction Coil",
        "run.hz.sensor.id": "COIL2320",
        "hz.sensor.manufacturer": "Phoenix Geophysics",
        "hz.sensor.type": "Induction Coil",
        "run.rrhx.sensor.id": "COIL2485",
        "rx.sensor.manufacturer": "Phoenix Geophysics",
        "rx.sensor.type": "Induction Coil",
        "run.rrhy.sensor.id": "COIL2487",
        "ry.sensor.manufacturer": "Phoenix Geophysics",
        "ry.sensor.type": "Induction Coil",
    }


@pytest.fixture(scope="module")
def expected_measurement_channels():
    """Expected measurement channel data for Phoenix EDI testing."""
    return {
        "ex": OrderedDict(
            [
                ("acqchan", "CH1"),
                ("azm", 0.0),
                ("chtype", "EX"),
                ("id", 5374.0537),
                ("x", -50.0),
                ("x2", 50.0),
                ("y", -0.0),
                ("y2", 0.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        ),
        "ey": OrderedDict(
            [
                ("acqchan", "CH2"),
                ("azm", 116.61629962451384),
                ("chtype", "EY"),
                ("id", 5375.0537),
                ("x", 22.4),
                ("x2", -22.4),
                ("y", -44.7),
                ("y2", 44.7),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        ),
        "hx": OrderedDict(
            [
                ("acqchan", "CH3"),
                ("azm", 0.0),
                ("chtype", "HX"),
                ("dip", 0.0),
                ("id", 5371.0537),
                ("x", 8.5),
                ("y", 8.5),
                ("z", 0.0),
            ]
        ),
        "hy": OrderedDict(
            [
                ("acqchan", "CH4"),
                ("azm", 90.0),
                ("chtype", "HY"),
                ("dip", 0.0),
                ("id", 5372.0537),
                ("x", -8.5),
                ("y", 8.5),
                ("z", 0.0),
            ]
        ),
        "hz": OrderedDict(
            [
                ("acqchan", "CH5"),
                ("azm", 0.0),
                ("chtype", "HZ"),
                ("dip", 0.0),
                ("id", 5373.0537),
                ("x", 21.2),
                ("y", -21.2),
                ("z", 0.0),
            ]
        ),
        "rrhx": OrderedDict(
            [
                ("acqchan", "CH6"),
                ("azm", 0.0),
                ("chtype", "RRHX"),
                ("dip", 0.0),
                ("id", 5376.0537),
                ("x", 8.5),
                ("y", 45008.5),
                ("z", 0.0),
            ]
        ),
        "rrhy": OrderedDict(
            [
                ("acqchan", "CH7"),
                ("azm", 90.0),
                ("chtype", "RRHY"),
                ("dip", 0.0),
                ("id", 5377.0537),
                ("x", -8.5),
                ("y", 45008.5),
                ("z", 0.0),
            ]
        ),
    }


@pytest.fixture(scope="module")
def expected_measurement_output():
    """Expected measurement output for Phoenix EDI testing."""
    return [
        "\n>=DEFINEMEAS\n",
        "    MAXCHAN=7\n",
        "    MAXRUN=999\n",
        "    MAXMEAS=7\n",
        "    REFLAT=-22:49:25.400000\n",
        "    REFLON=139:17:40.900000\n",
        "    REFELEV=158.0\n",
        "    REFTYPE=CART\n",
        "    UNITS=meter\n",
        "\n",
        ">HMEAS ID=5371.0537 CHTYPE=HX X=8.50 Y=8.50 Z=0.00 AZM=0.00 DIP=0.00 ACQCHAN=CH3\n",
        ">HMEAS ID=5372.0537 CHTYPE=HY X=-8.50 Y=8.50 Z=0.00 AZM=90.00 DIP=0.00 ACQCHAN=CH4\n",
        ">HMEAS ID=5373.0537 CHTYPE=HZ X=21.20 Y=-21.20 Z=0.00 AZM=0.00 DIP=0.00 ACQCHAN=CH5\n",
        ">EMEAS ID=5374.0537 CHTYPE=EX X=-50.00 Y=-0.00 Z=0.00 X2=50.00 Y2=0.00 Z2=0.00 AZM=0.00 ACQCHAN=CH1\n",
        ">EMEAS ID=5375.0537 CHTYPE=EY X=22.40 Y=-44.70 Z=0.00 X2=-22.40 Y2=44.70 Z2=0.00 AZM=116.62 ACQCHAN=CH2\n",
        ">HMEAS ID=5376.0537 CHTYPE=RRHX X=8.50 Y=45008.50 Z=0.00 AZM=0.00 DIP=0.00 ACQCHAN=CH6\n",
        ">HMEAS ID=5377.0537 CHTYPE=RRHY X=-8.50 Y=45008.50 Z=0.00 AZM=90.00 DIP=0.00 ACQCHAN=CH7\n",
    ]


@pytest.fixture(scope="module")
def expected_data_section():
    """Expected data section for Phoenix EDI testing."""
    return OrderedDict(
        [
            ("ex", "5374.0537"),
            ("ey", "5375.0537"),
            ("hx", "5371.0537"),
            ("hy", "5372.0537"),
            ("hz", "5373.0537"),
            ("maxblocks", 999),
            ("nchan", 7),
            ("nfreq", 80),
            ("rrhx", "5376.0537"),
            ("rrhy", "5377.0537"),
            ("sectid", "14-IEB0537A"),
        ]
    )


# =============================================================================
# Test Classes
# =============================================================================
class TestPhoenixEDI:
    """Test class for Phoenix EDI functionality using pytest."""

    @pytest.mark.parametrize(
        "key,expected_value",
        [
            ("acqby", "Phoenix"),
            ("acqdate", "2014-07-28T00:00:00+00:00"),
            ("coordinate_system", "geographic"),
            ("dataid", "14_IEB0537A"),
            ("datum", "WGS 84"),
            ("elevation", 158.0),
            ("fileby", "Phoenix"),
            ("filedate", "2014-08-01"),
            ("latitude", -22.823722222222223),
            ("longitude", 139.29469444444445),
            ("progdate", "2010-03-09"),
            ("progname", "mt_metadata"),
            ("progvers", "MT-Editor Ver 0.99.2.106"),
            ("stdvers", "SEG 1.0"),
        ],
    )
    def test_header_attributes(self, phoenix_edi_object, key, expected_value):
        """Test header attributes using parametrization."""
        h_value = getattr(phoenix_edi_object.Header, key.lower())
        assert h_value == expected_value

    def test_header_phoenix_flag(self, phoenix_edi_object):
        """Test that Phoenix EDI flag is set correctly."""
        assert phoenix_edi_object.Header.phoenix_edi is True

    def test_info(self, phoenix_edi_object, expected_info):
        """Test info dictionary."""
        assert phoenix_edi_object.Info.info_dict == expected_info

    @pytest.mark.parametrize("channel", ["ex", "ey", "hx", "hy", "hz", "rrhx", "rrhy"])
    def test_measurement_channels(
        self, phoenix_edi_object, expected_measurement_channels, channel
    ):
        """Test individual measurement channels using parametrization."""
        expected = expected_measurement_channels[channel]
        actual = phoenix_edi_object.Measurement.measurements[channel].to_dict(
            single=True
        )
        assert actual == expected

    def test_measurement_output(self, phoenix_edi_object, expected_measurement_output):
        """Test measurement write output."""
        actual_output = phoenix_edi_object.Measurement.write_measurement()
        assert actual_output == expected_measurement_output

    @pytest.mark.parametrize(
        "attr,expected,precision",
        [
            ("reflat", -22.82372, 5),
            ("reflon", 139.294694, 5),
            ("refelev", 158.0, 2),
        ],
    )
    def test_measurement_reference_values(
        self, phoenix_edi_object, attr, expected, precision
    ):
        """Test measurement reference values with specified precision."""
        actual = getattr(phoenix_edi_object.Measurement, attr)
        assert abs(actual - expected) < 10 ** (-precision)

    def test_data_section(self, phoenix_edi_object, expected_data_section):
        """Test data section properties."""
        assert phoenix_edi_object.Data.to_dict(single=True) == expected_data_section

    @pytest.mark.parametrize("channel", ["hx", "hy", "hz", "ex", "ey", "rrhx", "rrhy"])
    def test_data_section_channel_ids(
        self, phoenix_edi_object, expected_data_section, channel
    ):
        """Test data section channel IDs match expected values."""
        expected_id = expected_data_section[channel]
        actual_id = getattr(phoenix_edi_object.Data, channel)
        assert str(float(expected_id)) == actual_id


class TestToTF:
    """Test class for EDI to TF conversion."""

    def test_station_metadata(self, phoenix_edi_object, phoenix_tf_object):
        """Test station metadata conversion from EDI to TF."""
        edi_st = phoenix_edi_object.station_metadata.to_dict(single=True)
        tf_st = phoenix_tf_object.station_metadata.to_dict(single=True)

        for edi_key, edi_value in edi_st.items():
            assert (
                edi_value == tf_st[edi_key]
            ), f"Station metadata mismatch for {edi_key}"

    def test_survey_metadata(self, phoenix_edi_object, phoenix_tf_object):
        """Test survey metadata conversion from EDI to TF."""
        edi_st = phoenix_edi_object.survey_metadata.to_dict(single=True)
        tf_st = phoenix_tf_object.survey_metadata.to_dict(single=True)

        for edi_key, edi_value in edi_st.items():
            assert (
                edi_value == tf_st[edi_key]
            ), f"Survey metadata mismatch for {edi_key}"

    @pytest.mark.parametrize(
        "method,expected",
        [
            ("has_impedance", True),
            ("has_tipper", True),
            ("has_inverse_signal_power", True),
            ("has_residual_covariance", True),
        ],
    )
    def test_tf_properties(self, phoenix_tf_object, method, expected):
        """Test TF object properties using parametrization."""
        result = getattr(phoenix_tf_object, method)()
        assert result == expected

    def test_impedance_error_non_zero(self, phoenix_tf_object):
        """Test that impedance errors are non-zero."""
        assert (phoenix_tf_object.impedance_error.data != 0).all()


class TestFromTF:
    """Test class for TF to EDI conversion."""

    def test_station_metadata(self, phoenix_tf_object, phoenix_tf_to_edi_object):
        """Test station metadata conversion from TF to EDI."""
        edi_st = phoenix_tf_to_edi_object.station_metadata.to_dict(single=True)
        tf_st = phoenix_tf_object.station_metadata.to_dict(single=True, required=False)

        for edi_key, edi_value in edi_st.items():
            if edi_key in ["comments"]:
                # Comments are expected to be different
                assert (
                    edi_value != tf_st[edi_key]
                ), f"Comments should be different for {edi_key}"
            else:
                assert (
                    edi_value == tf_st[edi_key]
                ), f"Station metadata mismatch for {edi_key}"

    def test_survey_metadata(self, phoenix_tf_object, phoenix_tf_to_edi_object):
        """Test survey metadata conversion from TF to EDI."""
        edi_st = phoenix_tf_to_edi_object.survey_metadata.to_dict(single=True)
        tf_st = phoenix_tf_object.survey_metadata.to_dict(single=True)

        for edi_key, edi_value in edi_st.items():
            assert (
                edi_value == tf_st[edi_key]
            ), f"Survey metadata mismatch for {edi_key}"

    @pytest.mark.parametrize(
        "method,expected",
        [
            ("has_impedance", True),
            ("has_tipper", True),
            ("has_inverse_signal_power", True),
            ("has_residual_covariance", True),
        ],
    )
    def test_tf_properties(self, phoenix_tf_object, method, expected):
        """Test TF object properties using parametrization."""
        result = getattr(phoenix_tf_object, method)()
        assert result == expected

    def test_impedance_error_non_zero(self, phoenix_tf_object):
        """Test that impedance errors are non-zero."""
        assert (phoenix_tf_object.impedance_error.data != 0).all()


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__])
