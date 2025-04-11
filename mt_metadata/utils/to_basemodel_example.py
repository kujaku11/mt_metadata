"""
Convert a JSON schema to a Pydantic model using the `pydantic` library.
This script reads a JSON schema file, generates a Pydantic model with type annotations,
and saves it to a Python file.

It also formats the generated code using `black`.

"""

# =====================================================
# Imports
# =====================================================
from pathlib import Path
import json
import subprocess
from pydantic import BaseModel, Field
from typing import Annotated, Optional, List, Dict, Any, Union

# =====================================================
# Map JSON Schema types to Python types
TYPE_MAPPING = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "array": "List[Any]",
    "object": "Dict[str, Any]",
}
TAB = " " * 4


def generate_pydantic_model_with_types(json_schema_path: str) -> Path:
    """
    Generate a Pydantic model from a JSON schema file and save it to a Python file.
    The generated model will use `Annotated` and `Field` for type annotations.

    Parameters
    ----------
    json_schema_path : str
        path to the JSON schema file

    Returns
    -------
    Path
        _description_
    """
    with open(json_schema_path, "r") as f:
        schema = json.load(f)

    class_definitions = []
    class_name = schema.get("title", "GeneratedModel").capitalize()

    required_fields = schema.get("required", [])
    properties = schema.get("properties", {})

    # Create field definitions
    for field_name, field_attrs in properties.items():
        field_type = TYPE_MAPPING.get(
            field_attrs.get("type", "string"), "Any"
        )  # Fallback to Any if type is unknown
        if field_name not in required_fields:
            field_type = f"Optional[{field_type}]"

        field_default = field_attrs["default"]
        if field_default in [None, ""]:
            field_default = "None"

        # Use Annotated with Field
        field_definition = f"{TAB}{field_name}: Annotated[{field_type}, Field("
        field_parts = [field_definition]

        # Add attributes to Field
        field_parts.append(f"{TAB}default={field_default},")
        for attr_name, attr_value in field_attrs.items():
            if attr_name in ["default"]:
                continue
            # if attr_value is not None:  # Skip if attribute is None
            field_parts.append(f"{TAB}{attr_name}={repr(attr_value)},")
        field_parts.append(")]\n")

        class_definitions.append("\n".join(field_parts))

    # Generate the class definition
    class_code = [
        f"class {class_name}(BaseModel):",
        f"{TAB}model_config = ConfigDict(validate_assignment=True, extras='allow', coerce_numbers_to_str=True)",
        "\n".join(class_definitions) or "    pass",
    ]

    # Write to output file
    with open(output_path, "w") as f:
        f.write("from pydantic import BaseModel, Field, ConfigDict\n")
        f.write("from typing import Annotated, Optional, List, Dict, Any\n\n")
        f.write("\n".join(class_code))

    subprocess.run(["black", output_path])
    print(
        f"Pydantic model with Annotated and types generated and saved to {output_path}"
    )


# Example usage
generate_pydantic_model_with_types(
    r"C:\Users\jpeacock\OneDrive - DOI\Documents\GitHub\mt_metadata\mt_metadata\standards\timeseries\person_schema.json",
    r"C:\Users\jpeacock\OneDrive - DOI\Documents\GitHub\mt_metadata\mt_metadata\timeseries\person_schema.py",
)
