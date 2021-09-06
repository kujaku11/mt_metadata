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
import inspect
from pathlib import Path
from collections import OrderedDict
from xml.etree import cElementTree as et

from mt_metadata.transfer_functions import emtf_xml
from mt_metadata.utils.mt_logger import setup_logger
from mt_metadata.base import helpers
from mt_metadata.utils.validators import validate_attribute
from mt_metadata.transfer_functions.tf import Instrument

meta_classes = dict([(validate_attribute(k), v) for k, v in inspect.getmembers(emtf_xml, inspect.isclass)])
meta_classes["instrument"] = Instrument
meta_classes["magnetometer"] = Instrument
# =============================================================================
# EMTFXML
# =============================================================================

class EMTFXML(emtf_xml.EMTF):
    """
    This is meant to follow Anna's XML schema for transfer functions
    """
    
    def __init__(self):
        super().__init__()
        self._root_dict = None
        self.logger = setup_logger(self.__class__.__name__)
        self.external_url = emtf_xml.ExternalUrl()
        self.primary_data = emtf_xml.PrimaryData()
        self.attachment = emtf_xml.Attachment()
        self.provenance = emtf_xml.Provenance()
        self.copyright = emtf_xml.Copyright()
        self.site = emtf_xml.Site()
        self.field_notes = [emtf_xml.FieldNotes()]
        self.processing_info = emtf_xml.ProcessingInfo()
        self.statistical_estimates = emtf_xml.StatisticalEstimates()
        self.data_types = emtf_xml.DataTypes()
        self.site_layout = emtf_xml.SiteLayout()
        self.tf = emtf_xml.TransferFunction()
        
        
        self.element_keys = [
            "description",
            "product_id",
            "sub_type", 
            "notes",
            "external_url",
            "primary_data",
            "attachment",
            "provenance",
            "copyright",
            "site",
            "field_notes",
            "processing_info",
            "statistical_estimates",
            "data_types",
            "site_layout",
            "data"
            ]
        
        self._reader_dict = {
            "description": self._read_description,
            "product_id": self._read_product_id,
            "sub_type": self._read_sub_type,
            "notes": self._read_notes,
            "tags": self._read_tags,
            "field_notes": self._read_field_notes,
            "statistical_estimates": self._read_statistical_estimates,
            "site_layout": self._read_site_layout,
            "data_types": self._read_data_types,
            "data": self._read_data,
            }
        
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
        self._root_dict = root_dict

        for element in self.element_keys:
            if element in self._reader_dict.keys():
                self._reader_dict[element](root_dict)
            else:
                self._read_element(root_dict, element)
                
    def _read_single(self, root_dict, key):
        try:
            setattr(self, key, root_dict[key])
        except KeyError:
            self.logger.debug("no description in xml")
        
    def _read_description(self, root_dict):
        self._read_single(root_dict, "description")

    def _read_product_id(self, root_dict):
        self._read_single(root_dict, "product_id")
        
    def _read_sub_type(self, root_dict):
        self._read_single(root_dict, "sub_type")
    
    def _read_notes(self, root_dict):
        self._read_single(root_dict, "notes")
        
    def _read_tags(self, root_dict):
        self._read_single(root_dict, "tags")
            
    def _read_element(self, root_dict, element_name):
        """
        generic read an element given a name 
        
        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :param element_name: DESCRIPTION
        :type element_name: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        element_name = validate_attribute(element_name)
        if element_name in ["field_notes"]:
            self._read_field_notes(root_dict)
        elif element_name in ["statistical_estimates"]:
            self._read_statistical_estimates(root_dict)
        elif element_name in ["site_layout"]:
            self._read_site_layout(root_dict)
        else:
            try:
                value = root_dict[element_name]
                element_dict = {element_name: value}
                getattr(self, element_name).from_dict(element_dict)
                    
            except KeyError:
                print(f"No {element_name} in EMTF XML")
                self.logger.debug(f"No {element_name} in EMTF XML")
            
    def _read_field_notes(self, root_dict):
        """
        Field notes are odd so have a special reader to do it piece by
        painstaking piece.
        
        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self.field_notes = []
        for run in root_dict["field_notes"]:
            f = meta_classes["field_notes"]()
            f.run = run["run"]
            f.instrument.from_dict({"instrument": run["instrument"]})
            
            
            if isinstance(run["magnetometer"], list):
                f.magnetometer = []
                for mag in run["magnetometer"]:
                    m = meta_classes["magnetometer"]()
                    m.from_dict({"magnetometer": mag})
                    f.magnetometer.append(m)
            else:
                f.magnetometer = meta_classes["magnetometer"]()
                f.magnetometer.from_dict({"magnetometer": run["magnetometer"]})
                
            if isinstance(run["dipole"], list):
                f.dipole = []
                for mag in run["dipole"]:
                    m = meta_classes["dipole"]()
                    m.from_dict({"dipole": mag})
                    f.dipole.append(m)
            else:
                f.dipole = meta_classes["dipole"]()
                f.dipole.from_dict({"dipole": run["dipole"]})
            
            self.field_notes.append(f)
            
            
    def _read_statistical_estimates(self, root_dict):
        """
        Read in statistical estimate descriptions
        
        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        self.statistical_estimates.estimates_list = root_dict["statistical_estimates"]["estimate"]
            
    def _read_data_types(self, root_dict):
        """
        Read in data types
        
        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        self.data_types.data_types_list = root_dict["data_types"]["data_type"]
        
    def _read_site_layout(self, root_dict):
        """
        read site layout into the proper input/output channels
        
        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        # read input channels
        for ch in ['input_channels', 'output_channels']:
            ch_list = []
            try:
                c_list = root_dict["site_layout"][ch]["magnetic"]
                if c_list is None:
                    continue
                if not isinstance(c_list, list):
                    c_list = [c_list]
                ch_list += [{"magnetic": ch_dict} for ch_dict in c_list]
                    
            except (KeyError):
                pass
            
            try:
                c_list = root_dict["site_layout"][ch]["electric"]
                if c_list is None:
                    continue
                if not isinstance(c_list, list):
                    c_list = [c_list]
                ch_list += [{"electric": ch_dict} for ch_dict in c_list]
            except (KeyError):
                pass

            setattr(self.site_layout, ch, ch_list)
            

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
            res = []
            for item in root_dict:
                item = self._convert_keys_to_lower_case(item)
                res.append(item)
        return res
    
    def _read_data(self, root_dict):
        """
        Read data use 
        :param root_dict: DESCRIPTION
        :type root_dict: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        self.tf = emtf_xml.TransferFunction()
        self.tf.read_data(root_dict)
    
        
        
            
        
        
