# -*- coding: utf-8 -*-
"""
Example of how to read in a StationXML and create an MTH5 file,
and translate back to a StationXML from MTH5 file

The MTH5 file will contain only the metadata.  When data is 
added the metadata will be checked for consistency and data 
always wins.

"""

from mth5 import mth5
from mt_metadata.timeseries import stationxml
from mt_metadata.utils import STATIONXML_01

# instantiate a translator for StationXML <-> Experiment
translator = stationxml.XMLInventoryMTExperiment()

# read StationXML, translate to metadata.timeseries.Experiment object
experiment = translator.xml_to_mt(stationxml_fn=STATIONXML_01)

# create MTH5 from experiment metadata
m = mth5.MTH5()
m.open_mth5(r"from_stationxml.h5")
m.from_experiment(experiment)

# Output StationXML from an MTH5 file
new_experiment = m.to_experiment()
new_station_xml = translator.mt_to_xml(new_experiment, 
                                       stationxml_fn="new_stationxml.xml")

m.close_mth5()
