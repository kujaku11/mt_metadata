# -*- coding: utf-8 -*-
"""
Stub for CrossPowers feature.
"""

from mt_metadata.features.base_feature import BaseFeature

class CrossPowers(BaseFeature):
    """
    Stub feature class for cross powers.
    """
    # __doc__ = write_lines(attr_dict)

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

    # debug notes from a session with GPT.
    # def from_dict(self, input_dict):
    #     # Defensive copy to avoid mutating caller's dict
    #     input_dict = dict(input_dict)
    #     # Always set name, defaulting to 'cross_powers' if not present
    #     self.name = input_dict.get("name", "cross_powers")
    #     # Set any other attributes present in input_dict
    #     for key, value in input_dict.items():
    #         if key != "name":
    #             setattr(self, key, value)

    # def to_dict(self, single=False):
    #     d = super().to_dict(single=single)
    #     if "name" not in d or d["name"] is None:
    #         d["name"] = "cross_powers"
    #     return d
