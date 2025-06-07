"""
FeatureWeightSpec is the next key layer of abstraction after WeightKernels.

It ties together a feature (including its parameterization),
and one or more weighting kernels (like MonotonicWeightKernel).

This will let you do things like:
- Evaluate "coherence" between ex and hy with a taper kernel
- Apply multiple kernels to the same feature (e.g., low cut and high cut)
- Plug this into a higher-level channel weighting model

"""

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.features.feature import Feature
from mt_metadata.features.weights.monotonic_weight_kernel import MonotonicWeightKernel
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
        self._feature = None  # <-- initialize the backing variable directly
        super().__init__(attr_dict=attr_dict, **kwargs)
        weight_kernels = kwargs.get("weight_kernels", [])
        self.weight_kernels = weight_kernels


    def post_from_dict(self):
        # If feature is a dict, force the setter logic to run
        if isinstance(self.feature, dict):
            self.feature = self.feature
        # Optionally, do the same for weight_kernels if needed

    def from_dict(self, d):
        # If 'feature' is a dict, convert it to the correct object before base from_dict
        if "feature" in d and isinstance(d["feature"], dict):
            self.feature = d["feature"]  # This will use your property setter
            d["feature"] = self.feature  # Now it's the correct object
        super().from_dict(d)
        self.post_from_dict()


    @property
    def feature(self):
        return self._feature

    @feature.setter
    def feature(self, value):
        """
        Set the feature for this weight spec.
        If a dict is provided, it will be used to initialize the feature object.
        If an object is provided, it will be used directly.
        Unwraps nested 'feature' keys if present.


        TODO: FIXME (circular import)
        Should be able to use a model like:
        SUPPORTED_FEATURE_CLASS_MAP = {
        "coherence": Coherence,
        # "multiple_coherence": MultipleCoherence,
        # Add more as needed
        }
        but that will result in a circular import if Coherence import at the top of module.

        """
        # Unwrap if wrapped in 'feature' repeatedly
        while isinstance(value, dict) and "feature" in value and isinstance(value["feature"], dict):
            value = value["feature"]
        if isinstance(value, dict):
            feature_name = value.get("name")
            # Import here to avoid circular import at module level
            print(f"Feature setter: feature_name={feature_name}, value={value}")  # DEBUG
            if feature_name == "coherence":
                from mt_metadata.features.coherence import Coherence
                feature_cls = Coherence
            elif feature_name == "striding_window_coherence":
                from mt_metadata.features.coherence import StridingWindowCoherence
                feature_cls = StridingWindowCoherence
            else:
                msg = f"feature_name {feature_name} not recognized -- resorting to base class"
                self.logger.warning(msg)
                from mt_metadata.features.feature import Feature
                feature_cls = Feature
            self._feature = feature_cls(**value)
            print(f"Feature setter: instantiated {self._feature.__class__}")  # DEBUG
        else:
            self._feature = value
            print(f"Feature setter: set directly to {type(value)}")  # DEBUG


    @property
    def weight_kernels(self):
        return self._weight_kernels

    @weight_kernels.setter
    def weight_kernels(self, value):
        """
        Ensure weight_kernels are properly initialized.
        """
        self._weight_kernels = _unpack_weight_kernels(weight_kernels=value)

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
    result = []
    for wk in weight_kernels:
        # Unwrap if wrapped in "weight_kernel" (TODO: Delete, or revert after mt_metadata pydantic upgrade.)
        if isinstance(wk, dict) and "weight_kernel" in wk:
            wk = wk["weight_kernel"]
        if isinstance(wk, dict):
            if "activation_style" in wk or wk.get("style") == "activation":
                result.append(ActivationMonotonicWeightKernel(**wk))
            elif "half_window_style" in wk or wk.get("style") == "taper":
                result.append(TaperMonotonicWeightKernel(**wk))
            else:
                result.append(MonotonicWeightKernel(**wk))
        else:
            result.append(wk)
    return result

def unwrap_known_wrappers(obj, known_keys=None):
    """
    Recursively unwraps dicts/lists for known single-key wrappers.
    """
    if known_keys is None:
        known_keys = {"feature_weight_spec", "channel_weight_spec", "weight_kernel", "feature"}
    if isinstance(obj, dict):
        # If it's a single-key dict and the key is known, unwrap
        while (
            len(obj) == 1
            and next(iter(obj)) in known_keys
            and isinstance(obj[next(iter(obj))], (dict, list))
        ):
            obj = obj[next(iter(obj))]
        # Recurse into dict values
        return {k: unwrap_known_wrappers(v, known_keys) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [unwrap_known_wrappers(item, known_keys) for item in obj]
    else:
        return obj

# Patch FeatureWeightSpec.from_dict to unwrap wrappers
orig_from_dict = FeatureWeightSpec.from_dict

def from_dict_unwrap(self, d):
    d = unwrap_known_wrappers(d)
    return orig_from_dict(self, d)

FeatureWeightSpec.from_dict = from_dict_unwrap

# --------------- TODO: Move the snippets below into tests/ -----------------
def tst_init():
    fws = FeatureWeightSpec()
    # Test loading from updated dict for TaperMonotonicWeightKernel
    fws.from_dict({
        "feature": {
            "name": "coherence",
            "ch1": "ex",
            "ch2": "hy"
        },
        "weight_kernels": [
            {
                "style": "taper",
                "half_window_style": "hann",
                "transition_lower_bound": 0.3,
                "transition_upper_bound": 0.8,
                "threshold": "low cut"
            }
        ]
    })
    print("1", type(fws.feature))
    print(fws)
     # Force the setter to run on the dict
    fws.feature = fws.feature
    print("2", type(fws.feature))
    print(fws)

def tst_from_json():
    fws = FeatureWeightSpec()
    fws.from_dict(
        {
            "feature": {
                "name": "multiple_coherence",
                "output_channel": "ey"
            },
            "weight_kernels": [
                {
                    "weight_kernel": {
                        "half_window_style": "hann",
                        "transition_lower_bound": 0.4,
                        "transition_upper_bound": 0.8,
                        "threshold": "low cut"
                    }
                }
            ]
        }
    )


if __name__ == "__main__":
    tst_init()
    tst_from_json()
