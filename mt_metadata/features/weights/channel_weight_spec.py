"""
processing_weights candidate:
    {
                            "channel_weight_spec": {
                                "output_channels": [
                                    "ex"
                                ],
                                "combination_style": "multiplication",
                                "features": [
                                    {
                                        "feature_name": "coherence",
                                        "feature_params": {
                                            "ch1": "ex",
                                            "ch2": "hy"
                                        },
                                        "window_style": "threshold",
                                        "window_params": {
                                            "min": 0.8,
                                            "max": "+inf"
                                        }
                                    },
                                    {
                                        "feature_name": "multiple_coherence",
                                        "feature_params": {
                                            "output_channel": "ex"
                                        },
                                        "window_style": "threshold",
                                        "window_params": {
                                            "min": 0.9,
                                            "max": 1.1
                                        }
                                    }
                                ]
                            }
                        }
"""
"""

    Notes, and doc for weights PR.

    channel_weight_specs is a candidate name for the json block like the following:
    >>> diff processing_configuration_template.json test_processing_config_with_weights_block.json
    (Another candidate name could be `processing_weights`, or `weights`, but the final nomenclature
    can be sorted out after there is a functional prototype with the appropriate structure.)


    This block is basically a dict that maps an output channel name to a ChannelWeightSpec (CWS) object.

    There are at least three places we would like to be able to plug in such a dict to the processing flow.
    1. At the frequency_band level, so that each band can be associated with a specialty CWS
    2. At the decimation_level level, so that all bands in a GIB have a common, default.
    3. At a high level, so that all processing uses them.
    TAI: In future, hopefully we could insert a custom CWS for a specific band, but leave
    all other bands to use the DecimationLevel defaul CWS, for example.  i.e. the CWS can
    be defined for different scopes.

    TODO FIXME: IN mt_metadata/transfer_functions/processing/auaora/processing.py
    when you output a json, it looks like the `decimations` level should be named:
    `decimation_levels` instead.

    The general model I'll try to follow will be to open an itearable of objects
    with a plural of the object name. For example, the processing block called "bands"
    follows with an itearble of:
    {
        "band": {
            "center_averaging_type": "geometric",
            ...
            "index_min": 25
        }
    }
    ...
    {
        "band": {
            "center_averaging_type": "geometric",
            ...
            "index_min": 25
        }
    }

    Will start by plugging this into the DecimationLevel.

    TODO: Determine if this class, which represents a single element of a list
    of channel weight specs, which will be in the json, should have a wrapper or not.

    In the same way that a DecimationLevel has Bands,
    it will also have ChannelWeightSpecs.
"""

# from .feature_weight_spec import FeatureWeightSpec
from mt_metadata.features.weights.feature_weight_spec import FeatureWeightSpec

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base

from mt_metadata.features.weights.standards import SCHEMA_FN_PATHS

attr_dict = get_schema("channel_weight_spec", SCHEMA_FN_PATHS)

class ChannelWeightSpec(Base):
    """
    ChannelWeightSpec

    Defines a weighting model for one output channel (e.g., ex, ey, hz).
    Combines multiple feature-based weighting specifications into a
    single weight using the specified combination strategy.
    """
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        super().__init__(attr_dict=attr_dict, **kwargs)
        # super().__init__()
        # self.from_dict(kwargs)
        self.features = kwargs.get("features", [])
        # self._features = [
        #     FeatureWeightSpec(**f) if isinstance(f, dict) else f
        #     for f in kwargs.get("features", [])
        # ]

    def from_dict(self, input_dict):
        """
        Override the from_dict method to handle the 'features' attribute explicitly.
        """
        super().from_dict(input_dict)  # Populate attributes from the schema
        if "features" in input_dict:
            self.features = [
                FeatureWeightSpec(**f) if isinstance(f, dict) else f
                for f in input_dict["features"]
            ]


    # TODO: consider adding this:
    # def to_dict(self):
    #     """
    #     Since features isn’t in the schema, to_dict() won’t include it.
    #     If you ever need to dump this object to a fully serializable form
    #     (e.g., for caching, metadata output), you might want:
    #
    #     Returns
    #     -------
    #
    #     """
    #     out = super().to_dict()
    #     out["features"] = [f.to_dict() for f in self.features]
    #     return out

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, val):
        self._features = [
            FeatureWeightSpec(**f) if isinstance(f, dict) else f for f in val
        ]


    def evaluate(self, feature_values_dict):
        """
        Evaluate the channel weight by combining weights from all features.

        Parameters
        ----------
        feature_values_dict : dict
            Dictionary mapping feature names to their computed values.
            e.g., {"coherence": ndarray, "multiple_coherence": ndarray}

        Returns
        -------
        channel_weight : float or np.ndarray
        """
        import numpy as np

        weights = []
        for feature_spec in self.features:
            fname = feature_spec.feature_name
            if fname not in feature_values_dict:
                raise KeyError(f"Feature values missing for '{fname}'")

            w = feature_spec.evaluate(feature_values_dict[fname])
            weights.append(w)

        if not weights:
            return 1.0

        combo = self.combination_style
        if combo == "multiplication":
            return np.prod(weights, axis=0)
        elif combo == "mean":
            return np.mean(weights, axis=0)
        elif combo == "minimum":
            return np.min(weights, axis=0)
        elif combo == "maximum":
            return np.max(weights, axis=0)
        else:
            raise ValueError(f"Unknown combination style: {combo}")



def tst_from_json():
    example_json_dict = {
        "combination_style": "multiplication",
        "features": [
            {
                "feature_name": "coherence",
                "feature_params": {"ch1": "ex", "ch2": "hy"},
                "weight_kernels": [
                    {
                        "threshold": "low cut",
                        "half_window_style": "hann",
                        "transition_lower_bound": 0.3,
                        "transition_upper_bound": 0.8
                    }
                ]
            },
            {
                "feature_name": "multiple_coherence",
                "feature_params": {"output_channel": "ex"},
                "weight_kernels": [
                    {
                        "threshold": "low cut",
                        "half_window_style": "rectangle",
                        "transition_lower_bound": 0.9,
                        "transition_upper_bound": 0.9
                    }
                ]
            }
        ]
    }
    cws = ChannelWeightSpec()
    cws.from_dict(example_json_dict)
    print("OK")


def main():
    tst_from_json()

if __name__ == "__main__":
    main()
