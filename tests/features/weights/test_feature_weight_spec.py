"""
    Unit test for FeatureWeightSpec class
"""
import unittest
import numpy as np
from mt_metadata.features.coherence import Coherence
from mt_metadata.features.weights.feature_weight_spec import FeatureWeightSpec
from mt_metadata.features.weights.feature_weight_spec import _unpack_weight_kernels
from mt_metadata.features.weights.monotonic_weight_kernel import MonotonicWeightKernel
from mt_metadata.features.weights.monotonic_weight_kernel import TaperMonotonicWeightKernel


class TestFeatureWeightSpec(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the class for testing.
        This method is called once for the entire test class.
        """
        cls.example_feature_dict = {
            "feature": {
                "name": "coherence",
                "ch1": "ex",
                "ch2": "hy",
                "detrend": "linear",
                "window": {
                    "clock_zero_type": "ignore",
                    "normalized": True,
                    "num_samples": 512,
                    "overlap": 128,
                    "type": "hamming"
                }
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
        }


    def setUp(self):
        """
        Set up a FeatureWeightSpec instance for testing.
        """
        self.kernel1 = TaperMonotonicWeightKernel(
            transition_lower_bound=0.2,
            transition_upper_bound=0.5,
            half_window_style="hann",
            threshold="low cut",
        )
        self.kernel2 = TaperMonotonicWeightKernel(
            transition_lower_bound=0.6,
            transition_upper_bound=0.9,
            half_window_style="hann",
            threshold="high cut",
        )
        self.feature = Coherence(
            channel1="ex",
            channel2="hy",
        )  # Use coherence   as the feature
        self.feature_weight_spec = FeatureWeightSpec(
        feature=self.feature,  # Pass the coherence feature
        weight_kernels=[self.kernel1, self.kernel2],
    )
        
        # self.feature_weight_spec = FeatureWeightSpec(
        #     feature_params={"param1": "value1"},
        #     weight_kernels=[self.kernel1, self.kernel2],
        # )

    def test_init_from_dict(self):
        feature_weight_spec = FeatureWeightSpec()
        feature_weight_spec.from_dict(d=self.example_feature_dict)

    def test_features(self):
        """
        Test the features property.
        """
        self.assertEqual(self.feature_weight_spec.feature, self.feature)

    # def test_feature_params(self):
    #     """
    #     Test the feature_params property.
    #     """
    #     self.assertEqual(self.feature_weight_spec.feature_params, {"param1": "value1"})

    def test_weight_kernels(self):
        """
        Test the weight_kernels property.
        """
        self.assertEqual(len(self.feature_weight_spec.weight_kernels), 2)
        self.assertIsInstance(self.feature_weight_spec.weight_kernels[0], TaperMonotonicWeightKernel)

    def test_evaluate(self):
        """
        Test the evaluate method.
        """
        feature_values = np.array([0.1, 0.3, 0.7, 1.0])
        combined_weights = self.feature_weight_spec.evaluate(feature_values)

        # Ensure the output is the correct shape
        self.assertEqual(combined_weights.shape, feature_values.shape)

        # Check specific values (example assertions)
        self.assertAlmostEqual(combined_weights[0], 0.0, places=5)
        self.assertGreater(combined_weights[2], 0.0)

    def test_unpack_weight_kernels(self):
        """
        Test the _unpack_weight_kernels function.
        """
        weight_kernels = [
            {"transition_lower_bound": 0.1, "transition_upper_bound": 0.4},
            self.kernel1,
        ]
        unpacked_kernels = _unpack_weight_kernels(weight_kernels)
        self.assertEqual(len(unpacked_kernels), 2)
        self.assertIsInstance(unpacked_kernels[0], MonotonicWeightKernel)


if __name__ == "__main__":
    unittest.main()
