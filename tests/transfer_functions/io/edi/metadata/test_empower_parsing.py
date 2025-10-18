#!/usr/bin/env python3
"""
Test script to verify Empower EDI parsing improvements
"""

from mt_metadata import TF_EDI_EMPOWER
from mt_metadata.transfer_functions.io.edi.metadata.information import Information


def test_empower_parsing():
    """Test the improved Empower EDI parsing"""

    with open(TF_EDI_EMPOWER, "r") as f:
        edi_lines = f.readlines()

    # Create Information object and parse
    info = Information()
    info.read_info(edi_lines)

    print("=== EMPOWER EDI PARSING RESULTS ===")
    print(f"Phoenix file detected: {info._phoenix_file}")
    print(f"Empower file detected: {info._empower_file}")
    print(f"Number of info items parsed: {len(info.info_dict)}")

    print("\n=== PARSED INFO DICT ===")
    for key, value in info.info_dict.items():
        if isinstance(value, list) and len(value) > 3:
            print(f"{key}: [List with {len(value)} items]")
        else:
            print(f"{key}: {value}")

    print("\n=== COMPONENT-SPECIFIC ATTRIBUTES ===")
    components = ["ex", "ey", "hx", "hy", "hz", "rrhx", "rrhy"]
    for comp in components:
        comp_attrs = {k: v for k, v in info.info_dict.items() if f"run.{comp}." in k}
        if comp_attrs:
            print(f"\n{comp.upper()} attributes:")
            for k, v in comp_attrs.items():
                print(f"  {k}: {v}")


if __name__ == "__main__":
    test_empower_parsing()
