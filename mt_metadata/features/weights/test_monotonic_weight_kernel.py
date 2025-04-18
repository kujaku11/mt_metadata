import numpy as np
from mt_metadata.features.weights.monotonic_weight_kernel import MonotonicWeightKernel

def test_monotonic_weight_kernel():
    # Example input dictionary for initialization
    kernel_dict = {
        "transition_lower_bound": 0.3,
        "transition_upper_bound": 0.8,
        "half_window_style": "hann",
        "threshold": "low cut"
    }

    # Initialize the kernel
    kernel = MonotonicWeightKernel().from_dict(kernel_dict)

    # Test input values
    test_values = np.array([0.1, 0.3, 0.5, 0.8, 1.0])

    # Evaluate the kernel
    weights = kernel.evaluate(test_values)

    # Print results
    print("Input values:", test_values)
    print("Computed weights:", weights)

    # Assertions to verify correctness
    assert weights[0] == 0.0, "Weight for value below lower bound should be 0"
    assert weights[-1] == 1.0, "Weight for value above upper bound should be 1"
    assert len(weights) == len(test_values), "Output length should match input length"

    print("MonotonicWeightKernel test passed!")

if __name__ == "__main__":
    test_monotonic_weight_kernel()