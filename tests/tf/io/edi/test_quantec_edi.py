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
from mt_metadata.transfer_functions.io import edi
from mt_metadata import TF_EDI_QUANTEC

# =============================================================================
# Quantec
# =============================================================================
class TestQuantecEDI(unittest.TestCase):
    def setUp(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_QUANTEC)

    def test_header(self):
        head = {
            "acqby": "Quantec Geoscience",
            "acqdate": "2014-11-15T00:00:00+00:00",
            "coordinate_system": "geographic",
            "country": "Australia",
            "county": "Boulia",
            "dataid": "Geoscience Australia",
            "datum": "WGS84",
            "elevation": 122.0,
            "enddate": "2014-11-15T00:00:00+00:00",
            "fileby": "Quantec Geoscience",
            "filedate": "2014-11-17",
            "latitude": -23.051133333333333,
            "longitude": 139.46753333333334,
            "progdate": "2012-10-10",
            "progname": "mt_metadata",
            "progvers": "MTeditor_v1d",
            "state": "Queensland",
            "stdvers": "1.0",
        }

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)
                
    def test_info(self):
        info_list = ['MAXLINES=1000']
        
        self.assertListEqual(info_list, self.edi_obj.Info.info_list)
        
    def test_measurement_ex(self):
        ch = OrderedDict([('acqchan', None),
                     ('chtype', 'EX'),
                     ('id', '14.001'),
                     ('x', -50.0),
                     ('x2', 50.0),
                     ('y', 0.0),
                     ('y2', 0.0),
                     ('z', 0.0),
                     ('z2', 0.0)])
        
        self.assertDictEqual(ch, 
                             self.edi_obj.Measurement.meas_ex.to_dict(single=True))
        
    def test_measurement_ey(self):
        ch = OrderedDict([('acqchan', None),
                     ('chtype', 'EY'),
                     ('id', '15.001'),
                     ('x', 0.0),
                     ('x2', 0.0),
                     ('y', -50.0),
                     ('y2', 50.0),
                     ('z', 0.0),
                     ('z2', 0.0)])
        
        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_ey.to_dict(single=True))
        
    def test_measurement_hx(self):
        ch = OrderedDict([('acqchan', None),
                     ('azm', 0.0),
                     ('chtype', 'HX'),
                     ('dip', 0.0),
                     ('id', '11.001'),
                     ('x', 0.0),
                     ('y', 0.0),
                     ('z', 0.0)])
        
        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_hx.to_dict(single=True))
        
    def test_measurement_hy(self):
        ch = OrderedDict([('acqchan', None),
                     ('azm', 90.0),
                     ('chtype', 'HY'),
                     ('dip', 0.0),
                     ('id', '12.001'),
                     ('x', 0.0),
                     ('y', 0.0),
                     ('z', 0.0)])
        
        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_hy.to_dict(single=True))
        
    def test_measurement_hz(self):
        ch = OrderedDict([('acqchan', None),
                     ('azm', 0.0),
                     ('chtype', 'HZ'),
                     ('dip', 0.0),
                     ('id', '13.001'),
                     ('x', 0.0),
                     ('y', 0.0),
                     ('z', 0.0)])
        
        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_hz.to_dict(single=True))
        
    def test_measurement_rrhx(self):
        ch = OrderedDict([('acqchan', None),
                     ('azm', 0.0),
                     ('chtype', 'RRHX'),
                     ('dip', 0.0),
                     ('id', '11.001'),
                     ('x', 0.0),
                     ('y', 0.0),
                     ('z', 0.0)])
        
        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_rrhx.to_dict(single=True))
        
    def test_measurement_rrhy(self):
        ch = OrderedDict([('acqchan', None),
                     ('azm', 90.0),
                     ('chtype', 'RRHY'),
                     ('dip', 0.0),
                     ('id', '12.001'),
                     ('x', 0.0),
                     ('y', 0.0),
                     ('z', 0.0)])
        
        self.assertDictEqual(ch, self.edi_obj.Measurement.meas_rrhy.to_dict(single=True))
        


        
# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()