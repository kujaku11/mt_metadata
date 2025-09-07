# -*- coding: utf-8 -*-
"""
Standalone test for Band basemodel that bypasses import issues
"""

import os
import sys

import numpy as np
import pandas as pd


# Add the module path directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))

from typing import Annotated

from pydantic import computed_field, Field, field_validator, ValidationInfo

# Import only what we need directly, avoiding __init__.py
from mt_metadata.base import MetadataBase
from mt_metadata.common.enumerations import StrEnumerationBase


# Define the enums and Band class inline to avoid import issues
class CenterAveragingTypeEnum(StrEnumerationBase):
    arithmetic = "arithmetic"
    geometric = "geometric"


class ClosedEnum(StrEnumerationBase):
    left = "left"
    right = "right"
    both = "both"


class Band(MetadataBase):
    decimation_level: Annotated[
        int,
        Field(
            default=None,
            description="Decimation level for the band",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    index_max: Annotated[
        int,
        Field(
            default=None,
            description="maximum band index",
            examples=["10"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    index_min: Annotated[
        int,
        Field(
            default=None,
            description="minimum band index",
            examples=["10"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    frequency_max: Annotated[
        float,
        Field(
            default=0.0,
            description="maximum band frequency",
            examples=["0.04296875"],
            alias=None,
            json_schema_extra={
                "units": "Hertz",
                "required": True,
            },
        ),
    ]

    frequency_min: Annotated[
        float,
        Field(
            default=0.0,
            description="minimum band frequency",
            examples=["0.03515625"],
            alias=None,
            json_schema_extra={
                "units": "Hertz",
                "required": True,
            },
        ),
    ]

    center_averaging_type: Annotated[
        CenterAveragingTypeEnum,
        Field(
            default="geometric",
            description="type of average to apply when computing the band center",
            examples=["geometric"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    closed: Annotated[
        ClosedEnum,
        Field(
            default="left",
            description="whether interval is open or closed",
            examples=["left"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    name: Annotated[
        str,
        Field(
            default=None,
            description="Name of the band",
            examples=["0.039062"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value: str, info: ValidationInfo) -> str:
        if value is None or value == "":
            # Calculate center frequency manually since it's not available in info.data
            freq_min = info.data.get("frequency_min", 0)
            freq_max = info.data.get("frequency_max", 0)
            if freq_min > 0 and freq_max > 0:
                center_freq = np.sqrt(freq_min * freq_max)
                return f"{center_freq:.6f}"
            else:
                return "unknown"
        return str(value)

    @computed_field
    @property
    def lower_bound(self) -> float:
        return self.frequency_min

    @computed_field
    @property
    def upper_bound(self) -> float:
        return self.frequency_max

    @computed_field
    @property
    def width(self) -> float:
        """returns the width of the band (the bandwidth)."""
        return self.upper_bound - self.lower_bound

    @computed_field
    @property
    def lower_closed(self) -> bool:
        return self.to_interval().closed_left

    @computed_field
    @property
    def upper_closed(self) -> bool:
        return self.to_interval().closed_right

    def _indices_from_frequencies(self, frequencies: np.ndarray) -> np.ndarray:
        """

        Parameters
        ----------
        frequencies: numpy array
            Intended to represent the one-sided (positive) frequency axis of
            the data that has been FFT-ed

        Returns
        -------
        indices: numpy array of integers
            Integer indices of the fourier coefficients associated with the
            frequecies passed as input argument
        """
        if self.lower_closed:
            cond1 = frequencies >= self.lower_bound
        else:
            cond1 = frequencies > self.lower_bound
        if self.upper_closed:
            cond2 = frequencies <= self.upper_bound
        else:
            cond2 = frequencies < self.upper_bound

        indices = np.where(cond1 & cond2)[0]
        return indices

    def set_indices_from_frequencies(self, frequencies: np.ndarray) -> None:
        """assumes min/max freqs are defined"""
        indices = self._indices_from_frequencies(frequencies)
        self.index_min = indices[0]
        self.index_max = indices[-1]

    def to_interval(self):
        return pd.Interval(
            self.frequency_min, self.frequency_max, closed=self.closed.value
        )

    @property
    def harmonic_indices(self):
        """
        Assumes all harmoincs between min and max are present in the band

        Returns
        -------
        numpy array of integers corresponding to harminic indices
        """
        return np.arange(self.index_min, self.index_max + 1)

    def in_band_harmonics(self, frequencies: np.ndarray):
        """
        Parameters
        ----------
        frequencies: array-like, floating poirt

        Returns: numpy array
            the actual harmonics or frequencies in band, rather than the indices.
        -------

        """
        indices = self._indices_from_frequencies(frequencies)
        harmonics = frequencies[indices]
        return harmonics

    @property
    def center_frequency(self) -> float:
        """
        Returns
        -------
        center_frequency: float
            The frequency associated with the band center.
        """
        if self.center_averaging_type == "geometric":
            return np.sqrt(self.lower_bound * self.upper_bound)
        elif self.center_averaging_type == "arithmetic":
            return (self.lower_bound + self.upper_bound) / 2
        else:
            # Default fallback, could raise an error or return a default value
            return float("nan")

    @property
    def center_period(self) -> float:
        """Returns the inverse of center frequency."""
        return 1.0 / self.center_frequency

    def overlaps(self, other) -> bool:
        """Check if this band overlaps with another"""
        ivl = self.to_interval()
        other_ivl = other.to_interval()
        return ivl.overlaps(other_ivl)

    def contains(self, other) -> bool:
        """Check if this band contains nother"""
        ivl = self.to_interval()
        cond1 = ivl.__contains__(other.lower_bound)
        cond2 = ivl.__contains__(other.upper_bound)
        return cond1 & cond2

    @computed_field
    @property
    def fractional_bandwidth(self):
        """
            See
            - https://en.wikipedia.org/wiki/Bandwidth_(signal_processing)#Fractional_bandwidth
            - https://en.wikipedia.org/wiki/Q_factor

        Returns
        -------

        """
        return self.width / self.center_frequency

    @computed_field
    @property
    def Q(self):
        return 1.0 / self.fractional_bandwidth


def test_band_creation():
    """Test basic Band creation"""
    band = Band(
        frequency_min=2.0,
        frequency_max=3.0,
        decimation_level=0,
        index_min=20,
        index_max=30,
        center_averaging_type=CenterAveragingTypeEnum.geometric,
        closed=ClosedEnum.left,
        name="test_band",
    )

    print(f"Band created successfully!")
    print(f"Name: {band.name}")
    print(f"Frequency range: {band.frequency_min} - {band.frequency_max} Hz")
    print(f"Center frequency: {band.center_frequency:.6f} Hz")
    print(f"Width: {band.width} Hz")
    print(f"Closed: {band.closed}")
    print(f"Lower bound: {band.lower_bound}")
    print(f"Upper bound: {band.upper_bound}")

    return band


def test_band_indices():
    """Test band frequency indexing"""
    frequencies = 0.1 * np.arange(100)  # 0-10Hz

    band = Band(
        frequency_min=2.0,
        frequency_max=3.0,
        decimation_level=0,
        index_min=0,
        index_max=0,  # Will be set by set_indices_from_frequencies
        center_averaging_type=CenterAveragingTypeEnum.geometric,
        closed=ClosedEnum.left,
        name="test_indices",
    )

    band.set_indices_from_frequencies(frequencies)
    print(f"Index range after frequency analysis: {band.index_min} - {band.index_max}")

    harmonics = band.in_band_harmonics(frequencies)
    print(
        f"In-band harmonics: {len(harmonics)} frequencies from {harmonics[0]:.1f} to {harmonics[-1]:.1f} Hz"
    )

    return band


if __name__ == "__main__":
    print("Testing Band class...")

    try:
        band1 = test_band_creation()
        print("✓ Band creation test passed")
    except Exception as e:
        print(f"✗ Band creation test failed: {e}")

    try:
        band2 = test_band_indices()
        print("✓ Band indices test passed")
    except Exception as e:
        print(f"✗ Band indices test failed: {e}")

    print("\nDone!")
