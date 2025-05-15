# =====================================================
# Imports
# =====================================================
import json
from enum import Enum
from pathlib import Path

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema, CoreSchema


# =====================================================


class StrEnumerationBase(str, Enum):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: type[Enum], handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        # Define a schema that validates and converts input to lowercase
        return core_schema.no_info_plain_validator_function(cls._validate_lowercase)

    @classmethod
    def _validate_lowercase(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"Expected string, got {type(value)}")
        value_lower = value.lower()
        valid_values = [member.value.lower() for member in cls]
        if value_lower not in valid_values:
            raise ValueError(f"Invalid value: {value}. Must be one of {valid_values}.")
        return value


class DataTypeEnum(StrEnumerationBase):
    RMT = "RMT"
    AMT = "AMT"
    BBMT = "BBMT"
    LPMT = "LPMT"
    ULPMT = "ULPMT"
    MT = "MT"
    LP = "LP"
    BB = "BB"
    WB = "WB"
    other = "other"


class ChannelLayoutEnum(StrEnumerationBase):
    L = "L"
    X = "X"
    other = "other"


class OrientationMethodEnum(StrEnumerationBase):
    compass = "compass"
    GPS = "GPS"
    theodolite = "theodolite"
    other = "other"


class GeographicReferenceFrameEnum(StrEnumerationBase):
    geographic = "geographic"
    geomagnetic = "geomagnetic"


class ChannelOrientationEnum(StrEnumerationBase):
    orthogonal = "orthogonal"
    station = "station"
    other = "other"


class GeomagneticModelEnum(str, Enum):
    """split by - if needed"""

    EMAG2 = "EMAG2"
    EMM = "EMM"
    HDGM = "HDGM"
    IGRF = "IGRF"
    WMM = "WMM"
    unknown = "unknown"
    other = "other"

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: type[Enum], handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        # Define a schema that validates and converts input to lowercase
        return core_schema.no_info_plain_validator_function(cls._validate_lowercase)

    @classmethod
    def _validate_lowercase(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"Expected string, got {type(value)}")
        value_lower = value.lower().split("-")[0]
        valid_values = [member.value.lower() for member in cls]
        if value_lower not in valid_values:
            raise ValueError(f"Invalid value: {value}. Must be one of {valid_values}.")
        return value


class FilterTypeEnum(StrEnumerationBase):
    fap_table = "fap"
    zpk = "zpk"
    time_delay = "time_delay"
    coefficient = "coefficient"
    fir = "fir"
    other = "other"


class SymmetryEnum(StrEnumerationBase):
    NONE = "NONE"
    ODD = "ODD"
    EVEN = "EVEN"


# Load the licenses JSON file
filename = Path(__file__).parent.parent.joinpath("data", "licenses.json")
with open(filename, "r") as fid:
    licenses = json.load(fid)

# Process the license IDs to make them valid Python identifiers
license_variable_list = [
    {"license_key": "CC_0", "license_value": "CC0"},
    {"license_key": "CC0", "license_value": "CC0"},
    {"license_key": "CC_BY", "license_value": "CC BY"},
    {"license_key": "CC_BY_SA", "license_value": "CC BY-SA"},
    {"license_key": "CC_BY_NC", "license_value": "CC BY-NC"},
    {"license_key": "CC_BY_NA_SA", "license_value": "CC BY-NC-SA"},
    {"license_key": "CC_BY_ND", "license_value": "CC BY-ND"},
    {"license_key": "CC_BY_NC_ND", "license_value": "CC BY-NC-ND"},
]
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


class SignConventionEnum(str, Enum):
    plus = "+"
    minus = "-"
