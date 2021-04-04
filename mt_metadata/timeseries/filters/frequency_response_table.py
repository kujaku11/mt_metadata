"""
Helper class intended to assist with the reading in of generic FAP files.
Idea is to leave the FrequencyResponseTableFilter class lean and not clutter
it with a bunch of custom read methods that we may need for various calibrations
from various manufacturers.

"""
import numpy as np
import pandas as pd
import re

RAD2DEG = 180 / np.pi
DEG2RAD = 1./RAD2DEG
DEGREE_LABELS = ['degrees', 'deg']
MILLIRADIAN_LABELS = ['milliradians', 'mrad', 'mradians']
RADIAN_LABELS = ['rad', 'radians']

class FrequencyResponseTable(object):

    def __init__(self, **kwargs):
        self.frequencies = kwargs.get('frequencies', None)
        self.amplitudes = kwargs.get('amplitudes', None)
        self.phases = kwargs.get('phases', None)
        self.frequency_units = None
        self.amplitude_units = None
        self.phase_units = None
        self.units_out = None
        self.units_in = None
        self.columns_order = None

    def validate_units(self):
        fail = False
        if self.frequency_units is None:
            print("Frequency Units Not Specified")
            fail = True
        if self.amplitude_units is None:
            print("Amplitude Units Not Specified")
            fail = True
        if self.phase_units is None:
            print("Phase Units Not Specified")
            fail = True
        if fail:
            raise Exception


    def parse_header(self, filepath):
        """
        handles the specific case of fap headers of the following form:
        Frequency [Hz],Amplitude [V/nT],phase [degrees]
        """

        # <initialize rparams>
        frequency_units = None
        amplitude_units = None
        phase_units = None
        # <\initialize rparams>

        with open(filepath) as f:
            header_list = f.readline().strip().split(',')
        if len(header_list) != 3:
            logger.warn(f"Header indicates unexpected number of columns -- expected 3, got {len(header_list)}")

        columns_order = 3*[None]
        looking_for = ['frequency', 'amplitude', 'phase']
        for i, text_string in enumerate(header_list):
            for label in looking_for:
                if re.search(label, text_string.lower()):
                    columns_order[i] = label
                    if label == 'frequency':
                        self.frequency_units = text_string.split('[', 1)[1].split(']')[0]
                    elif label == 'amplitude':
                        self.amplitude_units = text_string.split('[', 1)[1].split(']')[0]
                    elif label == 'phase':
                        self.phase_units = text_string.split('[', 1)[1].split(']')[0]

        self.validate_units()

        units_out, units_in = self.amplitude_units.split('/')
        self.units_out = units_out.strip()
        self.units_in = units_in.strip()

        self.columns_order = columns_order

        return

    def load_from_csv(self, filepath, set_phase_to_radians=True):
        """
        Parameters
        ----------
        filepath

        Returns
        -------

        """
        self.parse_header(filepath)
        df = pd.read_csv(filepath, skiprows=1, names=self.columns_order)
        if set_phase_to_radians:
            if self.phase_units.lower() in RADIAN_LABELS:
                pass
            elif self.phase_units.lower() in DEGREE_LABELS:
                df['phase'] = df['phase']*DEG2RAD
            elif self.phase_units.lower() in MILLIRADIAN_LABELS:
                df['phase'] = df['phase']*1000.0
            else:
                print(f"Tried to cast phase to radians but did not recognize {self.phase_units} units")
            self.phase_units = 'radians'

        return df
