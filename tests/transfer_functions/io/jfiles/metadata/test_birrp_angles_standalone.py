# -*- coding: utf-8 -*-
"""
Standalone test for BirrpAngles class to avoid import issues.

This is a focused test that imports only the necessary parts to test BirrpAngles
without running into import issues in the broader jfiles package.
"""

import json
import sys
from pathlib import Path
from xml.etree import ElementTree as et

import numpy as np
import pytest


# Add the root of the project to sys.path
root_path = Path(__file__).parent.parent.parent.parent.parent.parent
sys.path.insert(0, str(root_path))

# Now we can import the necessary base classes directly
from mt_metadata.base import MetadataBase


# Load BirrpAngles by executing the module directly
birrp_angles_path = (
    root_path / "mt_metadata/transfer_functions/io/jfiles/metadata/birrp_angles.py"
)
with open(birrp_angles_path) as f:
    code = compile(f.read(), birrp_angles_path, "exec")
    namespace = {"MetadataBase": MetadataBase}
    exec(code, namespace)
    BirrpAngles = namespace["BirrpAngles"]


def test_basic_instantiation():
    """Test basic BirrpAngles instantiation."""
    angles = BirrpAngles()
    assert angles.theta1 == 0.0
    assert angles.theta2 == 0.0
    assert angles.phi == 0.0
    assert isinstance(angles.theta1, float)
    assert isinstance(angles.theta2, float)
    assert isinstance(angles.phi, float)


def test_custom_values():
    """Test BirrpAngles with custom values."""
    angles = BirrpAngles(theta1=45.0, theta2=90.0, phi=180.0)
    assert angles.theta1 == 45.0
    assert angles.theta2 == 90.0
    assert angles.phi == 180.0


def test_type_conversion():
    """Test type conversion for angle values."""
    angles = BirrpAngles(theta1=45, theta2="90.5", phi=np.float32(180.0))
    assert angles.theta1 == 45.0
    assert angles.theta2 == 90.5
    assert angles.phi == 180.0
    assert isinstance(angles.theta1, float)
    assert isinstance(angles.theta2, float)
    assert isinstance(angles.phi, float)


def test_field_assignment():
    """Test field assignment after instantiation."""
    angles = BirrpAngles()
    angles.theta1 = 30.0
    angles.theta2 = 60.0
    angles.phi = 270.0

    assert angles.theta1 == 30.0
    assert angles.theta2 == 60.0
    assert angles.phi == 270.0


def test_to_dict():
    """Test dictionary serialization."""
    angles = BirrpAngles(theta1=45.0, theta2=90.0, phi=180.0)
    result = angles.to_dict()

    assert isinstance(result, dict)
    assert result["theta1"] == 45.0
    assert result["theta2"] == 90.0
    assert result["phi"] == 180.0


def test_from_dict():
    """Test dictionary deserialization."""
    angles = BirrpAngles()
    data = {"theta1": 30.0, "theta2": 60.0, "phi": 270.0}
    angles.from_dict(data)

    assert angles.theta1 == 30.0
    assert angles.theta2 == 60.0
    assert angles.phi == 270.0


def test_round_trip_dict():
    """Test round-trip dictionary conversion."""
    original = BirrpAngles(theta1=123.456, theta2=78.901, phi=234.567)
    dict_data = original.to_dict()

    new_angles = BirrpAngles()
    new_angles.from_dict(dict_data)

    assert new_angles.theta1 == pytest.approx(original.theta1)
    assert new_angles.theta2 == pytest.approx(original.theta2)
    assert new_angles.phi == pytest.approx(original.phi)


def test_to_json():
    """Test JSON serialization."""
    angles = BirrpAngles(theta1=45.0, theta2=90.0, phi=180.0)
    json_str = angles.to_json()

    assert isinstance(json_str, str)
    # Parse to verify it's valid JSON
    json_data = json.loads(json_str)
    assert isinstance(json_data, dict)


def test_json_round_trip():
    """Test JSON round-trip conversion."""
    original = BirrpAngles(theta1=123.456, theta2=78.901, phi=234.567)
    json_str = original.to_json()
    json_data = json.loads(json_str)

    new_angles = BirrpAngles()
    new_angles.from_dict(json_data)

    assert new_angles.theta1 == pytest.approx(original.theta1)
    assert new_angles.theta2 == pytest.approx(original.theta2)
    assert new_angles.phi == pytest.approx(original.phi)


def test_to_xml():
    """Test XML serialization."""
    angles = BirrpAngles(theta1=45.0, theta2=90.0, phi=180.0)

    # Test XML element
    xml_element = angles.to_xml(string=False)
    assert isinstance(xml_element, et.Element)
    assert xml_element.tag == "BirrpAngles"

    # Test XML string
    xml_string = angles.to_xml(string=True)
    assert isinstance(xml_string, str)
    assert "BirrpAngles" in xml_string


def test_negative_angles():
    """Test negative angle values."""
    angles = BirrpAngles(theta1=-45.0, theta2=-90.0, phi=-180.0)
    assert angles.theta1 == -45.0
    assert angles.theta2 == -90.0
    assert angles.phi == -180.0


def test_large_angles():
    """Test large angle values."""
    angles = BirrpAngles(theta1=720.0, theta2=1080.0, phi=1440.0)
    assert angles.theta1 == 720.0
    assert angles.theta2 == 1080.0
    assert angles.phi == 1440.0


def test_precision():
    """Test floating point precision."""
    angles = BirrpAngles(theta1=45.123456789, theta2=90.987654321, phi=180.555555555)
    assert angles.theta1 == pytest.approx(45.123456789)
    assert angles.theta2 == pytest.approx(90.987654321)
    assert angles.phi == pytest.approx(180.555555555)


def test_equality():
    """Test equality comparison."""
    angles1 = BirrpAngles(theta1=45.0, theta2=90.0, phi=180.0)
    angles2 = BirrpAngles(theta1=45.0, theta2=90.0, phi=180.0)
    angles3 = BirrpAngles(theta1=30.0, theta2=60.0, phi=120.0)

    assert angles1 == angles2
    assert angles1 != angles3


def test_invalid_values():
    """Test that invalid values raise errors."""
    angles = BirrpAngles()

    with pytest.raises(Exception):  # ValidationError or similar
        angles.theta1 = "not_a_number"

    with pytest.raises(Exception):
        angles.theta2 = []

    with pytest.raises(Exception):
        angles.phi = {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
