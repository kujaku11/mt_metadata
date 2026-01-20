# -*- coding: utf-8 -*-
# =============================================================================
# Imports
# =============================================================================

from pydantic import model_validator

from mt_metadata.features.feature import Feature

# =============================================================================


class FeatureTS(Feature):
    """
    Stub feature class for time series features.
    """

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, data: dict) -> dict:
        data["name"] = "feature_ts"
        data["description"] = "A feature for storing time series information."
        data["domain"] = "time"
        return data
