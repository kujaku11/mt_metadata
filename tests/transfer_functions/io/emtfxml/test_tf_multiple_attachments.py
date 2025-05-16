# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 13:27:16 2023

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
import unittest

from mt_metadata import TF_XML_MULTIPLE_ATTACHMENTS
from mt_metadata.transfer_functions.io.emtfxml import EMTFXML


# =============================================================================


class TestEMTFXMLMultipleAttachments(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.x = EMTFXML(fn=TF_XML_MULTIPLE_ATTACHMENTS)
        self.maxDiff = None

    def test_len_attachments(self):
        self.assertEqual(4, len(self.x.attachment._attachments))

    def test_to_xml_string(self):
        true_string = [
            '<?xml version="1.0" encoding="UTF-8"?>\n<Attachment>\n    <Filename>kak/kak.mtres.all.1r1.rp</Filename>\n</Attachment>\n',
            '<?xml version="1.0" encoding="UTF-8"?>\n<Attachment>\n    <Filename>kak/kak.mtres.all.1r2.rp</Filename>\n</Attachment>\n',
            '<?xml version="1.0" encoding="UTF-8"?>\n<Attachment>\n    <Filename>kak/kak.mtres.all.2r1.rp</Filename>\n</Attachment>\n',
            '<?xml version="1.0" encoding="UTF-8"?>\n<Attachment>\n    <Filename>kak/kak.mtres.all.2r2.rp</Filename>\n</Attachment>\n',
        ]

        self.assertEqual(true_string, self.x.attachment.to_xml(string=True))


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    unittest.main()
