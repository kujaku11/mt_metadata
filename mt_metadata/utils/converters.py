from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import json

SAVEPATH = Path(__file__).parent.parent.joinpath("standards")


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


def get_new_file_path(filename, save_path=SAVEPATH):
    """
    Get the new filename

    Parameters
    ----------
    filename : _type_
        _description_
    """

    parts = Path(filename).parts
    index = parts.index("mt_metadata") + 2
    new_file_path = save_path.joinpath("\\".join(parts[index:-2]))
    new_file_path.mkdir(parents=True, exist_ok=True)
    return new_file_path


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

    new_file = get_new_file_path(filename).joinpath(f"{object_name}_schema.json")
    write_json(new_file, new)

    return new_file
