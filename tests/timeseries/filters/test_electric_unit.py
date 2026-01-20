"""
Test to instantiate some filters based on StationXML inputs.

Notes:
    1. We process Network level XML and iterate through it to get stations, channels and stages.
       Obspy's Inventory() chunks the StationXML stages up nicely, and we can use isinstance()
       to verify we're getting expected objects.

    2. Our filter classes can wrap the stage objects provided by obspy.

    3. Potential obspy contributions: Consider contributing fap table readers for StationXML to obspy.
"""

import pytest

try:
    from obspy.core import inventory

    from mt_metadata.timeseries.filters.obspy_stages import create_filter_from_stage
except ImportError:
    pytest.skip("obspy is not installed.", allow_module_level=True)

from mt_metadata import STATIONXML_ELECTRIC
from mt_metadata.timeseries.filters import (
    ChannelResponse,
    CoefficientFilter,
    PoleZeroFilter,
    TimeDelayFilter,
)


@pytest.fixture
def obspy_inventory():
    """Create an obspy inventory from the electric StationXML."""
    return inventory.read_inventory(STATIONXML_ELECTRIC.as_posix())


@pytest.fixture
def stages(obspy_inventory):
    """Get the response stages from the inventory."""
    return obspy_inventory.networks[0].stations[0].channels[0].response.response_stages


@pytest.fixture
def instrument_sensitivity(obspy_inventory):
    """Get the instrument sensitivity from the inventory."""
    return (
        obspy_inventory.networks[0]
        .stations[0]
        .channels[0]
        .response.instrument_sensitivity
    )


@pytest.fixture
def channel_response(stages):
    """Create a ChannelResponse object from the stages."""
    filters_list = [create_filter_from_stage(s) for s in stages]
    return ChannelResponse(filters_list=filters_list)


def test_inventory_type(obspy_inventory, subtests):
    """Test that the inventory is of the correct type."""
    with subtests.test("inventory is Inventory instance"):
        assert isinstance(obspy_inventory, inventory.Inventory)


def test_instrument_sensitivity(channel_response, instrument_sensitivity, subtests):
    """Test the computed instrument sensitivity matches the expected value."""
    with subtests.test("computed sensitivity matches expected"):
        computed_sensitivity = channel_response.compute_instrument_sensitivity(
            instrument_sensitivity.frequency, 12
        )
        assert (
            pytest.approx(computed_sensitivity, abs=1) == instrument_sensitivity.value
        )


def test_stage_01(stages, subtests):
    """Test the first stage (5-pole Butterworth low-pass filter)."""
    f1 = create_filter_from_stage(stages[0])

    with subtests.test("filter type"):
        assert isinstance(f1, PoleZeroFilter)

    with subtests.test("filter name"):
        assert f1.name.lower() == "electric field 5 pole butterworth low-pass"

    with subtests.test("filter type property"):
        assert f1.type == "zpk"

    with subtests.test("units in"):
        assert f1.units_in == "milliVolt per kilometer"

    with subtests.test("units out"):
        assert f1.units_out == "milliVolt per kilometer"

    with subtests.test("number of poles"):
        assert f1.n_poles == 5

    with subtests.test("number of zeros"):
        assert f1.n_zeros == 0

    with subtests.test("normalization factor"):
        assert pytest.approx(f1.normalization_factor, abs=0.01) == 313383.60

    with subtests.test("poles value 1"):
        assert f1.poles[0] == pytest.approx((-3.883009 + 11.951875j))

    with subtests.test("poles value 2"):
        assert f1.poles[1] == pytest.approx((-3.883009 - 11.951875j))

    with subtests.test("poles value 3"):
        assert f1.poles[2] == pytest.approx((-10.166194 + 7.386513j))

    with subtests.test("poles value 4"):
        assert f1.poles[3] == pytest.approx((-10.166194 - 7.386513j))

    with subtests.test("poles value 5"):
        assert f1.poles[4] == pytest.approx((-12.566371 + 0j))


def test_stage_02(stages, subtests):
    """Test the second stage (1-pole Butterworth high-pass filter)."""
    f2 = create_filter_from_stage(stages[1])

    with subtests.test("filter type"):
        assert isinstance(f2, PoleZeroFilter)

    with subtests.test("filter name"):
        assert f2.name.lower() == "electric field 1 pole butterworth high-pass"

    with subtests.test("filter type property"):
        assert f2.type == "zpk"

    with subtests.test("normalization factor"):
        assert pytest.approx(f2.normalization_factor, abs=0.01) == 1

    with subtests.test("number of poles"):
        assert f2.n_poles == 1

    with subtests.test("number of zeros"):
        assert f2.n_zeros == 1

    with subtests.test("poles value"):
        assert f2.poles[0] == pytest.approx(-0.000167 + 0j)

    with subtests.test("zeros value"):
        assert f2.zeros[0] == pytest.approx(0j)


def test_stage_03(stages, subtests):
    """Test the third stage (mV/km to V/m conversion)."""
    f3 = create_filter_from_stage(stages[2])

    with subtests.test("filter type"):
        assert isinstance(f3, CoefficientFilter)

    with subtests.test("filter name"):
        assert f3.name == "mV/km to V/m"

    with subtests.test("filter type property"):
        assert f3.type == "coefficient"

    with subtests.test("gain value"):
        assert pytest.approx(f3.gain, abs=0.000001) == 1e-6

    with subtests.test("units in"):
        assert f3.units_in == "milliVolt per kilometer"

    with subtests.test("units out"):
        assert f3.units_out == "Volt per meter"


def test_stage_04(stages, subtests):
    """Test the fourth stage (V/m to V conversion)."""
    f4 = create_filter_from_stage(stages[3])

    with subtests.test("filter type"):
        assert isinstance(f4, CoefficientFilter)

    with subtests.test("filter name"):
        assert f4.name == "V/m to V"

    with subtests.test("filter type property"):
        assert f4.type == "coefficient"

    with subtests.test("gain value"):
        assert pytest.approx(f4.gain, abs=0.01) == 84.5

    with subtests.test("units in"):
        assert f4.units_in == "Volt per meter"

    with subtests.test("units out"):
        assert f4.units_out == "Volt"


def test_stage_05(stages, subtests):
    """Test the fifth stage (V to counts conversion)."""
    f5 = create_filter_from_stage(stages[4])

    with subtests.test("filter type"):
        assert isinstance(f5, CoefficientFilter)

    with subtests.test("filter name"):
        assert f5.name == "V to counts (electric)"

    with subtests.test("filter type property"):
        assert f5.type == "coefficient"

    with subtests.test("gain value"):
        assert f5.gain == 484733700000000.0

    with subtests.test("units in"):
        assert f5.units_in == "Volt"

    with subtests.test("units out"):
        assert f5.units_out == "digital counts"


def test_stage_06(stages, subtests):
    """Test the sixth stage (time delay filter)."""
    f6 = create_filter_from_stage(stages[5])

    with subtests.test("filter type"):
        assert isinstance(f6, TimeDelayFilter)

    with subtests.test("filter name"):
        assert f6.name == "electric time offset"

    with subtests.test("filter type property"):
        assert f6.type == "time delay"

    with subtests.test("delay value"):
        assert f6.delay == 0.1525

    with subtests.test("units in"):
        assert f6.units_in == "digital counts"

    with subtests.test("units out"):
        assert f6.units_out == "digital counts"
