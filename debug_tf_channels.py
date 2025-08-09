#!/usr/bin/env python3
"""
Debug script to examine TF object channel positions after loading from EMTFXML.
"""


from mt_metadata import TF_XML
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io.emtfxml import EMTFXML


def main():
    print("=== TF Object Channel Position Debug ===")

    # Load TF from EMTFXML
    tf = TF(fn=TF_XML)
    tf.read()

    print("\n--- Station Metadata Runs ---")
    print(f"Number of runs: {len(tf.station_metadata.runs)}")

    for i, run in enumerate(tf.station_metadata.runs):
        print(f"\nRun {i}: {run.id}")

        # Check magnetic channels
        for comp in ["hx", "hy", "hz"]:
            try:
                ch = getattr(run, comp)
                print(
                    f"  {comp}: location=({ch.location.x}, {ch.location.y}, {ch.location.z})"
                )
                print(
                    f"       trans_az={ch.translated_azimuth}, meas_az={ch.measurement_azimuth}"
                )
            except AttributeError:
                print(f"  {comp}: Not found")

        # Check electric channels
        for comp in ["ex", "ey"]:
            try:
                ch = getattr(run, comp)
                print(
                    f"  {comp}: negative=({ch.negative.x}, {ch.negative.y}, {ch.negative.z})"
                )
                print(
                    f"       positive=({ch.positive.x2}, {ch.positive.y2}, {ch.positive.z2})"
                )
                print(f"       dipole_length={ch.dipole_length}")
                print(
                    f"       trans_az={ch.translated_azimuth}, meas_az={ch.measurement_azimuth}"
                )
            except AttributeError:
                print(f"  {comp}: Not found")

    print("\n--- Compare with Original EMTFXML ---")
    original = EMTFXML(TF_XML)

    print(f"Original input channels: {len(original.site_layout.input_channels)}")
    for ch in original.site_layout.input_channels:
        print(f"  {ch.name}: ({ch.x}, {ch.y}, {ch.z})")

    print(f"Original output channels: {len(original.site_layout.output_channels)}")
    for ch in original.site_layout.output_channels:
        print(f"  {ch.name}: ({ch.x}, {ch.y}, {ch.z})")
        if hasattr(ch, "x2"):
            print(f"    x2={ch.x2}, y2={ch.y2}, z2={ch.z2}")


if __name__ == "__main__":
    main()
