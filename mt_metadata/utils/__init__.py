"""Unit test package for mth5."""
from pathlib import Path

# assume tests is on the root level of mt_metadata
TEST_ROOT = Path(__file__).parent.parent.parent

STATIONXML_01 = TEST_ROOT.joinpath("data/stationxml/fdsn_no_mt_info.xml")
STATIONXML_02 = TEST_ROOT.joinpath("data/stationxml/mtml_single_station.xml")
STATIONXML_MAGNETIC = TEST_ROOT.joinpath("data/stationxml/mtml_magnetometer_example.xml")
STATIONXML_ELECTRIC = TEST_ROOT.joinpath("data/stationxml/mtml_electrode_example.xml")
MT_EXPERIMENT_SINGLE_STATION = TEST_ROOT.joinpath("data/xml/single_station_mt_experiment.xml")
