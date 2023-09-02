# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 15:20:59 2022

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
attr_dict = get_schema("band", SCHEMA_FN_PATHS)


# =============================================================================
class Band(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        super().__init__(attr_dict=attr_dict, **kwargs)

    def harmonic_indices(self, continuous=True):
        """
        Assumes all harmincs between min and max are present in the band

        Parameters
        ----------
        continuous: bool
            Placeholder for future version which may support ignoring some harmonics.  True for now

        Returns
        -------
        numpy array of integers corresponding to harminic indices
        """
        if continuous:
            return np.arange(self.index_min, self.index_max+1)
        else:
            raise NotImplementedError("discontinuities in frequency band are not supported")

    # should add properties to calculate index from frequency and vise-versa
    # which is pretty much what is in FrequencyBand
