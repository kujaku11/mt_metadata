# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:21:06 2021

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
import numpy as np

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("emeasurement", SCHEMA_FN_PATHS)

# ==============================================================================
# magnetic measurements
# ==============================================================================
class EMeasurement(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self._fmt_dict = {
            "id": "<",
            "chtype": "<",
            "x": "<.2f",
            "y": "<.2f",
            "z": "<.2f",
            "x2": "<.2f",
            "y2": "<.2f",
            "z2": "<.2f",
            "azm": "<.2f",
            "acqchan": "<",
        }

        super().__init__(attr_dict=attr_dict, **kwargs)

        if self.x != 0 or self.y != 0 or self.x2 != 0 or self.y2 != 0:
            self.azm = self.azimuth

    def __str__(self):
        return "\n".join(
            [f"{k} = {v}" for k, v in self.to_dict(single=True).items()]
        )

    def __repr__(self):
        return self.__str__()

    @property
    def dipole_length(self):
        try:
            if hasattr(self, "z"):
                return np.sqrt(
                    (self.x2 - self.x) ** 2
                    + (self.y2 - self.y) ** 2
                    + self.z**2
                )
            else:
                return np.sqrt(
                    (self.x2 - self.x) ** 2 + (self.y2 - self.y) ** 2
                )
        except TypeError:
            return 0

    @property
    def azimuth(self):
        try:
            return np.rad2deg(
                np.arctan2((self.y2 - self.y), (self.x2 - self.x))
            )
        except (ZeroDivisionError, TypeError):
            return 0.0

    @property
    def channel_number(self):
        if self.acqchan != None:
            if not isinstance(self.acqchan, (int, float)):
                try:
                    return [
                        int("".join(i for i in self.acqchan if i.isdigit()))
                    ][0]
                except (IndexError, ValueError):
                    return 0
            return self.acqchan
        return 0

    def write_meas_line(self):
        """
        write string
        :return: DESCRIPTION
        :rtype: TYPE

        """

        line = [">emeas".upper()]

        for mkey, mfmt in self._fmt_dict.items():
            try:
                line.append(f"{mkey.upper()}={getattr(self, mkey):{mfmt}}")
            except (ValueError, TypeError):
                line.append(f"{mkey.upper()}={0.0:{mfmt}}")

        return f"{' '.join(line)}\n"
