# -*- coding: utf-8 -*-
"""
Root logging

Created on Mon May 18 15:34:05 2020

@author: jpeacock
"""

import logging
import logging.config
from pathlib import Path
import yaml

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
CONF_PATH = Path(__file__).parent
CONF_FILE = Path.joinpath(CONF_PATH, "logging_config.yaml")
LOG_PATH = CONF_PATH.parent.parent.joinpath("logs")
LEVEL_DICT = {"debug": logging.DEBUG,
              "info": logging.INFO,
              "warning": logging.WARNING,
              "error": logging.ERROR,
              "critical": logging.CRITICAL}

if not CONF_FILE.exists():
    CONF_FILE = None

class MTLogger:
    @staticmethod
    def load_config():
        config_file = Path(CONF_FILE)
        with open(config_file, "r") as fid:
            config_dict = yaml.safe_load(fid)
        logging.config.dictConfig(config_dict)

    @staticmethod
    def get_logger(logger_name, fn=None, level="debug"):
        logger = logging.getLogger(logger_name)
        logger.addHandler(logging.NullHandler())
        if fn is not None:
            fn = LOG_PATH.joinpath(fn)
            fn_handler = logging.FileHandler(fn, mode="a")
            fn_handler.setFormatter(FORMATTER)
            fn_handler.setLevel(LEVEL_DICT[level.lower()])
            logger.addHandler(fn_handler)

        return logger
