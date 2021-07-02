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
    TimeDelayFilter)
# =============================================================================

fn_path = Path(r"c:\Users\jpeacock\Documents\GitHub\mt_metadata\docs\source")

for level in [Survey, Station, Run, Auxiliary, Electric, Magnetic, 
              PoleZeroFilter, FrequencyResponseTableFilter, CoefficientFilter,
              FIRFilter, TimeDelayFilter]:
    
    lines = [".. role:: red",
             ".. role:: blue",
             ".. role:: navy",
             ""]

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
        
        
        
