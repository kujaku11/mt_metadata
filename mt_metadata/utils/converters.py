"""
Converters to convert old JSON schema to new JSON schema and then to pydantic basemodel
and then to pydantic basemodel with types.

"""

# =====================================================
# Imports
# =====================================================
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import json
import black

from pathlib import Path

from mt_metadata.utils.mttime import MTime

from pathlib import Path
import json
from pydantic import BaseModel, Field
from typing import Annotated, Optional, List, Dict, Any, Union

try:
    from datamodel_code_generator import DataModelType, PythonVersion
    from datamodel_code_generator.model import get_data_model_types
    from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
except ImportError:
    print(
        "datamodel-codegen is not installed. Please install it using 'pip install datamodel-codegen'."
    )

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
    "array": "List[Any]",
    "object": "Dict[str, Any]",
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


def get_default_value(data_type, default_value=None, required=False):
    """
    get default value based on the data type

    Parameters
    ----------
    data_type : _type_
        _description_
    default_value : _type_, optional
        _description_, by default None
    """

    if not required:
        return None

    if data_type in ["string"]:
        if default_value is None:
            return ""
        else:
            return str(default_value)
    elif data_type in ["int"]:
        if default_value is None:
            return 0
        else:
            return int(default_value)
    elif data_type in ["float"]:
        if default_value is None:
            return 0.0
        else:
            return float(default_value)
    elif data_type in ["boolean"]:
        return bool(default_value)


def get_alias_name(alias_name):
    """
    Get the alias name, and return None if empty

    Parameters
    ----------
    alias_name : _type_
        _description_
    """
    if alias_name in [[], None, "", "None", "none"]:
        return None
    else:
        return alias_name


def get_new_basemodel_filename(filename, save_path=MTMETADATA_SAVEPATH):
    """
    Get the new filename json schema

    Parameters
    ----------
    filename : _type_
        _description_
    """
    filename = Path(filename)
    # Get the parts of the filename
    parts = Path(filename).parts
    index = parts.index("standards") + 1
    new_file_directory = save_path.joinpath("\\".join(parts[index:-1]))
    new_file_directory.mkdir(parents=True, exist_ok=True)
    new_filename = new_file_directory.joinpath(f"{filename.stem}_basemodel.py")
    return new_filename


def get_new_schema_filename(filename, save_path=STANDARDS_SAVEPATH):
    """
    Get the new filename for pydantic python file

    Parameters
    ----------
    filename : _type_
        _description_
    """

    parts = Path(filename).parts
    index = parts.index("mt_metadata") + 2
    new_file_directory = save_path.joinpath("\\".join(parts[index:-2]))
    new_file_directory.mkdir(parents=True, exist_ok=True)
    new_filename = new_file_directory.joinpath(filename.name)
    return new_filename


def to_json_schema(filename: Union[str, Path]) -> Dict[str, Any]:
    """
    Convert a dictionary to a JSON schema.

    Args:
        data (Dict[str, Any]): The data to convert.

    Returns:
        Dict[str, Any]: The JSON schema.
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
        if "list" in value["style"]:
            new["properties"][key]["type"] = "array"
            new["properties"][key]["default"] = []
            new["properties"][key]["items"] = {}
            new["properties"][key]["items"]["type"] = value["type"]
        else:
            new["properties"][key]["type"] = value["type"]
            new["properties"][key]["default"] = get_default_value(
                value["type"],
                default_value=value["default"],
                required=value["required"],
            )
        new["properties"][key]["description"] = value["description"]
        new["properties"][key]["title"] = key
        new["properties"][key]["examples"] = value["example"]

        new["properties"][key]["alias"] = get_alias_name(value["alias"])
        new["properties"][key]["units"] = value["units"]
        if value["required"]:
            new["required"].append(key)
        # need to sort out string formats
        if value["style"] == "controlled vocabulary":
            new["properties"][key]["enum"] = value["options"]

        if "alpha numeric" in value["style"]:
            new["properties"][key]["pattern"] = "^[a-zA-Z0-9]*$"

    new_file = get_new_schema_filename(filename)
    write_json(new_file, new)

    return new_file


def from_jsonschema_to_pydantic_basemodel(filename: Union[str, Path], **kwargs) -> Path:
    """
    make basemodel from json schema

    Parameters
    ----------
    filename : _type_
        _description_
    """
    filename = Path(filename)
    new_filename = get_new_basemodel_filename(filename, MTMETADATA_SAVEPATH)

    data_model_types = get_data_model_types(
        DataModelType.PydanticV2BaseModel,
        target_python_version=PythonVersion.PY_311,
        target_datetime_class=MTime,
    )

    parser = JsonSchemaParser(
        filename,
        data_model_type=data_model_types.data_model,
        data_model_root_type=data_model_types.root_model,
        data_model_field_type=data_model_types.field_model,
        data_type_manager_type=data_model_types.data_type_manager,
        dump_resolve_reference_action=data_model_types.dump_resolve_reference_action,
        field_extra_keys=["alias", "units", "default", "required"],
        use_annotated=True,
        use_union_operator=True,
        field_constraints=True,
        snake_case_field=True,
        allow_extra_fields=True,
        strip_default_none=False,
        field_include_all_keys=True,
        apply_default_values_for_required_fields=True,
    )

    result = parser.parse()

    with open(new_filename, "w") as fid:
        fid.write(result)

    return new_filename


def generate_pydantic_basemodel(json_schema_filename: Union[str, Path]) -> Path:
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
    class_name = schema.get("title", "GeneratedModel").capitalize()

    required_fields = schema.get("required", [])
    properties = schema.get("properties", {})

    # Create field definitions
    for field_name, field_attrs in properties.items():
        # Fallback to Any if type is unknown
        field_type = TYPE_MAPPING.get(field_attrs.get("type", "string"), "Any")
        field_attrs["required"] = True
        if field_name not in required_fields:
            field_type = f"{field_type} | None"
            field_attrs["required"] = False

        field_default = get_default_value(
            field_attrs["type"],
            default_value=field_attrs["default"],
            required=field_name in required_fields,
        )
        if field_default in [""]:
            field_default = "''"

        # Use Annotated with Field
        field_definition = f"{TAB}{field_name}: Annotated[{field_type}, Field("
        field_parts = [field_definition]

        # Add attributes to Field
        field_parts.append(f"{TAB}default={field_default},")
        ## need to add json_schema_extra attributes [units, required]
        json_schema_extra = {}
        for attr_name, attr_value in field_attrs.items():
            if attr_name in ["default"]:
                continue
            elif attr_name in ["units", "required"]:
                json_schema_extra[attr_name] = attr_value
            else:
                field_parts.append(f"{TAB}{attr_name}={repr(attr_value)},")
        field_parts.append(f"{TAB}json_schema_extra=" + "{")
        for jkey, jvalue in json_schema_extra.items():
            field_parts.append(f"{jkey}={jvalue}")
        field_parts.append("}")

        if field_attrs["required"]:
            field_parts.append(")]\n")
        else:
            field_parts.append(f")] = {field_default}\n")

        class_definitions.append("\n".join(field_parts))

    # Generate the class definition
    class_code = [
        f"class {class_name}(MetadataBase):",
        f"{TAB}model_config = ConfigDict(validate_assignment=True, ",
        "coerce_numbers_to_str=True, validate_default=True)",
        "\n".join(class_definitions) or f"{TAB}pass",
    ]

    lines = [
        "#=====================================================",
        "# Imports",
        "#=====================================================",
        "from pydantic import BaseModel, Field, ConfigDict",
        "from typing import Annotated, Optional, List, Dict, Any\n",
        # "from mt_metadata.base import MetadataBase",
        "",
        "#=====================================================",
    ]
    lines += class_code
    line = "\n".join(lines)

    # Format the code using black
    # This will format the code according to PEP 8 style guide
    try:
        line = black.format_str(line, mode=black.FileMode())
    except Exception as error:
        print(f"{json_schema_filename.name} Error formatting code: {error}")

    # Write to output file
    with open(new_filename, "w") as f:
        f.write(line)

    print(f"Saved to {new_filename}")
    return new_filename
