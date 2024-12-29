"""
This module contains the metadata ShortTimeFourierTransform (STFT) metadata class.

Development Notes:
    This is part of a refactoring of the FCDecimation and aurora DecimationLevel

    Both of those classes are essentially used to represent Spectrograms,
    and in the Aurora DecimationLevel case, there are also information about processing included.

    This class pulls out the metadata that are associated with the application of the STFT.

    "harmonic_indices"
    "method"
    "min_num_stft_windows"
    "per_window_detrend_type"
    "pre_fft_detrend_type"
    "prewhitening_type"
    "recoloring"


Created on Sat Dec 28 18:39:00 2024

@author: kkappler

"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.transfer_functions.processing.standards import SCHEMA_FN_PATHS

# =============================================================================
attr_dict = get_schema("short_time_fourier_transform", SCHEMA_FN_PATHS)


# =============================================================================


class ShortTimeFourierTransform(Base):
    """
        The ShortTimeFourierTransform (STFT) class contains information about how to apply the STFT
        to the time series.

    """
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        """
            Constructor.
            :param kwargs: TODO: add description
        """
        super().__init__(attr_dict=attr_dict, **kwargs)


def main():
    stft = ShortTimeFourierTransform()


if __name__ == "__main__":
    main()
