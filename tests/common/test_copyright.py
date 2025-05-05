import pytest
from mt_metadata.common import Copyright, LicenseEnum


def test_copyright_default_values():
    """
    Test the default values of the Copyright model.
    """
    copyright = Copyright()

    assert copyright.release_license == "CC BY 4.0"


def test_copyright_valid_license():
    """
    Test the Copyright model with a valid license.
    """
    copyright = Copyright(release_license="MIT")

    assert copyright.release_license == "MIT"


def test_copyright_valid_license_with_formatting():
    """
    Test the Copyright model with a valid license that requires formatting.
    """
    copyright = Copyright(release_license="CC BY 4.0")

    assert copyright.release_license == "CC-BY-4.0"


def test_copyright_invalid_license():
    """
    Test the Copyright model with an invalid license.
    """
    with pytest.raises(
        NameError, match="License is not an acceptable license: INVALID_LICENSE"
    ):
        Copyright(release_license="INVALID_LICENSE")


def test_copyright_partial_values():
    """
    Test the Copyright model with partial values.
    """
    copyright = Copyright()

    assert copyright.release_license == "CC BY 4.0"


def test_copyright_enum_membership():
    """
    Test that the release_license value is a valid member of LicenseEnum.
    """
    copyright = Copyright(release_license="Apache-2.0")

    assert copyright.release_license in [license.value for license in LicenseEnum]
