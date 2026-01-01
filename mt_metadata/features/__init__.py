# -*- coding: utf-8 -*-
"""
======================
Features Metadata
======================

The Features module provides metadata containers for defining and calculating
features from magnetotelluric data in both time domain and frequency domain.

Features are computed quantities that characterize data quality, signal properties,
or specific aspects of the electromagnetic response. This module supports various
feature types including coherence metrics, spectral characteristics, and custom
user-defined features.

MetadataBase Objects
--------------------
* Feature - Base class for all feature metadata, defining feature type, parameters,
  and computation methods
* FeatureTSRun - Time series run features for time domain calculations (e.g.,
  signal statistics, anomaly detection)
* FeatureFCRun - Fourier coefficient run features for frequency domain calculations
  (e.g., spectral quality metrics, transfer function properties)
* FeatureDecimationChannel - Channel-specific features at different decimation
  levels for multi-resolution analysis
* StridingWindowCoherence - Coherence calculated over striding windows to assess
  signal consistency and quality over time
* SUPPORTED_FEATURE_DICT - Registry of all available feature types and their
  configurations

Usage
-----
Features metadata objects define:
- Feature type and calculation method
- Input parameters and thresholds
- Output specifications
- Applicable frequency bands or time windows
- Quality control criteria

These metadata containers ensure reproducible feature calculations and facilitate
sharing of feature extraction pipelines across different processing workflows.

"""

from .feature_ts_run import FeatureTSRun
from .feature_fc_run import FeatureFCRun
from .feature_decimation_channel import FeatureDecimationChannel
from .feature import Feature
from .striding_window_coherence import StridingWindowCoherence


__all__ = [
    "FeatureTSRun",
    "FeatureFCRun",
    "Feature",
    "FeatureDecimationChannel",
    "StridingWindowCoherence",
    "SUPPORTED_FEATURE_DICT",
]

# Import the supported feature dictionary from the registry to avoid circular imports
from mt_metadata.features.registry import SUPPORTED_FEATURE_DICT
