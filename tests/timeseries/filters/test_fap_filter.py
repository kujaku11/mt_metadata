import pathlib

import numpy as np
import pytest
from pydantic import ValidationError

from mt_metadata.timeseries.filters import FrequencyResponseTableFilter
from mt_metadata.timeseries.filters.helper_functions import (
    make_frequency_response_table_filter,
)


try:
    from obspy.core.inventory.response import ResponseListResponseStage
except ImportError:
    ResponseListResponseStage = None


@pytest.fixture
def fap_filter():
    """Fixture to create a FrequencyResponseTableFilter instance."""
    fap = FrequencyResponseTableFilter(
        units_in="volt", units_out="nanotesla", name="example_fap"
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


def test_type(fap_filter, subtests):
    with subtests.test("test type"):
        assert fap_filter.type == "fap"

    with subtests.test("test type bad set to 'fir'"):
        fap_filter.type = "fir"
        assert fap_filter.type == "fap"


def test_gain(fap_filter, subtests):
    with subtests.test(msg="string input"):
        fap_filter.gain = ".25"
        assert fap_filter.gain == 0.25

    with subtests.test(msg="negative string input"):
        fap_filter.gain = "-.25"
        assert fap_filter.gain == -0.25

    with subtests.test(msg="integer input"):
        fap_filter.gain = int(1)
        assert fap_filter.gain == 1

    with subtests.test(msg="failing input"):
        with pytest.raises(ValidationError):
            fap_filter.gain = "a"


def test_phases_in_degrees(fap_filter):
    degree_phases = np.arange(100)
    fap_filter.phases = degree_phases
    assert np.allclose(fap_filter.phases, np.deg2rad(degree_phases))


def test_phases_in_milliradians(fap_filter):
    milli_radian_phases = np.arange(100) * 1000 * np.pi / 2
    fap_filter.phases = milli_radian_phases
    assert np.allclose(fap_filter.phases, milli_radian_phases / 1000)


def test_complex_response(fap_filter, subtests):
    cr = fap_filter.complex_response(fap_filter.frequencies)

    with subtests.test("test dtype"):
        assert cr.dtype.type == np.complex128

    with subtests.test("test amplitude"):
        cr_amp = np.abs(cr)
        assert np.allclose(np.abs(fap_filter.amplitudes), cr_amp)

    with subtests.test("test phase"):
        cr_phase = np.unwrap(np.angle(cr, deg=False))
        assert np.allclose(cr_phase[:-10], fap_filter.phases[:-10])


def test_type(fap_filter, subtests):
    with subtests.test("test type"):
        assert fap_filter.type == "fap"


@pytest.mark.skipif(ResponseListResponseStage is None, reason="obspy is not installed.")
def test_to_obspy_stage(fap_filter, subtests):
    units_in = fap_filter.units_in
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

    with subtests.test("test units in description"):
        assert stage.input_units_description == fap_filter.units_in_object.name

    with subtests.test("test units in"):
        assert stage.input_units == fap_filter.units_in_object.symbol

    with subtests.test("test units out description"):
        assert stage.output_units_description == fap_filter.units_out_object.name

    with subtests.test("test units out"):
        assert stage.output_units == fap_filter.units_out_object.symbol

    with subtests.test("test description"):
        assert stage.description == "frequency amplitude phase lookup table"

    with subtests.test("test name"):
        assert stage.name == fap_filter.name


def test_helper_functions():
    mc_fap = [
        "Frequency [Hz],Amplitude [V/nT],Phase [degrees]\n",
        "0.0001,0.00016,90\n",
        "0.00015,0.00024,90\n",
        "0.0002,0.00032,89.9\n",
        "0.0003,0.00048,89.9\n",
        "0.0004,0.00065,89.9\n",
        "0.0006,0.00097,89.8\n",
        "0.0008,0.00129,89.8\n",
        "0.001,0.00162,89.7\n",
        "0.0015,0.00242,89.5\n",
        "0.002,0.00323,89.4\n",
        "0.003,0.00485,89.1\n",
        "0.004,0.00646,88.8\n",
        "0.006,0.00969,88.2\n",
        "0.008,0.0129,87.5\n",
        "0.01,0.0161,86.9\n",
        "0.015,0.0241,85.4\n",
        "0.02,0.0321,83.9\n",
        "0.03,0.0478,80.9\n",
        "0.04,0.0632,77.9\n",
        "0.06,0.0923,72.2\n",
        "0.08,0.118,66.8\n",
        "0.1,0.142,61.8\n",
        "0.15,0.1879,51.2\n",
        "0.2,0.2199,43\n",
        "0.3,0.256,31.9\n",
        "0.4,0.273,25\n",
        "0.6,0.2879,17.3\n",
        "0.8,0.293,13.1\n",
        "1,0.296,10.6\n",
        "1.5,0.2989,7.1\n",
        "2,0.3,5.3\n",
        "3,0.3009,3.6\n",
        "4,0.3009,2.7\n",
        "8,0.3009,-0.1\n",
        "10,0.3009,-0.8\n",
        "20,0.3009,-3.2\n",
        "30,0.3009,-5.3\n",
        "40,0.3009,-7.3\n",
        "80,0.3009,-15.4\n",
        "100,0.3019,-18.7\n",
        "200,0.298,-38.9\n",
        "400,0.272,-79.8\n",
        "500,0.2469,-100.7\n",
        "800,0.15,-156.6\n",
        "1000,0.101,-185.4\n",
    ]
    fn = pathlib.Path("bf4.csv")
    with open(fn, "w") as f:
        f.writelines(mc_fap)
    fap_obj = make_frequency_response_table_filter(fn, case="bf4")
    assert len(fap_obj.amplitudes) == len(mc_fap) - 1
    fn.unlink()


@pytest.fixture
def fap_filter_basic():
    """Fixture to create a FrequencyResponseTableFilter instance."""
    fap = FrequencyResponseTableFilter(
        frequencies=np.array([0.001, 0.01, 0.1, 1.0, 10.0]),
        amplitudes=np.array([1e-3, 1e-2, 1e-1, 1.0, 10.0]),
        phases=np.array([-90, -45, 0, 45, 90]),
        instrument_type="example_instrument",
        units_in="Volt",
        units_out="nanoTesla",
        name="example_fap",
        description="example description",
    )
    return fap


def test_frequencies_validation(fap_filter_basic, subtests):
    with subtests.test("Valid frequencies"):
        assert np.allclose(fap_filter_basic.frequencies, [0.001, 0.01, 0.1, 1.0, 10.0])

    with subtests.test("Empty frequencies"):
        fap_filter_basic.frequencies = []
        assert fap_filter_basic.frequencies.size == 0

    with subtests.test("Invalid frequencies"):
        with pytest.raises(TypeError):
            fap_filter_basic.frequencies = {"invalid": "data"}


def test_amplitudes_validation(fap_filter_basic, subtests):
    with subtests.test("Valid amplitudes"):
        assert np.allclose(fap_filter_basic.amplitudes, [1e-3, 1e-2, 1e-1, 1.0, 10.0])

    with subtests.test("Empty amplitudes"):
        fap_filter_basic.amplitudes = []
        assert fap_filter_basic.amplitudes.size == 0

    with subtests.test("Invalid amplitudes"):
        with pytest.raises(TypeError):
            fap_filter_basic.amplitudes = {"invalid": "data"}


def test_phases_validation(fap_filter_basic, subtests):
    with subtests.test("Valid phases in degrees"):
        assert np.allclose(fap_filter_basic.phases, np.deg2rad([-90, -45, 0, 45, 90]))

    with subtests.test("Phases in degrees converted to radians"):
        fap_filter_basic.phases = [0, 90, 180]
        assert np.allclose(fap_filter_basic.phases, np.deg2rad([0, 90, 180]))

    with subtests.test("Phases in milli-radians converted to radians"):
        fap_filter_basic.phases = [0, 1000 * np.pi / 2, 2000 * np.pi / 2]
        assert np.allclose(fap_filter_basic.phases, [0, np.pi / 2, np.pi])

    # skip for now.  But should look further into why this fails.
    with subtests.test("Invalid string phases"):
        with pytest.raises(TypeError):
            fap_filter_basic.phases = "invalid"


def test_min_max_frequency(fap_filter_basic, subtests):
    with subtests.test("Minimum frequency"):
        assert fap_filter_basic.min_frequency == 0.001

    with subtests.test("Maximum frequency"):
        assert fap_filter_basic.max_frequency == 10.0

    with subtests.test("Empty frequencies"):
        fap_filter_basic.frequencies = []
        assert fap_filter_basic.min_frequency == 0.0
        assert fap_filter_basic.max_frequency == 0.0


def test_complex_response_basic(fap_filter_basic, subtests):
    frequencies = np.array([0.001, 0.01, 0.1, 1.0, 10.0])
    response = fap_filter_basic.complex_response(frequencies)

    with subtests.test("Response dtype"):
        assert response.dtype == np.complex128

    with subtests.test("Amplitude response"):
        amplitude_response = np.abs(response)
        assert np.allclose(amplitude_response, fap_filter_basic.amplitudes)

    with subtests.test("Phase response"):
        phase_response = np.unwrap(np.angle(response))
        assert np.allclose(phase_response, fap_filter_basic.phases)


@pytest.mark.skipif(ResponseListResponseStage is None, reason="obspy is not installed.")
def test_to_obspy_stage_basic(fap_filter_basic, subtests):
    stage = fap_filter_basic.to_obspy(
        stage_number=1, normalization_frequency=1.0, sample_rate=10.0
    )

    with subtests.test("Stage instance"):
        assert isinstance(stage, ResponseListResponseStage)

    with subtests.test("Stage gain"):
        assert stage.stage_gain == fap_filter_basic.gain

    with subtests.test("Stage frequencies"):
        frequencies = np.array([r.frequency for r in stage.response_list_elements])
        assert np.allclose(frequencies, fap_filter_basic.frequencies)

    with subtests.test("Stage amplitudes"):
        amplitudes = np.array([r.amplitude for r in stage.response_list_elements])
        assert np.allclose(amplitudes, fap_filter_basic.amplitudes)

    with subtests.test("Stage phases"):
        phases = np.array([r.phase for r in stage.response_list_elements])
        assert np.allclose(phases, fap_filter_basic.phases)


@pytest.mark.skipif(ResponseListResponseStage is None, reason="obspy is not installed.")
def test_from_obspy_stage(fap_filter_basic, subtests):
    """Test the from_obspy_stage method with a filter to obspy conversion and back."""
    # First, create an obspy stage from our filter
    obspy_stage = fap_filter_basic.to_obspy(
        stage_number=1, normalization_frequency=1.0, sample_rate=10.0
    )

    # Then create a new filter from the obspy stage
    new_filter = FrequencyResponseTableFilter.from_obspy_stage(obspy_stage)

    with subtests.test("test frequencies"):
        assert np.allclose(new_filter.frequencies, fap_filter_basic.frequencies)

    with subtests.test("test amplitudes"):
        assert np.allclose(new_filter.amplitudes, fap_filter_basic.amplitudes)

    with subtests.test("test phases"):
        assert np.allclose(new_filter.phases, fap_filter_basic.phases)

    with subtests.test("test gain"):
        assert new_filter.gain == fap_filter_basic.gain

    with subtests.test("test units in"):
        assert new_filter.units_in == fap_filter_basic.units_in

    with subtests.test("test units out"):
        assert new_filter.units_out == fap_filter_basic.units_out

    with subtests.test("test name"):
        assert new_filter.name == fap_filter_basic.name

    with subtests.test("test type"):
        assert new_filter.type == "fap"


@pytest.mark.skipif(ResponseListResponseStage is None, reason="obspy is not installed.")
def test_from_obspy_stage_custom_parameters(subtests):
    """Test from_obspy_stage with a manually created obspy stage."""
    # Create response list elements
    from obspy.core.inventory.response import ResponseListElement

    response_elements = [
        ResponseListElement(frequency=0.001, amplitude=0.001, phase=0.0),
        ResponseListElement(frequency=0.01, amplitude=0.01, phase=np.pi / 4),
        ResponseListElement(frequency=0.1, amplitude=0.1, phase=np.pi / 2),
        ResponseListElement(frequency=1.0, amplitude=1.0, phase=3 * np.pi / 4),
        ResponseListElement(frequency=10.0, amplitude=10.0, phase=np.pi),
    ]

    # Create a custom ResponseListResponseStage
    custom_stage = ResponseListResponseStage(
        stage_sequence_number=3,
        stage_gain=2.5,
        stage_gain_frequency=0.5,
        input_units="V",
        input_units_description="volts",
        output_units="nT",
        output_units_description="nanoteslas",
        response_list_elements=response_elements,
        name="Custom FAP Filter",
        description="Test FAP filter from obspy stage",
        resource_id=None,
        resource_id2=None,
        decimation_input_sample_rate=None,
        decimation_factor=None,
        decimation_offset=None,
        decimation_delay=None,
        decimation_correction=None,
    )

    # Create filter from stage
    filter_from_stage = FrequencyResponseTableFilter.from_obspy_stage(custom_stage)

    with subtests.test("test filter type"):
        assert filter_from_stage.type == "fap"

    with subtests.test("test name"):
        assert filter_from_stage.name == "Custom FAP Filter"

    with subtests.test("test frequencies"):
        expected_frequencies = np.array([0.001, 0.01, 0.1, 1.0, 10.0])
        assert np.allclose(filter_from_stage.frequencies, expected_frequencies)

    with subtests.test("test amplitudes"):
        expected_amplitudes = np.array([0.001, 0.01, 0.1, 1.0, 10.0])
        assert np.allclose(filter_from_stage.amplitudes, expected_amplitudes)

    with subtests.test("test phases"):
        expected_phases = np.array([0.0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi])
        assert np.allclose(filter_from_stage.phases, expected_phases)

    with subtests.test("test gain"):
        assert filter_from_stage.gain == 2.5

    with subtests.test("test units in"):
        assert filter_from_stage.units_in == "Volt"

    with subtests.test("test units out"):
        assert filter_from_stage.units_out == "nanoTesla"

    with subtests.test("test description"):
        assert filter_from_stage.comments.value == "Test FAP filter from obspy stage"


@pytest.mark.skipif(ResponseListResponseStage is None, reason="obspy is not installed.")
def test_roundtrip_conversion(subtests):
    """Test round-trip conversion from FrequencyResponseTableFilter to obspy and back."""
    # Create original filter with specific values
    original_filter = FrequencyResponseTableFilter(
        frequencies=np.array([0.005, 0.05, 0.5, 5.0, 50.0]),
        amplitudes=np.array([0.2, 0.4, 0.6, 0.8, 1.0]),
        phases=np.deg2rad(np.array([-180, -90, 0, 90, 180])),
        units_in="mV",
        units_out="nT",
        name="test roundtrip",
        description="Test roundtrip conversion",
        gain=3.5,
    )

    # Convert to obspy stage
    obspy_stage = original_filter.to_obspy(
        1, sample_rate=200, normalization_frequency=0.5
    )

    # Convert back to FrequencyResponseTableFilter
    round_trip_filter = FrequencyResponseTableFilter.from_obspy_stage(obspy_stage)

    with subtests.test("test frequencies preserved"):
        assert np.allclose(round_trip_filter.frequencies, original_filter.frequencies)

    with subtests.test("test amplitudes preserved"):
        assert np.allclose(round_trip_filter.amplitudes, original_filter.amplitudes)

    with subtests.test("test phases preserved"):
        assert np.allclose(round_trip_filter.phases, original_filter.phases)

    with subtests.test("test gain preserved"):
        assert round_trip_filter.gain == original_filter.gain

    with subtests.test("test units in preserved"):
        assert round_trip_filter.units_in == original_filter.units_in

    with subtests.test("test units out preserved"):
        assert round_trip_filter.units_out == original_filter.units_out

    with subtests.test("test name preserved"):
        assert round_trip_filter.name == original_filter.name

    with subtests.test("test description preserved"):
        # Description might be updated in the obspy stage
        assert round_trip_filter.comments.value is not None

    with subtests.test("test type preserved"):
        assert round_trip_filter.type == "fap"


@pytest.mark.skipif(ResponseListResponseStage is None, reason="obspy is not installed.")
def test_from_obspy_stage_with_empty_data(subtests):
    """Test from_obspy_stage with empty response elements."""
    # Create a ResponseListResponseStage with no response elements
    empty_stage = ResponseListResponseStage(
        stage_sequence_number=1,
        stage_gain=1.0,
        stage_gain_frequency=1.0,
        input_units="V",
        input_units_description="volts",
        output_units="count",
        output_units_description="digital counts",
        response_list_elements=[],
        name="Empty FAP Filter",
    )

    # Create filter from stage
    empty_filter = FrequencyResponseTableFilter.from_obspy_stage(empty_stage)

    with subtests.test("test filter created"):
        assert isinstance(empty_filter, FrequencyResponseTableFilter)

    with subtests.test("test empty frequencies"):
        assert empty_filter.frequencies.size == 0

    with subtests.test("test empty amplitudes"):
        assert empty_filter.amplitudes.size == 0

    with subtests.test("test empty phases"):
        assert empty_filter.phases.size == 0
