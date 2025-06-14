# -*- coding: utf-8 -*-
"""

Created on Wed Dec  8 11:00:57 2021

:author: Jared Peacock

:license: MIT

"""

from mt_metadata.base import Base, get_schema

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines

from .standards import SCHEMA_FN_PATHS


# =============================================================================
attr_dict = get_schema("ch", SCHEMA_FN_PATHS)
# =============================================================================


class CH(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        super().__init__(attr_dict=attr_dict, **kwargs)
