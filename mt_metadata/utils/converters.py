from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import json

from pathlib import Path

from mt_metadata.utils.mttime import MTime

from datamodel_code_generator import DataModelType, PythonVersion
from datamodel_code_generator.model import get_data_model_types
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser

STANDARDS_SAVEPATH = Path(__file__).parent.parent.joinpath("standards")
MTMETADATA_SAVEPATH = Path(__file__).parent.parent


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


def get_new_basemodel_filename(filename, save_path=STANDARDS_SAVEPATH):
    """
    Get the new filename json schema

    Parameters
    ----------
    filename : _type_
        _description_
    """

    parts = Path(filename).parts
    index = parts.index("standards") + 1
    new_file_directory = save_path.joinpath("\\".join(parts[index:-1]))
    new_file_directory.mkdir(parents=True, exist_ok=True)
    new_filename = new_file_directory.joinpath(f"{filename.stem}.py")
    return new_filename


def get_new_schema_filename(filename, save_path=MTMETADATA_SAVEPATH):
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
        new["properties"][key]["type"] = value["type"]
        new["properties"][key]["description"] = value["description"]
        new["properties"][key]["title"] = key
        new["properties"][key]["examples"] = value["example"]
        new["properties"][key]["default"] = get_default_value(
            value["type"], default_value=value["default"], required=value["required"]
        )
        new["properties"][key]["alias"] = get_alias_name(value["alias"])
        new["properties"][key]["units"] = value["units"]
        if value["required"]:
            new["required"].append(key)
        # need to sort out string formats
        if value["style"] == "controlled vocabulary":
            new["properties"][key]["enum"] = value["options"]
        if "list" in value["style"]:
            new["properties"][key]["type"] = "array"
            new["properties"][key]["items"] = {}
            new["properties"][key]["items"]["type"] = value["type"]
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


type_dict = {"string": str, "integer": int, "float": float}


def from_jsonschema_to_pydantic_basemodel_homebrew(
    filename: Union[str, Path], **kwargs
) -> Path:
    """
    Create a pydantic basemodel by hand

    Parameters
    ----------
    filename : Union[str, Path]
        _description_

    Returns
    -------
    Path
        _description_
    """
    tab = " " * 4
    filename = Path(filename)
    new_filename = get_new_basemodel_filename(filename)

    with open(filename, "r") as fid:
        schema = json.load(fid)

    lines = [
        "# Imports",
        "from __future__ import annotations",
        "from typing import Annotated",
        "from pydantic import BaseModel, ConfigDict, Field",
        "",
    ]

    class_name = schema["title"]
    lines.append(f"class {class_name}(BaseModel):")
    lines.append(
        f"{tab}model_config = ConfigDict(extra='allow', validate_assignment=True)"
    )
    for field in schema["properties"]:
        required = False
        if field["title"] in schema["required"]:
            required = True

        lines.append(f"{field['title']}: Annotated[]")


def convert_old_standards_to_new_standards():
    """
    Convert all old standards to json schema files
    """
    pass


from typing import Any, Type, Optional
from pydantic import BaseModel, Field, create_model
from enum import Enum


def json_schema_to_base_model(schema: dict[str, Any]) -> Type[BaseModel]:
    type_mapping = {
        "string": str,
        "integer": int,
        "number": float,
        "boolean": bool,
        "array": list,
        "object": dict,
    }

    properties = schema.get("properties", {})
    required_fields = schema.get("required", [])
    model_fields = {}

    for field_name, field_props in properties.items():
        json_type = field_props.get("type", "string")
        enum_values = field_props.get("enum")

        if enum_values:
            enum_name = f"{field_name.capitalize()}Enum"
            field_type = Enum(enum_name, {v: v for v in enum_values})
        else:
            field_type = type_mapping.get(json_type, Any)

        default_value = field_props.get("default", ...)
        nullable = field_props.get("nullable", False)
        description = field_props.get("title", "")

        if nullable:
            field_type = Optional[field_type]

        if field_name not in required_fields:
            default_value = field_props.get("default", None)

        model_fields[field_name] = (
            field_type,
            Field(default_value, description=description),
        )

    return create_model(schema.get("title", "DynamicModel"), **model_fields)
