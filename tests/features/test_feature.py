import pytest
from mt_metadata.features.feature import Feature


def test_all_supported_features_instantiable():
    for feature_id, cls in Feature._make_supported_features_dict().items():
        d = {"feature_id": feature_id, "name": f"test_{feature_id}"}
        # Provide minimal required fields for known features
        if feature_id in ("coherence", "striding_window_coherence", "cross_powers"):
            d["ch1"] = "ex"
            d["ch2"] = "hy"
        # FeatureTS and FeatureFC only require 'feature_id' and 'name' for now
        obj = Feature.from_feature_id(d)
        assert isinstance(obj, cls)
