"""

When about to make commits, try ~/software/irismt/mt_metadata/tests/pytest test*

2021-02-14
Test to instantite some filters based in StationXML inputs.

Notes:
    1. In this example I have we are receiving a Network level XML and we need to iterate
    through it to get the stations, channels and stages.   In general we will need a
    methods that work with these XMLs and iterate through them.

    It looks like obspy's Inventory() chunks the StationXML stages up nicely.
    Moreover we can use instance checks (eg isinstance() as way to confirm we are
    getting what we think we are getting,

    2. It looks like stage.__dict__ is pretty comprehensive, but I dont like how it passes
    poles as _poles and zeros as _zeros.
    Actually, here's the thing, our filter class looks like it could just wrap the stage

    3. Obspy contributions?  Do we want to contribute fap table readers for StationXML to obspy?


"""

import unittest
import pytest

try:
    from obspy.core import inventory
    from mt_metadata.timeseries.filters.obspy_stages import create_filter_from_stage
except ImportError:
    pytest.skip("obspy is not installed.", allow_module_level=True)

from mt_metadata.timeseries.filters import (
    ChannelResponse,
    PoleZeroFilter,
    CoefficientFilter,
    TimeDelayFilter,
)
from mt_metadata import STATIONXML_ELECTRIC


class TestFilterElectric(unittest.TestCase):
    """
    Test filter translation from :class:`obspy.inventory.Network
    """

    def setUp(self):
        self.inventory = inventory.read_inventory(STATIONXML_ELECTRIC.as_posix())
        self.stages = (
            self.inventory.networks[0].stations[0].channels[0].response.response_stages
        )
        self.instrument_sensitivity = (
            self.inventory.networks[0]
            .stations[0]
            .channels[0]
            .response.instrument_sensitivity
        )

    def test_inventory_type(self):
        self.assertIsInstance(self.inventory, inventory.Inventory)

    def test_instrument_sensitivity(self):
        filters_list = [create_filter_from_stage(s) for s in self.stages]
        cr = ChannelResponse(filters_list=filters_list)

        self.assertAlmostEqual(
            cr.compute_instrument_sensitivity(
                self.instrument_sensitivity.frequency, 12
            ),
            self.instrument_sensitivity.value,
            0,
        )

    def test_stage_01(self):
        f1 = create_filter_from_stage(self.stages[0])
        self.assertIsInstance(f1, PoleZeroFilter)
        self.assertEqual(f1.name.lower(), "electric field 5 pole butterworth low-pass")
        self.assertEqual(f1.type, "zpk")
        self.assertEqual(f1.units_in, "millivolt per kilometer")
        self.assertEqual(f1.units_out, "millivolt per kilometer")
        self.assertEqual(f1.n_poles, 5)
        self.assertEqual(f1.n_zeros, 0)
        self.assertAlmostEqual(f1.normalization_factor, 313383.60, 2)
        self.assertListEqual(
            list(f1.poles),
            [
                (-3.883009 + 11.951875j),
                (-3.883009 - 11.951875j),
                (-10.166194 + 7.386513j),
                (-10.166194 - 7.386513j),
                (-12.566371 + 0j),
            ],
        )

    def test_stage_02(self):
        f2 = create_filter_from_stage(self.stages[1])

        self.assertIsInstance(f2, PoleZeroFilter)
        self.assertEqual(f2.name.lower(), "electric field 1 pole butterworth high-pass")
        self.assertEqual(f2.type, "zpk")
        self.assertAlmostEqual(f2.normalization_factor, 1, 2)
        self.assertEqual(f2.n_poles, 1)
        self.assertEqual(f2.n_zeros, 1)
        self.assertListEqual(list(f2.poles), [-0.000167 + 0j])
        self.assertListEqual(list(f2.zeros), [0j])

    def test_stage_03(self):
        # a no pole, no zero filter converts to a coefficient filter
        f2 = create_filter_from_stage(self.stages[2])
        self.assertIsInstance(f2, CoefficientFilter)
        self.assertEqual(f2.name, "mV/km to V/m")
        self.assertEqual(f2.type, "coefficient")
        self.assertAlmostEqual(f2.gain, 1e-6, 2)
        self.assertEqual(f2.units_in, "mV/km")
        self.assertEqual(f2.units_out, "V/m")

    def test_stage_04(self):
        f2 = create_filter_from_stage(self.stages[3])
        self.assertIsInstance(f2, CoefficientFilter)
        self.assertEqual(f2.name, "V/m to V")
        self.assertEqual(f2.type, "coefficient")
        self.assertAlmostEqual(f2.gain, 84.5, 2)
        self.assertEqual(f2.units_in, "V/m")
        self.assertEqual(f2.units_out, "V")

    def test_stage_05(self):
        f2 = create_filter_from_stage(self.stages[4])
        self.assertIsInstance(f2, CoefficientFilter)
        self.assertEqual(f2.name, "V to counts (electric)")
        self.assertEqual(f2.type, "coefficient")
        self.assertEqual(f2.gain, 484733700000000.0)
        self.assertEqual(f2.units_in, "V")
        self.assertEqual(f2.units_out, "count")

    def test_stage_06(self):
        f2 = create_filter_from_stage(self.stages[5])
        self.assertIsInstance(f2, TimeDelayFilter)
        self.assertEqual(f2.name, "electric time offset")
        self.assertEqual(f2.type, "time delay")
        self.assertEqual(f2.delay, 0.1525)
        self.assertEqual(f2.units_in, "count")
        self.assertEqual(f2.units_out, "count")


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


def test_inventory_type(obspy_inventory):
    """Test that the inventory is of the correct type."""
    assert isinstance(obspy_inventory, inventory.Inventory)


def test_instrument_sensitivity(channel_response, instrument_sensitivity):
    """Test the computed instrument sensitivity matches the expected value."""
    computed_sensitivity = channel_response.compute_instrument_sensitivity(
        instrument_sensitivity.frequency, 12
    )
    assert pytest.approx(computed_sensitivity, abs=1) == instrument_sensitivity.value


def test_stage_01(stages, subtests):
    """Test the first stage (5-pole Butterworth low-pass filter)."""
    f1 = create_filter_from_stage(stages[0])

    with subtests.test("filter type"):
        assert isinstance(f1, PoleZeroFilter)

    with subtests.test("filter name"):
        assert f1.name.lower() == "electric field 5 pole butterworth low-pass"

    with subtests.test("filter details"):
        assert f1.type == "zpk"
        assert f1.units_in == "millivolt per kilometer"
        assert f1.units_out == "millivolt per kilometer"
        assert f1.n_poles == 5
        assert f1.n_zeros == 0
        assert pytest.approx(f1.normalization_factor, abs=0.01) == 313383.60

    with subtests.test("poles"):
        expected_poles = [
            (-3.883009 + 11.951875j),
            (-3.883009 - 11.951875j),
            (-10.166194 + 7.386513j),
            (-10.166194 - 7.386513j),
            (-12.566371 + 0j),
        ]
        assert all(p1 == pytest.approx(p2) for p1, p2 in zip(f1.poles, expected_poles))


def test_stage_02(stages, subtests):
    """Test the second stage (1-pole Butterworth high-pass filter)."""
    f2 = create_filter_from_stage(stages[1])

    with subtests.test("filter type"):
        assert isinstance(f2, PoleZeroFilter)

    with subtests.test("filter details"):
        assert f2.name.lower() == "electric field 1 pole butterworth high-pass"
        assert f2.type == "zpk"
        assert pytest.approx(f2.normalization_factor, abs=0.01) == 1
        assert f2.n_poles == 1
        assert f2.n_zeros == 1

    with subtests.test("poles and zeros"):
        assert f2.poles == pytest.approx([-0.000167 + 0j])
        assert f2.zeros == pytest.approx([0j])


def test_stage_03(stages, subtests):
    """Test the third stage (mV/km to V/m conversion)."""
    f3 = create_filter_from_stage(stages[2])

    with subtests.test("filter type"):
        assert isinstance(f3, CoefficientFilter)

    with subtests.test("filter details"):
        assert f3.name == "mv per km to v per m".lower()
        assert f3.type == "coefficient"
        assert pytest.approx(f3.gain, abs=0.000001) == 1e-6
        assert f3.units_in == "mV/km"
        assert f3.units_out == "V/m"


def test_stage_04(stages, subtests):
    """Test the fourth stage (V/m to V conversion)."""
    f4 = create_filter_from_stage(stages[3])

    with subtests.test("filter type"):
        assert isinstance(f4, CoefficientFilter)

    with subtests.test("filter details"):
        assert f4.name == "v per m to v".lower()
        assert f4.type == "coefficient"
        assert pytest.approx(f4.gain, abs=0.01) == 84.5
        assert f4.units_in == "V/m"
        assert f4.units_out == "V"


def test_stage_05(stages, subtests):
    """Test the fifth stage (V to counts conversion)."""
    f5 = create_filter_from_stage(stages[4])

    with subtests.test("filter type"):
        assert isinstance(f5, CoefficientFilter)

    with subtests.test("filter details"):
        assert f5.name == "V to counts (electric)".lower()
        assert f5.type == "coefficient"
        assert f5.gain == 484733700000000.0
        assert f5.units_in == "V"
        assert f5.units_out == "count"


def test_stage_06(stages, subtests):
    """Test the sixth stage (time delay filter)."""
    f6 = create_filter_from_stage(stages[5])

    with subtests.test("filter type"):
        assert isinstance(f6, TimeDelayFilter)

    with subtests.test("filter details"):
        assert f6.name == "electric time offset"
        assert f6.type == "time delay"
        assert f6.delay == 0.1525
        assert f6.units_in == "count"
        assert f6.units_out == "count"


if __name__ == "__main__":
    unittest.main()
