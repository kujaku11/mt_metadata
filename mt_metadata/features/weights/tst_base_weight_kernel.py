from mt_metadata.features.weights.base import BaseWeightKernel

class TestWeightKernel(BaseWeightKernel):
    """
    A simple subclass of BaseWeightKernel for testing purposes.
    """
    def __init__(self, **kwargs):
        # Skip schema validation for testing purposes
        super().__init__()
        #self.example_param = kwargs.get("weight_type", None)

    def evaluate(self, values):
        """
        A mock implementation of the evaluate method that simply returns the input values.
        """
        return values

def test_base_weight_kernel():
    # Example input dictionary for initialization
    kernel_dict = {
        "weight_type": "test_value"  # Add any parameters you want to test
    }

    # Initialize the test kernel
    kernel = TestWeightKernel(**kernel_dict)

    # Test input values
    test_values = [1, 2, 3, 4, 5]

    # Evaluate the kernel
    output_values = kernel.evaluate(test_values)

    # Print results
    print("Input values:", test_values)
    print("Output values:", output_values)

    # Assertions to verify correctness
    assert output_values == test_values, "Output values should match input values"
    assert kernel.example_param == "test_value", "example_param should be set correctly"

    print("BaseWeightKernel test passed!")

if __name__ == "__main__":
    test_base_weight_kernel()