# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 13:39:39 2025

@author: jpeacock
"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

import xarray as xr
import numpy as np

# =============================================================================
# attr_dict = get_schema("feature", SCHEMA_FN_PATHS)

from mt_metadata.features.base_feature import BaseFeature

def _make_supported_features_dict():
    # TODO Import all supported fetaures here
    from mt_metadata.features.coherence import Coherence
    from mt_metadata.features.coherence import StridingWindowCoherence
    SUPPORTED_FEATURE_DICT = {}
    SUPPORTED_FEATURE_DICT["coherence"] = Coherence
    SUPPORTED_FEATURE_DICT["striding_window_coherence"] = StridingWindowCoherence
    return SUPPORTED_FEATURE_DICT

# =============================================================================
class Feature(BaseFeature):
    # __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self._data = None
        self._supported_features = _make_supported_features_dict()

    def from_dict(self, input_dict):
        """
        Instantiate a feature from a dictionary. Requires a 'name' key.
        """
        if "name" not in input_dict.keys():
            msg = f"Features must have a name, supported features are {self._supported_features.keys()}"
            self.logger.error(msg)
            raise KeyError(msg)
        feature = self._supported_features[input_dict.pop("name")]
        feature_obj = feature()
        feature_obj.from_dict(input_dict)

    @property
    def data(self):
        return self._data


    @data.setter
    def data(self, value):
        """
            Sets the data for this feature.
        """
        if not isinstance(value, (xr.DataArray, xr.Dataset, np.ndarray)):
            raise TypeError("Data must be a numpy array or xarray.")
        self._data = value



