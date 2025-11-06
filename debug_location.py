#!/usr/bin/env python3

import sys


sys.path.insert(0, r"c:\Users\peaco\OneDrive\Documents\GitHub\mt_metadata")

from mt_metadata import TF_EDI_METRONIX
from mt_metadata.transfer_functions.core import TF


# Create TF object
print("Loading TF object...")
tf_obj = TF(fn=TF_EDI_METRONIX)
tf_obj.read()

# Create EDI object from TF
print("Converting TF to EDI...")
edi_obj = tf_obj.to_edi()

# Compare station metadata
print("\nTF station metadata (required=False):")
tf_st = tf_obj.station_metadata.to_dict(single=True, required=False)
for key, value in tf_st.items():
    if "location" in key.lower():
        print(f"  {key}: {value}")

print("\nEDI station metadata:")
edi_st = edi_obj.station_metadata.to_dict(single=True)
for key, value in edi_st.items():
    if "location" in key.lower():
        print(f"  {key}: {value}")

print("\nDifferences:")
for key in edi_st.keys():
    if edi_st[key] != tf_st.get(key):
        print(f"  {key}: EDI={edi_st[key]} vs TF={tf_st.get(key)}")
