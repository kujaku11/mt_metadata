#!/usr/bin/env python3

from mt_metadata import TF_AVG
from mt_metadata.transfer_functions.core import TF


# Load the TF data
tf = TF(fn=TF_AVG)
tf.read()

print("=== SURVEY METADATA ===")
survey_meta = tf.survey_metadata.to_dict(single=True)
for k, v in survey_meta.items():
    print(f'            ("{k}", {repr(v)}),')

print("\n=== STATION METADATA ===")
station_meta = tf.station_metadata.to_dict(single=True)
# Remove creation_time as it varies
if "provenance.creation_time" in station_meta:
    del station_meta["provenance.creation_time"]
for k, v in station_meta.items():
    print(f'            ("{k}", {repr(v)}),')

print("\n=== RUN METADATA ===")
run_meta = tf.station_metadata.runs[0].to_dict(single=True)
for k, v in run_meta.items():
    print(f'            ("{k}", {repr(v)}),')

print("\n=== KEY VALUES FOR PARAMETRIC TESTS ===")
print("Survey fields:")
print(f'    datum: {repr(survey_meta["datum"])}')
print(f'    release_license: {repr(survey_meta["release_license"])}')

print("Station fields:")
print(f'    data_type: {repr(station_meta["data_type"])}')
print(f'    location.datum: {repr(station_meta["location.datum"])}')
