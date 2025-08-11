#!/usr/bin/env python3

from mt_metadata import TF_ZMM
from mt_metadata.transfer_functions.core import TF


tf = TF(fn=TF_ZMM)
tf.read()

print("ZMM SURVEY ACTUAL VALUES:")
survey = tf.survey_metadata.to_dict(single=True)
for k, v in survey.items():
    print(f'("{k}", {repr(v)}),')

print("\nZMM STATION ACTUAL VALUES:")
station = tf.station_metadata.to_dict(single=True)
excluded = ["provenance.creation_time"]
for k, v in station.items():
    if k not in excluded:
        print(f'("{k}", {repr(v)}),')

print("\nZMM RUN ACTUAL VALUES:")
run = tf.station_metadata.runs[0].to_dict(single=True)
for k, v in run.items():
    if k not in excluded:
        print(f'("{k}", {repr(v)}),')

print("\nZMM IMPEDANCE VALUES:")
print(f"Shape: {tf.impedance.shape}")
print(f"First: {tf.impedance[0]}")
print(f"Last: {tf.impedance[-1]}")

print("\nZMM TIPPER VALUES:")
print(f"Shape: {tf.tipper.shape}")
print(f"First: {tf.tipper[0]}")
print(f"Last: {tf.tipper[-1]}")
