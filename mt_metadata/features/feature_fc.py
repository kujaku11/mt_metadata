# -*- coding: utf-8 -*-
# mt_metadata/features/feature_fc.py
# =============================================================================
# Imports
# =============================================================================

from pydantic import model_validator

from mt_metadata.features.feature import Feature

# =============================================================================


class FeatureFC(Feature):
    """
    Stub feature class for feature_fc.
    """

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, data: dict) -> dict:
        data["name"] = "feature_fc"
        data["description"] = "A feature for storing feature_fc information."
        data["domain"] = "frequency"
        return data
