# -*- coding: utf-8 -*-
"""
Tests for the ChannelResponse filter class
"""

import pytest
import numpy as np

from unittest.mock import patch


from mt_metadata.timeseries.filters import (
    FrequencyResponseTableFilter,
    PoleZeroFilter,
    CoefficientFilter,
    ChannelResponse,
    TimeDelayFilter,
)

try:
    from obspy.core.inventory.response import ResponseListResponseStage
except ImportError:
    ResponseListResponseStage = None


@pytest.fixture
def time_delay_filter():
    """Create a time delay filter for testing"""
    return TimeDelayFilter(
        units_in="volt",
        units_out="volt",
        delay=-0.25,
        name="example_time_delay",
    )


@pytest.fixture
def fap_filter():
    """Create a frequency-amplitude-phase filter for testing"""
    fap = FrequencyResponseTableFilter(
        units_in="volt", units_out="volt", name="example_fap"
    )

    fap.frequencies = [
        1.95312000e-03,
        2.76214000e-03,
        3.90625000e-03,
        5.52427000e-03,
        7.81250000e-03,
        1.10485000e-02,
        1.56250000e-02,
        2.20971000e-02,
        3.12500000e-02,
        4.41942000e-02,
        6.25000000e-02,
        8.83883000e-02,
        1.25000000e-01,
        1.76780000e-01,
        2.50000000e-01,
        3.53550000e-01,
        5.00000000e-01,
        7.07110000e-01,
        1.00000000e00,
        1.41420000e00,
        2.00000000e00,
        2.82840000e00,
        4.00000000e00,
        5.65690000e00,
        8.00000000e00,
        1.13140000e01,
        1.60000000e01,
        2.26270000e01,
        3.20000000e01,
        4.52550000e01,
        6.40000000e01,
        9.05100000e01,
        1.28000000e02,
        1.81020000e02,
        2.56000000e02,
        3.62040000e02,
        5.12000000e02,
        7.24080000e02,
        1.02400000e03,
        1.44820000e03,
        2.04800000e03,
        2.89630000e03,
        4.09600000e03,
        5.79260000e03,
        8.19200000e03,
        1.15850000e04,
    ]

    fap.amplitudes = [
        1.59009000e-03,
        3.07497000e-03,
        5.52793000e-03,
        9.47448000e-03,
        1.54565000e-02,
        2.49498000e-02,
        3.96462000e-02,
        7.87192000e-02,
        1.57134000e-01,
        3.09639000e-01,
        5.94224000e-01,
        1.12698000e00,
        2.01092000e00,
        3.33953000e00,
        5.00280000e00,
        6.62396000e00,
        7.97545000e00,
        8.82872000e00,
        9.36883000e00,
        9.64102000e00,
        9.79664000e00,
        9.87183000e00,
        9.90666000e00,
        9.92845000e00,
        9.93559000e00,
        9.93982000e00,
        9.94300000e00,
        9.93546000e00,
        9.93002000e00,
        9.90873000e00,
        9.86383000e00,
        9.78129000e00,
        9.61814000e00,
        9.26461000e00,
        8.60175000e00,
        7.18337000e00,
        4.46123000e00,
        -8.72600000e-01,
        -5.15684000e00,
        -2.95111000e00,
        -9.28512000e-01,
        -2.49850000e-01,
        -5.75682000e-02,
        -1.34293000e-02,
        -1.02708000e-03,
        1.09577000e-03,
    ]

    fap.phases = [
        7.60824000e-02,
        1.09174000e-01,
        1.56106000e-01,
        2.22371000e-01,
        3.12020000e-01,
        4.41080000e-01,
        6.23548000e-01,
        8.77188000e-01,
        1.23360000e00,
        1.71519000e00,
        2.35172000e00,
        3.13360000e00,
        3.98940000e00,
        4.67269000e00,
        4.96593000e00,
        4.65875000e00,
        3.95441000e00,
        3.11098000e00,
        2.30960000e00,
        1.68210000e00,
        1.17928000e00,
        8.20015000e-01,
        5.36474000e-01,
        3.26955000e-01,
        1.48051000e-01,
        -8.24275000e-03,
        -1.66064000e-01,
        -3.48852000e-01,
        -5.66625000e-01,
        -8.62435000e-01,
        -1.25347000e00,
        -1.81065000e00,
        -2.55245000e00,
        -3.61512000e00,
        -5.00185000e00,
        -6.86158000e00,
        -8.78698000e00,
        -9.08920000e00,
        -4.22925000e00,
        2.15533000e-01,
        6.00661000e-01,
        3.12368000e-01,
        1.31660000e-01,
        5.01553000e-02,
        1.87239000e-02,
        6.68243000e-03,
    ]

    return fap


@pytest.fixture
def pole_zero_filter():
    """Create a pole-zero filter for testing"""
    pz = PoleZeroFilter(units_in="volt", units_out="volt", name="example_zpk_response")
    pz.poles = [
        (-6.283185 + 10.882477j),
        (-6.283185 - 10.882477j),
        (-12.566371 + 0j),
    ]
    pz.zeros = []
    pz.normalization_factor = 2002.269

    return pz


@pytest.fixture
def coeff_filter():
    """Create a coefficient filter for testing"""
    return CoefficientFilter(
        units_in="V",
        units_out="V",
        name="example_coefficient",
        gain=10,
    )


@pytest.fixture
def channel_response(pole_zero_filter, fap_filter, coeff_filter, time_delay_filter):
    """Create a channel response with multiple filters"""
    cr = ChannelResponse(
        filters_list=[pole_zero_filter, fap_filter, coeff_filter, time_delay_filter]
    )
    cr.frequencies = np.logspace(-5, 5, 500)
    return cr


def test_pass_band(channel_response):
    """Test the pass_band property of ChannelResponse"""
    assert np.allclose(channel_response.pass_band, np.array([0.1018629, 1.02334021]))


def test_complex_response(channel_response, subtests):
    """Test the complex_response method of ChannelResponse"""
    cr = channel_response.complex_response()
    pb = channel_response.pass_band
    index_0 = np.where(channel_response.frequencies == pb[0])[0][0]
    index_1 = np.where(channel_response.frequencies == pb[-1])[0][0]

    with subtests.test("test dtype"):
        assert cr.dtype.type == np.complex128

    with subtests.test("test amplitude"):
        cr_amp = np.abs(cr)
        # check the slope in the passband
        slope = np.log10(cr_amp[index_1] / cr_amp[index_0]) / np.log10(
            channel_response.frequencies[index_1]
            / channel_response.frequencies[index_0]
        )
        assert abs(slope) < 1

    with subtests.test("test phase"):
        cr_phase = np.unwrap(np.angle(cr, deg=False))
        slope = (cr_phase[index_1] - cr_phase[index_0]) / np.log10(
            channel_response.frequencies[index_1]
            / channel_response.frequencies[index_0]
        )
        assert abs(slope) < np.pi


def test_unit_fail(channel_response):
    """Test that filters with inconsistent units raise an error"""
    cr1 = CoefficientFilter(units_in="volt", units_out="mV")
    cr2 = CoefficientFilter(units_in="nanotesla", units_out="count")

    with pytest.raises(ValueError):
        channel_response.filters_list = [cr1, cr2]


def test_delay_filters(channel_response, time_delay_filter):
    """Test the delay_filters property"""
    delay_names = [f.name for f in channel_response.delay_filters]
    assert delay_names == [time_delay_filter.name]


def test_non_delay_filters(
    channel_response, pole_zero_filter, fap_filter, coeff_filter
):
    """Test the non_delay_filters property"""
    non_delay_names = [f.name for f in channel_response.non_delay_filters]
    assert non_delay_names == [
        pole_zero_filter.name,
        fap_filter.name,
        coeff_filter.name,
    ]


def test_names(
    channel_response, pole_zero_filter, fap_filter, coeff_filter, time_delay_filter
):
    """Test the names property"""
    assert channel_response.names == [
        pole_zero_filter.name,
        fap_filter.name,
        coeff_filter.name,
        time_delay_filter.name,
    ]


def test_total_delay(channel_response, time_delay_filter):
    """Test the total_delay property"""
    assert channel_response.total_delay == time_delay_filter.delay


def test_normalization_frequency(channel_response):
    """Test the normalization_frequency property"""
    assert np.round(channel_response.normalization_frequency, 3) == 0.323


def test_instrument_sensitivity(channel_response, subtests):
    """Test the compute_instrument_sensitivity method"""
    s = 62.01227179
    for sig_figs in [3, 6, 9]:
        with subtests.test(significant_digits=sig_figs):
            assert np.round(
                channel_response.compute_instrument_sensitivity(sig_figs=sig_figs),
                sig_figs - 1,
            ) == np.round(s, sig_figs - 1)


def test_units_in(channel_response, pole_zero_filter):
    """Test the units_in property"""
    assert channel_response.units_in == pole_zero_filter.units_in


def test_units_out(channel_response, time_delay_filter):
    """Test the units_out property"""
    assert channel_response.units_out == time_delay_filter.units_out


@pytest.mark.skipif(ResponseListResponseStage is None, reason="obspy is not installed")
def test_to_obspy_stage(fap_filter, subtests):
    """Test the to_obspy method of FrequencyResponseTableFilter"""
    stage = fap_filter.to_obspy(2, sample_rate=10, normalization_frequency=1)

    with subtests.test("test instance"):
        assert isinstance(stage, ResponseListResponseStage)

    with subtests.test("test stage number"):
        assert stage.stage_sequence_number == 2

    with subtests.test("test gain"):
        assert stage.stage_gain == fap_filter.gain

    with subtests.test("test amplitude"):
        amp = np.array([r.amplitude for r in stage.response_list_elements])
        assert np.allclose(amp, fap_filter.amplitudes)

    with subtests.test("test phase"):
        phase = np.array([r.phase for r in stage.response_list_elements])
        assert np.allclose(phase, fap_filter.phases)

    with subtests.test("test frequency"):
        f = np.array([r.frequency for r in stage.response_list_elements])
        assert np.allclose(f, fap_filter.frequencies)

    with subtests.test("test normalization frequency"):
        assert stage.stage_gain_frequency == 1

    with subtests.test("test units in"):
        assert stage.input_units == fap_filter.units_in_object.symbol

    with subtests.test("test units out"):
        assert stage.output_units == fap_filter.units_out_object.symbol

    with subtests.test("test units in description"):
        assert stage.input_units_description == fap_filter.units_in_object.name

    with subtests.test("test units out description"):
        assert stage.output_units_description == fap_filter.units_out_object.name

    with subtests.test("test description"):
        assert stage.description == "frequency amplitude phase lookup table"

    with subtests.test("test name"):
        assert stage.name == fap_filter.name


@pytest.fixture
def channel_response_with_filters():
    """Create a channel response with multiple filters for testing"""
    # Create PoleZeroFilter
    pz = PoleZeroFilter(units_in="volt", units_out="volt", name="example_zpk_response")
    pz.poles = [
        (-6.283185 + 10.882477j),
        (-6.283185 - 10.882477j),
        (-12.566371 + 0j),
    ]
    pz.zeros = []
    pz.normalization_factor = 2002.269

    # Create TimeDelayFilter
    td = TimeDelayFilter(
        units_in="volt",
        units_out="volt",
        delay=-0.25,
        name="example_time_delay",
    )

    # Create channel response
    cr = ChannelResponse(filters_list=[pz, td])
    cr.frequencies = np.logspace(-3, 3, 100)
    return cr


@patch("matplotlib.pyplot.figure", autospec=True)
@patch("matplotlib.pyplot.show", autospec=True)
def test_plot_response_basic(mock_show, mock_figure, channel_response_with_filters):
    """Test basic functionality of plot_response method"""
    # Reset the mock counts before the test
    mock_figure.reset_mock()
    mock_show.reset_mock()

    # Call the plot_response method
    channel_response_with_filters.plot_response(x_units="frequency")

    # Verify that figure was created at least once and show was called
    assert mock_figure.call_count >= 1, "plt.figure should be called at least once"
    mock_show.assert_called_once()


@patch("matplotlib.pyplot.figure", autospec=True)
@patch("matplotlib.pyplot.show", autospec=True)
def test_plot_response_with_delay_and_decimation(
    mock_show, mock_figure, channel_response_with_filters
):
    """Test plot_response with include_delay=True"""
    # Reset the mock counts before the test
    mock_figure.reset_mock()
    mock_show.reset_mock()

    # Call the plot_response method with include_delay=True
    channel_response_with_filters.plot_response(include_delay=True)

    # Verify that figure was created at least once and show was called
    assert mock_figure.call_count >= 1, "plt.figure should be called at least once"
    mock_show.assert_called_once()


@patch("matplotlib.pyplot.figure", autospec=True)
@patch("matplotlib.pyplot.show", autospec=True)
def test_plot_response_with_custom_frequencies(
    mock_show, mock_figure, channel_response_with_filters
):
    """Test plot_response with custom frequencies"""
    # Reset the mock counts before the test
    mock_figure.reset_mock()
    mock_show.reset_mock()

    custom_frequencies = np.logspace(-2, 2, 50)

    # Call the plot_response method with custom frequencies
    channel_response_with_filters.plot_response(frequencies=custom_frequencies)

    # Verify that figure was created at least once and show was called
    assert mock_figure.call_count >= 1, "plt.figure should be called at least once"
    mock_show.assert_called_once()

    # Verify that frequencies were updated in the channel_response object
    assert np.array_equal(channel_response_with_filters.frequencies, custom_frequencies)
