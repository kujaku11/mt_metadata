# -*- coding: utf-8 -*-

from .feature_ts_run import FeatureTSRun
from .feature_fc_run import FeatureFCRun
from .feature_decimation_channel import FeatureDecimationChannel
from .feature import Feature
from .striding_window_coherence import StridingWindowCoherence


__all__ = [
    "FeatureTSRun",
    "FeatureFCRun",
    "Feature",
    "FeatureDecimationChannel",
    "StridingWindowCoherence",
    "SUPPORTED_FEATURE_DICT",
]

# Import the supported feature dictionary from the registry to avoid circular imports
from mt_metadata.features.registry import SUPPORTED_FEATURE_DICT
