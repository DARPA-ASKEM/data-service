from fastapi import APIRouter, Depends, HTTPException, Response, status

from tds.model.model import Model
from tds.operation import create

router = APIRouter()
route_prefix = "mdl"


@router.post("", **create.fastapi_endpoint_config)
def model_post(payload: Model) -> Response:
    """
    Create model and return its ID
    """
    print(payload)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": 1}),
    )
