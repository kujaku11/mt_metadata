#!/usr/bin/env python3
"""
Test script to verify Empower EDI parsing improvements - simplified version
"""

from mt_metadata import TF_EDI_EMPOWER


def test_empower_parsing():
    """Test the improved Empower EDI parsing"""
    try:
        from mt_metadata.transfer_functions.io.edi.metadata.information import (
            Information,
        )

        with open(TF_EDI_EMPOWER, "r") as f:
            edi_lines = f.readlines()

        # Create Information object and parse
        info = Information()
        info.read_info(edi_lines)

        print("=== EMPOWER EDI PARSING RESULTS ===")
        print(f"Phoenix file detected: {info._phoenix_file}")
        print(f"Empower file detected: {info._empower_file}")
        print(f"Number of info items parsed: {len(info.info_dict)}")

        # Check for key indicators that parsing worked
        key_indicators = [
            "transfer_function.software.name",
            "station.geographic_name",
            "run.ex.dipole_length",
            "run.hx.sensor.model",
            "run.hx.sensor.id",
        ]

        print("\n=== KEY PARSING INDICATORS ===")
        for key in key_indicators:
            value = info.info_dict.get(key, "NOT FOUND")
            print(f"{key}: {value}")

        # Check component attributes
        print("\n=== COMPONENT ATTRIBUTES FOUND ===")
        components_found = set()
        for key in info.info_dict.keys():
            if key.startswith("run."):
                component = key.split(".")[1]
                components_found.add(component)

        print(f"Components found: {sorted(components_found)}")

        return len(info.info_dict) > 10  # Basic success check

    except Exception as e:
        print(f"Error during parsing: {e}")
        return False


if __name__ == "__main__":
    success = test_empower_parsing()
    print(f"\nParsing test {'PASSED' if success else 'FAILED'}")
