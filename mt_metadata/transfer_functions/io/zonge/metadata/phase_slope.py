# -*- coding: utf-8 -*-
"""

Created on Wed Dec  8 10:29:50 2021

:author: Jared Peacock

:license: MIT

"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("phase_slope", SCHEMA_FN_PATHS)
# =============================================================================


class PhaseSlope(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        super().__init__(attr_dict=attr_dict, **kwargs)
