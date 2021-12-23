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
from mt_metadata.base.helpers import write_block

fn_path = Path(__file__).parent.joinpath("source")
# =============================================================================


def write_ts_metadata_standards():
    
    from mt_metadata.timeseries import (
        Survey,
        Station,
        Run,
        Auxiliary,
        Electric,
        Magnetic,
    )
    from mt_metadata.timeseries.filters import (
        PoleZeroFilter,
        FrequencyResponseTableFilter,
        CoefficientFilter,
        FIRFilter,
        TimeDelayFilter,
    )
    
    for level in [
        Survey,
        Station,
        Run,
        Auxiliary,
        Electric,
        Magnetic,
        PoleZeroFilter,
        FrequencyResponseTableFilter,
        CoefficientFilter,
        FIRFilter,
        TimeDelayFilter,
    ]:
    
        lines = [".. role:: red", ".. role:: blue", ".. role:: navy", ""]
    
        obj = level()
        lines += [f"{obj._class_name.capitalize()}"]
        lines += ["=" * len(lines[-1])]
        lines += ["", ""]
    
        for key, k_dict in obj._attr_dict.items():
            if k_dict["required"]:
                k_dict["required"] = ":red:`True`"
            else:
                k_dict["required"] = ":blue:`False`"
            lines += write_block(key, k_dict)
    
        fn = fn_path.joinpath(f"ts_{obj._class_name}.rst")
        with fn.open(mode="w") as fid:
            fid.write("\n".join(lines))
            
def write_tf_metadata_standards():
    
    from mt_metadata.transfer_functions.tf import (
        Survey,
        Station,
        Run,
        Auxiliary,
        Electric,
        Magnetic,
        TransferFunction
    )
    
    for level in [
        Survey,
        Station,
        Run,
        Auxiliary,
        Electric,
        Magnetic,
        TransferFunction
    ]:
    
        lines = [".. role:: red", ".. role:: blue", ".. role:: navy", ""]
    
        obj = level()
        lines += [f"{obj._class_name.capitalize()}"]
        lines += ["=" * len(lines[-1])]
        lines += ["", ""]
    
        for key, k_dict in obj._attr_dict.items():
            if k_dict["required"]:
                k_dict["required"] = ":red:`True`"
            else:
                k_dict["required"] = ":blue:`False`"
            lines += write_block(key, k_dict)
    
        fn = fn_path.joinpath(f"tf_{obj._class_name}.rst")
        with fn.open(mode="w") as fid:
            fid.write("\n".join(lines))

def write_emtfxml_metadata_standards():
    
    from mt_metadata.transfer_functions.io.emtfxml.metadata import (
        EMTF, 
        ExternalUrl,
        PrimaryData,
        Attachment,
        Provenance,
        Copyright,
        Site,
        FieldNotes,
        ProcessingInfo,
        StatisticalEstimates,
        Estimate,
        DataTypes,
        DataType,
        SiteLayout)
    
    for level in [
        EMTF, 
        ExternalUrl,
        PrimaryData,
        Attachment,
        Provenance,
        Copyright,
        Site,
        FieldNotes,
        ProcessingInfo,
        StatisticalEstimates,
        Estimate,
        DataTypes,
        DataType,
        SiteLayout
    ]:
    
        lines = [".. role:: red", ".. role:: blue", ".. role:: navy", ""]
    
        obj = level()
        lines += [f"{obj._class_name.capitalize()}"]
        lines += ["=" * len(lines[-1])]
        lines += ["", ""]
    
        for key, k_dict in obj._attr_dict.items():
            if k_dict["required"]:
                k_dict["required"] = ":red:`True`"
            else:
                k_dict["required"] = ":blue:`False`"
            lines += write_block(key, k_dict)
    
        fn = fn_path.joinpath(f"emtfxml_{obj._class_name}.rst")
        with fn.open(mode="w") as fid:
            fid.write("\n".join(lines))
            
# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    write_ts_metadata_standards()
    write_tf_metadata_standards()
    write_emtfxml_metadata_standards()
