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
attr_dict = get_schema("base_feature", SCHEMA_FN_PATHS)

# =============================================================================
class Feature(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        super().__init__(attr_dict=attr_dict, **kwargs)
        self._data = None
        self._supported_features = self._make_supported_features_dict()

    @staticmethod
    def _make_supported_features_dict():
        from mt_metadata.features.coherence import Coherence
        from mt_metadata.features.coherence import StridingWindowCoherence
        from mt_metadata.features.cross_powers import CrossPowers
        from mt_metadata.features.feature_ts import FeatureTS
        from mt_metadata.features.feature_fc import FeatureFC
        SUPPORTED_FEATURE_DICT = {}
        SUPPORTED_FEATURE_DICT["coherence"] = Coherence
        SUPPORTED_FEATURE_DICT["striding_window_coherence"] = StridingWindowCoherence
        SUPPORTED_FEATURE_DICT["cross_powers"] = CrossPowers
        SUPPORTED_FEATURE_DICT["feature_ts"] = FeatureTS
        SUPPORTED_FEATURE_DICT["feature_fc"] = FeatureFC
        return SUPPORTED_FEATURE_DICT

    @classmethod
    def from_feature_id(cls, meta_dict):
        """
        Factory: instantiate the correct feature class based on 'feature_id'.
        """
        if "feature_id" not in meta_dict:
            raise KeyError("Feature metadata must include 'feature_id'.")
        feature_id = meta_dict["feature_id"]
        supported = cls._make_supported_features_dict()
        if feature_id not in supported:
            raise KeyError(f"Unknown feature_id '{feature_id}'. Supported: {list(supported.keys())}")
        feature_cls = supported[feature_id]
        obj = feature_cls()
        obj.from_dict(meta_dict)
        return obj

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if not isinstance(value, (xr.DataArray, xr.Dataset, np.ndarray)):
            raise TypeError("Data must be a numpy array or xarray.")
        self._data = value



