"""
Converters to convert old JSON schema to new JSON schema and then to pydantic basemodel
and then to pydantic basemodel with types.

"""

import json

# =====================================================
# Imports
# =====================================================
from pathlib import Path
from typing import Any, Dict, Union

import black
import isort
from loguru import logger


# try:
#     from datamodel_code_generator import DataModelType, PythonVersion
#     from datamodel_code_generator.model import get_data_model_types
#     from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
# except ImportError:
#     logger.warning(
#         "datamodel-codegen is not installed. Please install it using 'pip install datamodel-codegen'."
#     )

# =====================================================
# Constants
# =====================================================
# Define the path to the standards directory and the mt_metadata directory
STANDARDS_SAVEPATH = Path(__file__).parent.parent.joinpath("standards")
MTMETADATA_SAVEPATH = Path(__file__).parent.parent

TYPE_MAPPING = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "bool": "bool",
    "array": "List[Any]",
    "object": "Dict[str, Any]",
}

JSON_TYPE_MAPPING = {
    "string": "string",
    "integer": "integer",
    "float": "number",
    "boolean": "boolean",
    "array": "array",
    "object": "object",
    "null": "null",
}
TAB = " " * 4
# =====================================================


def load_json(filename: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a JSON file and return its contents as a dictionary.

    Args:
        filename (Union[str, Path]): The path to the JSON file.

    Returns:
        Dict[str, Any]: The contents of the JSON file as a dictionary.
    """
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def write_json(filename: Union[str, Path], data: Dict[str, Any]) -> None:
    """
    Write a dictionary to a JSON file.

    Args:
        filename (Union[str, Path]): The path to the JSON file.
        data (Dict[str, Any]): The data to write to the file.
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def get_default_value(
    data_type: str, default_value: Any = None, required: bool = False
) -> Any:
    """
    Get default value based on information provided.

    Parameters
    ----------
    data_type : str
        data type name
    default_value : Any, optional
        given default value, by default None
    required : bool, optional
        is required, by default False

    Returns
    -------
    Any
        default value
    """

    if not required:
        return None

    if data_type in ["string"]:
        if default_value is None:
            return ""
        else:
            return f"'{str(default_value)}'"
    elif data_type in ["int"]:
        if default_value is None:
            return 0
        else:
            return int(default_value)
    elif data_type in ["float", "number"]:
        if default_value is None:
            return 0.0
        elif isinstance(default_value, str):
            try:
                return float(default_value)
            except ValueError:
                return 0.0
        elif isinstance(default_value, (list, tuple)):
            return []

        else:
            return float(default_value)
    elif data_type in ["boolean"]:
        return bool(default_value)


def get_alias_name(alias_name: str) -> str:
    """
    Get the alias name, and return None if empty

    Parameters
    ----------
    alias_name : str
        alias name
    """
    if alias_name in [[], None, "", "None", "none"]:
        return None
    else:
        return alias_name


def get_new_basemodel_filename(
    filename: Path | str, save_path: Path = MTMETADATA_SAVEPATH
) -> Path:
    """
    Get new file name for new BaseModel.

    Will place into `mt_metadata/mt_metadata/...`

    Parameters
    ----------
    filename : Path | str
        json schema standards file name
    save_path : Path, optional
        default path to save to, by default MTMETADATA_SAVEPATH

    Returns
    -------
    Path
        new file path to new BaseModel object.
    """
    filename = Path(filename)
    # Get the parts of the filename
    parts = Path(filename).parts
    index = parts.index("standards") + 1
    new_file_directory = save_path.joinpath("\\".join(parts[index:-1]))
    new_file_directory.mkdir(parents=True, exist_ok=True)
    new_filename = new_file_directory.joinpath(f"{filename.stem}_basemodel.py")
    return new_filename


def get_new_schema_filename(
    filename: str | Path, save_path: Path = STANDARDS_SAVEPATH
) -> Path:
    """
    Get new file path to a JSON schema file.  Will be place into
    `mt_metadata/mt_metadata/standards/...`

    Parameters
    ----------
    filename : str | Path
        old JSON file
    save_path : Path, optional
        default directory to save to, by default STANDARDS_SAVEPATH

    Returns
    -------
    Path
        new file path to JSON Schema file.
    """

    parts = Path(filename).parts
    index = parts.index("mt_metadata") + 2
    new_file_directory = save_path.joinpath("\\".join(parts[index:-2]))
    new_file_directory.mkdir(parents=True, exist_ok=True)
    new_filename = new_file_directory.joinpath(filename.name)
    return new_filename


def to_json_schema(filename: str | Path) -> Path:
    """
    Convert old JSON files to a JSON Schema file.

    Parameters
    ----------
    filename : Union[str, Path]
        file path to old JSON file

    Returns
    -------
    Path
        File path to new JSON Schema file

    Raises
    ------
    KeyError
        if `type` is not in old JSON file
    """
    filename = Path(filename)
    old = load_json(filename)
    object_name = filename.stem

    new = {"title": object_name}
    new["type"] = "object"
    new["properties"] = {}
    new["required"] = []
    new["description"] = object_name
    for key, value in old.items():
        new["properties"][key] = {}

        # map type to JSON schema type
        try:
            json_type = JSON_TYPE_MAPPING[value["type"]]
        except KeyError:
            raise KeyError(f"Could not find the type {value['type']} in the type dict.")
        # if the style is a list then use array
        if "list" in value["style"]:
            new["properties"][key]["type"] = "array"
            new["properties"][key]["default"] = []
            new["properties"][key]["items"] = {}
            new["properties"][key]["items"]["type"] = json_type

        else:
            new["properties"][key]["default"] = get_default_value(
                value["type"],
                default_value=value["default"],
                required=value["required"],
            )
        new["properties"][key]["description"] = value["description"]
        new["properties"][key]["title"] = key
        new["properties"][key]["examples"] = value["example"]
        new["properties"][key]["type"] = json_type
        new["properties"][key]["alias"] = get_alias_name(value["alias"])
        new["properties"][key]["units"] = value["units"]
        if value["required"]:
            new["required"].append(key)

        # need to sort out string formats
        if value["style"] == "controlled vocabulary":
            new["properties"][key]["enum"] = value["options"]

        elif value["style"] == "alpha numeric":
            new["properties"][key]["pattern"] = "^[a-zA-Z0-9]*$"

        elif value["style"] in ["date time", "date", "time"]:
            new["properties"][key]["format"] = "date-time"

        elif value["style"] in ["email"]:
            new["properties"][key]["format"] = "email"

        elif value["style"] in ["url"]:
            new["properties"][key]["format"] = "uri"

    # write new file
    new_file = get_new_schema_filename(filename)
    write_json(new_file, new)

    return new_file


# def from_jsonschema_to_pydantic_basemodel(filename: Union[str, Path], **kwargs) -> Path:
#     """
#     make basemodel from json schema

#     Parameters
#     ----------
#     filename : _type_
#         _description_
#     """
#     filename = Path(filename)
#     new_filename = get_new_basemodel_filename(filename, MTMETADATA_SAVEPATH)

#     data_model_types = get_data_model_types(
#         DataModelType.PydanticV2BaseModel,
#         target_python_version=PythonVersion.PY_311,
#         target_datetime_class=MTime,
#     )

#     parser = JsonSchemaParser(
#         filename,
#         data_model_type=data_model_types.data_model,
#         data_model_root_type=data_model_types.root_model,
#         data_model_field_type=data_model_types.field_model,
#         data_type_manager_type=data_model_types.data_type_manager,
#         dump_resolve_reference_action=data_model_types.dump_resolve_reference_action,
#         field_extra_keys=["alias", "units", "default", "required"],
#         use_annotated=True,
#         use_union_operator=True,
#         field_constraints=True,
#         snake_case_field=True,
#         allow_extra_fields=True,
#         strip_default_none=False,
#         field_include_all_keys=True,
#         apply_default_values_for_required_fields=True,
#     )

#     result = parser.parse()

#     with open(new_filename, "w") as fid:
#         fid.write(result)

#     return new_filename


def snake_to_camel(snake_str: str) -> str:
    components = snake_str.split("_")
    camel_case_str = "".join(x.title() for x in components)
    return camel_case_str


type_imports = {
    "List": "from typing import List",
    "Dict": "from typing import Dict",
    "Any": "from typing import Any",
}


def generate_pydantic_basemodel(json_schema_filename: Union[str, Path]) -> str:
    """
    Generate a Pydantic model from a JSON schema file and save it to a Python file.
    The generated model will use `Annotated` and `Field` for type annotations.

    Parameters
    ----------
    json_schema_filename : str | Path
        path to the JSON schema file

    Returns
    -------
    Path
        _description_
    """
    json_schema_filename = Path(json_schema_filename)
    if not json_schema_filename.exists():
        raise FileNotFoundError(f"{json_schema_filename} does not exist.")
    if not json_schema_filename.suffix == ".json":
        raise FileNotFoundError(
            f"{json_schema_filename} is not a json file. Please provide a json file."
        )

    with open(json_schema_filename, "r") as fid:
        schema = json.load(fid)

    new_filename = get_new_basemodel_filename(json_schema_filename, MTMETADATA_SAVEPATH)

    class_definitions = []
    class_name = snake_to_camel(schema.get("title", "GeneratedModel"))

    required_fields = schema.get("required", [])
    properties = schema.get("properties", {})

    imports = ["from typing import Annotated", "from pydantic import Field"]

    datetime_keys = []
    enum_lines = []
    has_comment = False
    has_units = False
    # Create field definitions
    for field_name, field_attrs in properties.items():
        if field_name in ["units", "unit"]:
            has_units = True
        # Check if the field is a comment
        elif field_name in ["comments", "comment"]:
            has_comment = True
            field_type = "Comment"
            imports.append("from mt_metadata.common import Comment")
            field_attrs["default_factory"] = "lambda: Comment()"
            # class_definitions.append(f"{TAB}{field_name}: {field_type}")

            # continue
        # Fallback to Any if type is unknown
        else:
            field_type = TYPE_MAPPING.get(field_attrs.get("type", "string"), "Any")
        # get typing imports
        for type_key in type_imports.keys():
            if type_key in field_type:
                imports.append(type_imports[type_key])

        # if date time then use MTime as the object, need to add some types
        # a default factory.
        if field_attrs.get("format") == "date-time":
            field_type = "MTime | str | float | int | np.datetime64 | pd.Timestamp"
            imports.append("import numpy as np")
            imports.append("import pandas as pd")
            imports.append("from mt_metadata.common.mttime import MTime")
            field_attrs["default_factory"] = "lambda: MTime(time_stamp=None)"
            datetime_keys.append(field_name)

        # if email format the use EmailStr object and import
        elif field_attrs.get("format") == "email":
            field_type = "EmailStr"
            imports.append("from pydantic import EmailStr")
        # if uri format the use HttpUrl object and import
        elif field_attrs.get("format") == "uri":
            field_type = "HttpUrl"
            imports.append("from pydantic import HttpUrl")

        # enumerated types
        if field_attrs.get("enum", None) is not None:
            # Convert enum list to a string representation
            enum_lines.append(f"class {snake_to_camel(field_name)}Enum(str, Enum):")
            for enum_value in field_attrs["enum"]:
                enum_lines.append(
                    f"{TAB}{enum_value.replace(' ', '_')} = '{enum_value}'"
                )
            imports.append("from enum import Enum")
            field_type = f"{snake_to_camel(field_name)}Enum"

        # check if required.  Again required is a metadata standard not
        # a pydantic standard. If required in pydantic then the user
        # must supply a default value.  Which is not the older way
        # mt-metadata was used, and not the desired way of using it.
        field_attrs["required"] = True
        if field_name not in required_fields:
            if "Comment" in field_type:
                field_type = "Comment"
            else:
                field_type = f"{field_type} | None"
            field_attrs["required"] = False

        # get the default value based on type
        field_default = get_default_value(
            field_attrs["type"],
            default_value=field_attrs["default"],
            required=field_name in required_fields,
        )
        # "" is skipped by pydantic need to set it at "''"
        if field_default in [""]:
            field_default = "''"
        elif isinstance(field_default, str) and "''" in field_default:
            field_default = field_default.replace("''", '"')
            if field_default == '"':
                field_default = '""'

        # Use Annotated with Field
        field_definition = f"{TAB}{field_name}: Annotated[{field_type}, Field("
        field_parts = [field_definition]

        # Add attributes to Field
        if field_attrs.get("default_factory", None) is None:
            field_parts.append(f"{TAB}default={field_default},")
        else:
            field_parts.append(
                f"{TAB}default_factory={field_attrs['default_factory']},"
            )

        # need to add json_schema_extra attributes [units, required]
        json_schema_extra = {}
        for attr_name, attr_value in field_attrs.items():
            if attr_name in [
                "default",
                "title",
                "format",
                "enum",
                "type",
                "default_factory",
            ]:
                continue
            elif attr_name in ["examples"]:
                attr_value = [attr_value]
                # newer versions of pydantic use examples in json_schema_extra
                # field_parts.append(f"{TAB}{attr_name}={repr(attr_value)},")
                json_schema_extra["examples"] = repr(attr_value)
            elif attr_name in ["units", "required"]:
                json_schema_extra[attr_name] = attr_value

            else:
                field_parts.append(f"{TAB}{attr_name}={repr(attr_value)},")

        # Add json_schema_extra as a dictionary
        if json_schema_extra:
            json_extra_line = f"{TAB}json_schema_extra=" + "{"
            for jkey, jvalue in json_schema_extra.items():
                json_extra_line += f"'{jkey}':{repr(jvalue)},"
        json_extra_line += "},\n"
        field_parts.append(json_extra_line)

        # if field_attrs["required"]:
        field_parts.append(f"{TAB})]\n")
        # else:
        #     field_parts.append(f")] = {field_default}\n")

        class_definitions.append("\n".join(field_parts))

    if datetime_keys:
        imports.append("from pydantic import field_validator")
        for key in datetime_keys:
            class_definitions.append(
                f"{TAB}@field_validator('{key}', mode='before')\n"
                f"{TAB}@classmethod\n"
                f"{TAB}def validate_{key}(cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str):\n"
                f"{TAB*2}return MTime(time_stamp=field_value)\n"
            )

    if has_comment:
        class_definitions.append(
            f"{TAB}@field_validator('comments', mode='before')\n"
            f"{TAB}@classmethod\n"
            f"{TAB}def validate_comments(cls, value, info: ValidationInfo) -> Comment:\n"
            f"{TAB*2}if isinstance(value, str):\n"
            f"{TAB*3}return Comment(value=value)\n"
            f"{TAB*2}return value\n"
        )

        imports.append("from pydantic import field_validator, ValidationInfo")

    if has_units:
        print(f"adding units to {new_filename}")
        class_definitions.append(
            f"{TAB}@field_validator('units', mode='before')\n"
            f"{TAB}@classmethod\n"
            f"{TAB}def validate_units(cls, value: str) -> str:\n"
            f"{TAB*2}if value in [None, '']:\n"
            f"{TAB*3}return ''\n"
            f"{TAB*2}try:\n"
            f"{TAB*3}unit_object = get_unit_object(value)\n"
            f"{TAB*3}return unit_object.name\n"
            f"{TAB*2}except ValueError as error:\n"
            f"{TAB*3}raise KeyError(error)\n"
            f"{TAB*2}except KeyError as error:\n"
            f"{TAB*3}raise KeyError(error)\n"
        )
        imports.append("from mt_metadata.common.units import get_unit_object")
        imports.append("from pydantic import field_validator, ValidationInfo")

    # Generate the class definition, dont need config dict as that is
    # already initiated in MetadataBase.
    class_code = [
        f"class {class_name}(MetadataBase):",
        "\n".join(class_definitions) or f"{TAB}pass",
    ]

    imports = "\n".join(imports)
    lines = [
        "#=====================================================",
        "# Imports",
        "#=====================================================",
        f"{imports}",
        "from mt_metadata.base import MetadataBase",
        "#=====================================================",
    ]

    lines += enum_lines
    lines += class_code
    line = "\n".join(lines)

    return clean_and_format_code(line, new_filename)


def clean_and_format_code(code_str: str, filename: str | Path | None = None) -> str:
    """
    Clean and format Python code by removing unused imports and formatting with isort and black.

    Parameters
    ----------
    code_str : str
        Python code as a string
    filename : str, optional
        Filename for error reporting, by default None

    Returns
    -------
    str
        Cleaned and formatted code
    """
    # First, remove unused imports using autoflake
    try:
        import autoflake

        code_str = autoflake.fix_code(
            code_str,
            remove_all_unused_imports=True,
            remove_unused_variables=False,
            expand_star_imports=True,
        )
    except ImportError:
        logger.warning(
            "autoflake is not installed. Unused imports will not be removed. "
            "Install with 'pip install autoflake'."
        )
    except Exception as error:
        if filename:
            logger.warning(f"{filename} Error removing unused imports: {error}")
        else:
            logger.warning(f"Error removing unused imports: {error}")

    # Then format using isort
    try:
        import_config = {
            "force_single_line": False,  # One import per line
            "force_alphabetical_sort_within_sections": True,  # Sort alphabetically within sections
            "order_by_type": True,  # Order by import type
            "sections": ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"],
            "lines_after_imports": 2,  # Add 2 blank lines after imports
        }

        code_str = isort.code(code_str, **import_config)
    except Exception as error:
        if filename:
            logger.warning(f"{filename} Error formatting code using isort: {error}")
        else:
            logger.warning(f"Error formatting code using isort: {error}")

    # Finally format using black
    try:
        code_str = black.format_str(code_str, mode=black.FileMode())
    except Exception as error:
        if filename:
            logger.warning(f"{filename} Error formatting code using black: {error}")
        else:
            logger.warning(f"Error formatting code using black: {error}")

    # Write the formatted code back to the file
    if filename is not None:
        with open(filename, "w") as f:
            f.write(code_str)

    return code_str


def reformat(filename: str | Path) -> str:
    """
    Reformat a Python file by removing unused imports and formatting with isort and black.

    Parameters
    ----------
    filename : str | Path
        Path to the Python file to be reformatted
    """
    filename = Path(filename)
    if not filename.exists():
        raise FileNotFoundError(f"{filename} does not exist.")

    with open(filename, "r") as f:
        code_str = f.read()

    # Clean and format the code
    return clean_and_format_code(code_str, filename)
