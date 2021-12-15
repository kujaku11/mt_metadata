# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

# =============================================================================
#
# =============================================================================
import unittest
import numpy as np

from collections import OrderedDict
from mt_metadata.transfer_functions.io.edi import EDI
from mt_metadata.utils.mttime import MTime
from mt_metadata import TF_EDI_SPECTRA, TF_EDI_SPECTRA_OUT
from mt_metadata.transfer_functions.core import TF

# =============================================================================
# CGG
# =============================================================================
class TestSpectraEDI(unittest.TestCase):
    def setUp(self):
        self.edi_spectra = EDI(fn=TF_EDI_SPECTRA)
        self.edi_z = EDI(fn=TF_EDI_SPECTRA_OUT)
        self.maxDiff = None

    def test_header(self):
        head = {
            "ACQBY": "Quantec Consulting",
            "COORDINATE_SYSTEM": "geographic",
            "DATAID": "SAGE_2005",
            "DATUM": "WGS84",
            "ELEV": 0.,
            "EMPTY": 1e+32,
            "FILEBY": "Quantec Consulting",
            "LAT": 35.55,
            "LON": -106.28333333333333,
        }

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_spectra.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("acquire date"):
            self.assertEqual(self.edi_spectra.Header._acqdate, MTime("2004-07-03"))

        with self.subTest("units"):
            self.assertNotEqual(
                self.edi_spectra.Header.units, "millivolts_per_kilometer_per_nanotesla"
            )

    def test_info(self):
        info_list = ['MAXLINES=1000']
        
        self.assertListEqual(info_list, self.edi_spectra.Info.info_list)
        
    def test_measurement_ex(self):
        ch = OrderedDict([('acqchan', None),
                     ('chtype', 'EX'),
                     ('id', 14.001),
                     ('x', 4872.0),
                     ('x2', 4843.0),
                     ('y', -3577.0),
                     ('y2', -3482.0),
                     ('z', 0.0),
                     ('z2', 0.0)])
        
        self.assertDictEqual(ch, 
                             self.edi_spectra.Measurement.meas_ex.to_dict(single=True))
        
    def test_measurement_ey(self):
        ch = OrderedDict([('acqchan', None),
                     ('chtype', 'EY'),
                     ('id', 15.001),
                     ('x', 4906.0),
                     ('x2', 4810.0),
                     ('y', -3515.0),
                     ('y2', -3544.0),
                     ('z', 0.0),
                     ('z2', 0.0)])
        
        self.assertDictEqual(ch, self.edi_spectra.Measurement.meas_ey.to_dict(single=True))
        
    def test_measurement_hx(self):
        ch = OrderedDict([('acqchan', None),
                     ('azm', 107.0),
                     ('chtype', 'HX'),
                     ('dip', 0.0),
                     ('id', 11.001),
                     ('x', 4858.0),
                     ('y', -3530.0),
                     ('z', 0.0)])
        
        self.assertDictEqual(ch, self.edi_spectra.Measurement.meas_hx.to_dict(single=True))
        
    def test_measurement_hy(self):
        ch = OrderedDict([('acqchan', None),
                     ('azm', -163.0),
                     ('chtype', 'HY'),
                     ('dip', 0.0),
                     ('id', 12.001),
                     ('x', 4858.0),
                     ('y', -3530.0),
                     ('z', 0.0)])
        
        self.assertDictEqual(ch, self.edi_spectra.Measurement.meas_hy.to_dict(single=True))
        
    def test_measurement_hz(self):
        ch = OrderedDict([('acqchan', None),
                     ('azm', 0.0),
                     ('chtype', 'HZ'),
                     ('dip', 0.0),
                     ('id', 13.001),
                     ('x', 4858.0),
                     ('y', -3530.0),
                     ('z', 0.0)])
        
        self.assertDictEqual(ch, self.edi_spectra.Measurement.meas_hz.to_dict(single=True))
        
    def test_measurement_rrhx(self):
        ch = OrderedDict([('acqchan', None),
                     ('azm', 107.0),
                     ('chtype', 'RRHX'),
                     ('dip', 0.0),
                     ('id', 11.001),
                     ('x', 4858.0),
                     ('y', -3530.0),
                     ('z', 0.0)])
        
        self.assertDictEqual(ch, self.edi_spectra.Measurement.meas_rrhx.to_dict(single=True))
        
    def test_measurement_rrhy(self):
        ch = OrderedDict([('acqchan', None),
                     ('azm', -163.0),
                     ('chtype', 'RRHY'),
                     ('dip', 0.0),
                     ('id', 12.001),
                     ('x', 4858.0),
                     ('y', -3530.0),
                     ('z', 0.0)])
        
        self.assertDictEqual(ch, self.edi_spectra.Measurement.meas_rrhy.to_dict(single=True))

    def test_measurement(self):
        m_list = ['MAXCHAN=7',
         'MAXRUN=999',
         'MAXMEAS=99999',
         'UNITS=M',
         'REFLAT=35:33:00',
         'REFLONG=-106:17:00']
        
        self.assertListEqual(
            m_list, 
            self.edi_spectra.Measurement.measurement_list[0:len(m_list)])
        
        with self.subTest("reflat"):
            self.assertAlmostEqual(35.55, self.edi_spectra.Measurement.reflat, 2)
            
        with self.subTest("reflon"):
            self.assertAlmostEqual(-106.2833, self.edi_spectra.Measurement.reflon, 4)
            
        with self.subTest("reflong"):
            self.assertAlmostEqual(-106.2833, self.edi_spectra.Measurement.reflong, 4)
            
        with self.subTest("refelev"):
            self.assertAlmostEqual(0.0, self.edi_spectra.Measurement.refelev, 2)

    def test_data_section(self):
        d_list = ['SECTID=Ex',
         'NCHAN=7',
         'NFREQ=33',
         'MAXBLKS=100',
         '//7',
         '11.001    12.001    13.001    14.001    15.001    11.001    12.001']
        
        self.assertListEqual(d_list, self.edi_spectra.Data.data_list)
        
    def test_z(self):
        self.assertTrue(np.isclose(self.edi_spectra.z, self.edi_z.z).all())
        
    def test_z_err(self):
        self.assertTrue(np.isclose(self.edi_spectra.z_err, self.edi_z.z_err).all())
        
    def test_t(self):
        self.assertTrue(np.isclose(self.edi_spectra.t, self.edi_z.t).all()) 
        
    def test_t_err(self):
        self.assertTrue(np.isclose(self.edi_spectra.t_err, self.edi_z.t_err).all())
        
class TestToTF(unittest.TestCase):
    def setUp(self):
        self.edi = EDI(fn=TF_EDI_SPECTRA)
        self.tf = TF(fn=TF_EDI_SPECTRA)
        
    def test_station_metadata(self):
        self.assertTrue(self.edi.station_metadata == self.tf.station_metadata)
        
    def test_survey_metadata(self):
        self.assertTrue(self.edi.survey_metadata == self.tf.survey_metadata)
        
    def test_has_impedance(self):
        self.assertTrue(self.tf.has_impedance())
        
    def test_has_tipper(self):
        self.assertTrue(self.tf.has_tipper())
        
    def test_has_isp(self):
        self.assertTrue(self.tf.has_inverse_signal_power())
        
    def test_has_residual_covariance(self):
        self.assertTrue(self.tf.has_residual_covariance())
        
        
        
        
        
        
    
        
        

# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()