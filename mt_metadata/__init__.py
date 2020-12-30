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
from pathlib import Path
from mt_metadata.utils import mt_logger

__author__ = """Jared Peacock"""
__email__ = "jpeacock@usgs.gov"
__version__ = "0.1.0"

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

module_path = Path(__file__).parent 
log_config_file = module_path.joinpath("utils", "logging_config.yaml")

logger = mt_logger.MTLogger().get_logger("mt_metadata")
logger.debug("Starting MT Metadata")

# with open(log_config_file, "r") as fid:
#     config_dict = yaml.safe_load(fid)
# logging.config.dictConfig(config_dict)

# # open root logger
# logger = logging.getLogger(__name__)

# # make sure everything is working
# logger.info("Started mt_metadata")
# logger.debug("Beginning debug mode for mt_metadata")
# debug_fn = logger.root.handlers[1].baseFilename
# error_fn = logger.root.handlers[2].baseFilename

# logger.info("Debug Log file can be found at {0}".format(debug_fn))
# logger.info("Error Log file can be found at {0}".format(error_fn))