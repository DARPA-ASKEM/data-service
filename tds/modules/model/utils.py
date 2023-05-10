from typing import List


def orm_to_params(parameters: List):
    """
    Convert SQL parameter search to dict
    """
    return [
        {
            "id": param.id,
            "name": param.name,
            "type": jsonable_encoder(param.type),
            "default_value": param.default_value,
            "state_variable": param.state_variable,
        }
        for param in parameters
    ]
