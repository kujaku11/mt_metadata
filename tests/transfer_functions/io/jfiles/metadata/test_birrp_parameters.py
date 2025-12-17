# =====================================================
# Imports
# =====================================================
import json
import xml.etree.ElementTree as ET

import pytest

from mt_metadata.base.metadata import MetadataBase
from mt_metadata.transfer_functions.io.jfiles.metadata.birrp_parameters import (
    BirrpParameters,
)


# =====================================================
# Test Classes
# =====================================================
class TestBirrpParametersInstantiation:
    """Test BirrpParameters instantiation and basic functionality."""

    def test_default_instantiation(self):
        """Test default instantiation works."""
        params = BirrpParameters()
        assert isinstance(params, BirrpParameters)
        assert isinstance(params, MetadataBase)

    def test_basic_instantiation(self):
        """Test instantiation with basic parameter values."""
        params = BirrpParameters(
            outputs=2, inputs=2, references=2, tbw=2.0, deltat=1.0, nfft=8192.0
        )
        assert params.outputs == 2
        assert params.inputs == 2
        assert params.references == 2
        assert params.tbw == 2.0
        assert params.deltat == 1.0
        assert params.nfft == 8192.0

    def test_comprehensive_instantiation(self):
        """Test instantiation with all parameters."""
        params = BirrpParameters(
            outputs=2,
            inputs=2,
            references=2,
            tbw=2.0,
            deltat=1.0,
            nfft=8192.0,
            nsctinc=2.0,
            nsctmax=10.0,
            nf1=4,
            nfinc=2,
            nfsect=4,
            uin=0.01,
            ainlin=-999.0,
            ainuin=0.99,
            c2threshe=0.35,
            nz=0,
            c2threshe1=0.35,
            npcs=2,
            nar=5,
            imode=0,
            jmode=0,
            ncomp=5,
        )
        assert params.outputs == 2
        assert params.nfft == 8192.0
        assert params.ainlin == -999.0
        assert params.ncomp == 5

    @pytest.mark.parametrize(
        "field_name,test_value",
        [
            ("outputs", 3),
            ("inputs", 4),
            ("references", 2),
            ("nf1", 8),
            ("nfinc", 4),
            ("nfsect", 16),
            ("nz", 1),
            ("npcs", 10),
            ("nar", 7),
            ("imode", 2),
            ("jmode", 1),
            ("ncomp", 6),
        ],
    )
    def test_integer_field_assignment(self, field_name, test_value):
        """Test assignment of integer fields."""
        params = BirrpParameters()
        setattr(params, field_name, test_value)
        assert getattr(params, field_name) == test_value
        assert isinstance(getattr(params, field_name), int)

    @pytest.mark.parametrize(
        "field_name,test_value",
        [
            ("tbw", 4.0),
            ("deltat", 0.5),
            ("nfft", 16384.0),
            ("nsctinc", 4.0),
            ("nsctmax", 20.0),
            ("uin", 0.05),
            ("ainlin", -500.0),
            ("ainuin", 0.95),
            ("c2threshe", 0.4),
            ("c2threshe1", 0.3),
        ],
    )
    def test_float_field_assignment(self, field_name, test_value):
        """Test assignment of float fields."""
        params = BirrpParameters()
        setattr(params, field_name, test_value)
        assert getattr(params, field_name) == test_value
        assert isinstance(getattr(params, field_name), float)

    def test_inheritance_from_metadata_base(self):
        """Test that BirrpParameters inherits from MetadataBase."""
        params = BirrpParameters()
        assert isinstance(params, MetadataBase)
        assert hasattr(params, "to_dict")
        assert hasattr(params, "from_dict")
        assert hasattr(params, "to_json")
        assert hasattr(params, "to_xml")


class TestFieldValidation:
    """Test field validation and type conversion."""

    @pytest.fixture
    def empty_params(self):
        """Fixture providing empty BirrpParameters instance."""
        return BirrpParameters()

    @pytest.mark.parametrize(
        "field_name,valid_values",
        [
            ("outputs", [1, 2, 3, 5, 10, 100]),
            ("inputs", [1, 2, 4, 8, 16]),
            ("references", [0, 1, 2, 3]),
            ("nf1", [1, 4, 8, 16, 32]),
            ("nfinc", [1, 2, 4]),
            ("nfsect", [1, 4, 8, 16]),
            ("nz", [0, 1]),
            ("npcs", [1, 2, 5, 10, 20]),
            ("nar", [0, 1, 5, 10, 15]),
            ("imode", [0, 1, 2]),
            ("jmode", [0, 1, 2]),
            ("ncomp", [1, 2, 3, 4, 5, 6]),
        ],
    )
    def test_valid_integer_values(self, empty_params, field_name, valid_values):
        """Test valid integer values for each integer field."""
        for value in valid_values:
            setattr(empty_params, field_name, value)
            assert getattr(empty_params, field_name) == value
            assert isinstance(getattr(empty_params, field_name), int)

    @pytest.mark.parametrize(
        "field_name,valid_values",
        [
            ("tbw", [0.0, 1.0, 2.0, 4.0, 8.0, 16.0]),
            ("deltat", [-1.0, -0.5, 0.0, 0.5, 1.0, 2.0]),
            ("nfft", [0.0, 1024.0, 2048.0, 4096.0, 8192.0, 16384.0]),
            ("nsctinc", [0.0, 1.0, 2.0, 4.0, 8.0]),
            ("nsctmax", [0.0, 1.0, 2.0, 10.0, 20.0, 100.0]),
            ("uin", [0.0, 0.01, 0.05, 0.1, 0.5]),
            ("ainlin", [-999.0, -500.0, -100.0, 0.0, 100.0]),
            ("ainuin", [0.0, 0.5, 0.9, 0.95, 0.99, 1.0]),
            ("c2threshe", [0.0, 0.1, 0.25, 0.35, 0.5, 0.8]),
            ("c2threshe1", [0.0, 0.1, 0.25, 0.35, 0.5, 0.8]),
        ],
    )
    def test_valid_float_values(self, empty_params, field_name, valid_values):
        """Test valid float values for each float field."""
        for value in valid_values:
            setattr(empty_params, field_name, value)
            assert getattr(empty_params, field_name) == value
            assert isinstance(getattr(empty_params, field_name), float)

    @pytest.mark.parametrize(
        "field_name,input_val,expected",
        [
            ("outputs", "2", 2),
            ("inputs", "4", 4),
            ("references", "1", 1),
            ("nf1", "8", 8),
            ("nfinc", "2", 2),
            ("nfsect", "16", 16),
            ("nz", "0", 0),
            ("npcs", "10", 10),
            ("nar", "5", 5),
            ("imode", "1", 1),
            ("jmode", "0", 0),
            ("ncomp", "3", 3),
        ],
    )
    def test_integer_string_conversion(
        self, empty_params, field_name, input_val, expected
    ):
        """Test that string values are converted to integers."""
        setattr(empty_params, field_name, input_val)
        assert getattr(empty_params, field_name) == expected
        assert isinstance(getattr(empty_params, field_name), int)

    @pytest.mark.parametrize(
        "field_name,input_val,expected",
        [
            ("tbw", "2.0", 2.0),
            ("deltat", "1.0", 1.0),
            ("nfft", "8192.0", 8192.0),
            ("nsctinc", "4.0", 4.0),
            ("nsctmax", "10.0", 10.0),
            ("uin", "0.01", 0.01),
            ("ainlin", "-999.0", -999.0),
            ("ainuin", "0.99", 0.99),
            ("c2threshe", "0.35", 0.35),
            ("c2threshe1", "0.3", 0.3),
        ],
    )
    def test_float_string_conversion(
        self, empty_params, field_name, input_val, expected
    ):
        """Test that string values are converted to floats."""
        setattr(empty_params, field_name, input_val)
        assert getattr(empty_params, field_name) == expected
        assert isinstance(getattr(empty_params, field_name), float)

    @pytest.mark.parametrize(
        "field_name",
        [
            "outputs",
            "inputs",
            "references",
            "nf1",
            "nfinc",
            "nfsect",
            "nz",
            "npcs",
            "nar",
            "imode",
            "jmode",
            "ncomp",
        ],
    )
    @pytest.mark.parametrize(
        "invalid_val", ["not_a_number", "abc", [1, 2], {"key": "value"}, (1 + 2j)]
    )
    def test_invalid_integer_values_raise_error(
        self, empty_params, field_name, invalid_val
    ):
        """Test that invalid integer values raise ValidationError."""
        with pytest.raises(Exception):  # Could be ValidationError or ValueError
            setattr(empty_params, field_name, invalid_val)

    @pytest.mark.parametrize(
        "field_name",
        [
            "tbw",
            "deltat",
            "nfft",
            "nsctinc",
            "nsctmax",
            "uin",
            "ainlin",
            "ainuin",
            "c2threshe",
            "c2threshe1",
        ],
    )
    @pytest.mark.parametrize(
        "invalid_val", ["not_a_number", "abc", [1.0, 2.0], {"key": "value"}, (1 + 2j)]
    )
    def test_invalid_float_values_raise_error(
        self, empty_params, field_name, invalid_val
    ):
        """Test that invalid float values raise ValidationError."""
        with pytest.raises(Exception):  # Could be ValidationError or ValueError
            setattr(empty_params, field_name, invalid_val)

    def test_none_values_handling(self, empty_params):
        """Test None values for fields."""
        # Integer fields default to None and should accept None
        assert empty_params.outputs is None
        assert empty_params.inputs is None

        # Float fields default to 0.0
        assert empty_params.tbw == 0.0
        assert empty_params.deltat == 0.0

        # Test that reassignment of None converts to 0.0 for float fields
        empty_params.tbw = None
        assert empty_params.tbw == 0.0

        empty_params.deltat = None
        assert empty_params.deltat == 0.0

    def test_field_metadata(self, empty_params):
        """Test that field metadata is accessible."""
        field_info = empty_params.model_fields
        assert "outputs" in field_info
        assert "tbw" in field_info

        # Check field descriptions exist
        outputs_field = field_info["outputs"]
        assert hasattr(outputs_field, "description")
        assert "Number of output channels" in str(outputs_field.description)


class TestDictionaryOperations:
    """Test dictionary conversion operations."""

    @pytest.fixture
    def sample_params(self):
        """Fixture providing sample BirrpParameters with data."""
        return BirrpParameters(
            outputs=2,
            inputs=2,
            references=2,
            tbw=2.0,
            deltat=1.0,
            nfft=8192.0,
            nf1=4,
            uin=0.01,
            c2threshe=0.35,
        )

    def test_to_dict_default_values(self):
        """Test to_dict with default values."""
        params = BirrpParameters()
        data_dict = params.to_dict()
        assert isinstance(data_dict, dict)
        assert "birrp_parameters" in data_dict

        params_data = data_dict["birrp_parameters"]
        assert params_data["outputs"] is None
        assert params_data["tbw"] == 0.0
        assert params_data["deltat"] == 0.0

    def test_to_dict_custom_values(self, sample_params):
        """Test to_dict with custom values."""
        data_dict = sample_params.to_dict()
        params_data = data_dict["birrp_parameters"]

        assert params_data["outputs"] == 2
        assert params_data["inputs"] == 2
        assert params_data["tbw"] == 2.0
        assert params_data["nfft"] == 8192.0
        assert params_data["uin"] == 0.01

    def test_from_dict_basic(self):
        """Test from_dict basic functionality."""
        data = {
            "outputs": 3,
            "inputs": 3,
            "references": 1,
            "tbw": 4.0,
            "deltat": 0.5,
            "nfft": 4096.0,
        }
        params = BirrpParameters(**data)
        assert params.outputs == 3
        assert params.inputs == 3
        assert params.tbw == 4.0
        assert params.nfft == 4096.0

    def test_round_trip_dictionary(self, sample_params):
        """Test dictionary round trip conversion."""
        original_dict = sample_params.to_dict()

        # Create new instance from dict data, filtering None values for integer fields
        params_data = original_dict["birrp_parameters"]
        # Filter out None values which cause validation errors when passed explicitly
        filtered_data = {k: v for k, v in params_data.items() if v is not None}
        new_params = BirrpParameters(**filtered_data)

        # Compare the important non-None fields
        assert new_params.outputs == sample_params.outputs
        assert new_params.inputs == sample_params.inputs
        assert new_params.tbw == sample_params.tbw
        assert new_params.nfft == sample_params.nfft
        assert new_params.uin == sample_params.uin

    def test_from_dict_partial_data(self):
        """Test from_dict with partial data."""
        data = {"outputs": 4, "tbw": 8.0, "uin": 0.05}
        params = BirrpParameters(**data)

        assert params.outputs == 4
        assert params.tbw == 8.0
        assert params.uin == 0.05
        # Check defaults for unspecified fields
        assert params.inputs is None
        assert params.deltat == 0.0


class TestJSONSerialization:
    """Test JSON serialization operations."""

    @pytest.fixture
    def sample_params(self):
        """Fixture providing sample BirrpParameters."""
        return BirrpParameters(
            outputs=2,
            inputs=3,
            tbw=2.0,
            deltat=1.0,
            nf1=4,
            uin=0.01,
            c2threshe=0.35,
            nar=5,
        )

    def test_to_json_basic(self, sample_params):
        """Test basic JSON serialization."""
        json_str = sample_params.to_json()
        assert isinstance(json_str, str)

        # Parse back to verify
        data = json.loads(json_str)
        assert "birrp_parameters" in data

        params_data = data["birrp_parameters"]
        assert params_data["outputs"] == 2
        assert params_data["tbw"] == 2.0

    def test_json_round_trip(self, sample_params):
        """Test JSON round trip conversion."""
        json_str = sample_params.to_json()
        data = json.loads(json_str)

        # Create new instance, filtering None values
        params_data = data["birrp_parameters"]
        filtered_data = {k: v for k, v in params_data.items() if v is not None}
        new_params = BirrpParameters(**filtered_data)

        # Compare key fields
        assert new_params.outputs == sample_params.outputs
        assert new_params.tbw == sample_params.tbw
        assert new_params.uin == sample_params.uin
        assert new_params.c2threshe == sample_params.c2threshe

    def test_json_handles_none_values(self):
        """Test JSON serialization handles None values."""
        params = BirrpParameters(outputs=2, tbw=1.0)  # Mix of None and non-None
        json_str = params.to_json()
        data = json.loads(json_str)

        params_data = data["birrp_parameters"]
        assert params_data["outputs"] == 2
        assert params_data["inputs"] is None
        assert params_data["tbw"] == 1.0


class TestXMLSerialization:
    """Test XML serialization operations."""

    @pytest.fixture
    def sample_params(self):
        """Fixture providing sample BirrpParameters."""
        return BirrpParameters(
            outputs=2, inputs=2, tbw=2.0, deltat=1.0, nf1=4, c2threshe=0.35
        )

    def test_to_xml_element(self, sample_params):
        """Test XML element generation."""
        xml_element = sample_params.to_xml()
        assert isinstance(xml_element, ET.Element)
        assert xml_element.tag == "birrp_parameters"

    def test_to_xml_string(self, sample_params):
        """Test XML string generation."""
        xml_str = sample_params.to_xml(string=True)
        assert isinstance(xml_str, str)
        assert "<birrp_parameters>" in xml_str
        assert "<outputs>2</outputs>" in xml_str
        assert "<tbw>2.0</tbw>" in xml_str

    def test_xml_contains_values(self, sample_params):
        """Test XML contains expected values."""
        xml_str = sample_params.to_xml(string=True)

        # Check that values are present
        assert "<outputs>2</outputs>" in xml_str
        assert "<inputs>2</inputs>" in xml_str
        assert "<tbw>2.0</tbw>" in xml_str
        assert "<deltat>1.0</deltat>" in xml_str
        assert "<nf1>4</nf1>" in xml_str


class TestEdgeCasesAndErrorHandling:
    """Test edge cases and error conditions."""

    def test_negative_values_handling(self):
        """Test handling of negative values where appropriate."""
        # deltat can be negative (sample rate)
        params = BirrpParameters(deltat=-1.0)
        assert params.deltat == -1.0

        # ainlin can be negative
        params = BirrpParameters(ainlin=-999.0)
        assert params.ainlin == -999.0

        # Most other fields should accept negative values (no explicit constraints)
        params = BirrpParameters(outputs=-1)  # Though this may not make physical sense
        assert params.outputs == -1

    def test_zero_values_handling(self):
        """Test handling of zero values."""
        params = BirrpParameters(
            outputs=0,
            inputs=0,
            references=0,
            tbw=0.0,
            deltat=0.0,
            nfft=0.0,
            nf1=0,
            uin=0.0,
            c2threshe=0.0,
        )
        assert params.outputs == 0
        assert params.tbw == 0.0
        assert params.nf1 == 0

    def test_large_values_handling(self):
        """Test handling of large values."""
        params = BirrpParameters(
            outputs=1000000, nfft=1048576.0, uin=999.99, c2threshe=1000.0
        )
        assert params.outputs == 1000000
        assert params.nfft == 1048576.0
        assert params.uin == 999.99

    def test_equality_comparison(self):
        """Test equality comparison between instances."""
        params1 = BirrpParameters(outputs=2, tbw=2.0, uin=0.01)
        params2 = BirrpParameters(outputs=2, tbw=2.0, uin=0.01)
        params3 = BirrpParameters(outputs=3, tbw=2.0, uin=0.01)

        # Test that equal parameters have equal field values
        assert params1.outputs == params2.outputs
        assert params1.tbw == params2.tbw
        assert params1.uin == params2.uin

        # Test that different parameters have different field values
        assert params1.outputs != params3.outputs  # 2 != 3
        assert params1.tbw == params3.tbw  # Same tbw
        assert params1.uin == params3.uin  # Same uin

    def test_type_coercion_edge_cases(self):
        """Test edge cases in type coercion."""
        params = BirrpParameters()

        # Float to int coercion only works for whole numbers
        params.outputs = 2.0  # Should convert to 2 (no fractional part)
        assert params.outputs == 2
        assert isinstance(params.outputs, int)

        # Fractional floats should raise error
        with pytest.raises(Exception):
            params.outputs = 2.7  # Should fail due to fractional part

        # Int to float coercion
        params.tbw = 5  # Should convert to 5.0
        assert params.tbw == 5.0
        assert isinstance(params.tbw, float)

    def test_field_access_patterns(self):
        """Test various field access patterns."""
        params = BirrpParameters()

        # Test all integer fields have None default
        int_fields = [
            "outputs",
            "inputs",
            "references",
            "nf1",
            "nfinc",
            "nfsect",
            "nz",
            "npcs",
            "nar",
            "imode",
            "jmode",
            "ncomp",
        ]
        for field in int_fields:
            assert getattr(params, field) is None

        # Test all float fields have 0.0 default
        float_fields = [
            "tbw",
            "deltat",
            "nfft",
            "nsctinc",
            "nsctmax",
            "uin",
            "ainlin",
            "ainuin",
            "c2threshe",
            "c2threshe1",
        ]
        for field in float_fields:
            assert getattr(params, field) == 0.0


class TestPerformanceAndBatchOperations:
    """Test performance and batch operations."""

    def test_batch_instantiation(self):
        """Test creating multiple instances efficiently."""
        instances = []
        for i in range(100):
            params = BirrpParameters(
                outputs=i % 5 + 1,
                inputs=i % 3 + 1,
                tbw=float(i % 10),
                deltat=float(i % 2),
            )
            instances.append(params)

        assert len(instances) == 100
        assert all(isinstance(p, BirrpParameters) for p in instances)

    def test_batch_serialization(self):
        """Test batch serialization performance."""
        instances = [
            BirrpParameters(outputs=i, tbw=float(i), uin=float(i / 100))
            for i in range(1, 51)
        ]

        # Test dict conversion
        dicts = [p.to_dict() for p in instances]
        assert len(dicts) == 50
        assert all("birrp_parameters" in d for d in dicts)

        # Test JSON conversion
        jsons = [p.to_json() for p in instances]
        assert len(jsons) == 50
        assert all(isinstance(j, str) for j in jsons)

    def test_large_parameter_values_performance(self):
        """Test performance with large parameter values."""
        params = BirrpParameters(
            outputs=999999,
            inputs=888888,
            references=777777,
            tbw=123456.789,
            deltat=987654.321,
            nfft=1048576.0,
            nf1=65536,
            uin=999.999,
            c2threshe=0.999999,
        )

        # Test that operations still work efficiently
        dict_data = params.to_dict()
        json_data = params.to_json()
        xml_data = params.to_xml(string=True)

        assert isinstance(dict_data, dict)
        assert isinstance(json_data, str)
        assert isinstance(xml_data, str)


class TestIntegrationAndWorkflow:
    """Test integration scenarios and complete workflows."""

    def test_complete_birrp_workflow_scenario(self):
        """Test a complete BIRRP parameter setup workflow."""
        # Step 1: Create parameters for a typical MT processing scenario
        params = BirrpParameters(
            outputs=2,  # Ex, Ey
            inputs=2,  # Hx, Hy
            references=3,  # Hz, Ex, Ey reference
            tbw=2.0,  # Time-bandwidth product
            deltat=1.0,  # 1 second sampling
            nfft=8192.0,  # FFT length
            nsctinc=2.0,  # Section increment
            nsctmax=10.0,  # Max sections
            nf1=4,  # First frequency index
            nfinc=2,  # Frequency increment
            nfsect=32,  # Frequency sections
            uin=0.01,  # Small leverage
            ainlin=-999.0,  # Bounded influence
            ainuin=0.99,  # Large leverage
            c2threshe=0.35,  # E coherency threshold
            nz=1,  # Use Hz threshold
            c2threshe1=0.35,  # Hz coherency threshold
            npcs=2,  # Data segments
            nar=5,  # AR filter order
            imode=0,  # Data file mode
            jmode=0,  # Time mode
            ncomp=5,  # Total components
        )

        # Step 2: Validate the setup
        assert params.outputs == 2
        assert params.inputs == 2
        assert params.references == 3
        assert params.ncomp == 5

        # Step 3: Convert to various formats for processing
        dict_data = params.to_dict()
        json_data = params.to_json()
        xml_data = params.to_xml(string=True)

        # Step 4: Verify all conversions worked
        assert "birrp_parameters" in dict_data
        assert "outputs" in json_data
        assert "<outputs>2</outputs>" in xml_data

    def test_multiple_format_round_trip(self):
        """Test round trip through multiple serialization formats."""
        original = BirrpParameters(
            outputs=3,
            inputs=2,
            tbw=4.0,
            deltat=0.5,
            nf1=8,
            uin=0.05,
            c2threshe=0.4,
            nar=7,
        )

        # Dict round trip
        dict_data = original.to_dict()["birrp_parameters"]
        filtered_dict_data = {k: v for k, v in dict_data.items() if v is not None}
        from_dict = BirrpParameters(**filtered_dict_data)

        # JSON round trip
        json_data = json.loads(original.to_json())["birrp_parameters"]
        filtered_json_data = {k: v for k, v in json_data.items() if v is not None}
        from_json = BirrpParameters(**filtered_json_data)

        # Verify key fields are equivalent
        assert from_dict.outputs == original.outputs == from_json.outputs
        assert from_dict.inputs == original.inputs == from_json.inputs
        assert from_dict.tbw == original.tbw == from_json.tbw
        assert from_dict.uin == original.uin == from_json.uin
        assert from_dict.c2threshe == original.c2threshe == from_json.c2threshe

    def test_error_recovery_workflow(self):
        """Test error recovery in realistic scenarios."""
        # Test partial parameter recovery
        params = BirrpParameters()

        # Simulate setting parameters that might fail
        successful_params = []
        failed_params = []

        test_values = [
            ("outputs", 2),
            ("inputs", "invalid"),
            ("tbw", 4.0),
            ("deltat", "not_a_number"),
            ("nf1", 8),
            ("uin", [1, 2, 3]),
        ]

        for field_name, value in test_values:
            try:
                setattr(params, field_name, value)
                successful_params.append((field_name, value))
            except Exception:
                failed_params.append((field_name, value))

        # Should have some successful and some failed
        assert len(successful_params) > 0
        assert len(failed_params) > 0

        # Successful parameters should be set
        assert params.outputs == 2
        assert params.tbw == 4.0
        assert params.nf1 == 8
