#!/usr/bin/env python3
"""
Debug script to examine what TF object's station metadata contains.
"""


from mt_metadata import TF_XML
from mt_metadata.transfer_functions.core import TF


def main():
    print("=== TF Station Metadata Deep Debug ===")

    # Create TF object
    tf = TF(fn=TF_XML)
    tf.read()

    print(f"\nTF station metadata runs: {len(tf.station_metadata.runs)}")

    for i, run in enumerate(tf.station_metadata.runs):
        print(f"\nRun {i}: {run.id}")
        print(f"  Channels recorded electric: {run.channels_recorded_electric}")
        print(f"  Channels recorded magnetic: {run.channels_recorded_magnetic}")

        print(f"  All channel names: {[ch.component for ch in run.channels]}")

        # Check all channels
        for ch in run.channels:
            comp = ch.component
            print(f"  Channel {comp}:")
            print(f"    Type: {type(ch).__name__}")
            if hasattr(ch, "location"):
                print(
                    f"    Location: ({ch.location.x}, {ch.location.y}, {ch.location.z})"
                )
            if hasattr(ch, "negative"):
                print(
                    f"    Negative: ({ch.negative.x}, {ch.negative.y}, {ch.negative.z})"
                )
            if hasattr(ch, "positive"):
                print(
                    f"    Positive: ({ch.positive.x2}, {ch.positive.y2}, {ch.positive.z2})"
                )


if __name__ == "__main__":
    main()
