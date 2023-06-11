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
__version__ = "0.2.3"

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
    "default",
]

# =============================================================================
# Initiate loggers
# =============================================================================
LOG_LEVEL = "info"

load_logging_config()
debug_logger = setup_logger(
    __name__, fn=f"mt_metadata_{LOG_LEVEL}", level=LOG_LEVEL
)
debug_logger.debug(f"Starting MT Metadata {LOG_LEVEL} Log File")

error_logger = setup_logger("error", fn="mt_metadata_error", level="error")


# test data files
# assume tests is on the root level of mt_metadata
DATA_DIR = Path(__file__).absolute().parent

### Station XML files
STATIONXML_01 = DATA_DIR.joinpath("data/stationxml/fdsn_no_mt_info.xml")
STATIONXML_02 = DATA_DIR.joinpath("data/stationxml/mtml_single_station.xml")
STATIONXML_MAGNETIC = DATA_DIR.joinpath(
    "data/stationxml/mtml_magnetometer_example.xml"
)
STATIONXML_ELECTRIC = DATA_DIR.joinpath(
    "data/stationxml/mtml_electrode_example.xml"
)
STATIONXML_FAP = DATA_DIR.joinpath(
    "data/stationxml/station_xml_with_fap_example.xml"
)
STATIONXML_FIR = DATA_DIR.joinpath(
    "data/stationxml/station_xml_with_fir_example.xml"
)
STATIONXML_MULTIPLE_NETWORKS = DATA_DIR.joinpath(
    "data/stationxml/multiple_networks_example.xml"
)

### MT EXPERIMENT files
MT_EXPERIMENT_SINGLE_STATION = DATA_DIR.joinpath(
    "data/mt_xml/single_station_mt_experiment.xml"
)
MT_EXPERIMENT_MULTIPLE_RUNS = DATA_DIR.joinpath(
    "data/mt_xml/multi_run_experiment.xml"
)
MT_EXPERIMENT_MULTIPLE_RUNS_02 = DATA_DIR.joinpath(
    "data/mt_xml/multi_run_experiment_02.xml"
)

### Transfer function files
TF_ZMM = DATA_DIR.joinpath("data/transfer_functions/tf_zmm.zmm")
TF_ZSS_TIPPER = DATA_DIR.joinpath("data/transfer_functions/tf_zss_tipper.zss")
TF_JFILE = DATA_DIR.joinpath("data/transfer_functions/tf_jfile.j")
TF_XML = DATA_DIR.joinpath("data/transfer_functions/tf_xml.xml")
TF_XML_NO_SITE_LAYOUT = DATA_DIR.joinpath(
    "data/transfer_functions/tf_xml_no_site_layout.xml"
)
TF_XML_COMPLETE_REMOTE_INFO = DATA_DIR.joinpath(
    "data/transfer_functions/tf_xml_complete_remote_info.xml"
)
TF_POOR_XML = DATA_DIR.joinpath("data/transfer_functions/tf_poor_xml.xml")
TF_EDI_PHOENIX = DATA_DIR.joinpath("data/transfer_functions/tf_edi_phoenix.edi")
TF_EDI_METRONIX = DATA_DIR.joinpath(
    "data/transfer_functions/tf_edi_metronix.edi"
)
TF_EDI_CGG = DATA_DIR.joinpath("data/transfer_functions/tf_edi_cgg.edi")
TF_EDI_QUANTEC = DATA_DIR.joinpath("data/transfer_functions/tf_edi_quantec.edi")
TF_EDI_RHO_ONLY = DATA_DIR.joinpath(
    "data/transfer_functions/tf_edi_rho_only.edi"
)
TF_EDI_SPECTRA = DATA_DIR.joinpath(
    "data/transfer_functions/tf_edi_spectra_in.edi"
)
TF_EDI_SPECTRA_OUT = DATA_DIR.joinpath(
    "data/transfer_functions/tf_edi_spectra_out.edi"
)
TF_EDI_NO_ERROR = DATA_DIR.joinpath(
    "data/transfer_functions/tf_edi_no_error.edi"
)
TF_AVG = DATA_DIR.joinpath("data/transfer_functions/tf_avg.avg")
TF_AVG_TIPPER = DATA_DIR.joinpath("data/transfer_functions/tf_avg_tipper.avg")
TF_AVG_NEWER = DATA_DIR.joinpath("data/transfer_functions/tf_avg_newer.avg")
