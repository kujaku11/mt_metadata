#!/usr/bin/env python3
"""
Debug script to trace channel position preservation through the full roundtrip.
"""


from mt_metadata import TF_XML
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io.emtfxml import EMTFXML


def main():
    print("=== Detailed Channel Position Roundtrip Debug ===")

    # Step 1: Load original EMTFXML and check site layout
    print("\n--- Step 1: Original EMTFXML Site Layout ---")
    original = EMTFXML(TF_XML)

    print(f"Original site layout input channels:")
    for ch in original.site_layout.input_channels:
        print(f"  {ch.name}: ({ch.x}, {ch.y}, {ch.z})")

    print(f"Original site layout output channels:")
    for ch in original.site_layout.output_channels:
        print(f"  {ch.name}: ({ch.x}, {ch.y}, {ch.z})")
        if hasattr(ch, "x2"):
            print(f"    x2={ch.x2}, y2={ch.y2}, z2={ch.z2}")

    # Step 2: Get station metadata from original EMTFXML
    print("\n--- Step 2: Station Metadata from Original EMTFXML ---")
    station_meta = original.station_metadata
    print(f"Number of runs in station metadata: {len(station_meta.runs)}")

    for i, run in enumerate(station_meta.runs):
        print(f"\nRun {i}: {run.id}")

        # Check all channels
        for ch_name in ["hx", "hy", "hz", "ex", "ey"]:
            try:
                ch = run.get_channel(ch_name)
                if ch.component in ["hx", "hy", "hz"]:
                    print(
                        f"  {ch_name}: location=({ch.location.x}, {ch.location.y}, {ch.location.z})"
                    )
                elif ch.component in ["ex", "ey"]:
                    print(
                        f"  {ch_name}: neg=({ch.negative.x}, {ch.negative.y}, {ch.negative.z})"
                    )
                    print(
                        f"        pos=({ch.positive.x2}, {ch.positive.y2}, {ch.positive.z2})"
                    )
            except AttributeError:
                print(f"  {ch_name}: Not found in run")

    # Step 3: Create TF and check what happens
    print("\n--- Step 3: TF Object Created ---")
    tf = TF(fn=TF_XML)
    tf.read()
    print(f"TF station metadata runs: {len(tf.station_metadata.runs)}")

    # Step 4: Convert TF back to EMTFXML and see what station_metadata setter does
    print("\n--- Step 4: Converting TF Back to EMTFXML ---")

    # Let's manually trace through the station_metadata setter logic
    emtf_new = EMTFXML()

    # This will trigger the station_metadata setter
    emtf_new.station_metadata = tf.station_metadata

    print(f"New EMTFXML site layout input channels:")
    for ch in emtf_new.site_layout.input_channels:
        print(f"  {ch.name}: ({ch.x}, {ch.y}, {ch.z})")

    print(f"New EMTFXML site layout output channels:")
    for ch in emtf_new.site_layout.output_channels:
        print(f"  {ch.name}: ({ch.x}, {ch.y}, {ch.z})")
        if hasattr(ch, "x2"):
            print(f"    x2={ch.x2}, y2={ch.y2}, z2={ch.z2}")


if __name__ == "__main__":
    main()
