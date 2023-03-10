# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 08:52:43 2023

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
import unittest

import numpy as np
from collections import OrderedDict
from mt_metadata import TF_XML
from mt_metadata.transfer_functions.core import TF
from mt_metadata.transfer_functions.io.emtfxml import EMTFXML

# =============================================================================


class TestWriteEMTFXML(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tf = TF(fn=TF_XML)
        self.tf.read_tf_file()
        self.x1 = self.tf.write_tf_file(file_type="xml")
        self.maxDiff = None

        self.x0 = EMTFXML(TF_XML)


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
