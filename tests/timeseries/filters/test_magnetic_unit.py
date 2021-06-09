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


ToDo: 
-test ZerosPolesGainContinuous vs ZerosPolesGainDiscrete
(in one case we add a 'dt' as a kwarg)

20210216:
1. Revisit base class
2. continue on implementation
3. Set a call With Anna


"""
import unittest
from obspy.core import inventory

from mt_metadata.timeseries.filters import (
    ChannelResponseFilter,
    PoleZeroFilter,
    CoefficientFilter,
    TimeDelayFilter,
)
from mt_metadata.utils import STATIONXML_MAGNETIC
from mt_metadata.timeseries.filters.obspy_stages import create_filter_from_stage


class TestFilterMagnetic(unittest.TestCase):
    """
    Test filter translation from :class:`obspy.inventory.Network
    """

    def setUp(self):
        self.inventory = inventory.read_inventory(STATIONXML_MAGNETIC.as_posix())
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
        cr = ChannelResponseFilter(filters_list=filters_list)

        self.assertAlmostEqual(
            cr.compute_instrument_sensitivity(self.instrument_sensitivity.frequency),
            self.instrument_sensitivity.value,
            0,
        )

    def test_stage_01(self):
        f1 = create_filter_from_stage(self.stages[0])
        self.assertIsInstance(f1, PoleZeroFilter)
        self.assertEqual(f1.name, "magnetic field 3 pole Butterworth low-pass".lower())
        self.assertEqual(f1.type, "zpk")
        self.assertEqual(f1.units_in, "nT")
        self.assertEqual(f1.units_out, "V")
        self.assertEqual(f1.n_poles, 3)
        self.assertEqual(f1.n_zeros, 0)
        self.assertAlmostEqual(f1.normalization_factor, 1984.31, 2)
        self.assertListEqual(
            list(f1.poles),
            [(-6.283185 + 10.882477j), (-6.283185 - 10.882477j), (-12.566371 + 0j)],
        )

    def test_stage_02(self):
        f2 = create_filter_from_stage(self.stages[1])
        self.assertIsInstance(f2, CoefficientFilter)
        self.assertEqual(f2.name, "magnatometer A to D".lower())
        self.assertEqual(f2.type, "coefficient")
        self.assertEqual(f2.gain, 100)
        self.assertEqual(f2.units_in, "V")
        self.assertEqual(f2.units_out, "count")

    def test_stage_03(self):
        f2 = create_filter_from_stage(self.stages[2])
        self.assertIsInstance(f2, TimeDelayFilter)
        self.assertEqual(f2.name, "Hz time offset".lower())
        self.assertEqual(f2.type, "time delay")
        self.assertEqual(f2.delay, 0.2455)
        self.assertEqual(f2.units_in, "count")
        self.assertEqual(f2.units_out, "count")
