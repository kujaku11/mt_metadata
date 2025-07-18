# -*- coding: utf-8 -*-
"""
Stub for CrossPowers feature.
"""

from mt_metadata.features.feature import Feature

class CrossPowers(Feature):
    """
    Stub feature class for cross powers.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "cross_powers"
        self.add_base_attribute(
            "name",
            "cross_powers",
            {
                "type": str,
                "required": True,
                "style": "free form",
                "description": "Name of the feature",
                "units": None,
                "options": [],
                "alias": [],
                "example": "cross_powers",
                "default": "cross_powers",
            },
        )
