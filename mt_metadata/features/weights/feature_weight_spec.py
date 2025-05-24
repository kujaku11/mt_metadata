"""
FeatureWeightSpec is the next key layer of abstraction after WeightKernels.

It ties together a feature (including its parameterization),
and one or more weighting kernels (like MonotonicWeightKernel).

This will let you do things like:

Evaluate "coherence" between ex and hy with a taper kernel

Apply multiple kernels to the same feature (e.g., low cut and high cut)

Plug this into a higher-level channel weighting model

"""

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.features.feature import Feature
from mt_metadata.features.weights.monotonic_weight_kernel import BaseMonotonicWeightKernel
from mt_metadata.features.weights.monotonic_weight_kernel import ActivationMonotonicWeightKernel
from mt_metadata.features.weights.monotonic_weight_kernel import TaperMonotonicWeightKernel
from mt_metadata.features.weights.standards import SCHEMA_FN_PATHS
import numpy as np

attr_dict = get_schema("base", SCHEMA_FN_PATHS)
# no need to add to attr dict if we have lists of mtmetadata objs.
# attr_dict.add_dict(Feature()._attr_dict, "feature")

class FeatureWeightSpec(Base):
    """
    FeatureWeightSpec

    Defines how a particular feature is used to weight an output channel.
    Includes parameters needed to compute the feature and one or more
    weight kernels to evaluate its influence.
    """
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        # self._feature_params = None
        self.feature = Feature()
        #self.weight_kernels = Feature()
        # if "feature_name" in kwargs.keys():
        #     feature = SUPPORTED_FEATURE_DICT[kwargs.pop("feature_name")]
        #     feature_obj = feature()
        #     feature_obj.from_dict(kwargs.pop("feature_params"))
        super().__init__(attr_dict=attr_dict, **kwargs)
        # self.feature_params = kwargs.get("feature_params", {})

        weight_kernels = kwargs.get("weight_kernels", [])
        self.weight_kernels = _unpack_weight_kernels(weight_kernels=weight_kernels)

    @property
    def feature(self):
        return self._feature

    @feature.setter
    def feature(self, value):
        self._feature = value

    @property
    def weight_kernels(self):
        return self._weight_kernels

    @weight_kernels.setter
    def weight_kernels(self, value):
        """
        Ensure weight_kernels are properly initialized.
        """
        self._weight_kernels = _unpack_weight_kernels(weight_kernels=value)


    # def from_dict(self, input_dict):
    #     """
    #     Custom from_dict to handle non-schema elements like feature_params and weight_kernels.
    #     """
    #     # Filter input_dict to include only keys defined in the schema
    #     schema_keys = set(self._attr_dict.keys())
    #     schema_dict = {k: v for k, v in input_dict.items() if k in schema_keys}
    #
    #     # Call the base class's from_dict with the filtered dictionary
    #     super().from_dict(schema_dict)
    #
    #     self.feature_params = input_dict.get("feature_params", {})
    #
    #     weight_kernels = input_dict.get("weight_kernels", [])
    #     self.weight_kernels = _unpack_weight_kernels(weight_kernels=weight_kernels)
    #
    # def to_dict(self):
    #     out = super().to_dict()
    #     out["feature_params"] = self.feature_params
    #     return out

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
    Determines the correct kernel class (Activation or Taper) based on keys.
    """
    from mt_metadata.features.weights.monotonic_weight_kernel import (
        ActivationMonotonicWeightKernel, TaperMonotonicWeightKernel, BaseMonotonicWeightKernel
    )
    result = []
    for wk in weight_kernels:
        if isinstance(wk, dict):
            if "activation_style" in wk or wk.get("style") == "activation":
                result.append(ActivationMonotonicWeightKernel(**wk))
            elif "half_window_style" in wk or wk.get("style") == "taper":
                result.append(TaperMonotonicWeightKernel(**wk))
            else:
                result.append(BaseMonotonicWeightKernel(**wk))
        else:
            result.append(wk)
    return result


def tst_init():
    fws = FeatureWeightSpec()

if __name__ == "__main__":
    tst_init()
