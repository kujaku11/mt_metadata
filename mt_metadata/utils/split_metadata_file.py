# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from pathlib import Path
sv_path = Path(r"c:\Users\jpeacock\Documents\GitHub\mt_metadata\mt_metadata\transfer_functions\tf")

with open(r"c:\Users\jpeacock\Documents\GitHub\mtpy\mtpy\core\metadata\metadata.py", "r") as fid:
    lines = fid.readlines()
    
baselines = ["# -*- coding: utf-8 -*-\n",
            '"""\n',
            "Created on Wed Dec 23 21:30:36 2020\n",
            "\n",
            ":copyright: \n",
            "    Jared Peacock (jpeacock@usgs.gov)\n",
            "\n",
            ":license: MIT\n",
            "\n",
            '"""\n',
            "# =============================================================================\n",
            "# Imports\n",
            "# =============================================================================\n",
            "from mt_metadata.base.helpers import write_lines\n",
            "from mt_metadata.base import get_schema, Base\n"
            "from .standards import SCHEMA_FN_PATHS\n",
            "\n",
            "# =============================================================================\n",
            "attr_dict = get_schema(name, SCHEMA_FN_PATHS)\n",
            "# =============================================================================\n",]
    
f_lines = list(baselines)
count = 0
name = None
for ii, line in enumerate(lines[850:], 850):
    if "class" == line[0:5]:
        count += 1
        if count == 1:
            name = line.split()[1].split('(')[0].lower()
            f_lines.append(line)
        else:
            print(name, f"line {ii}", count)
            with open(sv_path.joinpath(f"{name}.py"), "w") as fid:
                fid.writelines(f_lines)
            print(f"\twrote {name}.py")
            f_lines = baselines + [line]
            count += 1
            name = line.split()[1].split('(')[0].lower()
    else:
        f_lines.append(line.replace(f'ATTR_DICT["{name}"]', "attr_dict"))
    