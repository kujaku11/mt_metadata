# -*- coding: utf-8 -*-
"""
EMTFXML
==========

This is meant to follow Anna's XML schema for transfer functions

Created on Sat Sep  4 17:59:53 2021

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from pathlib import Path
from collections import OrderedDict
from xml.etree import cElementTree as et

from mt_metadata.transfer_functions import emtf_xml
from mt_metadata.utils.mt_logger import setup_logger
from mt_metadata.base import helpers
from mt_metadata.utils.validators import validate_attribute

# =============================================================================
# EMTFXML
# =============================================================================

class EMTFXML(emtf_xml.EMTF):
    """
    This is meant to follow Anna's XML schema for transfer functions
    """
    
    def __init__(self):
        super().__init__()
        self.external_url = emtf_xml.ExternalUrl()
        
    def read(self, fn):
        """
        Read xml file
        
        :param fn: DESCRIPTION
        :type fn: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        fn = Path(fn)
        if not fn.exists():
            raise IOError(f"Cannot find: {fn}")
            
        root = et.parse(fn).getroot()
        root_dict = helpers.element_to_dict(root)
        root_dict = root_dict[list(root_dict.keys())[0]]
        root_dict = self._convert_keys_to_lower_case(root_dict)
        
        
        self._read_description(root_dict)
        self._read_product_id(root_dict)
        self._read_notes(root_dict)
        self._read_tags(root_dict)
        self._read_external_url(root_dict)
        
    def _read_description(self, root_dict):
        self.description = root_dict["description"]
        
    def _read_product_id(self, root_dict):
        self.product_id = root_dict["product_id"]
    
    def _read_notes(self, root_dict):
        self.notes = root_dict["notes"]
        
    def _read_tags(self, root_dict):
        self.tags = root_dict["tags"]
        
    def _read_external_url(self, root_dict):
        self.external_url.from_dict(root_dict["external_url"])
        
    def _convert_keys_to_lower_case(self, root_dict):
        """
        Convert the key names to lower case and separated by _ if
        needed
        
        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        res = OrderedDict()
        if isinstance(root_dict, (dict, OrderedDict)):
            for key in root_dict.keys():
                new_key = validate_attribute(key)
                res[new_key] = root_dict[key]
                if isinstance(res[new_key], (dict, OrderedDict, list)):
                   res[new_key] = self._convert_keys_to_lower_case(res[new_key])
        elif isinstance(root_dict, list):
            for item in root_dict:
                item = self._convert_keys_to_lower_case(item)
        return res
            
        
    
        
        
            
        
        
