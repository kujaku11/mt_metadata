# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema
from .standards import SCHEMA_FN_PATHS
from . import Channel

# =============================================================================
attr_dict = get_schema("channel", SCHEMA_FN_PATHS)
# =============================================================================
class Auxiliary(Channel):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
