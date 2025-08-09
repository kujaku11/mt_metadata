#!/usr/bin/env python3
"""
Debug script to examine channel position preservation in EMTFXML roundtrip.
"""


from mt_metadata import TF_XML
from mt_metadata.transfer_functions.core import TF


def main():
    print("=== Channel Position Debug Analysis ===")

    # Load original EMTFXML
    from mt_metadata.transfer_functions.io.emtfxml import EMTFXML

    original = EMTFXML(TF_XML)

    # Create TF and convert back to EMTFXML
    tf = TF(fn=TF_XML)
    tf.read()
    roundtrip = tf.to_emtfxml()

    print("\n--- Original Site Layout Channels ---")
    print(f"Input channels: {len(original.site_layout.input_channels)}")
    for i, ch in enumerate(original.site_layout.input_channels):
        print(f"  {i}: name={ch.name}, x={ch.x}, y={ch.y}, z={ch.z}")

    print(f"Output channels: {len(original.site_layout.output_channels)}")
    for i, ch in enumerate(original.site_layout.output_channels):
        print(f"  {i}: name={ch.name}, x={ch.x}, y={ch.y}, z={ch.z}")
        if hasattr(ch, "x2"):
            print(f"      x2={ch.x2}, y2={ch.y2}, z2={ch.z2}")

    print("\n--- Roundtrip Site Layout Channels ---")
    print(f"Input channels: {len(roundtrip.site_layout.input_channels)}")
    for i, ch in enumerate(roundtrip.site_layout.input_channels):
        print(f"  {i}: name={ch.name}, x={ch.x}, y={ch.y}, z={ch.z}")

    print(f"Output channels: {len(roundtrip.site_layout.output_channels)}")
    for i, ch in enumerate(roundtrip.site_layout.output_channels):
        print(f"  {i}: name={ch.name}, x={ch.x}, y={ch.y}, z={ch.z}")
        if hasattr(ch, "x2"):
            print(f"      x2={ch.x2}, y2={ch.y2}, z2={ch.z2}")

    print("\n--- Position Differences ---")
    # Compare input channels
    if len(original.site_layout.input_channels) == len(
        roundtrip.site_layout.input_channels
    ):
        for i in range(len(original.site_layout.input_channels)):
            orig = original.site_layout.input_channels[i]
            rt = roundtrip.site_layout.input_channels[i]
            if orig.name.lower() == rt.name.lower():
                if orig.x != rt.x or orig.y != rt.y or orig.z != rt.z:
                    print(
                        f"INPUT DIFF {orig.name}: orig=({orig.x}, {orig.y}, {orig.z}) vs rt=({rt.x}, {rt.y}, {rt.z})"
                    )

    # Compare output channels
    if len(original.site_layout.output_channels) == len(
        roundtrip.site_layout.output_channels
    ):
        for i in range(len(original.site_layout.output_channels)):
            orig = original.site_layout.output_channels[i]
            rt = roundtrip.site_layout.output_channels[i]
            if orig.name.lower() == rt.name.lower():
                if orig.x != rt.x or orig.y != rt.y or orig.z != rt.z:
                    print(
                        f"OUTPUT DIFF {orig.name}: orig=({orig.x}, {orig.y}, {orig.z}) vs rt=({rt.x}, {rt.y}, {rt.z})"
                    )
                if hasattr(orig, "x2") and hasattr(rt, "x2"):
                    if orig.x2 != rt.x2 or orig.y2 != rt.y2 or orig.z2 != rt.z2:
                        print(
                            f"OUTPUT DIFF2 {orig.name}: orig=({orig.x2}, {orig.y2}, {orig.z2}) vs rt=({rt.x2}, {rt.y2}, {rt.z2})"
                        )


if __name__ == "__main__":
    main()
