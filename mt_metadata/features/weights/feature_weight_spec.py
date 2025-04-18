"""
FeatureWeightSpec is the next key layer of abstraction after WeightKernels.

It ties together a feature, its parameterization, and one or more weighting kernels (like MonotonicWeightKernel).

This will let you do things like:

Evaluate "coherence" between ex and hy with a taper kernel

Apply multiple kernels to the same feature (e.g., low cut and high cut)

Plug this into a higher-level channel weighting model

"""

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
import numpy as np

attr_dict = get_schema("base", SCHEMA_FN_PATHS)

from .monotonic_weight_kernel import MonotonicWeightKernel

class FeatureWeightSpec(Base):
    """
    FeatureWeightSpec

    Defines how a particular feature is used to weight an output channel.
    Includes parameters needed to compute the feature and one or more
    weight kernels to evaluate its influence.
    """
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        super().__init__(attr_dict=attr_dict, **kwargs)
        self.feature_params = kwargs.get("feature_params", {})

        weight_kernels = kwargs.get("weight_kernels", [])
        self.weight_kernels = _unpack_weight_kernels(weight_kernels=weight_kernels)
        
    @property
    def feature_params(self):
        return self._feature_params

    @feature_params.setter
    def feature_params(self, value):
        self._feature_params = value

    @property
    def weight_kernels(self):
        return self._weight_kernels

    @weight_kernels.setter
    def weight_kernels(self, value):
        """
        Ensure weight_kernels are properly initialized.
        """
        self._weight_kernels = _unpack_weight_kernels(weight_kernels=value)
        

    def from_dict(self, input_dict):
        """
        Custom from_dict to handle non-schema elements like feature_params and weight_kernels.
        """
        # Filter input_dict to include only keys defined in the schema
        schema_keys = set(self._attr_dict.keys())
        schema_dict = {k: v for k, v in input_dict.items() if k in schema_keys}

        # Call the base class's from_dict with the filtered dictionary
        super().from_dict(schema_dict)

        self.feature_params = input_dict.get("feature_params", {})

        weight_kernels = input_dict.get("weight_kernels", [])
        self.weight_kernels = _unpack_weight_kernels(weight_kernels=weight_kernels)

    def to_dict(self):
        out = super().to_dict()
        out["feature_params"] = self.feature_params
        return out
    
    def evaluate(self, feature_values):
        """
        Evaluate this feature's weighting based on the list of kernels.

        Parameters
        ----------
        feature_values : np.ndarray or float
            The computed values for this feature.

        Returns
        -------
        combined_weight : np.ndarray or float
            The combined weight from all kernels (e.g., multiplied together).
        """

        weights = [kernel.evaluate(feature_values) for kernel in self.weight_kernels]
        return np.prod(weights, axis=0) if weights else 1.0


def _unpack_weight_kernels(weight_kernels):
    """
    Unpack weight kernels from a list of dictionaries or objects.

    TODO: we will need a more general weight kernel unpacking function
    to handle different types of weight kernels.  This function is a placeholder
    for now.

    Parameters
    ----------
    weight_kernels : list
        List of weight kernel dictionaries or objects.

    Returns
    -------
    list
        List of unpacked weight kernel objects.
    """
    return [
        MonotonicWeightKernel(**wk) if isinstance(wk, dict) else wk
        for wk in weight_kernels
    ]
