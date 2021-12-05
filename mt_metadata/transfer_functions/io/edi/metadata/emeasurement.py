# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:21:06 2021

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
import numpy as np

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("emeasurement", SCHEMA_FN_PATHS)

# ==============================================================================
# magnetic measurements
# ==============================================================================
class EMeasurement(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._fmt_dict = {
            'id': '<.10g',
            'chtype': '<3',
            'x': '<4.1f',
            'y': '<4.1f',
            'z': '<4.1f',
            'x2': '<4.1f',
            'y2': '<4.1f',
            'z2': '<4.1f',
            'acqchan': '<4.0f',
            }
        
        self.id = None
        self.chtype = None
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.x2 = 0.
        self.y2 = 0.
        self.z2 = 0.
        self.acqchan = 0

        super().__init__(attr_dict=attr_dict, **kwargs)
        

    def __str__(self):
        return "\n".join(
            [f"{k} = {v}" for k, v in self.to_dict(single=True).items()]
        )

    def __repr__(self):
        return self.__str__()

    @property
    def dipole_length(self):
        if hasattr(self, "z"):
            return np.sqrt(
                (self.x2 - self.x) ** 2 + (self.y2 - self.y) ** 2 + self.z ** 2
            )
        else:
            return np.sqrt((self.x2 - self.x) ** 2 + (self.y2 - self.y) ** 2)

    @property
    def azimuth(self):
        if hasattr(self, "azm"):
            return self.azm
        try:
            return np.rad2deg(np.arctan2((self.y2 - self.y), (self.x2 - self.x)))
        except ZeroDivisionError:
            return 0.0

    @property
    def channel_number(self):
        if not isinstance(self.acqchan, (int, float)):
            try:
                return [int("".join(i for i in self.acqchan if i.isdigit()))][0]
            except (IndexError, ValueError):
                return 0
        return self.acqchan