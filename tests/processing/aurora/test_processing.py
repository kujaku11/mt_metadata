#!/usr/bin/env python3
"""
Test suite for processing_basemodel.py

This file tests the Processing class and BandSpecificationStyleEnum functionality.
All tests pass and cover the core functionality of the processing module.

Run with: python test_processing_final.py
"""

import os
import sys
import unittest


# Add project root to Python path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from mt_metadata.processing.aurora.decimation_level_basemodel import DecimationLevel
    from mt_metadata.processing.aurora.processing_basemodel import (
        BandSpecificationStyleEnum,
        Processing,
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the mt_metadata project root")
    sys.exit(1)


class TestBandSpecificationStyleEnum(unittest.TestCase):
    """Test BandSpecificationStyleEnum functionality."""

    def test_enum_values(self):
        """Test that enum has expected string representations."""
        self.assertIn("EMTF", str(BandSpecificationStyleEnum.EMTF))
        self.assertIn("band_edges", str(BandSpecificationStyleEnum.band_edges))

    def test_enum_string_inheritance(self):
        """Test that enum inherits from string."""
        self.assertIsInstance(BandSpecificationStyleEnum.EMTF, str)
        self.assertIsInstance(BandSpecificationStyleEnum.band_edges, str)

    def test_enum_from_string(self):
        """Test creating enum instances from string values."""
        emtf_enum = BandSpecificationStyleEnum("EMTF")
        self.assertEqual(emtf_enum, BandSpecificationStyleEnum.EMTF)

        band_edges_enum = BandSpecificationStyleEnum("band_edges")
        self.assertEqual(band_edges_enum, BandSpecificationStyleEnum.band_edges)

    def test_enum_comparison(self):
        """Test enum comparison operations."""
        emtf1 = BandSpecificationStyleEnum.EMTF
        emtf2 = BandSpecificationStyleEnum("EMTF")
        band_edges = BandSpecificationStyleEnum.band_edges

        # Test equality
        self.assertEqual(emtf1, emtf2)
        self.assertNotEqual(emtf1, band_edges)

        # Test identity
        self.assertIs(emtf1, BandSpecificationStyleEnum.EMTF)

    def test_enum_error_cases(self):
        """Test enum error handling for invalid values."""
        with self.assertRaises(ValueError):
            BandSpecificationStyleEnum("invalid_value")

        with self.assertRaises(ValueError):
            BandSpecificationStyleEnum("")

        with self.assertRaises((ValueError, TypeError)):
            BandSpecificationStyleEnum(123)


class TestProcessingBasics(unittest.TestCase):
    """Test basic Processing class functionality."""

    def test_default_instantiation(self):
        """Test creating Processing instance with defaults."""
        processing = Processing()

        # Check default values
        self.assertIsInstance(processing.decimations, list)
        self.assertEqual(len(processing.decimations), 0)
        self.assertIsNone(processing.band_specification_style)
        self.assertIsNone(processing.band_setup_file)
        self.assertEqual(processing.id, "")

    def test_field_assignment(self):
        """Test assigning values to Processing fields."""
        processing = Processing()

        # Test ID assignment
        processing.id = "test_processing_config"
        self.assertEqual(processing.id, "test_processing_config")

        # Test enum assignment
        processing.band_specification_style = BandSpecificationStyleEnum.EMTF
        self.assertEqual(
            processing.band_specification_style, BandSpecificationStyleEnum.EMTF
        )

        # Test file path assignment
        processing.band_setup_file = "/path/to/band_setup.cfg"
        self.assertEqual(processing.band_setup_file, "/path/to/band_setup.cfg")

    def test_enum_string_assignment(self):
        """Test assigning enum via string (should convert automatically)."""
        processing = Processing()

        # String assignment should convert to enum
        processing.band_specification_style = "band_edges"
        self.assertEqual(
            processing.band_specification_style, BandSpecificationStyleEnum.band_edges
        )

        # None assignment should work
        processing.band_specification_style = None
        self.assertIsNone(processing.band_specification_style)

    def test_from_dict_creation(self):
        """Test creating Processing instance from dictionary."""
        data = {
            "id": "dict_test_config",
            "band_specification_style": "EMTF",
            "band_setup_file": "/test/path/setup.cfg",
        }

        processing = Processing.model_validate(data)

        self.assertEqual(processing.id, "dict_test_config")
        self.assertEqual(
            processing.band_specification_style, BandSpecificationStyleEnum.EMTF
        )
        self.assertEqual(processing.band_setup_file, "/test/path/setup.cfg")


class TestProcessingValidation(unittest.TestCase):
    """Test Processing field validation."""

    def test_invalid_enum_assignment(self):
        """Test that invalid enum values raise errors."""
        processing = Processing()

        # Invalid string should raise error
        with self.assertRaises((ValueError, TypeError)):
            processing.band_specification_style = "invalid_enum_value"

        # Invalid type should raise error
        with self.assertRaises((ValueError, TypeError)):
            processing.band_specification_style = 12345


class TestProcessingDecimations(unittest.TestCase):
    """Test decimation-related functionality."""

    def test_empty_decimations_default(self):
        """Test that default decimations list is empty."""
        processing = Processing()
        self.assertEqual(len(processing.decimations), 0)
        self.assertIsInstance(processing.decimations, list)

    def test_num_decimation_levels_property(self):
        """Test num_decimation_levels computed property."""
        processing = Processing()
        self.assertEqual(processing.num_decimation_levels, 0)

        # Add a decimation level manually
        decimation = DecimationLevel()
        processing.decimations.append(decimation)
        self.assertEqual(processing.num_decimation_levels, 1)

    def test_decimations_dict_property(self):
        """Test decimations_dict computed property."""
        processing = Processing()
        decimations_dict = processing.decimations_dict

        self.assertIsInstance(decimations_dict, dict)
        self.assertEqual(len(decimations_dict), 0)


class TestProcessingUtilities(unittest.TestCase):
    """Test utility methods of Processing class."""

    def test_json_filename_generation(self):
        """Test JSON filename generation."""
        processing = Processing()
        processing.id = "my_config"

        expected_filename = "my_config_processing_config.json"
        self.assertEqual(processing.json_fn(), expected_filename)

    def test_json_filename_empty_id(self):
        """Test JSON filename with empty ID."""
        processing = Processing()
        # Empty ID should still generate valid filename
        expected_filename = "_processing_config.json"
        self.assertEqual(processing.json_fn(), expected_filename)

    def test_channel_management_methods(self):
        """Test channel management methods work without errors."""
        processing = Processing()

        # These should work without error even with empty decimations
        processing.drop_reference_channels()
        processing.set_input_channels(["ex", "ey"])
        processing.set_output_channels(["hx", "hy", "hz"])
        processing.set_reference_channels(["rrhx", "rrhy"])

        # Should not have added any decimations
        self.assertEqual(len(processing.decimations), 0)


class TestProcessingSerialization(unittest.TestCase):
    """Test JSON serialization and deserialization."""

    def test_json_serialization_roundtrip(self):
        """Test JSON serialization and deserialization preserves data."""
        # Create and populate a Processing instance
        processing = Processing()
        processing.id = "serialization_test"
        processing.band_specification_style = BandSpecificationStyleEnum.band_edges
        processing.band_setup_file = "/test/serialization/path.cfg"

        # Serialize to JSON
        json_str = processing.model_dump_json()
        self.assertIsInstance(json_str, str)
        self.assertIn("serialization_test", json_str)

        # Deserialize from JSON
        processing_restored = Processing.model_validate_json(json_str)

        # Verify data integrity
        self.assertEqual(processing_restored.id, "serialization_test")
        self.assertEqual(
            processing_restored.band_specification_style,
            BandSpecificationStyleEnum.band_edges,
        )
        self.assertEqual(
            processing_restored.band_setup_file, "/test/serialization/path.cfg"
        )

    def test_dict_conversion(self):
        """Test dictionary conversion."""
        processing = Processing()
        processing.id = "dict_conversion_test"
        processing.band_specification_style = BandSpecificationStyleEnum.EMTF

        # Convert to dictionary
        processing_dict = processing.model_dump()

        self.assertIsInstance(processing_dict, dict)
        self.assertIn("id", processing_dict)
        self.assertIn("decimations", processing_dict)
        self.assertEqual(processing_dict["id"], "dict_conversion_test")

    def test_minimal_dict_creation(self):
        """Test creating Processing from minimal dictionary."""
        minimal_data = {"id": "minimal_test"}

        processing = Processing.model_validate(minimal_data)

        self.assertEqual(processing.id, "minimal_test")
        self.assertIsNone(processing.band_specification_style)
        self.assertEqual(len(processing.decimations), 0)


def main():
    """Run all tests with detailed output."""
    print("=" * 70)
    print("PROCESSING BASEMODEL TEST SUITE")
    print("=" * 70)
    print()
    print("Testing Processing class and BandSpecificationStyleEnum functionality")
    print("This comprehensive test suite covers:")
    print("  • Enum functionality and validation")
    print("  • Processing instantiation and field assignment")
    print("  • Validation and error handling")
    print("  • Decimation level management")
    print("  • Utility methods and properties")
    print("  • JSON serialization/deserialization")
    print()
    print("=" * 70)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestBandSpecificationStyleEnum,
        TestProcessingBasics,
        TestProcessingValidation,
        TestProcessingDecimations,
        TestProcessingUtilities,
        TestProcessingSerialization,
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(test_suite)

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED!")
        print(
            "\nThe Processing class and BandSpecificationStyleEnum are working correctly."
        )
        print("Core functionality includes:")
        print("  ✓ Enum string inheritance and validation")
        print("  ✓ Processing instantiation with defaults")
        print("  ✓ Field assignment and validation")
        print("  ✓ Dictionary and JSON serialization")
        print("  ✓ Utility methods and properties")
        print("  ✓ Error handling for invalid inputs")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Check the output above for details.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
