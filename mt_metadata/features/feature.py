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
    from mt_metadata.features.cross_powers import CrossPowers  # Added stub
    from mt_metadata.features.feature_ts import FeatureTS  # Add stub for feature_ts
    from mt_metadata.features.feature_fc import FeatureFC  # Add stub for feature_fc
    SUPPORTED_FEATURE_DICT = {}
    SUPPORTED_FEATURE_DICT["coherence"] = Coherence
    SUPPORTED_FEATURE_DICT["striding_window_coherence"] = StridingWindowCoherence
    SUPPORTED_FEATURE_DICT["cross_powers"] = CrossPowers  # Register stub
    SUPPORTED_FEATURE_DICT["feature_ts"] = FeatureTS  # Register stub
    SUPPORTED_FEATURE_DICT["feature_fc"] = FeatureFC  # Register stub
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
            Accepts either a flat dict or a dict wrapped under a class name.
        """
        # print(f"[from_dict] initial input_dict: {input_dict}")  # DEBUG PRINT
        
        # Defensive copy to avoid mutating caller's dict
        input_dict = dict(input_dict)
        self.logger.debug(f"[from_dict] initial input_dict: {input_dict}")
        supported_keys = ["feature"] + [k.lower() for k in self._supported_features.keys()]
        
        # Unwrap if wrapped under a supported key
        if len(input_dict) == 1 and list(input_dict.keys())[0].lower() in supported_keys:
            only_key = list(input_dict.keys())[0]
            value = input_dict[only_key]
            print(f"[from_dict] value for key '{only_key}': {value} (type: {type(value)})")  # DEBUG PRINT
            self.logger.debug(f"[from_dict] value for key '{only_key}': {value} (type: {type(value)})")
            if not isinstance(value, dict):
                msg = f"Expected a dict for key '{only_key}', got {type(value)}: {value}"
                self.logger.error(msg)
                raise TypeError(msg)
            input_dict = dict(value)
            print(f"[from_dict] after first unwrap: {input_dict}")  # DEBUG PRINT
            self.logger.debug(f"[from_dict] after first unwrap: {input_dict}")

        # # PATCH: If still missing 'name', but only one key and that key is a supported feature, unwrap again
        # if "name" not in input_dict and len(input_dict) == 1:
        #     only_key = list(input_dict.keys())[0].lower()
        #     if only_key in self._supported_features:
        #         value = list(input_dict.values())[0]
        #         print(f"[from_dict] value for key '{only_key}' (second unwrap): {value} (type: {type(value)})")  # DEBUG PRINT
        #         self.logger.debug(f"[from_dict] value for key '{only_key}' (second unwrap): {value} (type: {type(value)})")
        #         if not isinstance(value, dict):
        #             msg = f"Expected a dict for key '{only_key}' (second unwrap), got {type(value)}: {value}"
        #             self.logger.error(msg)
        #             raise TypeError(msg)
        #         input_dict = dict(value)
        #         print(f"[from_dict] after second unwrap: {input_dict}")  # DEBUG PRINT
        #         self.logger.debug(f"[from_dict] after second unwrap: {input_dict}")
        if "name" not in input_dict:
            msg = f"Features must have a name, supported features are {self._supported_features.keys()}"
            self.logger.error(msg)
            raise KeyError(msg)
        
        feature_name = input_dict.pop("name")
        if feature_name not in self._supported_features:
            msg = f"Feature '{feature_name}' is not supported. Supported features are {self._supported_features.keys()}"
            self.logger.error(msg)
            raise KeyError(msg)

        feature = self._supported_features[feature_name]
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



