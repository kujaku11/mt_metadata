# -*- coding: utf-8 -*-
"""
Feature registry module to avoid circular imports.

This module defines the SUPPORTED_FEATURE_DICT that maps feature names to their classes.
It's separate from __init__.py to prevent circular import issues.
"""


def get_supported_feature_dict():
    """
    Get the supported feature dictionary with lazy imports to avoid circular dependencies.

    Returns
    -------
    dict
        Dictionary mapping feature names to feature classes
    """
    # Import here to avoid circular dependencies
    from mt_metadata.features.coherence import Coherence
    from mt_metadata.features.cross_powers import CrossPowers
    from mt_metadata.features.feature_fc import FeatureFC
    from mt_metadata.features.feature_ts import FeatureTS
    from mt_metadata.features.striding_window_coherence import StridingWindowCoherence

    return {
        "coherence": Coherence,
        "striding_window_coherence": StridingWindowCoherence,
        "cross_powers": CrossPowers,
        "feature_ts": FeatureTS,
        "feature_fc": FeatureFC,
    }


# For backward compatibility, we'll create the dictionary when this module is imported
# but using lazy imports
SUPPORTED_FEATURE_DICT = get_supported_feature_dict()
