from pathlib import Path

from datamodel_code_generator import DataModelType, PythonVersion
from datamodel_code_generator.model import get_data_model_types
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser

from mt_metadata.common.mttime import MTime


filename: Path = Path(
    r"C:\Users\jpeacock\OneDrive - DOI\Documents\GitHub\mt_metadata\mt_metadata\standards\timeseries\person_schema.json"
)

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
    field_extra_keys=["alias", "units", "default"],
    use_annotated=True,
    use_union_operator=True,
    field_constraints=True,
    snake_case_field=True,
    allow_extra_fields=True,
    strip_default_none=False,
    field_include_all_keys=True,
)

result = parser.parse()

with open(filename.parent.joinpath(f"{filename.stem}.py"), "w") as fid:
    fid.write(result)
