# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

from collections import OrderedDict

# =============================================================================
#
# =============================================================================
import pytest

from mt_metadata import TF_EDI_CGG
from mt_metadata.common.mttime import MTime
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io import edi


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture(scope="module")
def cgg_edi_obj():
    """Fixture to create EDI object once per module."""
    return edi.EDI(fn=TF_EDI_CGG)


@pytest.fixture(scope="module")
def cgg_tf_obj():
    """Fixture to create TF object once per module."""
    tf_obj = TF(TF_EDI_CGG)
    tf_obj.read()
    return tf_obj


@pytest.fixture(scope="module")
def cgg_tf_edi_obj(cgg_tf_obj):
    """Fixture to create EDI object from TF object once per module."""
    return cgg_tf_obj.to_edi()


# =============================================================================
# CGG EDI Tests
# =============================================================================
class TestCGGEDI:
    """Test CGG EDI file parsing."""

    def test_header(self, cgg_edi_obj):
        """Test header values."""
        head = {
            "ACQBY": "GSC_CGG",
            "COORDINATE_SYSTEM": "geographic",
            "DATAID": "TEST01",
            "DATUM": "WGS 84",
            "ELEV": 175.270,
            "EMPTY": 1.000000e32,
            "FILEBY": "",
            "LAT": -30.930285,
            "LOC": "Australia",
            "LON": 127.22923,
        }

        for key, value in head.items():
            if key == "ELEV":
                key = "elevation"
            elif key == "LAT":
                key = "latitude"
            elif key == "LON":
                key = "longitude"
            h_value = getattr(cgg_edi_obj.Header, key.lower())
            assert (
                h_value == value
            ), f"Header {key} mismatch: expected {value}, got {h_value}"

    def test_header_acquire_date(self, cgg_edi_obj):
        """Test acquire date."""
        assert cgg_edi_obj.Header.acqdate == MTime(time_stamp="06/05/14")

    def test_header_units(self, cgg_edi_obj):
        """Test units."""
        assert cgg_edi_obj.Header.units != "milliVolt per kilometer per nanoTesla"

    def test_info(self, cgg_edi_obj):
        """Test info section."""
        info_list = [
            ">INFO\n",
            "    maxinfo=31\n",
            "    /*\n",
            "    site info\n",
            "    run.acquired_by.author=Somebody\n",
            "    run.data_logger.id=222\n",
            "    run.ex.measurement_azimuth=0.0\n",
            "    run.ex.dipole_length=100.0\n",
            "    run.ey.dipole_length=100.0\n",
            "    run.ex.contact_resistance.start=44479800\n",
            "    run.ey.contact_resistance.start=41693800\n",
            "    h_site=E_SITE\n",
            "    run.hx.measurement_azimuth=0.0\n",
            "    run.hx.sensor.id=MFS06e-246\n",
            "    run.hy.sensor.id=MFS06e-249\n",
            "    run.hz.sensor.id=MFS06e-249\n",
            "    run.hx.h_field_max.start=169869\n",
            "    run.hy.h_field_max.start=164154\n",
            "    run.hz.h_field_max.start=2653\n",
            "    processing parameters\n",
            "    transfer_function.software.name=L13ss\n",
            "    transfer_function.processing_parameters=[ndec=1, nfft=128, ntype=1, rrtype=None, removelargelines=true, rotmaxe=false]\n",
            "    */\n",
        ]

        assert info_list == cgg_edi_obj.Info.write_info()

    @pytest.mark.parametrize(
        "channel,expected",
        [
            (
                "ex",
                OrderedDict(
                    [
                        ("acqchan", ""),
                        ("azm", 0.0),
                        ("chtype", "EX"),
                        ("id", 1004.001),
                        ("x", 0.0),
                        ("x2", 0.0),
                        ("y", 0.0),
                        ("y2", 0.0),
                        ("z", 0.0),
                        ("z2", 0.0),
                    ]
                ),
            ),
            (
                "ey",
                OrderedDict(
                    [
                        ("acqchan", ""),
                        ("azm", 0.0),
                        ("chtype", "EY"),
                        ("id", 1005.001),
                        ("x", 0.0),
                        ("x2", 0.0),
                        ("y", 0.0),
                        ("y2", 0.0),
                        ("z", 0.0),
                        ("z2", 0.0),
                    ]
                ),
            ),
            (
                "hx",
                OrderedDict(
                    [
                        ("acqchan", ""),
                        ("azm", 0.0),
                        ("chtype", "HX"),
                        ("dip", 0.0),
                        ("id", 1001.001),
                        ("x", 0.0),
                        ("y", 0.0),
                        ("z", 0.0),
                    ]
                ),
            ),
            (
                "hy",
                OrderedDict(
                    [
                        ("acqchan", ""),
                        ("azm", 90.0),
                        ("chtype", "HY"),
                        ("dip", 0.0),
                        ("id", 1002.001),
                        ("x", 0.0),
                        ("y", 0.0),
                        ("z", 0.0),
                    ]
                ),
            ),
            (
                "hz",
                OrderedDict(
                    [
                        ("acqchan", ""),
                        ("azm", 0.0),
                        ("chtype", "HZ"),
                        ("dip", 0.0),
                        ("id", 1003.001),
                        ("x", 0.0),
                        ("y", 0.0),
                        ("z", 0.0),
                    ]
                ),
            ),
            (
                "rrhx",
                OrderedDict(
                    [
                        ("acqchan", ""),
                        ("azm", 0.0),
                        ("chtype", "RRHX"),
                        ("dip", 0.0),
                        ("id", 1006.001),
                        ("x", 0.0),
                        ("y", 0.0),
                        ("z", 0.0),
                    ]
                ),
            ),
            (
                "rrhy",
                OrderedDict(
                    [
                        ("acqchan", ""),
                        ("azm", 90.0),
                        ("chtype", "RRHY"),
                        ("dip", 0.0),
                        ("id", 1007.001),
                        ("x", 0.0),
                        ("y", 0.0),
                        ("z", 0.0),
                    ]
                ),
            ),
        ],
    )
    def test_measurement_channels(self, cgg_edi_obj, channel, expected):
        """Test measurement channels using parametrize for efficiency."""
        assert expected == cgg_edi_obj.Measurement.measurements[channel].to_dict(
            single=True
        )

    def test_measurement_metadata(self, cgg_edi_obj):
        """Test measurement metadata."""
        m_list = [
            '    REFLOC="TEST01"\n',
            "    REFLAT=-30:55:49.026000\n",
            "    REFLON=127:13:45.228000\n",
            "    REFELEV=175.27\n",
            "    REFTYPE=cartesian\n",
            "    UNITS=meter\n",
        ]

        assert (
            m_list == cgg_edi_obj.Measurement.write_measurement()[4 : 4 + len(m_list)]
        )

    @pytest.mark.parametrize(
        "attr,expected,precision",
        [
            ("reflat", -30.930285, 5),
            ("reflon", 127.22923, 5),
            ("refelev", 175.27, 2),
        ],
    )
    def test_measurement_coordinates(self, cgg_edi_obj, attr, expected, precision):
        """Test measurement coordinates with different precisions."""
        actual = getattr(cgg_edi_obj.Measurement, attr)
        assert abs(actual - expected) < 10 ** (
            -precision
        ), f"{attr} mismatch: expected {expected}, got {actual}"

    @pytest.mark.parametrize(
        "array_type,expected_shape",
        [
            ("z", (73, 2, 2)),
            ("z_err", (73, 2, 2)),
            ("t", (73, 1, 2)),
            ("t_err", (73, 1, 2)),
            ("rotation_angle", (73,)),
        ],
    )
    def test_array_shapes(self, cgg_edi_obj, array_type, expected_shape):
        """Test array shapes."""
        array = getattr(cgg_edi_obj, array_type)
        assert array.shape == expected_shape

    def test_impedance_values(self, cgg_edi_obj):
        """Test impedance values."""
        # Test has zero
        assert cgg_edi_obj.z[0, 0, 0] == 0 + 0j
        # Test not zero
        assert cgg_edi_obj.z[1, 0, 0] != 0 + 0j

    def test_rotation_angle(self, cgg_edi_obj):
        """Test rotation angle."""
        assert (cgg_edi_obj.rotation_angle == 0).all()


# =============================================================================
# CGG TF Tests
# =============================================================================
class TestCGGTF:
    """Test CGG TF object functionality."""

    def test_header(self, cgg_tf_edi_obj):
        """Test header values."""
        head = {
            "ACQBY": "GSC_CGG",
            "COORDINATE_SYSTEM": "geographic",
            "DATAID": "TEST01",
            "DATUM": "WGS 84",
            "ELEV": 175.270,
            "EMPTY": 1.000000e32,
            "FILEBY": "",
            "LAT": -30.930285,
            "LOC": "Australia",
            "LON": 127.22923,
        }

        for key, value in head.items():
            if key == "ELEV":
                key = "elevation"
            elif key == "LAT":
                key = "latitude"
            elif key == "LON":
                key = "longitude"

            h_value = getattr(cgg_tf_edi_obj.Header, key.lower())
            assert (
                h_value == value
            ), f"Header {key} mismatch: expected {value}, got {h_value}"

    def test_header_acquire_date(self, cgg_tf_edi_obj):
        """Test acquire date."""
        assert cgg_tf_edi_obj.Header.acqdate == MTime(time_stamp="06/05/14")

    def test_header_units(self, cgg_tf_edi_obj):
        """Test units."""
        assert cgg_tf_edi_obj.Header.units == "milliVolt per kilometer per nanoTesla"

    def test_info(self, cgg_tf_edi_obj):
        """Test info section."""
        info_list = [
            ">INFO\n",
            "    survey.acquired_by.author=GSC_CGG\n",
            "    survey.datum=WGS 84\n",
            "    survey.geographic_name=Australia\n",
            "    survey.id=0\n",
            "    survey.project=EGC\n",
            "    survey.release_license=CC-BY-4.0\n",
            "    transfer_function.coordinate_system=geographic\n",
            "    transfer_function.id=TEST01\n",
            "    transfer_function.processed_date=2014-10-07T00:00:00+00:00\n",
            "    transfer_function.processing_parameters.ndec=1\n",
            "    transfer_function.processing_parameters.nfft=128\n",
            "    transfer_function.processing_parameters.ntype=1\n",
            "    transfer_function.processing_parameters.rrtype=None\n",
            "    transfer_function.processing_parameters.removelargelines=true\n",
            "    transfer_function.processing_parameters.rotmaxe=false\n",
            "    transfer_function.remote_references=[]\n",
            "    transfer_function.runs_processed=[TEST01a]\n",
            "    transfer_function.sign_convention=+\n",
            "    transfer_function.software.name=L13ss\n",
            "    transfer_function.units=milliVolt per kilometer per nanoTesla\n",
            "    provenance.creation_time=2014-10-07T00:00:00+00:00\n",
            "    provenance.software.version=Antlr3.Runtime:3.5.0.2;ContourEngine:1.0.41.8272;CoordinateSystemService:1.4.0.8439;DocumentCommon:1.4.0.8465;Fluent:2.1.0.0;GeoApi:1.7.0.0;hasp_net_windows:7.0.1.36183;Launcher:1.4.0.8471;MapDocument:1.4.0.8469;MTDocument:1.4.0.8459;MTDocumentDataProvider:1.4.0.8467;MTInversionCommon:1.4.0.8371;Ookii.Dialogs.Wpf:1.0.0.0;PlotElement:1.4.0.8466;PluginHost:1.4.0.8440;ProjNet:1.2.5085.21309;ShellEngine:1.4.0.8380;System.Windows.Interactivity:4.0.0.0;Utils:1.4.0.8449;Xceed.Wpf.AvalonDock:2.0.0.0;Xceed.Wpf.AvalonDock.Themes.Aero:2.0.0.0;Xceed.Wpf.Toolkit:1.9.0.0;\n",
            "    TEST01a.acquired_by.author=Somebody\n",
            "    TEST01a.channels_recorded_auxiliary=[rrhx, rrhy]\n",
            "    TEST01a.channels_recorded_electric=[ex, ey]\n",
            "    TEST01a.channels_recorded_magnetic=[hx, hy, hz]\n",
            "    TEST01a.data_logger.id=222\n",
            "    TEST01a.data_logger.power_source.voltage.end=0.0\n",
            "    TEST01a.data_logger.power_source.voltage.start=0.0\n",
            "    TEST01a.data_logger.timing_system.drift=0.0\n",
            "    TEST01a.data_logger.timing_system.type=GPS\n",
            "    TEST01a.data_logger.timing_system.uncertainty=0.0\n",
            "    TEST01a.data_type=BBMT\n",
            "    TEST01a.id=TEST01a\n",
            "    TEST01a.sample_rate=0.0\n",
            "    TEST01a.time_period.start=2014-06-05T00:00:00+00:00\n",
            "    TEST01a.hx.channel_id=1001.001\n",
            "    TEST01a.hx.channel_number=0\n",
            "    TEST01a.hx.component=hx\n",
            "    TEST01a.hx.h_field_max.end=0.0\n",
            "    TEST01a.hx.h_field_max.start=0.0\n",
            "    TEST01a.hx.h_field_min.end=0.0\n",
            "    TEST01a.hx.h_field_min.start=0.0\n",
            "    TEST01a.hx.location.datum=WGS 84\n",
            "    TEST01a.hx.measurement_azimuth=0.0\n",
            "    TEST01a.hx.measurement_tilt=0.0\n",
            "    TEST01a.hx.sensor.id=MFS06e-246\n",
            "    TEST01a.hx.sensor.type=magnetic\n",
            "    TEST01a.hx.type=magnetic\n",
            "    TEST01a.hy.channel_id=1002.001\n",
            "    TEST01a.hy.channel_number=0\n",
            "    TEST01a.hy.component=hy\n",
            "    TEST01a.hy.h_field_max.end=0.0\n",
            "    TEST01a.hy.h_field_max.start=0.0\n",
            "    TEST01a.hy.h_field_min.end=0.0\n",
            "    TEST01a.hy.h_field_min.start=0.0\n",
            "    TEST01a.hy.location.datum=WGS 84\n",
            "    TEST01a.hy.measurement_azimuth=90.0\n",
            "    TEST01a.hy.measurement_tilt=0.0\n",
            "    TEST01a.hy.sensor.id=MFS06e-249\n",
            "    TEST01a.hy.sensor.type=magnetic\n",
            "    TEST01a.hy.translated_azimuth=90.0\n",
            "    TEST01a.hy.type=magnetic\n",
            "    TEST01a.hz.channel_id=1003.001\n",
            "    TEST01a.hz.channel_number=0\n",
            "    TEST01a.hz.component=hz\n",
            "    TEST01a.hz.h_field_max.end=0.0\n",
            "    TEST01a.hz.h_field_max.start=0.0\n",
            "    TEST01a.hz.h_field_min.end=0.0\n",
            "    TEST01a.hz.h_field_min.start=0.0\n",
            "    TEST01a.hz.location.datum=WGS 84\n",
            "    TEST01a.hz.measurement_azimuth=0.0\n",
            "    TEST01a.hz.measurement_tilt=0.0\n",
            "    TEST01a.hz.sensor.id=MFS06e-249\n",
            "    TEST01a.hz.sensor.type=magnetic\n",
            "    TEST01a.hz.type=magnetic\n",
            "    TEST01a.ex.ac.end=0.0\n",
            "    TEST01a.ex.ac.start=0.0\n",
            "    TEST01a.ex.channel_id=1004.001\n",
            "    TEST01a.ex.channel_number=0\n",
            "    TEST01a.ex.component=ex\n",
            "    TEST01a.ex.contact_resistance.end=0.0\n",
            "    TEST01a.ex.contact_resistance.start=44479800.0\n",
            "    TEST01a.ex.dc.end=0.0\n",
            "    TEST01a.ex.dc.start=0.0\n",
            "    TEST01a.ex.dipole_length=100.0\n",
            "    TEST01a.ex.measurement_azimuth=0.0\n",
            "    TEST01a.ex.measurement_tilt=0.0\n",
            "    TEST01a.ex.negative.datum=WGS 84\n",
            "    TEST01a.ex.negative.type=electric\n",
            "    TEST01a.ex.positive.datum=WGS 84\n",
            "    TEST01a.ex.positive.type=electric\n",
            "    TEST01a.ex.type=electric\n",
            "    TEST01a.ey.ac.end=0.0\n",
            "    TEST01a.ey.ac.start=0.0\n",
            "    TEST01a.ey.channel_id=1005.001\n",
            "    TEST01a.ey.channel_number=0\n",
            "    TEST01a.ey.component=ey\n",
            "    TEST01a.ey.contact_resistance.end=0.0\n",
            "    TEST01a.ey.contact_resistance.start=41693800.0\n",
            "    TEST01a.ey.dc.end=0.0\n",
            "    TEST01a.ey.dc.start=0.0\n",
            "    TEST01a.ey.dipole_length=100.0\n",
            "    TEST01a.ey.measurement_azimuth=0.0\n",
            "    TEST01a.ey.measurement_tilt=0.0\n",
            "    TEST01a.ey.negative.datum=WGS 84\n",
            "    TEST01a.ey.negative.type=electric\n",
            "    TEST01a.ey.positive.datum=WGS 84\n",
            "    TEST01a.ey.positive.type=electric\n",
            "    TEST01a.ey.type=electric\n",
            "    TEST01a.rrhx.channel_id=1006.001\n",
            "    TEST01a.rrhx.channel_number=0\n",
            "    TEST01a.rrhx.component=rrhx\n",
            "    TEST01a.rrhx.location.datum=WGS 84\n",
            "    TEST01a.rrhx.measurement_azimuth=0.0\n",
            "    TEST01a.rrhx.measurement_tilt=0.0\n",
            "    TEST01a.rrhx.sensor.type=magnetic\n",
            "    TEST01a.rrhx.type=auxiliary\n",
            "    TEST01a.rrhy.channel_id=1007.001\n",
            "    TEST01a.rrhy.channel_number=0\n",
            "    TEST01a.rrhy.component=rrhy\n",
            "    TEST01a.rrhy.location.datum=WGS 84\n",
            "    TEST01a.rrhy.measurement_azimuth=90.0\n",
            "    TEST01a.rrhy.measurement_tilt=0.0\n",
            "    TEST01a.rrhy.sensor.type=magnetic\n",
            "    TEST01a.rrhy.translated_azimuth=90.0\n",
            "    TEST01a.rrhy.type=auxiliary\n",
        ]

        assert info_list == cgg_tf_edi_obj.Info.write_info()

    @pytest.mark.parametrize(
        "channel,expected",
        [
            (
                "ex",
                OrderedDict(
                    [
                        ("acqchan", "1004.001"),
                        ("azm", 0.0),
                        ("chtype", "ex"),
                        ("id", 1004.001),
                        ("x", 0.0),
                        ("x2", 0.0),
                        ("y", 0.0),
                        ("y2", 0.0),
                        ("z", 0.0),
                        ("z2", 0.0),
                    ]
                ),
            ),
            (
                "ey",
                OrderedDict(
                    [
                        ("acqchan", "1005.001"),
                        ("azm", 0.0),
                        ("chtype", "ey"),
                        ("id", 1005.001),
                        ("x", 0.0),
                        ("x2", 0.0),
                        ("y", 0.0),
                        ("y2", 0.0),
                        ("z", 0.0),
                        ("z2", 0.0),
                    ]
                ),
            ),
            (
                "hx",
                OrderedDict(
                    [
                        ("acqchan", "1001.001"),
                        ("azm", 0.0),
                        ("chtype", "hx"),
                        ("dip", 0.0),
                        ("id", 1001.001),
                        ("x", 0.0),
                        ("y", 0.0),
                        ("z", 0.0),
                    ]
                ),
            ),
            (
                "hy",
                OrderedDict(
                    [
                        ("acqchan", "1002.001"),
                        ("azm", 90.0),
                        ("chtype", "hy"),
                        ("dip", 0.0),
                        ("id", 1002.001),
                        ("x", 0.0),
                        ("y", 0.0),
                        ("z", 0.0),
                    ]
                ),
            ),
            (
                "hz",
                OrderedDict(
                    [
                        ("acqchan", "1003.001"),
                        ("azm", 0.0),
                        ("chtype", "hz"),
                        ("dip", 0.0),
                        ("id", 1003.001),
                        ("x", 0.0),
                        ("y", 0.0),
                        ("z", 0.0),
                    ]
                ),
            ),
        ],
    )
    def test_measurement_channels(self, cgg_tf_edi_obj, channel, expected):
        """Test measurement channels using parametrize for efficiency."""
        assert expected == cgg_tf_edi_obj.Measurement.measurements[channel].to_dict(
            single=True
        )

    def test_measurement_metadata(self, cgg_tf_edi_obj):
        """Test measurement metadata."""
        m_dict = OrderedDict(
            [
                ("maxchan", 7),
                ("maxmeas", 7),
                ("maxrun", 999),
                ("refelev", 175.27),
                ("reflat", -30.930285),
                ("refloc", "TEST01"),
                ("reflon", 127.22923),
                ("reftype", "cartesian"),
                ("units", "meter"),
            ]
        )

        for key, value in m_dict.items():
            if key in ["reflat", "reflon", "refelev"]:
                actual = getattr(cgg_tf_edi_obj.Measurement, key)
                assert (
                    abs(actual - value) < 1e-5
                ), f"{key} mismatch: expected {value}, got {actual}"
            else:
                actual = getattr(cgg_tf_edi_obj.Measurement, key)
                assert (
                    value == actual
                ), f"{key} mismatch: expected {value}, got {actual}"

    def test_data_section(self, cgg_tf_edi_obj):
        """Test data section."""
        d_list = OrderedDict(
            [
                ("ex", "1004.001"),
                ("ey", "1005.001"),
                ("hx", "1001.001"),
                ("hy", "1002.001"),
                ("hz", "1003.001"),
                ("maxblocks", 999),
                ("nchan", 7),
                ("nfreq", 73),
                ("rrhx", "1006.001"),
                ("rrhy", "1007.001"),
                ("sectid", "TEST01"),
            ]
        )

        assert d_list == cgg_tf_edi_obj.Data.to_dict(single=True)

    @pytest.mark.parametrize(
        "array_type,expected_shape",
        [
            ("z", (73, 2, 2)),
            ("z_err", (73, 2, 2)),
            ("t", (73, 1, 2)),
            ("t_err", (73, 1, 2)),
            ("rotation_angle", (73,)),
        ],
    )
    def test_array_shapes(self, cgg_tf_edi_obj, array_type, expected_shape):
        """Test array shapes."""
        array = getattr(cgg_tf_edi_obj, array_type)
        assert array.shape == expected_shape

    def test_impedance_values(self, cgg_tf_edi_obj):
        """Test impedance values."""
        # Test has zero
        assert cgg_tf_edi_obj.z[0, 0, 0] == 0 + 0j
        # Test not zero
        assert cgg_tf_edi_obj.z[1, 0, 0] != 0 + 0j

    def test_rotation_angle(self, cgg_tf_edi_obj):
        """Test rotation angle."""
        assert (cgg_tf_edi_obj.rotation_angle == 0).all()

    def test_set_rotation_angle_to_tf(self, cgg_tf_obj):
        """Test setting rotation angle to TF."""
        a = cgg_tf_obj.to_edi()
        a.rotation_angle[:] = 13

        tf = TF()
        tf.from_edi(a)

        assert (tf._rotation_angle == a.rotation_angle).all()


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__])
