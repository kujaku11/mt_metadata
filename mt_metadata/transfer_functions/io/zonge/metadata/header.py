# -*- coding: utf-8 -*-
"""
====================
zonge
====================
    * Tools for interfacing with MTFT24
    * Tools for interfacing with MTEdit
    
    
Created on Tue Jul 11 10:53:23 2013
@author: jpeacock-pr
"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import Survey, Tx, Rx, MTEdit, Unit, GPS
from mt_metadata.utils.validators import validate_attribute

# =============================================================================
attr_dict = get_schema("header", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("survey", SCHEMA_FN_PATHS), name="survey")
attr_dict.add_dict(get_schema("tx", SCHEMA_FN_PATHS), name="tx")
attr_dict.add_dict(get_schema("rx", SCHEMA_FN_PATHS), name="rx")
attr_dict.add_dict(MTEdit()._attr_dict, name="m_t_edit")
attr_dict.add_dict(get_schema("gps", SCHEMA_FN_PATHS), name="g_p_s")
attr_dict.add_dict(get_schema("unit", SCHEMA_FN_PATHS), name="unit")


# =============================================================================

class Header(Base):
    __doc__ = write_lines(attr_dict)
    
    def __init__(self, **kwargs):
        self.survey = Survey()
        self.tx = Tx()
        self.rx = Rx()
        self.m_t_edit = MTEdit()
        self.g_p_s = GPS()
        self.unit = Unit()
        super().__init__(attr_dict=attr_dict, **kwargs)
        
        
    def read_header(self, lines):
        """
        Read the header of an AVG file and fill attributes accordingly
        
        :param lines: list of lines to read
        :type lines: list of strings

        """

        for ii, line in enumerate(lines):
            if line.find("=") > 0 and line.find("$") == 0:
                key, value = line[1:].split("=")
                key = ".".join([validate_attribute(k) for k in key.replace(":", ".").split('.')])
                
                value = value.lower().strip()
                if "," in value:
                    value = [v.strip() for v in value.split(",")]
                if "length" in key:
                    value = value.split()
                    if len(value) > 1:
                        value = value[0]
                    else: 
                        value = value[0].strip()
                self.set_attr_from_name(key, value)
            elif line[0] == "S":
                break
            
        return lines [ii:]
    
    

