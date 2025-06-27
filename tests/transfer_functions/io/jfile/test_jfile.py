# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

# =============================================================================
#
# =============================================================================
import unittest

from collections import OrderedDict
from mt_metadata.transfer_functions.io.jfiles import JFile
from mt_metadata import TF_JFILE

# =============================================================================
# CGG
# =============================================================================
class TestJFile(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.j_obj = JFile(fn=TF_JFILE)
        self.maxDiff = None

    def test_title(self):
        self.assertEqual(
            "BIRRP Version 5 basic mode output", self.j_obj.header.title
        )

    def test_birrp_parameters(self):
        birrp_params = OrderedDict(
            [
                ("ainlin", -999.0),
                ("ainuin", 0.999),
                ("c2threshe", 0.7),
                ("c2threshe1", 0.0),
                ("deltat", 0.1),
                ("imode", 2),
                ("inputs", 2),
                ("jmode", 0),
                ("nar", 3),
                ("ncomp", 0),
                ("nf1", 4),
                ("nfft", 5164.0),
                ("nfinc", 2),
                ("nfsect", 2),
                ("npcs", 1),
                ("nsctinc", 2.0),
                ("nsctmax", 7.0),
                ("nz", 0),
                ("outputs", 2),
                ("references", 2),
                ("tbw", 2.0),
                ("uin", 0.0),
            ]
        )

        self.assertDictEqual(
            birrp_params,
            self.j_obj.header.birrp_parameters.to_dict(single=True),
        )

    def test_data_blocks(self):
        db = [
            OrderedDict(
                [
                    (
                        "filnam",
                        "/data/mtpy/examples/birrp_processing/birrp_wd/birrp_data_3.txt",
                    ),
                    ("indices", 1),
                    ("ncomp", 4),
                    ("nread", 38750),
                    ("nskip", 0),
                ]
            ),
            OrderedDict(
                [
                    (
                        "filnam",
                        "/data/mtpy/examples/birrp_processing/birrp_wd/birrp_data_3.txt",
                    ),
                    ("indices", 3),
                    ("ncomp", 4),
                    ("nread", 38750),
                    ("nskip", 0),
                ]
            ),
        ]

        for ii, block in enumerate(db):
            with self.subTest(msg=f"block {ii}"):
                self.assertDictEqual(
                    block,
                    self.j_obj.header.data_blocks[ii].to_dict(single=True),
                )

    def test_station(self):
        self.assertEqual("BP05", self.j_obj.header.station)

    def test_impedance(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.j_obj.z.shape, (12, 2, 2))

        with self.subTest("err shape"):
            self.assertTupleEqual(self.j_obj.z_err.shape, (12, 2, 2))


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
