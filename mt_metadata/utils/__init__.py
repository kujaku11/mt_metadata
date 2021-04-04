"""Unit test package for mth5."""
from pathlib import Path

# assume tests is on the root level of mt_metadata
TEST_ROOT = Path(__file__).parent.parent.parent

STATIONXML_01 = TEST_ROOT.joinpath("data/xml/fdsn_no_mt_info.xml")
STATIONXML_02 = TEST_ROOT.joinpath("data/xml/mtml_single_station.xml")
STATIONXML_MAGNETIC = TEST_ROOT.joinpath("data/xml/mtml_magnetometer_example.xml")
STATIONXML_ELECTRIC = TEST_ROOT.joinpath("data/xml/mtml_electrode_example.xml")
