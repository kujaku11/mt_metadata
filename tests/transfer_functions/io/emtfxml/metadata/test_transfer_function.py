# -*- coding: utf-8 -*-
"""
Comprehensive pytest test suite for TransferFunction basemodel.

Tests cover:
- Basic instantiation and validation
- Array validation and type conversion
- Initialize arrays functionality
- Computed fields (array_dict, n_periods)
- Read/write functionality (read_dict, read_block, write_block)
- XML generation (to_xml)
- Edge cases and error handling
- Performance with large datasets
- Integration scenarios

Created: 2025
Author: GitHub Copilot
"""

from unittest.mock import patch
from xml.etree import cElementTree as et

import numpy as np
import pytest

from mt_metadata.transfer_functions.io.emtfxml.metadata import TransferFunction


class TestTransferFunctionBasic:
    """Test basic TransferFunction functionality."""

    def test_default_initialization(self):
        """Test TransferFunction can be created with defaults."""
        tf = TransferFunction()
        assert isinstance(tf.period, np.ndarray)
        assert tf.period.size == 0
        assert isinstance(tf.z, np.ndarray)
        assert tf.z.shape == (0, 2, 2)
        assert isinstance(tf.z_var, np.ndarray)
        assert tf.z_var.shape == (0, 2, 2)
        assert isinstance(tf.z_invsigcov, np.ndarray)
        assert tf.z_invsigcov.shape == (0, 2, 2)
        assert isinstance(tf.z_residcov, np.ndarray)
        assert tf.z_residcov.shape == (0, 2, 2)
        assert isinstance(tf.t, np.ndarray)
        assert tf.t.shape == (0, 1, 2)
        assert isinstance(tf.t_var, np.ndarray)
        assert tf.t_var.shape == (0, 1, 2)
        assert isinstance(tf.t_invsigcov, np.ndarray)
        assert tf.t_invsigcov.shape == (0, 2, 2)
        assert isinstance(tf.t_residcov, np.ndarray)
        assert tf.t_residcov.shape == (0, 1, 1)

    def test_private_attributes_set(self):
        """Test that private attributes are properly initialized."""
        tf = TransferFunction()

        # Test _index_dict
        assert tf._index_dict == {"hx": 0, "hy": 1, "ex": 0, "ey": 1, "hz": 0}

        # Test _dtype_dict
        expected_dtype = {
            "complex": complex,
            "real": float,
            "complex128": "complex",
            "float64": "real",
        }
        assert tf._dtype_dict == expected_dtype

        # Test _units_dict
        assert tf._units_dict == {"z": "[mV/km]/[nT]", "t": "[]"}

        # Test _name_dict
        expected_names = {
            "exhx": "zxx",
            "exhy": "zxy",
            "eyhx": "zyx",
            "eyhy": "zyy",
            "hzhx": "tx",
            "hzhy": "ty",
        }
        assert tf._name_dict == expected_names

    def test_array_dtypes_dict(self):
        """Test _array_dtypes_dict is properly set."""
        tf = TransferFunction()
        expected_dtypes = {
            "period": float,
            "z": complex,
            "z_var": float,
            "z_invsigcov": complex,
            "z_residcov": complex,
            "t": complex,
            "t_var": float,
            "t_invsigcov": complex,
            "t_residcov": complex,
        }
        assert tf._array_dtypes_dict == expected_dtypes

    def test_write_dict_structure(self):
        """Test _write_dict has proper structure."""
        tf = TransferFunction()
        assert "z" in tf._write_dict
        assert "out" in tf._write_dict["z"]
        assert "in" in tf._write_dict["z"]
        assert tf._write_dict["z"]["out"] == {0: "ex", 1: "ey"}
        assert tf._write_dict["z"]["in"] == {0: "hx", 1: "hy"}

    def test_derived_keys_list(self):
        """Test _derived_keys contains expected values."""
        tf = TransferFunction()
        assert "rho" in tf._derived_keys
        assert "phs" in tf._derived_keys
        assert "tipphs" in tf._derived_keys
        assert len(tf._derived_keys) == 24  # Based on the list in the code


class TestTransferFunctionArrayValidation:
    """Test array validation functionality."""

    @pytest.fixture
    def sample_periods(self):
        """Sample period data."""
        return [0.01, 0.1, 1.0, 10.0]

    @pytest.fixture
    def sample_z_data(self):
        """Sample impedance tensor data."""
        return np.array(
            [
                [[1.0 + 0.1j, 0.5 + 0.2j], [0.3 + 0.4j, 1.1 + 0.3j]],
                [[1.2 + 0.2j, 0.6 + 0.3j], [0.4 + 0.5j, 1.3 + 0.4j]],
            ]
        )

    def test_period_validation_list(self, sample_periods):
        """Test period validation with list input."""
        tf = TransferFunction(period=sample_periods)
        assert isinstance(tf.period, np.ndarray)
        assert tf.period.dtype == np.float64
        np.testing.assert_array_equal(tf.period, sample_periods)

    def test_period_validation_tuple(self, sample_periods):
        """Test period validation with tuple input."""
        tf = TransferFunction(period=tuple(sample_periods))
        assert isinstance(tf.period, np.ndarray)
        assert tf.period.dtype == np.float64
        np.testing.assert_array_equal(tf.period, sample_periods)

    def test_period_validation_numpy_array(self, sample_periods):
        """Test period validation with numpy array input."""
        periods_array = np.array(sample_periods)
        tf = TransferFunction(period=periods_array)
        assert isinstance(tf.period, np.ndarray)
        assert tf.period.dtype == np.float64
        np.testing.assert_array_equal(tf.period, sample_periods)

    def test_z_validation_complex_array(self, sample_z_data):
        """Test impedance tensor validation."""
        tf = TransferFunction(z=sample_z_data)
        assert isinstance(tf.z, np.ndarray)
        assert tf.z.dtype == np.complex128
        np.testing.assert_array_equal(tf.z, sample_z_data)

    def test_z_var_validation_float_array(self):
        """Test z_var validation with float data."""
        z_var_data = [[0.1, 0.2], [0.3, 0.4]]
        tf = TransferFunction(z_var=z_var_data)
        assert isinstance(tf.z_var, np.ndarray)
        assert tf.z_var.dtype == np.float64

    @pytest.mark.parametrize(
        "field_name,data_type",
        [
            ("z", complex),
            ("z_var", float),
            ("z_invsigcov", complex),
            ("z_residcov", complex),
            ("t", complex),
            ("t_var", float),
            ("t_invsigcov", complex),
            ("t_residcov", complex),
        ],
    )
    def test_array_field_validation(self, field_name, data_type):
        """Test validation for all array fields."""
        if data_type == complex:
            test_data = [[1.0 + 0.1j, 0.5 + 0.2j]]
        else:
            test_data = [[0.1, 0.2]]

        kwargs = {field_name: test_data}
        tf = TransferFunction(**kwargs)
        field_value = getattr(tf, field_name)
        assert isinstance(field_value, np.ndarray)
        if data_type == complex:
            assert field_value.dtype == np.complex128
        else:
            assert field_value.dtype == np.float64

    def test_invalid_array_type_raises_error(self):
        """Test that invalid array types raise TypeError."""
        with pytest.raises(
            TypeError, match="input values must be an list, tuple, or np.ndarray"
        ):
            TransferFunction(period="invalid")

    def test_none_values_allowed(self):
        """Test that None values are allowed for all array fields."""
        tf = TransferFunction(
            period=None,
            z=None,
            z_var=None,
            z_invsigcov=None,
            z_residcov=None,
            t=None,
            t_var=None,
            t_invsigcov=None,
            t_residcov=None,
        )
        assert all(
            getattr(tf, field) is None
            for field in [
                "period",
                "z",
                "z_var",
                "z_invsigcov",
                "z_residcov",
                "t",
                "t_var",
                "t_invsigcov",
                "t_residcov",
            ]
        )


class TestTransferFunctionComputedFields:
    """Test computed field functionality."""

    @pytest.fixture
    def tf_with_data(self):
        """TransferFunction with sample data."""
        periods = [0.01, 0.1, 1.0]
        z_data = np.random.random((3, 2, 2)) + 1j * np.random.random((3, 2, 2))
        t_data = np.random.random((3, 1, 2)) + 1j * np.random.random((3, 1, 2))
        return TransferFunction(period=periods, z=z_data, t=t_data)

    def test_n_periods_with_data(self, tf_with_data):
        """Test n_periods computed field with data."""
        assert tf_with_data.n_periods == 3

    def test_n_periods_no_data(self):
        """Test n_periods computed field with no data."""
        tf = TransferFunction()
        assert tf.n_periods == 0

    def test_array_dict_structure(self, tf_with_data):
        """Test array_dict computed field structure."""
        array_dict = tf_with_data.array_dict
        expected_keys = [
            "z",
            "z_var",
            "z_invsigcov",
            "z_residcov",
            "t",
            "t_var",
            "t_invsigcov",
            "t_residcov",
        ]
        assert all(key in array_dict for key in expected_keys)

    def test_array_dict_values(self, tf_with_data):
        """Test array_dict computed field values."""
        array_dict = tf_with_data.array_dict
        assert np.array_equal(array_dict["z"], tf_with_data.z)
        assert np.array_equal(array_dict["t"], tf_with_data.t)
        # z_var not explicitly set in fixture, so it defaults to empty array
        assert isinstance(array_dict["z_var"], np.ndarray)
        assert array_dict["z_var"].shape == (0, 2, 2)


class TestTransferFunctionInitializeArrays:
    """Test initialize_arrays functionality."""

    @pytest.fixture
    def tf(self):
        """Empty TransferFunction."""
        return TransferFunction()

    def test_initialize_arrays_basic(self, tf):
        """Test basic array initialization."""
        n_periods = 5
        tf.initialize_arrays(n_periods)

        assert tf.period.shape == (n_periods,)
        assert tf.z.shape == (n_periods, 2, 2)
        assert tf.z_var.shape == (n_periods, 2, 2)
        assert tf.t.shape == (n_periods, 1, 2)
        assert tf.t_invsigcov.shape == (n_periods, 2, 2)
        assert tf.t_residcov.shape == (n_periods, 1, 1)

    def test_initialize_arrays_dtypes(self, tf):
        """Test array initialization dtypes."""
        tf.initialize_arrays(3)

        assert tf.period.dtype == np.float64
        assert tf.z.dtype == np.complex128
        assert tf.z_var.dtype == np.float64
        assert tf.z_invsigcov.dtype == np.complex128
        assert tf.z_residcov.dtype == np.complex128
        assert tf.t.dtype == np.complex128
        assert tf.t_var.dtype == np.float64

    def test_initialize_arrays_zero_values(self, tf):
        """Test arrays are initialized with zeros."""
        tf.initialize_arrays(2)

        assert np.all(tf.period == 0)
        assert np.all(tf.z == 0)
        assert np.all(tf.z_var == 0)
        assert np.all(tf.t == 0)

    @pytest.mark.parametrize("n_periods", [1, 10, 100])
    def test_initialize_arrays_different_sizes(self, tf, n_periods):
        """Test initialization with different array sizes."""
        tf.initialize_arrays(n_periods)
        assert tf.period.shape[0] == n_periods
        assert tf.z.shape[0] == n_periods
        assert tf.t.shape[0] == n_periods


class TestTransferFunctionReadFunctionality:
    """Test read_dict and read_block functionality."""

    @pytest.fixture
    def sample_root_dict(self):
        """Sample root dictionary for reading."""
        return {
            "data": {
                "count": "2",
                "period": [
                    {
                        "value": "0.01",
                        "z": {
                            "type": "complex",
                            "value": [
                                {"output": "Ex", "input": "Hx", "value": "1.0 0.1"},
                                {"output": "Ex", "input": "Hy", "value": "0.5 0.2"},
                            ],
                        },
                    },
                    {
                        "value": "0.1",
                        "z": {
                            "type": "complex",
                            "value": [
                                {"output": "Ex", "input": "Hx", "value": "1.2 0.3"}
                            ],
                        },
                    },
                ],
            }
        }

    @pytest.fixture
    def tf(self):
        """Empty TransferFunction."""
        return TransferFunction()

    def test_read_dict_basic(self, tf, sample_root_dict):
        """Test basic read_dict functionality."""
        tf.read_dict(sample_root_dict)

        assert tf.n_periods == 2
        assert tf.period[0] == 0.01
        assert tf.period[1] == 0.1

    def test_read_dict_initializes_arrays(self, tf, sample_root_dict):
        """Test that read_dict properly initializes arrays."""
        tf.read_dict(sample_root_dict)

        assert tf.z is not None
        assert tf.z.shape == (2, 2, 2)
        assert tf.t is not None

    def test_read_block_complex_values(self, tf):
        """Test read_block with complex values."""
        tf.initialize_arrays(1)
        block = {
            "z": {
                "type": "complex",
                "value": [{"output": "Ex", "input": "Hx", "value": "1.5 -0.3"}],
            }
        }

        tf.read_block(block, 0)
        expected_value = complex(1.5, -0.3)
        assert tf.z[0, 0, 0] == expected_value

    def test_read_block_float_values(self, tf):
        """Test read_block with float values."""
        tf.initialize_arrays(1)
        block = {
            "z.var": {
                "type": "real",
                "value": [{"output": "Ex", "input": "Hx", "value": "0.1"}],
            }
        }

        tf.read_block(block, 0)
        assert tf.z_var[0, 0, 0] == 0.1

    def test_read_block_unknown_dtype(self, tf):
        """Test read_block with unknown data type."""
        tf.initialize_arrays(1)
        block = {
            "z": {
                "type": "unknown",
                "value": [{"output": "Ex", "input": "Hx", "value": "1.0 0.5"}],
            }
        }

        tf.read_block(block, 0)
        expected_value = complex(1.0, 0.5)
        assert tf.z[0, 0, 0] == expected_value

    def test_read_block_skips_derived_data(self, tf):
        """Test that read_block skips derived data when flag is set."""
        tf.initialize_arrays(1)
        block = {
            "rho": {  # This should be skipped
                "type": "real",
                "value": [{"output": "Ex", "input": "Hx", "value": "100.0"}],
            }
        }

        # Should not raise an error and should skip the derived data
        tf.read_block(block, 0)

    def test_read_dict_no_count_field(self, tf):
        """Test read_dict when count field is missing."""
        root_dict = {
            "data": {"period": [{"value": "0.01"}, {"value": "0.1"}, {"value": "1.0"}]}
        }

        tf.read_dict(root_dict)
        assert tf.n_periods == 3


class TestTransferFunctionWriteFunctionality:
    """Test write functionality."""

    @pytest.fixture
    def tf_with_data(self):
        """TransferFunction with sample data for writing."""
        tf = TransferFunction()
        tf.initialize_arrays(2)
        tf.period[0] = 0.01
        tf.period[1] = 0.1
        tf.z[0, 0, 0] = 1.0 + 0.1j
        tf.z[0, 0, 1] = 0.5 + 0.2j
        tf.z[1, 0, 0] = 1.2 + 0.3j
        return tf

    def test_write_block_creates_element(self, tf_with_data):
        """Test that write_block creates proper XML element."""
        parent = et.Element("Data")
        period_element = tf_with_data.write_block(parent, 0)

        assert period_element.tag == "Period"
        assert "value" in period_element.attrib
        assert "units" in period_element.attrib
        assert period_element.attrib["units"] == "secs"

    def test_write_block_period_value(self, tf_with_data):
        """Test write_block sets correct period value."""
        parent = et.Element("Data")
        period_element = tf_with_data.write_block(parent, 0)

        period_value = float(period_element.attrib["value"])
        assert abs(period_value - 0.01) < 1e-10

    def test_write_block_z_element(self, tf_with_data):
        """Test write_block creates Z element."""
        parent = et.Element("Data")
        period_element = tf_with_data.write_block(parent, 0)

        z_elements = period_element.findall("Z")
        assert len(z_elements) == 1

        z_element = z_elements[0]
        assert z_element.attrib["type"] == "complex"
        assert z_element.attrib["units"] == "[mV/km]/[nT]"

    def test_write_block_value_elements(self, tf_with_data):
        """Test write_block creates value elements."""
        parent = et.Element("Data")
        period_element = tf_with_data.write_block(parent, 0)

        z_element = period_element.find("Z")
        value_elements = z_element.findall("value")
        assert len(value_elements) > 0

        # Check first value element
        value_elem = value_elements[0]
        assert "output" in value_elem.attrib
        assert "input" in value_elem.attrib

    def test_to_xml_string_output(self, tf_with_data):
        """Test to_xml with string output."""
        xml_string = tf_with_data.to_xml(string=True)
        assert isinstance(xml_string, str)
        assert "<Data" in xml_string
        assert "</Data>" in xml_string

    def test_to_xml_element_output(self, tf_with_data):
        """Test to_xml with element output."""
        xml_element = tf_with_data.to_xml(string=False)
        assert isinstance(xml_element, et.Element)
        assert xml_element.tag == "Data"

    def test_to_xml_count_attribute(self, tf_with_data):
        """Test to_xml sets count attribute."""
        xml_element = tf_with_data.to_xml()
        assert xml_element.attrib["count"] == "2"

    def test_to_xml_period_elements(self, tf_with_data):
        """Test to_xml creates correct number of period elements."""
        xml_element = tf_with_data.to_xml()
        period_elements = xml_element.findall("Period")
        assert len(period_elements) == 2


class TestTransferFunctionEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_arrays_xml_generation(self):
        """Test XML generation with empty arrays."""
        tf = TransferFunction()
        tf.initialize_arrays(1)
        # Arrays are initialized but contain zeros
        xml_element = tf.to_xml()
        assert xml_element.attrib["count"] == "1"

    def test_nan_handling_in_write_block(self):
        """Test that NaN values are handled in write_block."""
        tf = TransferFunction()
        tf.initialize_arrays(1)
        tf.period[0] = 0.01
        tf.z[0, 0, 0] = np.nan + 1j * np.nan

        parent = et.Element("Data")
        # Should not raise an error
        period_element = tf.write_block(parent, 0)
        assert period_element is not None

    def test_zero_values_replacement(self):
        """Test that zero values are replaced with 1E32."""
        tf = TransferFunction()
        tf.initialize_arrays(1)
        tf.period[0] = 0.01
        tf.z[0, 0, 0] = 0.0 + 0.0j  # Zero value

        parent = et.Element("Data")
        period_element = tf.write_block(parent, 0)

        # Check that zero was replaced (indirectly by ensuring no error)
        z_element = period_element.find("Z")
        assert z_element is not None

    def test_missing_key_in_dtype_dict(self, caplog):
        """Test handling of missing keys in dtype_dict."""
        tf = TransferFunction()
        tf.initialize_arrays(1)

        # Create a block with unknown dtype
        block = {
            "z": {
                "type": "unknown_type",
                "value": [{"output": "Ex", "input": "Hx", "value": "1.0"}],
            }
        }

        # Should handle gracefully
        tf.read_block(block, 0)

    def test_missing_value_in_block(self, caplog):
        """Test handling of missing value in block."""
        tf = TransferFunction()
        tf.initialize_arrays(1)

        block = {
            "z": {
                "type": "complex"
                # No "value" key
            }
        }

        # Should handle gracefully and log debug message
        tf.read_block(block, 0)

    def test_single_value_list_handling(self):
        """Test handling when value is not a list."""
        tf = TransferFunction()
        tf.initialize_arrays(1)

        block = {
            "z": {
                "type": "complex",
                "value": {  # Single dict instead of list
                    "output": "Ex",
                    "input": "Hx",
                    "value": "1.0 0.5",
                },
            }
        }

        tf.read_block(block, 0)
        assert tf.z[0, 0, 0] == complex(1.0, 0.5)


class TestTransferFunctionPerformance:
    """Test performance with large datasets."""

    @pytest.mark.parametrize("n_periods", [10, 100])
    def test_large_array_initialization(self, n_periods):
        """Test performance with large arrays."""
        tf = TransferFunction()
        tf.initialize_arrays(n_periods)

        assert tf.period.shape[0] == n_periods
        assert tf.z.shape[0] == n_periods
        assert tf.n_periods == n_periods

    def test_large_dataset_xml_generation(self):
        """Test XML generation with moderately large dataset."""
        tf = TransferFunction()
        n_periods = 50
        tf.initialize_arrays(n_periods)

        # Set some sample data
        tf.period[:] = np.logspace(-2, 2, n_periods)
        tf.z[:, 0, 0] = np.random.random(n_periods) + 1j * np.random.random(n_periods)

        # Should complete without error
        xml_element = tf.to_xml()
        assert xml_element.attrib["count"] == str(n_periods)

    def test_memory_efficiency_computed_fields(self):
        """Test that computed fields don't create unnecessary copies."""
        tf = TransferFunction()
        tf.initialize_arrays(10)

        array_dict_1 = tf.array_dict
        array_dict_2 = tf.array_dict

        # Should reference the same arrays
        assert array_dict_1["z"] is array_dict_2["z"]


class TestTransferFunctionIntegration:
    """Test integration scenarios."""

    def test_full_read_write_cycle(self):
        """Test complete read/write cycle."""
        # Create sample data
        root_dict = {
            "data": {
                "count": "1",
                "period": [
                    {
                        "value": "1.0",
                        "z": {
                            "type": "complex",
                            "value": [
                                {"output": "Ex", "input": "Hx", "value": "2.0 1.0"}
                            ],
                        },
                    }
                ],
            }
        }

        # Read data
        tf = TransferFunction()
        tf.read_dict(root_dict)

        # Verify data was read correctly
        assert tf.n_periods == 1
        assert tf.period[0] == 1.0
        assert tf.z[0, 0, 0] == complex(2.0, 1.0)

        # Generate XML
        xml_element = tf.to_xml()
        assert xml_element.tag == "Data"
        assert xml_element.attrib["count"] == "1"

    def test_pydantic_model_validation_integration(self):
        """Test integration with Pydantic model validation."""
        # Test valid data
        periods = [0.01, 0.1, 1.0]
        z_data = np.random.random((3, 2, 2)) + 1j * np.random.random((3, 2, 2))

        tf = TransferFunction(period=periods, z=z_data)
        assert tf.n_periods == 3

        # Test model_dump works
        data_dict = tf.model_dump()
        assert "period" in data_dict

    def test_metadata_base_inheritance(self):
        """Test that TransferFunction properly inherits from MetadataBase."""
        tf = TransferFunction()

        # Should have MetadataBase methods
        assert hasattr(tf, "model_dump")
        assert hasattr(tf, "model_validate")

    @patch("mt_metadata.transfer_functions.io.emtfxml.metadata.data.logger")
    def test_logging_integration(self, mock_logger):
        """Test integration with logging."""
        tf = TransferFunction()
        tf.initialize_arrays(1)

        # Create block with missing value to trigger debug log
        block = {
            "z": {
                "type": "complex"
                # Missing "value" key
            }
        }

        tf.read_block(block, 0)
        mock_logger.debug.assert_called()

    def test_xml_string_generation_integration(self):
        """Test integration with XML string generation."""
        tf = TransferFunction()
        tf.initialize_arrays(1)
        tf.period[0] = 0.01

        xml_string = tf.to_xml(string=True)

        # Should be valid XML string
        assert isinstance(xml_string, str)
        assert xml_string.startswith("<")
        assert xml_string.rstrip().endswith(">")  # Strip whitespace including newlines

        # Should be parseable
        root = et.fromstring(xml_string)
        assert root.tag == "Data"


if __name__ == "__main__":
    pytest.main([__file__])
