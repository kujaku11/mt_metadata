"""Unit test package for mth5."""
from pathlib import Path

# assume tests is on the root level of mt_metadata
TEST_ROOT = Path(__file__).parent.parent.parent

STATIONXML_01 = TEST_ROOT.joinpath("data/fdsn-station_2021-02-12T23_28_49.xml")
STATIONXML_02 = TEST_ROOT.joinpath("data/StationXML_REW09.xml")
