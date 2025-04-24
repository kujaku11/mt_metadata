"""
Create a list of licenses using the SPDX license list.
This script fetches the SPDX license list from the SPDX GitHub repository
and creates a JSON file containing the license IDs and their corresponding names.

https://github.com/spdx/license-list-data/blob/main/json/licenses.json

"""

# =============================================================================
# Imports
# =============================================================================
from pathlib import Path
from enum import Enum
import json

# ==============================================================================

# Load the licenses JSON file
filename = Path(__file__).parent.joinpath("licenses.json")
with open(filename, "r") as fid:
    licenses = json.load(fid)

# Process the license IDs to make them valid Python identifiers
license_variable_list = []
for license in licenses["licenses"]:
    item = {}
    item["license_key"] = (
        license["licenseId"]
        .replace("-", "_")
        .replace(" ", "_")
        .replace(".", "_")
        .replace("(", "_")
        .replace(")", "_")
        .replace("/", "_")
        .replace(":", "_")
    )
    item["license_value"] = license["licenseId"]
    license_variable_list.append(item)

# Create an Enum class for the licenses
LicenseEnum = Enum(
    "LicenseEnum",  # Name of the Enum
    {
        entry["license_key"]: entry["license_value"] for entry in license_variable_list
    },  # Members
)
