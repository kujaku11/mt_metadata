# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import Citation

# =============================================================================
attr_dict = get_schema("copyright", SCHEMA_FN_PATHS)
# =============================================================================
class Copyright(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.citation = Citation()
        self.conditions_of_use = "".join(
            [
                "All data and metadata for this survey are ",
                "available free of charge and may be copied ",
                "freely, duplicated and further distributed ",
                "provided this data set is cited as the ",
                "reference. While the author(s) strive to ",
                "provide data and metadata of best possible ",
                "quality, neither the author(s) of this data ",
                "set, not IRIS make any claims, promises, or ",
                "guarantees about the accuracy, completeness, ",
                "or adequacy of this information, and expressly ",
                "disclaim liability for errors and omissions in ",
                "the contents of this file. Guidelines about ",
                "the quality or limitations of the data and ",
                "metadata, as obtained from the author(s), are ",
                "included for informational purposes only.",
            ]
        )
        self.release_license = None
        self.comments = None
        super().__init__(attr_dict=attr_dict, **kwargs)
