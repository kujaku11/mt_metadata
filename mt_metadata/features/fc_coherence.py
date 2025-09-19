# -*- coding: utf-8 -*-
"""

    This is a placeholder for FCCoherence feature class, which computes the magnitude-squared coherence
    from frequency-domain Fourier coefficients (FCs). It is a work in progress and will be
    implemented in the future.
"""

# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from ..transfer_functions.processing.window import Window
from typing import Tuple

import numpy as np
import scipy.signal as ssig

# =============================================================================
attr_dict = get_schema("feature", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("coherence", SCHEMA_FN_PATHS), None)
attr_dict.add_dict(Window()._attr_dict, "window")


# =============================================================================
class FCCoherence(Base):
    """
    Computes magnitude-squared coherence from frequency-domain Fourier coefficients (FCs).

    Given two sets of FCs (complex arrays, shape: [n_windows, n_freqs]), computes:
        Cxy(f) = |Sxy(f)|^2 / (Sxx(f) * Syy(f))
    where:
        Sxy(f) = mean(FC1(f) * conj(FC2(f)), axis=0)  # cross-power
        Sxx(f) = mean(|FC1(f)|^2, axis=0)             # auto-power
        Syy(f) = mean(|FC2(f)|^2, axis=0)             # auto-power
    """
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.channel_1 = None
        self.channel_2 = None
        super().__init__(attr_dict=attr_dict, **kwargs)
        self.name = "fc_coherence"
        self.domain = "frequency"
        self.description = (
            "Magnitude-squared coherence computed from frequency-domain Fourier coefficients (FCs). "
            "Cxy(f) = |Sxy(f)|^2 / (Sxx(f) * Syy(f)), where Sxy is the cross-power spectrum, "
            "Sxx and Syy are auto-power spectra, all estimated by averaging over windows."
        )

    @property
    def channel_pair_str(self) -> str:
        return f"{self.channel_1}, {self.channel_2}"

    def compute(self, fc1: np.ndarray, fc2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute magnitude-squared coherence from FCs.

        Parameters
        ----------
        fc1 : np.ndarray
            Fourier coefficients for channel 1, shape (n_windows, n_freqs)
        fc2 : np.ndarray
            Fourier coefficients for channel 2, shape (n_windows, n_freqs)

        Returns
        -------
        freqs : np.ndarray
            Frequency axis (if available, else None)
        coherence : np.ndarray
            Magnitude-squared coherence, shape (n_freqs,)
        """
        # Cross-power and auto-powers
        sxy = np.mean(fc1 * np.conj(fc2), axis=0)
        sxx = np.mean(np.abs(fc1) ** 2, axis=0)
        syy = np.mean(np.abs(fc2) ** 2, axis=0)
        # Magnitude-squared coherence
        coherence = np.abs(sxy) ** 2 / (sxx * syy)
        return None, coherence
