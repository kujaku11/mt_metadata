# -*- coding: utf-8 -*-
"""

Created on Wed Dec  8 11:29:57 2021

:author: Jared Peacock

:license: MIT

"""
# =============================================================================
#
# =============================================================================
import unittest
from collections import OrderedDict

import numpy as np

from mt_metadata import TF_AVG_NEWER
from mt_metadata.transfer_functions.io.zonge import ZongeMTAvg


# =============================================================================


class TestAVG(unittest.TestCase):
    @classmethod
    def setUpClass(self):

        self.avg = ZongeMTAvg(fn=TF_AVG_NEWER)
        self.avg.read()
        self.maxDiff = None

    def test_header(self):
        h = OrderedDict(
            [
                ("g_d_p.date", "06/30/2017"),
                ("g_d_p.prog_ver", "3899:zenacqv3.4e"),
                ("g_d_p.time", "21:30:19.000"),
                ("g_d_p.type", "zen"),
                ("g_p_s.datum", "wgs84"),
                ("g_p_s.lat", 44.1479163),
                ("g_p_s.lon", -111.0497517),
                ("g_p_s.u_t_m_zone", "12"),
                ("job.for", '"ngf"'),
                ("job.name", '"yellowstone"'),
                ("line.name", '"wb28"'),
                ("line.number", 28),
                ("m_t_edit.auto.phase_flip", "no"),
                ("m_t_edit.d_plus.use", "no"),
                ("m_t_edit.phase_slope.smooth", "robust"),
                ("m_t_edit.phase_slope.to_z_mag", "no"),
                ("m_t_edit.version", "3.12a applied 2021/02/18"),
                ("m_t_f_t24.version", "1.30h applied 2021/02/10"),
                ("rx.a_space", "1 m"),
                ("rx.gdp_stn", "2813"),
                ("rx.h_p_r", [0.0, 0.0, 180.0]),
                ("rx.length", 0.0),
                ("rx.s_space", "1"),
                ("stn.name", "2813"),
                ("survey.array", "tensor"),
                ("survey.datum", "wgs84"),
                ("survey.proj", "UTM"),
                ("survey.type", "mt"),
                ("survey.u_t_m_zone", "12"),
                ("tx.type", "natural"),
                ("unit.b", "nt"),
                ("unit.e", "uv/m"),
                ("unit.length", "m"),
            ]
        )
        self.assertDictEqual(h, self.avg.header.to_dict(single=True))

    def test_z(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.avg.z.shape, (37, 2, 2))

        with self.subTest("type"):
            self.assertEqual(self.avg.z.dtype.type, np.complex128)

        with self.subTest("non zero"):
            self.assertTrue(self.avg.z.all() != 0)

    def test_z_err(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.avg.z_err.shape, (37, 2, 2))

        with self.subTest("type"):
            self.assertEqual(self.avg.z_err.dtype.type, np.float64)

        with self.subTest("non zero"):
            self.assertTrue(self.avg.z_err.all() != 0)

    def test_frequency(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.avg.frequency.shape, (37,))

    def test_tipper(self):
        with self.subTest("non existant"):
            self.assertTrue(self.avg.t == None)


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
