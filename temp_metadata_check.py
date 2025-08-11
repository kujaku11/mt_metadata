#!/usr/bin/env python3

from mt_metadata import TF_ZSS_TIPPER
from mt_metadata.transfer_functions.core import TF


tf = TF(fn=TF_ZSS_TIPPER)
tf.read()

print("SURVEY ACTUAL VALUES:")
survey = tf.survey_metadata.to_dict(single=True)
for k, v in survey.items():
    print(f'("{k}", {repr(v)}),')

print("\nSTATION ACTUAL VALUES:")
station = tf.station_metadata.to_dict(single=True)
excluded = ["provenance.creation_time"]
for k, v in station.items():
    if k not in excluded:
        print(f'("{k}", {repr(v)}),')

print("\nRUN ACTUAL VALUES:")
run = tf.station_metadata.runs[0].to_dict(single=True)
for k, v in run.items():
    if k not in excluded:
        print(f'("{k}", {repr(v)}),')
