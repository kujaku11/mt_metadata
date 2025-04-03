from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import json


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
        new["properties"][key]["default"] = value["default"]
        new["properties"][key]["alias"] = value["alias"]
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

    new_file = filename.parent.joinpath(f"{object_name}_schema.json")
    write_json(new_file, new)

    return new_file
