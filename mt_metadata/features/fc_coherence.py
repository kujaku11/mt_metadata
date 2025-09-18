# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
from pydantic import computed_field, Field, model_validator

from mt_metadata.common.enumerations import StrEnumerationBase
from mt_metadata.features.coherence import Coherence
from mt_metadata.features.feature import Feature


# =====================================================
class BandDefinitionTypeEnum(StrEnumerationBase):
    Q = "Q"
    fractional_bandwidth = "fractional bandwidth"
    user_defined = "user defined"


class QRadiusEnum(StrEnumerationBase):
    constant_Q = "constant Q"
    user_defined = "user defined"


class FCCoherence(Coherence, Feature):
    minimum_fcs: Annotated[
        int,
        Field(
            default=2,
            description="The minimum number of Fourier coefficients needed to compute the feature.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["2"],
            },
        ),
    ]

    band_definition_type: Annotated[
        BandDefinitionTypeEnum,
        Field(
            default="Q",
            description="How the feature frequency bands are defined.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["user defined"],
            },
        ),
    ]

    q_radius: Annotated[
        QRadiusEnum,
        Field(
            default="constant Q",
            description="How the feature frequency bands are defined.",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["user defined"],
            },
        ),
    ]

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, data: dict) -> dict:
        data["name"] = "fc_coherence"
        data["domain"] = "frequency"
        data["description"] = (
            "Magnitude-squared coherence computed from frequency-domain Fourier coefficients (FCs). "
            "Cxy(f) = |Sxy(f)|^2 / (Sxx(f) * Syy(f)), where Sxy is the cross-power spectrum, "
            "Sxx and Syy are auto-power spectra, all estimated by averaging over windows."
        )
        return data

    @computed_field
    @property
    def channel_pair_str(self) -> str:
        return f"{self.channel_1}, {self.channel_2}"

    def compute(
        self, fc1: np.ndarray, fc2: np.ndarray
    ) -> tuple[np.ndarray | None, np.ndarray]:
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

        # Magnitude-squared coherence with protection against division by zero
        denominator = sxx * syy

        # Use numpy error handling to suppress division warnings
        with np.errstate(divide="ignore", invalid="ignore"):
            coherence = np.abs(sxy) ** 2 / denominator

        # Replace any infinite or NaN values with 0
        coherence = np.where(np.isfinite(coherence), coherence, 0.0)
        return None, coherence
