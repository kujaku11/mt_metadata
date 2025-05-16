# =====================================================
# Imports
# =====================================================
import json
from enum import Enum, EnumMeta
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


class SignConventionEnum(str, Enum):
    plus = "+"
    minus = "-"
    exp_plus = "exp (+iwt)"


## This is a better way to making an pydantic type of enumeration with a validator
class LicenseEnumMeta(EnumMeta):
    """Metaclass to dynamically load license data when the enum is defined"""

    def __new__(metacls, cls, bases, classdict):
        # Create the enum class first
        enum_class = super().__new__(metacls, cls, bases, classdict)

        # Load the licenses JSON file
        filename = Path(__file__).parent.parent.joinpath("data", "licenses.json")
        with open(filename, "r") as fid:
            licenses = json.load(fid)

        # Add base licenses
        base_licenses = [
            ("CC_0", "CC0"),
            ("CC0", "CC0"),
            ("CC_BY", "CC BY"),
            ("CC_BY_SA", "CC BY-SA"),
            ("CC_BY_NC", "CC BY-NC"),
            ("CC_BY_NA_SA", "CC BY-NC-SA"),
            ("CC_BY_ND", "CC BY-ND"),
            ("CC_BY_NC_ND", "CC BY-NC-ND"),
        ]

        # Create dynamic enum members
        member_dict = {}
        for key, value in base_licenses:
            member_dict[key] = value

        # Add licenses from JSON file
        for license in licenses["licenses"]:
            key = (
                license["licenseId"]
                .replace("-", "_")
                .replace(" ", "_")
                .replace(".", "_")
                .replace("(", "_")
                .replace(")", "_")
                .replace("/", "_")
                .replace(":", "_")
            )
            value = license["licenseId"]
            member_dict[key] = value

        # Now create the actual enum
        return Enum(enum_class.__name__, member_dict)


class LicenseEnum(str, Enum, metaclass=LicenseEnumMeta):
    """
    Enumeration of software licenses.
    Dynamically loaded from JSON data.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: type[Enum], handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(cls._validate)

    @classmethod
    def _validate(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"Expected string, got {type(value)}")

        # Check if the value is a valid license
        for member in cls:
            if member.value == value:
                return value

        # Handle case insensitivity or slight variations
        value_normalized = value.upper().replace("-", "_").replace(" ", "_")
        for member in cls:
            member_normalized = member.value.upper().replace("-", "_").replace(" ", "_")
            if member_normalized == value_normalized:
                return member.value

        raise ValueError(
            f"Invalid license: {value}. Must be one of the valid licenses."
        )
