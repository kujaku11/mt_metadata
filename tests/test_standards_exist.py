# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 15:32:48 2021

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""

import unittest
from pathlib import Path


def get_standard_dirs(dir_path):
    existing_dirs = list(set([fn.parent.as_posix() for fn in dir_path.rglob("*.json")]))
    existing_dirs = [fn[fn.rfind("mt_metadata") :] for fn in existing_dirs]

    return existing_dirs


def read_manifest(fn):
    lines = fn.read_text().split("\n")
    standards_dir_list = []
    for line in lines:
        if "recursive-include" in line and "json" in line:
            standards_dir_list.append(line.split()[1])

    return standards_dir_list


class TestStandards(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.home = Path(__file__).parent.parent
        self.manifest_fn = self.home.joinpath("MANIFEST.in")
        if not self.manifest_fn.exists():
            self.manifest_fn = self.home.parent.joinpath("MANIFEST.in")

    def test_standards_exist(self):
        existing_dirs = sorted(get_standard_dirs(self.home))
        manifest_dirs = sorted(read_manifest(self.manifest_fn))
        self.assertListEqual(existing_dirs, manifest_dirs)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
