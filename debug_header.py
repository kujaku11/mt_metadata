from mt_metadata.transfer_functions.io.jfiles.metadata.header import Header


# Test with the failing sample data
sample_lines = [
    "BIRRP Version 5 basic mode output",
    "# nout= 2 nin= 2 nrr= 2 tbw=  2.00 deltat=  1.00",
    "# filnam= test1.dat nskip= 0 nread= 1000 ncomp= 4",
    "# theta1=  0.00  theta2=  45.00  phi=  0.00",
    "# filnam= test2.dat nskip= 100 nread= 2000 ncomp= 4",
    "# theta1=  15.00  theta2=  60.00  phi=  30.00",
    "> lat=  40.0 lon= -120.0 elev= 1000.0",
    "  1.0000E-02  1.0000E-02",
]

header = Header()

# Debug the parsing logic step by step
header_lines = [j_line for j_line in sample_lines if "#" in j_line]
print("Header lines:", header_lines)
print("Title extraction:", header_lines[0][1:].strip())

fn_count = -1
for i, h_line in enumerate(header_lines[1:]):
    parsed = header._read_header_line(h_line)
    print(f"Line {i}: {h_line}")
    print(f"  Parsed: {parsed}")
    for key, value in parsed.items():
        if key in ["filnam", "nskip", "nread", "ncomp", "indices", "nfil"]:
            if key in ["nfil"]:
                fn_count += 1
            print(
                f'    Processing file key "{key}" - fn_count: {fn_count}, data_blocks len: {len(header.data_blocks)}'
            )
            print(f"    Would check: len({len(header.data_blocks)}) != {fn_count + 1}")
            if len(header.data_blocks) != fn_count + 1:
                print(f"    Adding new BirrpBlock")
                # header.data_blocks.append(BirrpBlock())
            else:
                print(f"    Using existing block at index {fn_count}")
