"""
Validation flow for JSON Schema
"""
import json

import requests
from jsonschema import ValidationError, validate


def validate_json_schema(obj_to_validate: dict, schema_obj: dict | bool = False):
    """
    Function validates the json object based on the associated schema.
    """
    print(obj_to_validate)
    if "schema" not in obj_to_validate and schema_obj is False:
        raise ValidationError(message="No schema provided for validation.")

    schema_request = requests.get(obj_to_validate["schema"])
    schema = json.loads(schema_request.content) if schema_obj is False else schema_obj
    return validate(instance=obj_to_validate, schema=schema)
