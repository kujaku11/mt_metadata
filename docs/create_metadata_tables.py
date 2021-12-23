# -*- coding: utf-8 -*-
"""

Make a block for each metadata keyword so that a user can search the documents
easier.

Created on Thu Jul 30 17:01:34 2020

:author: Jared Peacock

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from pathlib import Path
import importlib
import inspect

from mt_metadata.base.helpers import write_block

FN_PATH = Path(__file__).parent.joinpath("source")
# =============================================================================

def to_caps(name):
    """
    convert class name into mixed upper case
    
    :param name: DESCRIPTION
    :type name: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """
    
    return "".join(name.replace("_", " ").title().split())

def write_attribute_table_file(level, stem):
    """
    Write an attribute table for the given metadata class
    
    :param level: DESCRIPTION
    :type level: TYPE
    :param stem: DESCRIPTION
    :type stem: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """
    
    lines = [".. role:: red", ".. role:: blue", ".. role:: navy", ""]

    obj = level()
    lines += [f"{to_caps(obj._class_name)}"]
    lines += ["=" * len(lines[-1])]
    lines += ["", ""]

    for key, k_dict in obj._attr_dict.copy().items():
        if k_dict["required"]:
            k_dict["required"] = ":red:`True`"
        else:
            k_dict["required"] = ":blue:`False`"
        lines += write_block(key, k_dict)

    fn = FN_PATH.joinpath(f"{stem}_{obj._class_name}.rst")
    with fn.open(mode="w") as fid:
        fid.write("\n".join(lines))
    
    return fn

        
def write_metadata_standards(module_name, stem):
    """
    write a file for each metadata class in module
    
    :param module_name: DESCRIPTION
    :type module_name: TYPE
    :param stem: DESCRIPTION
    :type stem: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    """
    mod = importlib.import_module(module_name)
    
    mod_dict = dict(inspect.getmembers(mod, inspect.isclass))
    fn_list = []
    for key, obj in mod_dict.items():
        fn_list.append(write_attribute_table_file(obj, stem))
    
    return fn_list
    
            
# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    
    module_dict = {
        "mt_metadata.timeseries": ("ts", "Time Series"),
        "mt_metadata.timeseries.filters": ("ts_filter", "Time Series Filters"),
        "mt_metadata.transfer_functions.tf": ("tf", "Transfer Function"),
        "mt_metadata.transfer_functions.io.emtfxml.metadata": ("tf_emtfxml", "EMTF XML"),
        "mt_metadata.transfer_functions.io.edi.metadata": ("tf_edi", "EDI"),
        "mt_metadata.transfer_functions.io.zfiles.metadata": ("tf_zmm", "Z-Files"),
        "mt_metadata.transfer_functions.io.jfiles.metadata": ("tf_jfile", "J-Files"),
        "mt_metadata.transfer_functions.io.zonge.metadata": ("tf_zonge", "Zonge AVG"),
        }
    
    for module, stem in module_dict.items():
        fn_list = write_metadata_standards(module, stem[0])
        
        lines = [
            ".. role:: red",
            ".. role:: blue",
            ".. role:: navy",
            stem[1],
            "=" * 30,
            "",
            ".. toctree::",
            "    :maxdepth: 1",
            "    :caption: Metadata Definitions",
            "",
            ]
        lines += [f"{' '*4}{f.stem}" for f in fn_list]
        lines.append("")
                  
        with open(FN_PATH.joinpath(f"{stem[0]}_index.rst"), "w") as fid:
            fid.write("\n".join(lines))
                      
        
        
