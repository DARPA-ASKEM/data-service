"""
Validation flow for JSON Schema
"""
import json

import requests
from jsonschema import ValidationError, validate


def validate_json_schema(
    obj_to_validate: dict, schema_key: str = None, schema_obj: dict | bool = False
):
    """
    Function validates the json object based on the associated schema.
    """
    key = schema_key if schema_key else "schema"

    if key != "schema":
        obj_to_validate["schema"] = obj_to_validate[key]
        del obj_to_validate[key]

    schema_url = obj_to_validate["schema"]
    print(f"Using {schema_url} to validate object.")

    if "schema" not in obj_to_validate and schema_obj is False:
        raise ValidationError(message="No schema provided for validation.")

    schema_request = requests.get(obj_to_validate["schema"])
    schema = json.loads(schema_request.content) if schema_obj is False else schema_obj

    return validate(instance=obj_to_validate, schema=schema)
