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

from mt_metadata import STATIONXML_MAGNETIC
from mt_metadata.timeseries.filters import (
    ChannelResponse,
    CoefficientFilter,
    PoleZeroFilter,
    TimeDelayFilter,
)


@pytest.fixture
def obspy_inventory():
    """Create an obspy inventory from the magnetic StationXML."""
    return inventory.read_inventory(STATIONXML_MAGNETIC.as_posix())


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
            instrument_sensitivity.frequency
        )
        assert (
            pytest.approx(computed_sensitivity, abs=1) == instrument_sensitivity.value
        )


def test_stage_01(stages, subtests):
    """Test the first stage (3-pole Butterworth low-pass filter)."""
    f1 = create_filter_from_stage(stages[0])

    with subtests.test("filter type"):
        assert isinstance(f1, PoleZeroFilter)

    with subtests.test("filter name"):
        assert f1.name == "magnetic field 3 pole Butterworth low-pass"

    with subtests.test("filter type property"):
        assert f1.type == "zpk"

    with subtests.test("units in"):
        assert f1.units_in == "nanoTesla"

    with subtests.test("units out"):
        assert f1.units_out == "Volt"

    with subtests.test("number of poles"):
        assert f1.n_poles == 3

    with subtests.test("number of zeros"):
        assert f1.n_zeros == 0

    with subtests.test("normalization factor"):
        assert pytest.approx(f1.normalization_factor, abs=0.01) == 1984.31

    with subtests.test("poles value"):
        expected_poles = [
            (-6.283185 + 10.882477j),
            (-6.283185 - 10.882477j),
            (-12.566371 + 0j),
        ]
        for i, (pole, expected) in enumerate(zip(f1.poles, expected_poles)):
            with subtests.test(f"pole {i} value"):
                assert pole == pytest.approx(expected)


def test_stage_02(stages, subtests):
    """Test the second stage (V to counts conversion)."""
    f2 = create_filter_from_stage(stages[1])

    with subtests.test("filter type"):
        assert isinstance(f2, CoefficientFilter)

    with subtests.test("filter name"):
        assert f2.name == "magnatometer A to D"

    with subtests.test("filter type property"):
        assert f2.type == "coefficient"

    with subtests.test("gain value"):
        assert f2.gain == 100

    with subtests.test("units in"):
        assert f2.units_in == "Volt"

    with subtests.test("units out"):
        assert f2.units_out == "digital counts"


def test_stage_03(stages, subtests):
    """Test the third stage (time delay filter)."""
    f3 = create_filter_from_stage(stages[2])

    with subtests.test("filter type"):
        assert isinstance(f3, TimeDelayFilter)

    with subtests.test("filter name"):
        assert f3.name == "Hz time offset"

    with subtests.test("filter type property"):
        assert f3.type == "time delay"

    with subtests.test("delay value"):
        assert f3.delay == 0.2455

    with subtests.test("units in"):
        assert f3.units_in == "digital counts"

    with subtests.test("units out"):
        assert f3.units_out == "digital counts"
