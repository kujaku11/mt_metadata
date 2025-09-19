"""
    Container for weighting strategy to apply to a single tf estimation
    having a single output channel (usually one of "ex", "ey", "hz").

    candidate data structure is stored in test_helpers/channel_weight_specs_example.json
        
    Candidate names: processing_weights, feature_weights, channel_weights_spec, channel_weighting

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
    all other bands to use the DecimationLevel default CWS, for example.  i.e. the CWS can
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


from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.features.weights.feature_weight_spec import FeatureWeightSpec
from mt_metadata.features.weights.standards import SCHEMA_FN_PATHS
from mt_metadata.helper_functions import cast_to_class_if_dict
from mt_metadata.helper_functions import validate_setter_input
from typing import List, Union

import numpy as np
import xarray as xr

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
        self._weights = None

    @property
    def feature_weight_specs(self) -> List[FeatureWeightSpec]:
        """
            Return feature_weight_specs.

        """
        return self._feature_weight_specs

    @feature_weight_specs.setter
    def feature_weight_specs(self, value: Union[List[Union[FeatureWeightSpec, dict]], FeatureWeightSpec]) -> None:
        """
        Set features. If any are in dict form, cast them to FeatureWeightSpec objects before setting.

        :param value: FeatureWeightSpecs or equivalent dicts
        :type value: Union[List[Union[FeatureWeightSpec, dict]]

        """
        values = validate_setter_input(value, FeatureWeightSpec)
        fws_list = [cast_to_class_if_dict(obj, FeatureWeightSpec) for obj in values]
        self._feature_weight_specs = fws_list

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
        for feature_weight_spec in self.feature_weight_specs:
            fname = feature_weight_spec.feature.name
            if fname not in feature_values_dict:
                raise KeyError(f"Feature values missing for '{fname}'")

            w = feature_weight_spec.evaluate(feature_values_dict[fname])
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
    

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, value):
        if not isinstance(value, (xr.DataArray, xr.Dataset, np.ndarray, None.__class__)):
            raise TypeError("Data must be a numpy array or xarray.")
        self._weights = value

    def get_weights_for_band(self, band):
        """
        Extract weights for the frequency bin closest to the band's center frequency.
        
        TODO: Add tests.
        Parameters
        ----------
        band : object
            Should have a .center_frequency attribute (float, Hz).

        Returns
        -------
        weights : np.ndarray or xarray.DataArray
            Weights for the closest frequency bin.
        """
        if self.weights is None:
            raise ValueError("No weights have been set.")

        # Assume weights is an xarray.DataArray or Dataset with a 'frequency' dimension
        freq_axis = None
        if hasattr(self.weights, "dims"):
            # Try to find the frequency dimension
            for dim in self.weights.dims:
                if "freq" in dim:
                    freq_axis = dim
                    break
            if freq_axis is None:
                raise ValueError("Could not find frequency dimension in weights.")

            freqs = self.weights[freq_axis].values
        elif isinstance(self.weights, np.ndarray):
            # If it's a plain ndarray, assume first axis is frequency
            freqs = np.arange(self.weights.shape[0])
            freq_axis = 0
        else:
            raise TypeError("Weights must be an xarray.DataArray, Dataset, or numpy array.")

        # Find index of closest frequency
        idx = np.argmin(np.abs(freqs - band.center_frequency))

        # Extract weights for that frequency
        if hasattr(self.weights, "isel"):
            # xarray: use isel
            weights_for_band = self.weights.isel({freq_axis: idx})
        else:
            # numpy: index along first axis
            weights_for_band = self.weights[idx]

        return weights_for_band
