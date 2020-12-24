# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 12:46:13 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
from pathlib import Path
from mt_metadata.base import BaseDict

p = Path(r"c:\Users\jpeacock\Documents\GitHub\mt_metadata\mt_metadata\transfer_functions\tf\standards")

json_list = []
for fn in p.glob("*.csv"):
    print(fn)
    b = BaseDict()
    b.from_csv(fn)
    json_fn = Path(fn.parent, f"{fn.stem}.json")
    json_list.append(b.to_json(json_fn))