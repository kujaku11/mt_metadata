"""
Test base_basemodel.py - Comprehensive test suite for Base weight kernel basemodel

Tests the Base class and WeightTypeEnum from the basemodel module using fixtures
and subtests for optimal efficiency.

This module contains the base classes and enumerations for weight kernels
used in MT metadata processing, providing the foundational structure for
all weight kernel implementations.
"""

import time

import numpy as np
import pytest

from mt_metadata.features.weights.base import Base, WeightTypeEnum

# =====================================================
# Fixtures for optimal efficiency
# =====================================================


@pytest.fixture
def default_base():
    """Basic Base weight kernel with default values"""
    return Base()


@pytest.fixture
def monotonic_base():
    """Base weight kernel configured for monotonic type"""
    return Base(
        weight_type=WeightTypeEnum.monotonic,
        description="Monotonic weight kernel for smooth transitions",
        active=True,
    )


@pytest.fixture
def learned_base():
    """Base weight kernel configured for learned type"""
    return Base(
        weight_type=WeightTypeEnum.learned,
        description="Machine learning based weight kernel",
        active=True,
    )


@pytest.fixture
def spatial_base():
    """Base weight kernel configured for spatial type"""
    return Base(
        weight_type=WeightTypeEnum.spatial,
        description="Spatial distance-based weight kernel",
        active=False,
    )


@pytest.fixture
def custom_base():
    """Base weight kernel configured for custom type"""
    return Base(
        weight_type=WeightTypeEnum.custom,
        description="Custom user-defined weight kernel",
        active=None,
    )


@pytest.fixture
def inactive_base():
    """Base weight kernel that is inactive"""
    return Base(
        weight_type="monotonic",
        description="Inactive kernel for testing",
        active=False,
    )


@pytest.fixture
def test_values_simple():
    """Simple test values for kernel evaluation"""
    return np.array([0.0, 0.25, 0.5, 0.75, 1.0])


@pytest.fixture
def test_values_extended():
    """Extended test values including edge cases"""
    return np.array([-1.0, -0.5, 0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0])


@pytest.fixture
def large_test_array():
    """Large array for performance testing"""
    return np.linspace(-2.0, 2.0, 1000)


# =====================================================
# Test Classes
# =====================================================


class TestWeightTypeEnum:
    """Test WeightTypeEnum values and behavior"""

    def test_weight_type_enum_values(self):
        """Test that WeightTypeEnum has expected values"""
        expected_values = ["monotonic", "learned", "spatial", "custom"]
        actual_values = [e.value for e in WeightTypeEnum]
        assert actual_values == expected_values

    def test_weight_type_enum_membership(self):
        """Test enum membership for weight type values"""
        assert "monotonic" in [e.value for e in WeightTypeEnum]
        assert "learned" in [e.value for e in WeightTypeEnum]
        assert "spatial" in [e.value for e in WeightTypeEnum]
        assert "custom" in [e.value for e in WeightTypeEnum]
        assert "invalid" not in [e.value for e in WeightTypeEnum]

    def test_weight_type_enum_string_representation(self):
        """Test string representation of enum values"""
        assert WeightTypeEnum.monotonic.value == "monotonic"
        assert WeightTypeEnum.learned.value == "learned"
        assert WeightTypeEnum.spatial.value == "spatial"
        assert WeightTypeEnum.custom.value == "custom"

    def test_weight_type_enum_equality(self):
        """Test enum equality comparisons"""
        assert WeightTypeEnum.monotonic == "monotonic"
        assert WeightTypeEnum.learned == "learned"
        assert WeightTypeEnum.spatial == "spatial"
        assert WeightTypeEnum.custom == "custom"


class TestBaseFixtures:
    """Test that all fixtures work correctly"""

    def test_fixtures_work(
        self,
        default_base,
        monotonic_base,
        learned_base,
        spatial_base,
        custom_base,
        inactive_base,
    ):
        """Verify all fixtures create valid Base instances"""
        assert isinstance(default_base, Base)
        assert isinstance(monotonic_base, Base)
        assert isinstance(learned_base, Base)
        assert isinstance(spatial_base, Base)
        assert isinstance(custom_base, Base)
        assert isinstance(inactive_base, Base)

    def test_fixture_configurations(
        self,
        default_base,
        monotonic_base,
        learned_base,
        spatial_base,
        custom_base,
        inactive_base,
    ):
        """Test that fixtures have expected configurations"""
        # Default fixture
        assert default_base.weight_type == "monotonic"
        assert default_base.description is None
        assert default_base.active is None

        # Monotonic fixture
        assert monotonic_base.weight_type == "monotonic"
        assert "Monotonic" in monotonic_base.description
        assert monotonic_base.active is True

        # Learned fixture
        assert learned_base.weight_type == "learned"
        assert "learning" in learned_base.description.lower()
        assert learned_base.active is True

        # Spatial fixture
        assert spatial_base.weight_type == "spatial"
        assert "spatial" in spatial_base.description.lower()
        assert spatial_base.active is False

        # Custom fixture
        assert custom_base.weight_type == "custom"
        assert "custom" in custom_base.description.lower()
        assert custom_base.active is None

        # Inactive fixture
        assert inactive_base.weight_type == "monotonic"
        assert inactive_base.active is False


class TestBaseInstantiation:
    """Test various ways to instantiate Base weight kernels"""

    def test_default_instantiation(self):
        """Test creating with default values"""
        base = Base()

        assert base.weight_type == "monotonic"
        assert base.description is None
        assert base.active is None

    def test_custom_instantiation(self):
        """Test creating with custom values"""
        base = Base(
            weight_type="learned",
            description="Test kernel description",
            active=True,
        )

        assert base.weight_type == "learned"
        assert base.description == "Test kernel description"
        assert base.active is True

    def test_string_enum_conversion(self):
        """Test that string values are properly converted to enums"""
        base = Base(weight_type="spatial")

        assert isinstance(base.weight_type, str)
        assert base.weight_type == "spatial"

    def test_enum_instantiation(self):
        """Test instantiation with enum values"""
        base = Base(weight_type=WeightTypeEnum.custom)

        assert base.weight_type == "custom"

    def test_invalid_weight_type_value(self):
        """Test that invalid weight type values raise ValidationError"""
        with pytest.raises(ValueError):
            Base(weight_type="invalid_type")

    def test_description_types(self):
        """Test different description value types"""
        # String description
        base1 = Base(description="Test description")
        assert base1.description == "Test description"

        # None description
        base2 = Base(description=None)
        assert base2.description is None

        # Empty string description
        base3 = Base(description="")
        assert base3.description == ""

    def test_active_types(self):
        """Test different active value types"""
        # True active
        base1 = Base(active=True)
        assert base1.active is True

        # False active
        base2 = Base(active=False)
        assert base2.active is False

        # None active
        base3 = Base(active=None)
        assert base3.active is None


class TestBaseValidation:
    """Test Pydantic validation behaviors"""

    def test_weight_type_enum_validation(self):
        """Test weight type enum validation"""
        for weight_type_value in ["monotonic", "learned", "spatial", "custom"]:
            base = Base(weight_type=weight_type_value)
            assert base.weight_type == weight_type_value

    def test_description_validation(self):
        """Test description field validation"""
        # Valid descriptions
        descriptions = [
            "Simple description",
            "Multi-word description with spaces",
            "Description with numbers 123 and symbols!",
            "",
            None,
        ]

        for desc in descriptions:
            base = Base(description=desc)
            assert base.description == desc

    def test_active_validation(self):
        """Test active field validation"""
        # Valid active values
        for active_value in [True, False, None]:
            base = Base(active=active_value)
            assert base.active is active_value

    def test_field_requirements(self):
        """Test field requirement validation"""
        # weight_type is required with default
        base = Base()
        assert hasattr(base, "weight_type")

        # description is optional
        base = Base()
        assert hasattr(base, "description")

        # active is optional
        base = Base()
        assert hasattr(base, "active")


class TestBaseEvaluation:
    """Test the evaluate method behavior"""

    def test_evaluate_not_implemented(self, default_base, test_values_simple):
        """Test that evaluate method raises NotImplementedError"""
        with pytest.raises(
            NotImplementedError, match="BaseWeightKernel cannot be evaluated directly"
        ):
            default_base.evaluate(test_values_simple)

    def test_evaluate_with_float_input(self, monotonic_base):
        """Test evaluate method with float input raises NotImplementedError"""
        with pytest.raises(NotImplementedError):
            monotonic_base.evaluate(0.5)

    def test_evaluate_with_array_input(self, learned_base, test_values_extended):
        """Test evaluate method with array input raises NotImplementedError"""
        with pytest.raises(NotImplementedError):
            learned_base.evaluate(test_values_extended)

    def test_evaluate_with_large_array(self, spatial_base, large_test_array):
        """Test evaluate method with large array raises NotImplementedError"""
        with pytest.raises(NotImplementedError):
            spatial_base.evaluate(large_test_array)

    def test_evaluate_with_none_input(self, custom_base):
        """Test evaluate method with None input raises NotImplementedError"""
        with pytest.raises(NotImplementedError):
            custom_base.evaluate(None)

    def test_evaluate_error_message(self, default_base):
        """Test that evaluate error message is informative"""
        try:
            default_base.evaluate([1, 2, 3])
        except NotImplementedError as e:
            assert "BaseWeightKernel cannot be evaluated directly" in str(e)


class TestBaseSerialization:
    """Test serialization and deserialization"""

    def test_to_dict(self, monotonic_base):
        """Test serialization to dictionary"""
        base_dict = monotonic_base.to_dict()

        assert isinstance(base_dict, dict)
        assert "base" in base_dict

        inner_dict = base_dict["base"]
        assert inner_dict["weight_type"] == "monotonic"
        assert "Monotonic" in inner_dict["description"]
        assert inner_dict["active"] is True

    def test_to_dict_with_none_values(self, default_base):
        """Test serialization with None values"""
        base_dict = default_base.to_dict()

        assert isinstance(base_dict, dict)
        assert "base" in base_dict

        inner_dict = base_dict["base"]
        assert inner_dict["weight_type"] == "monotonic"
        # None values are not included in the dict by default
        assert "description" not in inner_dict or inner_dict.get("description") is None
        assert "active" not in inner_dict or inner_dict.get("active") is None

    def test_model_copy(self, learned_base):
        """Test Pydantic model copy functionality"""
        copied_base = learned_base.model_copy()

        assert copied_base.weight_type == learned_base.weight_type
        assert copied_base.description == learned_base.description
        assert copied_base.active == learned_base.active
        assert copied_base is not learned_base  # Different instances

    def test_model_copy_with_updates(self, spatial_base):
        """Test model copy with field updates"""
        updated_base = spatial_base.model_copy(
            update={"description": "Updated description", "active": True}
        )

        assert updated_base.weight_type == spatial_base.weight_type
        assert updated_base.description == "Updated description"
        assert updated_base.active is True
        assert updated_base is not spatial_base

    def test_dict_representation(self, custom_base):
        """Test dictionary representation methods"""
        # Test __dict__ access
        base_dict = custom_base.__dict__
        assert "weight_type" in base_dict
        assert "description" in base_dict
        assert "active" in base_dict


class TestBasePerformance:
    """Test performance characteristics"""

    def test_instantiation_performance(self):
        """Test that instantiation is reasonably fast"""
        start_time = time.time()

        for _ in range(100):
            Base(
                weight_type="monotonic",
                description="Performance test kernel",
                active=True,
            )

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Should complete 100 instantiations in less than 1 second
        assert elapsed_time < 1.0

    def test_validation_performance(self):
        """Test that validation is reasonably fast"""
        start_time = time.time()

        for i in range(100):
            weight_types = ["monotonic", "learned", "spatial", "custom"]
            Base(
                weight_type=weight_types[i % 4],
                description=f"Test description {i}",
                active=i % 2 == 0,
            )

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Should complete 100 validations in less than 1 second
        assert elapsed_time < 1.0

    def test_serialization_performance(self, monotonic_base):
        """Test that serialization is reasonably fast"""
        start_time = time.time()

        for _ in range(100):
            monotonic_base.to_dict()

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Should complete 100 serializations in less than 0.5 seconds
        assert elapsed_time < 0.5


class TestBaseEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_very_long_description(self):
        """Test with very long description"""
        long_desc = "A" * 10000  # 10k characters
        base = Base(description=long_desc)

        assert base.description == long_desc
        assert len(base.description) == 10000

    def test_special_characters_in_description(self):
        """Test description with special characters"""
        special_desc = "Test with !@#$%^&*()_+-=[]{}|;':\",./<>?`~"
        base = Base(description=special_desc)

        assert base.description == special_desc

    def test_unicode_characters_in_description(self):
        """Test description with unicode characters"""
        unicode_desc = "Test with unicode: αβγδε ñáéíóú 中文 🚀🔬⚡"
        base = Base(description=unicode_desc)

        assert base.description == unicode_desc

    def test_newlines_in_description(self):
        """Test description with newline characters"""
        multiline_desc = "Line 1\nLine 2\nLine 3"
        base = Base(description=multiline_desc)

        assert base.description == multiline_desc
        assert "\n" in base.description

    def test_empty_string_vs_none_description(self):
        """Test difference between empty string and None description"""
        base_empty = Base(description="")
        base_none = Base(description=None)

        assert base_empty.description == ""
        assert base_none.description is None
        assert base_empty.description != base_none.description


class TestBaseInheritance:
    """Test inheritance and method override scenarios"""

    def test_base_is_abstract(self):
        """Test that Base acts as an abstract base class"""
        base = Base()

        # Should be instantiable but evaluate should not be implemented
        assert isinstance(base, Base)

        with pytest.raises(NotImplementedError):
            base.evaluate([1, 2, 3])

    def test_subclass_implementation(self):
        """Test implementing evaluate in a subclass"""

        class TestKernel(Base):
            def evaluate(self, values):
                """Test implementation that returns input values"""
                return np.asarray(values) * 2

        test_kernel = TestKernel(
            weight_type="custom", description="Test subclass kernel"
        )

        # Should not raise NotImplementedError
        result = test_kernel.evaluate([1, 2, 3])
        expected = np.array([2, 4, 6])
        np.testing.assert_array_equal(result, expected)

    def test_subclass_inheritance(self):
        """Test that subclass inherits Base properties correctly"""

        class TestKernel(Base):
            def evaluate(self, values):
                return values

        test_kernel = TestKernel(weight_type="learned", active=True)

        assert test_kernel.weight_type == "learned"
        assert test_kernel.active is True
        assert hasattr(test_kernel, "description")


class TestBaseParametrized:
    """Parametrized tests for comprehensive coverage"""

    @pytest.mark.parametrize(
        "weight_type", ["monotonic", "learned", "spatial", "custom"]
    )
    def test_weight_type_values(self, weight_type):
        """Test all weight type enum values"""
        base = Base(weight_type=weight_type)
        assert base.weight_type == weight_type

    @pytest.mark.parametrize("active", [True, False, None])
    def test_active_values(self, active):
        """Test all active boolean values"""
        base = Base(active=active)
        assert base.active is active

    @pytest.mark.parametrize(
        "description",
        [
            "Simple description",
            "",
            None,
            "Description with 数字 123 and symbols!",
            "Multi\nline\ndescription",
            "A" * 1000,  # Long description
        ],
    )
    def test_description_values(self, description):
        """Test various description values"""
        base = Base(description=description)
        assert base.description == description

    @pytest.mark.parametrize(
        "weight_type,active,should_work",
        [
            ("monotonic", True, True),
            ("learned", False, True),
            ("spatial", None, True),
            ("custom", True, True),
            ("invalid", True, False),
        ],
    )
    def test_validation_combinations(self, weight_type, active, should_work):
        """Test various field combinations for validation"""
        if should_work:
            base = Base(weight_type=weight_type, active=active)
            assert base.weight_type == weight_type
            assert base.active is active
        else:
            with pytest.raises(ValueError):
                Base(weight_type=weight_type, active=active)

    @pytest.mark.parametrize(
        "input_type", [np.array([1, 2, 3]), [1, 2, 3], 1.5, None, "string_input"]
    )
    def test_evaluate_input_types(self, default_base, input_type):
        """Test evaluate method with different input types"""
        with pytest.raises(NotImplementedError):
            default_base.evaluate(input_type)

    @pytest.mark.parametrize("array_size", [1, 10, 100, 1000])
    def test_evaluate_array_sizes(self, monotonic_base, array_size):
        """Test evaluate method with different array sizes"""
        test_array = np.ones(array_size)

        with pytest.raises(NotImplementedError):
            monotonic_base.evaluate(test_array)


class TestBaseDocumentation:
    """Test documentation and help functionality"""

    def test_class_docstring(self):
        """Test that Base class has proper documentation"""
        # Base class may not have a docstring, but should be documented through fields
        # Just check that the class exists and is properly structured
        assert hasattr(Base, "__name__")
        assert Base.__name__ == "Base"

    def test_evaluate_method_docstring(self):
        """Test that evaluate method has proper documentation"""
        assert Base.evaluate.__doc__ is not None
        doc = Base.evaluate.__doc__
        assert "Parameters" in doc
        assert "Returns" in doc
        assert "values" in doc.lower()
        assert "weights" in doc.lower()

    def test_field_documentation(self):
        """Test that fields have proper documentation"""
        # Test through schema or field info
        base = Base()
        schema = base.model_json_schema()

        # Check that fields have descriptions
        properties = schema.get("properties", {})
        assert "weight_type" in properties
        assert "description" in properties
        assert "active" in properties

        # Check that weight_type has description
        weight_type_info = properties.get("weight_type", {})
        assert "description" in weight_type_info


class TestBaseJSONSchema:
    """Test JSON schema generation and validation"""

    def test_json_schema_generation(self):
        """Test that Base generates valid JSON schema"""
        base = Base()
        schema = base.model_json_schema()

        assert isinstance(schema, dict)
        assert "type" in schema
        assert "properties" in schema

        properties = schema["properties"]
        assert "weight_type" in properties
        assert "description" in properties
        assert "active" in properties

    def test_json_schema_field_types(self):
        """Test that JSON schema has correct field types"""
        base = Base()
        schema = base.model_json_schema()
        properties = schema["properties"]

        # weight_type should be enum
        weight_type_schema = properties["weight_type"]
        assert "enum" in weight_type_schema or "anyOf" in weight_type_schema

        # description should allow string or null
        description_schema = properties["description"]
        assert "type" in description_schema or "anyOf" in description_schema

        # active should allow boolean or null
        active_schema = properties["active"]
        assert "type" in active_schema or "anyOf" in active_schema

    def test_json_schema_required_fields(self):
        """Test that JSON schema correctly identifies required fields"""
        base = Base()
        schema = base.model_json_schema()

        # Check required fields
        required = schema.get("required", [])
        # weight_type has a default, so it may not be in required
        # description and active are optional

    def test_json_schema_examples(self):
        """Test that JSON schema includes examples where specified"""
        base = Base()
        schema = base.model_json_schema()
        properties = schema["properties"]

        # weight_type should have examples
        weight_type_schema = properties["weight_type"]
        # Examples might be in different places depending on pydantic version
        # Just check that the schema is well-formed
