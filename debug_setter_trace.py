#!/usr/bin/env python3
"""
Debug script to manually trace through the station_metadata setter logic.
"""


from mt_metadata import TF_XML
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io.emtfxml import EMTFXML
from mt_metadata.transfer_functions.io.emtfxml import metadata as emtf_xml


def main():
    print("=== Station Metadata Setter Debug ===")

    # Get TF object with proper station metadata
    tf = TF(fn=TF_XML)
    tf.read()

    # Create new EMTFXML object
    emtf_new = EMTFXML()

    # Manually trace through the setter logic
    sm = tf.station_metadata

    print(f"Processing {len(sm.runs)} runs")

    ch_in_dict = {}
    ch_out_dict = {}

    for r_idx, r in enumerate(sm.runs):
        print(f"\n--- Processing Run {r_idx}: {r.id} ---")

        # For magnetic channels
        for comp in ["hx", "hy", "hz"]:
            try:
                rch = getattr(r, comp)
                print(
                    f"Found magnetic channel {comp}: location=({rch.location.x}, {rch.location.y}, {rch.location.z})"
                )

                m_ch = emtf_xml.Magnetic()
                for item in ["x", "y", "z"]:
                    if getattr(rch.location, item) is None:
                        value = 0.0
                    else:
                        value = getattr(rch.location, item)
                    setattr(m_ch, item, value)

                m_ch.name = comp.capitalize()
                if rch.translated_azimuth is not None:
                    m_ch.orientation = rch.translated_azimuth
                else:
                    m_ch.orientation = rch.measurement_azimuth

                if comp in ["hx", "hy"]:
                    ch_in_dict[comp] = m_ch
                    print(
                        f"  Added to input dict: {comp} -> {m_ch.name} ({m_ch.x}, {m_ch.y}, {m_ch.z})"
                    )
                else:
                    ch_out_dict[comp] = m_ch
                    print(
                        f"  Added to output dict: {comp} -> {m_ch.name} ({m_ch.x}, {m_ch.y}, {m_ch.z})"
                    )

            except AttributeError:
                print(f"No magnetic channel {comp} found")

        # For electric channels
        for comp in ["ex", "ey"]:
            try:
                ch = getattr(r, comp)
                print(
                    f"Found electric channel {comp}: neg=({ch.negative.x}, {ch.negative.y}, {ch.negative.z}), pos=({ch.positive.x2}, {ch.positive.y2}, {ch.positive.z2})"
                )

                ch_out = emtf_xml.Electric()
                for item in ["x", "y", "z"]:
                    if getattr(ch.negative, item) is None:
                        value = 0.0
                    else:
                        value = getattr(ch.negative, item)
                    setattr(ch_out, item, value)

                for item in ["x2", "y2", "z2"]:
                    if getattr(ch.positive, item) is None:
                        value = 0.0
                    else:
                        value = getattr(ch.positive, item)
                    setattr(ch_out, item, value)

                ch_out.name = comp.capitalize()
                if ch.translated_azimuth is not None:
                    ch_out.orientation = ch.translated_azimuth
                else:
                    ch_out.orientation = ch.measurement_azimuth

                ch_out_dict[comp] = ch_out
                print(
                    f"  Added to output dict: {comp} -> {ch_out.name} ({ch_out.x}, {ch_out.y}, {ch_out.z}) -> ({ch_out.x2}, {ch_out.y2}, {ch_out.z2})"
                )

            except AttributeError:
                print(f"No electric channel {comp} found")

    print(f"\n--- Final Channel Dictionaries ---")
    print(f"Input channels dict: {list(ch_in_dict.keys())}")
    for k, v in ch_in_dict.items():
        print(f"  {k}: {v.name} ({v.x}, {v.y}, {v.z})")

    print(f"Output channels dict: {list(ch_out_dict.keys())}")
    for k, v in ch_out_dict.items():
        print(f"  {k}: {v.name} ({v.x}, {v.y}, {v.z})")
        if hasattr(v, "x2"):
            print(f"      -> ({v.x2}, {v.y2}, {v.z2})")

    # Set up site layout
    emtf_new.site_layout.input_channels = list(ch_in_dict.values())
    emtf_new.site_layout.output_channels = list(ch_out_dict.values())

    print(f"\n--- Final Site Layout ---")
    print(f"Input channels: {len(emtf_new.site_layout.input_channels)}")
    for ch in emtf_new.site_layout.input_channels:
        print(f"  {ch.name}: ({ch.x}, {ch.y}, {ch.z})")

    print(f"Output channels: {len(emtf_new.site_layout.output_channels)}")
    for ch in emtf_new.site_layout.output_channels:
        print(f"  {ch.name}: ({ch.x}, {ch.y}, {ch.z})")
        if hasattr(ch, "x2"):
            print(f"    x2={ch.x2}, y2={ch.y2}, z2={ch.z2}")


if __name__ == "__main__":
    main()
