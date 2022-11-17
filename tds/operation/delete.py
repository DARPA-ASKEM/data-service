"""
Standard objects to use for deletion operations
"""

fastapi_endpoint_config = {
    "responses": {
        404: {"model": str, "description": "The item was not found"},
        204: {"description": "Item deleted by ID"},
    }
}
