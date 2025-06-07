"""
Unit tests for ChannelWeightSpec
"""
import unittest
from mt_metadata.features.weights.channel_weight_spec import ChannelWeightSpec

class TestChannelWeightSpec(unittest.TestCase):
    def setUp(self):
        self.example_chws_dict = {
            "combination_style": "multiplication",
            "feature_weight_specs": [
                {
                    "feature_weight_spec": {
                        "feature":{
                            "name": "coherence",
                            "ch1": "ex",
                            "ch2": "hy"
                        },
                        "weight_kernels": [
                            {
                                "weight_kernel": {
                                    "style": "taper",
                                    "half_window_style": "hann",
                                    "transition_lower_bound": 0.3,
                                    "transition_upper_bound": 0.8,
                                    "threshold": "low cut"
                                }
                            }
                        ]
                    }
                },
                {
                    "feature_weight_spec": {
                        "feature":{
                            "name": "multiple_coherence",
                            "output_channel": "ex"
                        },
                        "weight_kernels": [
                            {
                                "weight_kernel": {
                                    "style": "taper",
                                    "half_window_style": "hann",
                                    "transition_lower_bound": 0.8,
                                    "transition_upper_bound": 0.9,
                                    "threshold": "low cut"
                                }
                            }
                        ]
                    }
                }
            ]
        }
        cws = ChannelWeightSpec()
        cws.from_dict(self.example_chws_dict)
        self.cws = cws

    def test_from_dict(self):
        self.assertEqual(self.cws.combination_style, "multiplication")
        self.assertEqual(len(self.cws.feature_weight_specs), 2)
        self.assertTrue(hasattr(self.cws.feature_weight_specs[0], 'feature'))
        self.assertTrue(hasattr(self.cws.feature_weight_specs[0], 'weight_kernels'))

    def test_repr(self):
        self.assertIsInstance(repr(self.cws), str)

    def test_evaluate_multiplication(self):
        # Get the kernel outputs for the test values
        fw0 = self.cws.feature_weight_specs[0].evaluate(0.5)
        fw1 = self.cws.feature_weight_specs[1].evaluate(0.8)
        expected = fw0 * fw1
        feature_values = {"coherence": 0.5, "multiple_coherence": 0.8}
        result = self.cws.evaluate(feature_values)
        self.assertAlmostEqual(result, expected)

    def test_evaluate_mean(self):
        self.cws.combination_style = "mean"
        feature_values = {"coherence": 0.5, "multiple_coherence": 0.8}
        fw0 = self.cws.feature_weight_specs[0].evaluate(0.5)
        fw1 = self.cws.feature_weight_specs[1].evaluate(0.8)
        expected = (fw0 + fw1) / 2
        result = self.cws.evaluate(feature_values)
        self.assertAlmostEqual(result, expected)

    def test_evaluate_minimum(self):
        self.cws.combination_style = "minimum"
        feature_values = {"coherence": 0.5, "multiple_coherence": 0.8}
        fw0 = self.cws.feature_weight_specs[0].evaluate(0.5)
        fw1 = self.cws.feature_weight_specs[1].evaluate(0.8)
        expected = min(fw0, fw1)
        result = self.cws.evaluate(feature_values)
        self.assertAlmostEqual(result, expected)

    def test_evaluate_maximum(self):
        self.cws.combination_style = "maximum"
        feature_values = {"coherence": 0.5, "multiple_coherence": 0.8}
        fw0 = self.cws.feature_weight_specs[0].evaluate(0.5)
        fw1 = self.cws.feature_weight_specs[1].evaluate(0.8)
        expected = max(fw0, fw1)
        result = self.cws.evaluate(feature_values)
        self.assertAlmostEqual(result, expected)

    def test_evaluate_missing_feature(self):
        feature_values = {"coherence": 0.5}  # missing 'multiple_coherence'
        with self.assertRaises(KeyError):
            self.cws.evaluate(feature_values)

    def test_evaluate_unknown_combination_style(self):
        self.cws.combination_style = "unknown"
        feature_values = {"coherence": 0.5, "multiple_coherence": 0.8}
        with self.assertRaises(ValueError):
            self.cws.evaluate(feature_values)

    def test_feature_weight_specs_setter(self):
        cws = ChannelWeightSpec()
        # Set with a single dict
        cws.feature_weight_specs = self.example_chws_dict["feature_weight_specs"][0]
        self.assertIsInstance(cws.feature_weight_specs, list)
        # Set with a list of dicts
        cws.feature_weight_specs = self.example_chws_dict["feature_weight_specs"]
        self.assertIsInstance(cws.feature_weight_specs, list)

if __name__ == "__main__":
    unittest.main()
