# -*- coding: utf-8 -*-
"""
This module contains the metadata Decimation class from aurora.

TODO: consider renaming to AuroraDecimation to contrast with other Decimation objects.

Created on Thu Feb 17 14:15:20 2022

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("decimation", SCHEMA_FN_PATHS)
# =============================================================================


class Decimation(Base):
    """
        The decimation class contains two key pieces of information:
        1. The decimation level, an integer that tells the sequential order in a decimation scheme.
        2. The decimation factor.  This is normally an integer, but the decimation.json does allow for floating point values.

    """
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        super().__init__(attr_dict=attr_dict, **kwargs)
