# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 10:33:27 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
from mt_metadata.utils.mt_logger import setup_logger

# =============================================================================
# Translate between metadata and inventory: mapping dictionaries
# =============================================================================
class BaseTranslator:
    """
    Base translator for StationXML <--> MT Metadata
    
    """

    def __init__(self):
        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")
        self.xml_translator = {
            "alternate_code": None,
            "code": None,
            "comments": None,
            "data_availability": None,
            "description": None,
            "historical_code": None,
            "identifiers": None,
            "restricted_status": None,
            "source_id": None,
        }
        
        self.mt_translator = self.flip_dict(self.xml_translator)
     
    @staticmethod
    def flip_dict(original_dict):
        """
        Flip keys and values of the dictionary
        
        Need to take care of duplicate names and lists of names
        
        :param original_dict: original dictionary
        :type original_dict: dict
        :return: reversed dictionary
        :rtype: dictionary
    
        """
        flipped_dict = {}
    
        for k, v in original_dict.items():
            if v in [None, "special"]:
                continue
            if k in [None]:
                continue
            if isinstance(v, (list, tuple)):
                # bit of a hack, needs to be more unique.
                for value in v:
                    flipped_dict[value] = k
            else:
                flipped_dict[str(v)] = k
    
        return flipped_dict
            