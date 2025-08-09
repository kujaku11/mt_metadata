from mt_metadata.common import Software


print("Software field definitions:")
for field_name in Software.model_fields:
    field = Software.model_fields[field_name]
    print(f"{field_name}: {field.annotation} (default: {field.default})")
