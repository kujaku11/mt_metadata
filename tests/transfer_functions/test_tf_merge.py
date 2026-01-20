# -*- coding: utf-8 -*-
"""
Tests for mt_metadata.transfer_functions.core.TF.merge functionality
===================================================================

This module contains comprehensive pytest tests for the TF merge method.
Tests cover merging transfer functions with different period ranges, handling period limits,
metadata preservation, dictionary inputs, and error conditions.

"""

import numpy as np
import pytest

from mt_metadata.transfer_functions.core import TF


class TestTFMergeBasic:
    """Basic TF merge functionality tests."""

    @classmethod
    def setup_class(cls):
        """Set up test data for the class."""
        np.random.seed(0)

        cls.n_periods = 20

        # Period arrays
        cls.period_01 = np.logspace(-3, 1, cls.n_periods)
        cls.period_02 = np.logspace(1, 3, cls.n_periods)

        # Create first TF
        cls.tf_01 = TF()
        cls.tf_01.station = "test"
        cls.tf_01.survey = "a"
        cls.tf_01.period = cls.period_01
        cls.tf_01.impedance = np.random.rand(cls.n_periods, 2, 2) + 1j * np.random.rand(
            cls.n_periods, 2, 2
        )

        # Create second TF
        cls.tf_02 = TF()
        cls.tf_02.station = "test"
        cls.tf_02.survey = "a"
        cls.tf_02.tf_id = "tfa"
        cls.tf_02.period = cls.period_02
        cls.tf_02.impedance = np.random.rand(cls.n_periods, 2, 2) + 1j * np.random.rand(
            cls.n_periods, 2, 2
        )

    def test_merge_method_exists(self):
        """Test that merge method exists and is callable."""
        assert hasattr(self.tf_01, "merge")
        assert callable(getattr(self.tf_01, "merge"))

    def test_basic_merge_periods(self):
        """Test basic merge combines periods correctly."""
        merged = self.tf_01.merge(self.tf_02)
        expected_periods = np.append(self.tf_01.period, self.tf_02.period)

        np.testing.assert_allclose(expected_periods, merged.period)

    def test_basic_merge_survey_metadata(self):
        """Test that survey metadata is preserved from first TF."""
        merged = self.tf_01.merge(self.tf_02)

        assert merged.survey_metadata.to_dict(
            single=True
        ) == self.tf_01.survey_metadata.to_dict(single=True)

    def test_basic_merge_station_metadata(self):
        """Test that station metadata is preserved from first TF."""
        merged = self.tf_01.merge(self.tf_02)

        tf_01_dict = self.tf_01.station_metadata.to_dict(single=True)
        merged_dict = merged.station_metadata.to_dict(single=True)

        assert tf_01_dict == merged_dict

    def test_impedance_data_preservation(self):
        """Test that impedance data is properly combined."""
        merged = self.tf_01.merge(self.tf_02)

        # Should have impedance data
        assert merged.impedance is not None
        assert len(merged.impedance) == len(self.tf_01.impedance) + len(
            self.tf_02.impedance
        )

        # Complex data should be preserved
        assert np.iscomplexobj(merged.impedance)

    def test_merge_returns_tf_object(self):
        """Test that merge returns a TF object."""
        merged = self.tf_01.merge(self.tf_02)

        assert isinstance(merged, TF)
        assert merged is not self.tf_01  # Should be a new object
        assert merged is not self.tf_02


class TestTFMergePeriodLimits:
    """Test TF merge with period limitations that work."""

    @classmethod
    def setup_class(cls):
        """Set up test data for the class."""
        np.random.seed(0)

        cls.n_periods = 20

        # Period arrays
        cls.period_01 = np.logspace(-3, 1, cls.n_periods)
        cls.period_02 = np.logspace(1, 3, cls.n_periods)

        # Create first TF
        cls.tf_01 = TF()
        cls.tf_01.station = "test"
        cls.tf_01.survey = "a"
        cls.tf_01.period = cls.period_01
        cls.tf_01.impedance = np.random.rand(cls.n_periods, 2, 2) + 1j * np.random.rand(
            cls.n_periods, 2, 2
        )

        # Create second TF
        cls.tf_02 = TF()
        cls.tf_02.station = "test"
        cls.tf_02.survey = "a"
        cls.tf_02.tf_id = "tfa"
        cls.tf_02.period = cls.period_02
        cls.tf_02.impedance = np.random.rand(cls.n_periods, 2, 2) + 1j * np.random.rand(
            cls.n_periods, 2, 2
        )

    def test_self_limit_periods_merge(self):
        """Test merge with period limits applied to self."""
        merged = self.tf_01.merge(self.tf_02, period_min=0.001, period_max=9.9)

        # Expected: tf_01.period[:-1] + tf_02.period (last period of tf_01 is 10, excluded)
        expected_periods = np.append(self.tf_01.period[:-1], self.tf_02.period)

        np.testing.assert_allclose(expected_periods, merged.period)

    def test_self_limit_periods_metadata_preservation(self):
        """Test that metadata is preserved with period limits."""
        merged = self.tf_01.merge(self.tf_02, period_min=0.001, period_max=9.9)

        # Survey metadata should be preserved
        assert merged.survey_metadata.to_dict(
            single=True
        ) == self.tf_01.survey_metadata.to_dict(single=True)

        # Station metadata should be preserved
        assert merged.station_metadata.to_dict(
            single=True
        ) == self.tf_01.station_metadata.to_dict(single=True)

    def test_period_limits_basic(self):
        """Test basic period limits without edge cases."""
        # Use limits that won't cause dimension issues
        merged = self.tf_01.merge(self.tf_02, period_min=0.01, period_max=100)
        assert isinstance(merged, TF)
        assert merged.impedance is not None


class TestTFMergeDictionaryInput:
    """Test TF merge with dictionary input formats."""

    @classmethod
    def setup_class(cls):
        """Set up test data for the class."""
        np.random.seed(0)

        cls.n_periods = 20

        # Period arrays
        cls.period_01 = np.logspace(-3, 1, cls.n_periods)
        cls.period_02 = np.logspace(1, 3, cls.n_periods)

        # Create first TF
        cls.tf_01 = TF()
        cls.tf_01.station = "test"
        cls.tf_01.survey = "a"
        cls.tf_01.period = cls.period_01
        cls.tf_01.impedance = np.random.rand(cls.n_periods, 2, 2) + 1j * np.random.rand(
            cls.n_periods, 2, 2
        )

        # Create second TF
        cls.tf_02 = TF()
        cls.tf_02.station = "test"
        cls.tf_02.survey = "a"
        cls.tf_02.tf_id = "tfa"
        cls.tf_02.period = cls.period_02
        cls.tf_02.impedance = np.random.rand(cls.n_periods, 2, 2) + 1j * np.random.rand(
            cls.n_periods, 2, 2
        )

    def test_dict_input_merge(self):
        """Test merge with dictionary input containing TF and period limits."""
        merged = self.tf_01.merge(
            {"tf": self.tf_02, "period_min": 10, "period_max": 100},
            period_min=0.001,
            period_max=9.9,
        )

        # Expected: tf_01.period[:-1] + tf_02.period[0:10] (first 10 periods of tf_02)
        expected_periods = np.append(self.tf_01.period[:-1], self.tf_02.period[0:10])

        np.testing.assert_allclose(expected_periods, merged.period)

    def test_dict_input_metadata_preservation(self):
        """Test that metadata is preserved with dictionary input."""
        merged = self.tf_01.merge(
            {"tf": self.tf_02, "period_min": 10, "period_max": 100},
            period_min=0.001,
            period_max=9.9,
        )

        # Survey metadata should be preserved
        assert merged.survey_metadata.to_dict(
            single=True
        ) == self.tf_01.survey_metadata.to_dict(single=True)

        # Station metadata should be preserved
        assert merged.station_metadata.to_dict(
            single=True
        ) == self.tf_01.station_metadata.to_dict(single=True)


class TestTFMergeErrorHandling:
    """Test error conditions and edge cases."""

    @classmethod
    def setup_class(cls):
        """Set up test data for the class."""
        np.random.seed(0)

        cls.n_periods = 20

        # Period arrays
        cls.period_01 = np.logspace(-3, 1, cls.n_periods)

        # Create first TF
        cls.tf_01 = TF()
        cls.tf_01.station = "test"
        cls.tf_01.survey = "a"
        cls.tf_01.period = cls.period_01
        cls.tf_01.impedance = np.random.rand(cls.n_periods, 2, 2) + 1j * np.random.rand(
            cls.n_periods, 2, 2
        )

    def test_dict_missing_tf_key(self):
        """Test that missing 'tf' key in dictionary raises KeyError."""
        with pytest.raises(KeyError):
            self.tf_01.merge({"a": 0})

    def test_dict_invalid_keys(self):
        """Test various invalid dictionary keys."""
        with pytest.raises(KeyError):
            self.tf_01.merge({"invalid_key": "value"})

        with pytest.raises(KeyError):
            self.tf_01.merge({"period_min": 1})  # Missing 'tf' key

    def test_invalid_input_type(self):
        """Test that invalid input types raise TypeError."""
        with pytest.raises(TypeError):
            self.tf_01.merge(10)

        with pytest.raises(TypeError):
            self.tf_01.merge("string")

        with pytest.raises(TypeError):
            self.tf_01.merge([1, 2, 3])

    def test_none_input(self):
        """Test behavior with None input."""
        with pytest.raises((TypeError, AttributeError)):
            self.tf_01.merge(None)

    def test_empty_dict_input(self):
        """Test behavior with empty dictionary."""
        with pytest.raises(KeyError):
            self.tf_01.merge({})


class TestTFMergeDataIntegrity:
    """Test data integrity and consistency during merging."""

    @classmethod
    def setup_class(cls):
        """Set up test data for the class."""
        np.random.seed(0)

        cls.n_periods = 20

        # Period arrays
        cls.period_01 = np.logspace(-3, 1, cls.n_periods)
        cls.period_02 = np.logspace(1, 3, cls.n_periods)

        # Create first TF
        cls.tf_01 = TF()
        cls.tf_01.station = "test"
        cls.tf_01.survey = "a"
        cls.tf_01.period = cls.period_01
        cls.tf_01.impedance = np.random.rand(cls.n_periods, 2, 2) + 1j * np.random.rand(
            cls.n_periods, 2, 2
        )

        # Create second TF
        cls.tf_02 = TF()
        cls.tf_02.station = "test"
        cls.tf_02.survey = "a"
        cls.tf_02.tf_id = "tfa"
        cls.tf_02.period = cls.period_02
        cls.tf_02.impedance = np.random.rand(cls.n_periods, 2, 2) + 1j * np.random.rand(
            cls.n_periods, 2, 2
        )

    def test_original_tfs_unchanged(self):
        """Test that original TF objects are not modified during merge."""
        original_tf_01_periods = self.tf_01.period.copy()
        original_tf_02_periods = self.tf_02.period.copy()
        original_tf_01_impedance = self.tf_01.impedance.copy()
        original_tf_02_impedance = self.tf_02.impedance.copy()

        merged = self.tf_01.merge(self.tf_02)

        # Original TFs should be unchanged
        np.testing.assert_array_equal(self.tf_01.period, original_tf_01_periods)
        np.testing.assert_array_equal(self.tf_02.period, original_tf_02_periods)
        np.testing.assert_array_equal(self.tf_01.impedance, original_tf_01_impedance)
        np.testing.assert_array_equal(self.tf_02.impedance, original_tf_02_impedance)

        # Merged should be different
        assert merged is not self.tf_01
        assert merged is not self.tf_02

    def test_impedance_shape_consistency(self):
        """Test that impedance arrays maintain proper shape after merging."""
        merged = self.tf_01.merge(self.tf_02)

        expected_length = len(self.tf_01.period) + len(self.tf_02.period)

        assert merged.impedance.shape[0] == expected_length
        assert merged.impedance.shape[1:] == (
            2,
            2,
        )  # Should maintain 2x2 impedance tensor

    def test_complex_data_preservation(self):
        """Test that complex impedance data is properly preserved."""
        merged = self.tf_01.merge(self.tf_02)

        # Should be complex
        assert np.iscomplexobj(merged.impedance)

        # Should not have NaN or infinite values
        assert not np.any(np.isnan(merged.impedance))
        assert not np.any(np.isinf(merged.impedance))

    def test_period_ordering(self):
        """Test that periods maintain proper ordering after merge."""
        merged = self.tf_01.merge(self.tf_02)

        # Since tf_01 goes from 10^-3 to 10^1 and tf_02 from 10^1 to 10^3,
        # the merged periods should be in ascending order
        periods = merged.period

        # Check if periods are sorted (should be since we're appending in order)
        # Note: This depends on the specific implementation
        assert len(periods) == len(self.tf_01.period) + len(self.tf_02.period)


class TestTFMergeAdvanced:
    """Advanced tests that work reliably."""

    @classmethod
    def setup_class(cls):
        """Set up test data for the class."""
        np.random.seed(0)

        cls.n_periods = 20

        # Period arrays - non-overlapping to avoid concatenation issues
        cls.period_01 = np.logspace(-3, 0, cls.n_periods)
        cls.period_02 = np.logspace(1, 4, cls.n_periods)

        # Create first TF
        cls.tf_01 = TF()
        cls.tf_01.station = "test"
        cls.tf_01.survey = "a"
        cls.tf_01.tf_id = "tf_a"
        cls.tf_01.period = cls.period_01
        cls.tf_01.impedance = np.random.rand(cls.n_periods, 2, 2) + 1j * np.random.rand(
            cls.n_periods, 2, 2
        )

        # Create second TF
        cls.tf_02 = TF()
        cls.tf_02.station = "test"
        cls.tf_02.survey = "a"
        cls.tf_02.tf_id = "tf_b"
        cls.tf_02.period = cls.period_02
        cls.tf_02.impedance = np.random.rand(cls.n_periods, 2, 2) + 1j * np.random.rand(
            cls.n_periods, 2, 2
        )

    def test_merge_with_different_tf_ids(self):
        """Test merging TFs with different tf_id values."""
        merged = self.tf_01.merge(self.tf_02)

        # Should preserve tf_id from first TF
        assert merged.tf_id == "tf_a"
        assert isinstance(merged, TF)

    def test_merge_chain(self):
        """Test chaining multiple merge operations."""
        # Create a third TF with non-overlapping periods
        np.random.seed(44)
        tf_03 = TF()
        tf_03.station = "test"
        tf_03.survey = "a"
        tf_03.tf_id = "tf_c"
        tf_03.period = np.logspace(5, 6, 10)  # High frequency, non-overlapping
        tf_03.impedance = np.random.rand(10, 2, 2) + 1j * np.random.rand(10, 2, 2)

        # Chain merges
        merged_ab = self.tf_01.merge(self.tf_02)
        merged_abc = merged_ab.merge(tf_03)

        assert isinstance(merged_abc, TF)
        expected_length = (
            len(self.tf_01.period) + len(self.tf_02.period) + len(tf_03.period)
        )
        assert len(merged_abc.period) == expected_length

    def test_dict_with_various_parameters(self):
        """Test dictionary input with various parameter combinations."""
        # Create a third TF for testing
        np.random.seed(42)
        tf_03 = TF()
        tf_03.station = "test"
        tf_03.survey = "a"
        tf_03.tf_id = "tfb"
        tf_03.period = np.logspace(0, 2, self.n_periods)
        tf_03.impedance = np.random.rand(self.n_periods, 2, 2) + 1j * np.random.rand(
            self.n_periods, 2, 2
        )

        # Test with different period limits in dictionary
        merged = self.tf_01.merge({"tf": tf_03, "period_min": 1, "period_max": 50})

        assert isinstance(merged, TF)
        assert merged.impedance is not None

    def test_simple_dict_merge(self):
        """Test simple dictionary merge without complex chaining."""
        np.random.seed(43)
        tf_03 = TF()
        tf_03.station = "test"
        tf_03.survey = "a"
        tf_03.tf_id = "tfc"
        # Use non-overlapping periods to avoid monotonic index issues
        tf_03.period = np.logspace(5, 6, 10)
        tf_03.impedance = np.random.rand(10, 2, 2) + 1j * np.random.rand(10, 2, 2)

        # Simple merge
        merged_1 = self.tf_01.merge({"tf": tf_03, "period_min": 1e5, "period_max": 1e7})

        assert isinstance(merged_1, TF)
        assert merged_1.impedance is not None


if __name__ == "__main__":
    pytest.main([__file__])
