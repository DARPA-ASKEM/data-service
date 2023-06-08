"""
Standard objects to use for creation operations
"""

fastapi_endpoint_config = {
    "responses": {
        201: {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {"id": {"type": "integer|string"}},
                    }
                }
            },
            "description": "Item was created",
        },
    }
}
