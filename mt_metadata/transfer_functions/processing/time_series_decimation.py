# -*- coding: utf-8 -*-
"""
This module contains the metadata TimeSeriesDecimation class.

Development Notes:
    This is part of a refactoring that seeks to separate the FCDecimation and aurora DecimationLevel
    from the time series decimation.

    The previous version of this class was in processing/aurora/decimation.py and had attrs
    ["level", "factor", "method", "sample_rate", "anti_alias_filter"],

    TODO: Consider adding a parent_sample_rate attribute to this class
    
Created on Thu Dec 26 12:00:00 2024

@author: kkappler

"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.transfer_functions.processing.standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("time_series_decimation", SCHEMA_FN_PATHS)
# =============================================================================


class TimeSeriesDecimation(Base):
    """
        The decimation class contains information about how to decimaate a time series as well
         as attributes to describe it's place in the mth5 hierarchy.
         Key pieces of information:
        1. The decimation level, an integer that tells the sequential order in a decimation scheme.
        2. The decimation factor.  This is normally an integer, but the decimation.json does allow for floating point values.

        Development Notes:
        -
    """
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        super().__init__(attr_dict=attr_dict, **kwargs)

    # Temporary workarounds while replacing legacy Decimation class
    # @property
    # def level(self):
    #     return self.decimation_level
    #
    # @property
    # def factor(self):
    #     return self.decimation_factor
    #
    # @property
    # def method(self):
    #     return self.decimation_method
    #
    # @property
    # def sample_rate(self):
    #     return self.sample_rate_decimation


#
# def main():
#     pass
#
#
# if __name__ == "__main__":
#     main()
