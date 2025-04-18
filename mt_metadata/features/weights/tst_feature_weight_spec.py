from mt_metadata.features.weights.feature_weight_spec import FeatureWeightSpec

def test_feature_weight_spec():
    example_feature_dict = {
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
    }
    feature = FeatureWeightSpec()
    feature.from_dict(example_feature_dict)
#    feature = FeatureWeightSpec(**example_feature_dict)

    # Check if the attributes are correctly populated
    assert feature.feature_name == "coherence"
    assert feature.feature_params == {"ch1": "ex", "ch2": "hy"}
    assert len(feature.weight_kernels) == 1
    assert feature.weight_kernels[0]["threshold"] == "low cut"
    assert feature.weight_kernels[0]["half_window_style"] == "hann"

    print("FeatureWeightSpec test passed!")

if __name__ == "__main__":
    test_feature_weight_spec()