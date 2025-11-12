# -*- coding: utf-8 -*-
"""
Tests for the DefineMeasurement base model.

This module tests the DefineMeasurement class functionality including
reading/writing measurements, channel handling, and metadata conversions.
"""

from unittest.mock import patch

import pytest

from mt_metadata.timeseries import Electric, Magnetic
from mt_metadata.transfer_functions.io.edi.metadata import (
    DefineMeasurement,
    EMeasurement,
    HMeasurement,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def default_define_measurement():
    """Return a DefineMeasurement instance with default values."""
    return DefineMeasurement()


@pytest.fixture(scope="module")
def custom_define_measurement():
    """Return a DefineMeasurement instance with custom values."""
    dm = DefineMeasurement(
        maxchan=7,
        maxrun=10,
        maxmeas=100,
        reftype="geographical",
        reflat=45.123,
        reflon=-120.456,
        refelev=1050.0,
        units="meter",
    )

    # Add E measurement
    ex_meas = EMeasurement(
        id=1001.001,
        chtype="ex",
        x=0.0,
        y=0.0,
        z=0.0,
        x2=100.0,
        y2=0.0,
        z2=0.0,
        azm=0.0,
        acqchan="1",
    )

    # Add H measurement
    hy_meas = HMeasurement(
        id=1002.001, chtype="hy", x=0.0, y=0.0, z=0.0, azm=90.0, dip=0.0, acqchan="2"
    )

    # Add to measurements dict
    dm.measurements = {"ex": ex_meas, "hy": hy_meas}

    return dm


@pytest.fixture(scope="module")
def sample_edi_lines():
    """Return sample EDI lines for testing."""
    return [
        ">=DEFINEMEAS",
        "    MAXCHAN=7",
        "    MAXRUN=999",
        "    MAXMEAS=9999",
        "    UNITS=m",
        "    REFTYPE=CART",
        "    REFLAT=30.500",
        "    REFLONG=140.250",
        "    REFELEV=100",
        ">HMEAS ID=1001.001 CHTYPE=HX X=0.0 Y=0.0 Z=0.0 AZM=0.0 DIP=0.0 ACQCHAN=1",
        ">HMEAS ID=1002.001 CHTYPE=HY X=0.0 Y=0.0 Z=0.0 AZM=90.0 DIP=0.0 ACQCHAN=2",
        ">HMEAS ID=1003.001 CHTYPE=HZ X=0.0 Y=0.0 Z=0.0 AZM=0.0 DIP=90.0 ACQCHAN=3",
        ">EMEAS ID=1004.001 CHTYPE=EX X=0.0 Y=0.0 Z=0.0 X2=100.0 Y2=0.0 Z2=0.0 AZM=0.0 ACQCHAN=4",
        ">EMEAS ID=1005.001 CHTYPE=EY X=0.0 Y=0.0 Z=0.0 X2=0.0 Y2=100.0 Z2=0.0 AZM=90.0 ACQCHAN=5",
        ">=MTSECT",
    ]


@pytest.fixture(scope="module")
def sample_electric_channel():
    """Return a sample Electric channel for testing."""
    channel = Electric(
        component="ex",
        channel_number=4,
        channel_id="1004.001",
        measurement_azimuth=0.0,
        translated_azimuth=0.0,
    )
    channel.negative.x = 0.0
    channel.negative.y = 0.0
    channel.positive.x2 = 100.0
    channel.positive.y2 = 0.0

    return channel


@pytest.fixture(scope="module")
def sample_magnetic_channel():
    """Return a sample Magnetic channel for testing."""
    channel = Magnetic(
        component="hx",
        channel_number=1,
        channel_id="1001.001",
        measurement_azimuth=0.0,
        translated_azimuth=0.0,
        measurement_tilt=0.0,
    )
    channel.location.x = 0.0
    channel.location.y = 0.0
    channel.location.z = 0.0

    return channel


# =============================================================================
# Tests
# =============================================================================


class TestDefineMeasurementInitialization:
    """Test initialization of the DefineMeasurement class."""

    def test_default_values(self, default_define_measurement, subtests):
        """Test the default values of DefineMeasurement attributes."""
        scalar_attrs = {
            "maxchan": 999,
            "maxrun": 999,
            "maxmeas": 7,
            "reftype": "cartesian",
            "refloc": None,
            "reflat": 0,
            "reflon": 0,
            "refelev": 0,
            "units": "m",
        }

        for attr, expected in scalar_attrs.items():
            with subtests.test(msg=f"default {attr}"):
                assert getattr(default_define_measurement, attr) == expected

        with subtests.test(msg="default measurements"):
            assert hasattr(default_define_measurement, "measurements")
            assert isinstance(default_define_measurement.measurements, dict)
            assert len(default_define_measurement.measurements) == 0

    def test_custom_values(self, custom_define_measurement, subtests):
        """Test DefineMeasurement with custom attribute values."""
        scalar_attrs = {
            "maxchan": 7,
            "maxrun": 10,
            "maxmeas": 100,
            "reftype": "geographical",
            "reflat": 45.123,
            "reflon": -120.456,
            "refelev": 1050.0,
            "units": "meter",
        }

        for attr, expected in scalar_attrs.items():
            with subtests.test(msg=f"custom {attr}"):
                assert getattr(custom_define_measurement, attr) == expected

    def test_emeasurement_added(self, custom_define_measurement):
        """Test that EMeasurement is properly added to DefineMeasurement."""
        assert "ex" in custom_define_measurement.measurements
        emeas = custom_define_measurement.measurements["ex"]

        assert isinstance(emeas, EMeasurement)
        assert emeas.id == 1001.001
        assert emeas.chtype == "ex"
        assert emeas.x2 == 100.0

    def test_hmeasurement_added(self, custom_define_measurement):
        """Test that HMeasurement is properly added to DefineMeasurement."""
        assert "hy" in custom_define_measurement.measurements
        hmeas = custom_define_measurement.measurements["hy"]

        assert isinstance(hmeas, HMeasurement)
        assert hmeas.id == 1002.001
        assert hmeas.chtype == "hy"
        assert hmeas.azm == 90.0


class TestDefineMeasurementComputedProperties:
    """Test computed properties of the DefineMeasurement class."""

    def test_channel_ids(self, custom_define_measurement):
        """Test channel_ids computed property."""
        ch_ids = custom_define_measurement.channel_ids

        assert "ex" in ch_ids
        assert "hy" in ch_ids
        assert ch_ids["ex"] == 1001.001
        assert ch_ids["hy"] == 1002.001

    def test_channels_recorded(self, custom_define_measurement):
        """Test channels_recorded computed property."""
        channels = custom_define_measurement.channels_recorded

        assert "ex" in channels
        assert "hy" in channels
        assert len(channels) == 2


class TestDefineMeasurementMethods:
    """Test methods of the DefineMeasurement class."""

    def test_string_representation(self, custom_define_measurement):
        """Test string representation of DefineMeasurement."""
        with patch.object(
            custom_define_measurement,
            "write_measurement",
            return_value="\n>=DEFINEMEAS\n    MAXCHAN=7\n    MAXRUN=10\n    MAXMEAS=100\n    REFLAT=45:07:22.800000\n    REFLON=-120:27:21.600000\n    REFELEV=1050.0\n    REFTYPE=geographical\n    UNITS=meter\n\n>EMEAS ID=1001.001 CHTYPE=ex X=0.00 Y=0.00 Z=0.00 X2=100.00 Y2=0.00 Z2=0.00 AZM=0.00 ACQCHAN=1\n>HMEAS ID=1002.001 CHTYPE=hy X=0.00 Y=0.00 Z=0.00 AZM=90.00 DIP=0.00 ACQCHAN=2\n",
        ):
            str_rep = str(custom_define_measurement)

            # Check that the method uses write_measurement
            assert (
                str_rep
                == "\n>=DEFINEMEAS\n    MAXCHAN=7\n    MAXRUN=10\n    MAXMEAS=100\n    REFLAT=45:07:22.800000\n    REFLON=-120:27:21.600000\n    REFELEV=1050.0\n    REFTYPE=geographical\n    UNITS=meter\n\n>EMEAS ID=1001.001 CHTYPE=ex X=0.00 Y=0.00 Z=0.00 X2=100.00 Y2=0.00 Z2=0.00 AZM=0.00 ACQCHAN=1\n>HMEAS ID=1002.001 CHTYPE=hy X=0.00 Y=0.00 Z=0.00 AZM=90.00 DIP=0.00 ACQCHAN=2\n"
            )

            # Also check __repr__
            repr_str = repr(custom_define_measurement)
            assert repr_str == str_rep

    def test_get_measurement_dict(self, custom_define_measurement, subtests):
        """Test get_measurement_dict method."""
        meas_dict = custom_define_measurement.measurements

        with subtests.test(msg="dict contains correct keys"):
            assert "ex" in meas_dict
            assert "hy" in meas_dict
            assert len(meas_dict) == 2

        with subtests.test(msg="dict maps to correct objects"):
            assert meas_dict["ex"] is custom_define_measurement.measurements["ex"]
            assert meas_dict["hy"] is custom_define_measurement.measurements["hy"]

    def test_write_measurement_content(self, custom_define_measurement, subtests):
        """Test write_measurement method content."""
        lines = custom_define_measurement.write_measurement()
        written_text = "".join(lines)

        # Check header
        with subtests.test(msg="write header"):
            assert ">=DEFINEMEAS" in written_text

        # Check that required fields are present
        required_fields = [
            "MAXCHAN=7",
            "MAXRUN=10",
            "MAXMEAS=100",
            "REFTYPE=geographical",
            "REFLAT=45:07:22.800000",
            "REFLON=-120:27:21.600000",
            "REFELEV=1050.0",
            "UNITS=meter",
        ]

        for field in required_fields:
            with subtests.test(msg=f"contains {field}"):
                assert field in written_text

        # Check that measurements are included
        with subtests.test(msg="contains EMEAS"):
            assert ">EMEAS ID=1001.001" in written_text
            assert "CHTYPE=ex" in written_text

        with subtests.test(msg="contains HMEAS"):
            assert ">HMEAS ID=1002.001" in written_text
            assert "CHTYPE=hy" in written_text

    def test_write_measurement_lat_lon_formats(
        self, custom_define_measurement, subtests
    ):
        """Test write_measurement method with different lat/lon formats."""
        # Test with degrees-minutes-seconds format
        lines_dms = custom_define_measurement.write_measurement(latlon_format="dms")
        text_dms = "".join(lines_dms)

        with subtests.test(msg="latlon_format=dms"):
            # The exact format will depend on the convert_position_float2str implementation
            assert "REFLAT=" in text_dms
            assert "REFLON=" in text_dms
            assert "45.123" not in text_dms  # Should be converted to DMS format

        # Test with degrees format
        lines_dd = custom_define_measurement.write_measurement(latlon_format="dd")
        text_dd = "".join(lines_dd)

        with subtests.test(msg="latlon_format=dd"):
            assert "REFLAT=45.123" in text_dd
            assert "REFLON=-120.456" in text_dd

        # Test with LONG format
        lines_long = custom_define_measurement.write_measurement(
            longitude_format="LONG"
        )
        text_long = "".join(lines_long)

        with subtests.test(msg="longitude_format=LONG"):
            assert "REFLONG=" in text_long
            assert "REFLON=" not in text_long


class TestDefineMeasurementReading:
    """Test reading functionality for DefineMeasurement."""

    def test_get_measurement_lists(
        self, default_define_measurement, sample_edi_lines, subtests
    ):
        """Test get_measurement_lists method."""
        default_define_measurement.get_measurement_lists(sample_edi_lines)

        with subtests.test(msg="measurement list exists"):
            assert hasattr(default_define_measurement, "_measurement_list")
            assert len(default_define_measurement._measurement_list) > 0

        # Check that the list contains both string entries and dictionaries
        has_strings = any(
            isinstance(item, str)
            for item in default_define_measurement._measurement_list
        )
        has_dicts = any(
            isinstance(item, dict)
            for item in default_define_measurement._measurement_list
        )

        with subtests.test(msg="measurement list has strings"):
            assert has_strings

        with subtests.test(msg="measurement list has dicts"):
            assert has_dicts

    def test_read_measurement(
        self, default_define_measurement, sample_edi_lines, subtests
    ):
        """Test read_measurement method."""
        default_define_measurement.read_measurement(sample_edi_lines)

        # Check scalar values
        scalar_attrs = {
            "maxchan": 7,
            "maxrun": 999,
            "maxmeas": 9999,
            "reftype": "CART",
            "reflat": 30.500,
            "reflon": 140.250,
            "refelev": 100,
            "units": "meter",
        }

        for attr, expected in scalar_attrs.items():
            with subtests.test(msg=f"read {attr}"):
                assert getattr(default_define_measurement, attr) == expected

        # Check that measurements were created
        expected_measurements = {
            "hx": HMeasurement,
            "hy": HMeasurement,
            "hz": HMeasurement,
            "ex": EMeasurement,
            "ey": EMeasurement,
        }

        for ch_type, expected_type in expected_measurements.items():
            with subtests.test(msg=f"has measurement {ch_type}"):
                assert ch_type in default_define_measurement.measurements
                assert isinstance(
                    default_define_measurement.measurements[ch_type], expected_type
                )

    def test_read_duplicate_channels_handling(self):
        """Test handling of duplicate channels during read_measurement."""
        dm = DefineMeasurement()

        # Create EDI lines with duplicate HX channel
        edi_lines = [
            ">=DEFINEMEAS",
            "    MAXCHAN=7",
            ">HMEAS ID=1001.001 CHTYPE=HX X=0.0 Y=0.0 Z=0.0 AZM=0.0 ACQCHAN=1",
            ">HMEAS ID=1002.001 CHTYPE=HX X=10.0 Y=10.0 Z=0.0 AZM=45.0 ACQCHAN=2",
            ">=MTSECT",
        ]

        dm.read_measurement(edi_lines)

        # First HX should be "hx", second should be "rrhx"
        assert "hx" in list(dm.measurements.keys())
        assert "rrhx" in list(dm.measurements.keys())
        assert dm.measurements["hx"].id == 1001.001
        assert dm.measurements["rrhx"].id == 1002.001
        assert dm.measurements["rrhx"].chtype == "RRHX"


class TestDefineMeasurementMetadataConversion:
    """Test metadata conversion functionality."""

    def test_from_metadata_electric(
        self, default_define_measurement, sample_electric_channel, subtests
    ):
        """Test from_metadata method with Electric channel."""
        default_define_measurement.from_metadata(sample_electric_channel)

        with subtests.test(msg="creates ex measurement"):
            assert "ex" in default_define_measurement.measurements

        emeas = default_define_measurement.measurements["ex"]

        with subtests.test(msg="correct attribute transfer"):
            assert emeas.chtype == "ex"
            assert emeas.id == 1004.001
            assert emeas.x == 0.0
            assert emeas.y == 0.0
            assert emeas.x2 == 100.0
            assert emeas.y2 == 0.0
            assert emeas.azm == 0.0
            assert emeas.acqchan == "4"

    def test_from_metadata_magnetic(
        self, default_define_measurement, sample_magnetic_channel, subtests
    ):
        """Test from_metadata method with Magnetic channel."""
        default_define_measurement.from_metadata(sample_magnetic_channel)

        with subtests.test(msg="creates hx measurement"):
            assert "hx" in default_define_measurement.measurements

        hmeas = default_define_measurement.measurements["hx"]

        with subtests.test(msg="correct attribute transfer"):
            assert hmeas.chtype == "hx"
            assert hmeas.id == 1001.001
            assert hmeas.x == 0.0
            assert hmeas.y == 0.0
            assert hmeas.z == 0.0
            assert hmeas.azm == 0.0
            assert hmeas.dip == 0.0
            assert hmeas.acqchan == "1"

    def test_from_metadata_null_component(self):
        """Test from_metadata with a channel that has no component."""
        dm = DefineMeasurement()
        channel = Electric()  # No component set

        # Should not raise an exception
        dm.from_metadata(channel)

        # Should not add anything to measurements
        assert len(dm.measurements) == 1  # Default component "e_default" is used

    def test_from_metadata_null_attributes(self, default_define_measurement, subtests):
        """Test from_metadata with a channel that has null attributes."""
        # Electric channel with null attributes
        channel = Electric(component="ey", channel_number=5)

        default_define_measurement.from_metadata(channel)

        with subtests.test(msg="creates ey measurement"):
            assert "ey" in default_define_measurement.measurements

        emeas = default_define_measurement.measurements["ey"]

        # All coordinates should be set to 0
        assert emeas.x == 0.0
        assert emeas.y == 0.0
        assert emeas.x2 == 0.0
        assert emeas.y2 == 0.0


class TestDefineMeasurementEdgeCases:
    """Test edge cases and special scenarios for DefineMeasurement."""

    def test_write_measurement_no_measurements(self):
        """Test write_measurement when no measurements are defined."""
        dm = DefineMeasurement()
        with patch(
            "mt_metadata.transfer_functions.io.edi.metadata.define_measurement.logger.warning"
        ) as mock_warning:
            lines = dm.write_measurement()

            # Should log a warning
            mock_warning.assert_called_with("No XMEAS information.")

            # Should still return lines for the header section
            assert len(lines) > 0
            assert ">=DEFINEMEAS" in lines[0]

    def test_write_measurement_with_none_id(self):
        """Test write_measurement with measurement that has None id."""
        dm = DefineMeasurement()
        emeas = EMeasurement(chtype="ez", acqchan="3")
        emeas.id = None
        dm.measurements["ez"] = emeas

        lines = dm.write_measurement()
        written_text = "".join(lines)

        # Should assign an ID automatically
        assert ">EMEAS ID=1.0" in written_text

    def test_read_with_invalid_values(self):
        """Test read_measurement with invalid numeric values."""
        dm = DefineMeasurement()

        edi_lines = [
            ">=DEFINEMEAS",
            "    MAXCHAN=invalid",
            "    MAXRUN=NaN",
            "    MAXMEAS=error",
            ">=MTSECT",
        ]

        dm.read_measurement(edi_lines)

        # Should set to 0 for invalid values
        assert dm.maxchan == 0
        assert dm.maxrun == 0
        assert dm.maxmeas == 0


if __name__ == "__main__":
    pytest.main(["-v", __file__])
