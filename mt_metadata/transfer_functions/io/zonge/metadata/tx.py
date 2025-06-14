# -*- coding: utf-8 -*-
"""

Created on Wed Dec  8 10:29:50 2021

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
attr_dict = get_schema("tx", SCHEMA_FN_PATHS)
# =============================================================================


class Tx(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        super().__init__(attr_dict=attr_dict, **kwargs)
