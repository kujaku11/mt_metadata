from mth5.helpers import add_attributes_to_metadata_class_pydantic

from mt_metadata.timeseries import Run


original_run = Run()
updated_run = add_attributes_to_metadata_class_pydantic(Run)

print(type(original_run))
print(type(updated_run))
print(isinstance(updated_run, Run))  # Should be True
