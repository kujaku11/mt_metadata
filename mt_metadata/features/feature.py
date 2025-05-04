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

# =============================================================================
# attr_dict = get_schema("feature", SCHEMA_FN_PATHS)

from mt_metadata.features.base_feature import BaseFeature

def _make_supported_features_dict():
    # TODO Import all supported fetaures here
    from mt_metadata.features.coherence import Coherence
    SUPPORTED_FEATURE_DICT = {}
    SUPPORTED_FEATURE_DICT["coherence"] = Coherence
    return SUPPORTED_FEATURE_DICT

# =============================================================================
class Feature(BaseFeature):
    # __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self._supported_features = _make_supported_features_dict()

    def from_dict(self, input_dict):
        if "name" not in input_dict.keys():
            msg = f"Features must have an ID (name), supported features are {SUPPORTED_FEATURE_DICT.keys()}"

        feature = SUPPORTED_FEATURE_DICT[input_dict.pop("feature_name")]
        feature_obj = feature()
        feature_obj.from_dict(input_dict)
        print("yay")



