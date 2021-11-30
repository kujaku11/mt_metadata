# -*- coding: utf-8 -*-
"""
==================
metadata
==================

This module deals with metadata as defined by the MT metadata standards.

There are multiple containers for each type of metadata, named appropriately.

Each container will be able to read and write:
    * dictionary
    * json
    * xml
    * csv?
    * pandas.Series
    * anything else?


Each container has an attribute called _attr_dict which dictates if the
attribute is included in output objects, the data type, whether it is a
required parameter, and the style of output.  This should help down the road
with validation and keeping the data types consistent.  And if things change
you should only have to changes these dictionaries.

:copyright:
    Jared Peacock (jpeacock@usgs.gov)
    
:license: 
    MIT


"""

# =============================================================================
# Package details
# =============================================================================


__author__ = """Jared Peacock"""
__email__ = "jpeacock@usgs.gov"
__version__ = "0.1.6"

# =============================================================================
# Imports
# =============================================================================
from pathlib import Path

from mt_metadata.utils.mt_logger import setup_logger, load_logging_config

# =============================================================================
# Global Variables
# =============================================================================


ACCEPTED_STYLES = [
    "name",
    "url",
    "email",
    "number",
    "date",
    "free form",
    "time",
    "date time",
    "name list",
    "number list",
    "controlled vocabulary",
    "alpha numeric",
]

REQUIRED_KEYS = [
    "attribute",
    "type",
    "required",
    "units",
    "style",
    "description",
    "options",
    "alias",
    "example",
]

# =============================================================================
# Initiate loggers
# =============================================================================
LOG_LEVEL = "info"

load_logging_config()
debug_logger = setup_logger(__name__, fn=f"mt_metadata_{LOG_LEVEL}", level=LOG_LEVEL)
debug_logger.debug(f"Starting MT Metadata {LOG_LEVEL} Log File")

error_logger = setup_logger("error", fn="mt_metadata_error", level="error")


# test data files
# assume tests is on the root level of mt_metadata
DATA_DIR = Path(__file__).absolute().parent

### Station XML files
STATIONXML_01 = DATA_DIR.joinpath("data/stationxml/fdsn_no_mt_info.xml")
STATIONXML_02 = DATA_DIR.joinpath("data/stationxml/mtml_single_station.xml")
STATIONXML_MAGNETIC = DATA_DIR.joinpath("data/stationxml/mtml_magnetometer_example.xml")
STATIONXML_ELECTRIC = DATA_DIR.joinpath("data/stationxml/mtml_electrode_example.xml")
STATIONXML_FAP = DATA_DIR.joinpath("data/stationxml/station_xml_with_fap_example.xml")
STATIONXML_FIR = DATA_DIR.joinpath("data/stationxml/station_xml_with_fir_example.xml")

### MT EXPERIMENT files
MT_EXPERIMENT_SINGLE_STATION = DATA_DIR.joinpath(
    "data/mt_xml/single_station_mt_experiment.xml"
)
MT_EXPERIMENT_MULTIPLE_RUNS = DATA_DIR.joinpath("data/mt_xml/multi_run_experiment.xml")
MT_EXPERIMENT_MULTIPLE_RUNS_02 = DATA_DIR.joinpath("data/mt_xml/multi_run_experiment_02.xml")

### Transfer function files
TF_ZMM = DATA_DIR.joinpath("data/transfer_functions/example_emtf.zmm")
TF_JFILE = DATA_DIR.joinpath("data/transfer_functions/example_birrp.j")
TF_XML = DATA_DIR.joinpath("data/transfer_functions/emtf_xml_example_02.xml")
TF_EDI_PHOENIX = DATA_DIR.joinpath("data/transfer_functions/IEB0537A_Phoenix.edi")
TF_EDI_METRONIX = DATA_DIR.joinpath("data/transfer_functions/IEB0858A_metronix.edi")
TF_EDI_CGG = DATA_DIR.joinpath("data/transfer_functions/EGC022_CGG.edi")
TF_EDI_QUANTEC = DATA_DIR.joinpath("data/transfer_functions/IEA00184_Qut.edi")
