"""
Test Empower parsing with sample data
"""

# Sample Empower info section for testing
sample_empower_info = [
    "PROJECT=",
    "SURVEY=",
    "YEAR=2023",
    "PROCESSEDBY=",
    "PROCESSINGSOFTWARE=EMpower v2.9.0.7",
    "SITENAME=Near Steamboat Springs, US (Mountain Standard Time)",
    "",
    "     UNIQUE ID: {88290cfe-9200-4cc2-a0dd-5ed7cd7f95ea}",
    "     PROCESS DATE: 2023-05-30 16:22",
    "     DECLINATION: 0°",
    "     STATIONS",
    "       ELECTRICS",
    "          RECORDING ID: 10526_2023-05-19-170246",
    "          INSTRUMENT TYPE: MTU-5C",
    "          STATION NAME: 701 Walden South",
    "          AZIMUTH: 0",
    "          EX",
    "            TAG: E1",
    "            LENGTH: 95.3 [m]",
    "            AC: 2.5 [V]",
    "            DC: 0.0537872 [V]",
    "            NEGATIVE RES: 1558.69 [Ω]",
    "          EY",
    "            TAG: E2",
    "            LENGTH: 99.1 [m]",
    "       MAGNETICS",
    "          RECORDING ID: 10526_2023-05-19-170246",
    "          INSTRUMENT TYPE: MTU-5C",
    "          HX",
    "            TAG: H1",
    "            SENSOR TYPE: MTC-155",
    "            SENSOR SERIAL: 57507",
    "          HY",
    "            TAG: H2",
    "            SENSOR TYPE: MTC-155",
]


def test_parsing():
    from mt_metadata.transfer_functions.io.edi.metadata.information import Information

    info = Information()
    info._parse_empower_info(sample_empower_info)

    print("=== PARSED RESULTS ===")
    for key, value in sorted(info.info_dict.items()):
        print(f"{key}: {value}")

    print("\n=== EXPECTED KEY MAPPINGS ===")
    expected_keys = [
        "transfer_function.software.name",
        "station.geographic_name",
        "run.ex.dipole_length",
        "run.hx.sensor.model",
        "run.hx.sensor.id",
    ]

    for key in expected_keys:
        value = info.info_dict.get(key, "NOT FOUND")
        print(f"{key}: {value}")


if __name__ == "__main__":
    test_parsing()
