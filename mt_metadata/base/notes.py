# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:35:45 2023

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
from pydantic import BaseModel

# =============================================================================
# pydantic Notes
# need to probably make each attribute a base class and then amalgamate them
# because we are not just type checking but style checking as well?


class Element(BaseModel, validate_assignment=True):
    @classmethod
    def parse_dict(cls, kw_dict):
        return cls.create_model(kw_dict)
