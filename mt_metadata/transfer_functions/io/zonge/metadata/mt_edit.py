# -*- coding: utf-8 -*-
"""

Created on Wed Dec  8 11:00:57 2021

:author: Jared Peacock

:license: MIT

"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import Auto, PhaseSlope, DPlus
# =============================================================================
attr_dict = get_schema("mt_edit", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("auto", SCHEMA_FN_PATHS), name="auto")
attr_dict.add_dict(get_schema("phase_slope", SCHEMA_FN_PATHS), name="phase_slope")
attr_dict.add_dict(get_schema("d_plus", SCHEMA_FN_PATHS), name="d_plus")
# =============================================================================

class MTEdit(Base):
    __doc__ = write_lines(attr_dict)
    
    def __init__(self, **kwargs):
        
        self.auto = Auto()
        self.phase_slope = PhaseSlope()
        self.d_plus = DPlus()
        super().__init__(attr_dict=attr_dict, **kwargs)

