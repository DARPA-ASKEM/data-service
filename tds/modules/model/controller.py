"""
TDS Model Controller.
"""
from logging import Logger
from typing import Any, Dict

from elasticsearch import NotFoundError
from elasticsearch import exceptions as es_exceptions
from fastapi import APIRouter, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from tds.db import es_client
from tds.modules.model.model import Model
from tds.modules.model.model_description import ModelDescription
from tds.modules.model.utils import (
    model_list_fields,
    model_list_response,
    model_response,
)
from tds.modules.model_configuration.model import ModelConfiguration
from tds.modules.model_configuration.response import (
    ModelConfigurationResponse,
    configuration_response,
)
from tds.operation import create, delete, retrieve, update

model_router = APIRouter()
logger = Logger(__name__)
es_index = Model.index

es = es_client()


@model_router.get(
    "/descriptions",
    response_model=list[ModelDescription],
    **retrieve.fastapi_endpoint_config,
)
def list_models(page_size: int = 100, page: int = 0) -> JSONResponse:
    """
    Retrieve the list of models from ES.
    """
    list_body = {
        "size": page_size,
        "source_excludes": ["model", "semantics"],
    }
    if page != 0:
        list_body["from"] = page
    res = es.search(index=es_index, **list_body)

    list_response = (
        model_list_response(res["hits"]["hits"]) if res["hits"]["hits"] else []
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=list_response,
    )


@model_router.post(
    "/search",
    response_model=list[ModelDescription],
    **retrieve.fastapi_endpoint_config,
)
# pylint: disable=dangerous-default-value
def search_models(
    payload: Dict[str, Any] = {"match_all": {}},
    page_size: int = 100,
    page: int = 0,
) -> JSONResponse:
    """
    Search models by providing any valid Elasticsearch query.
    These may include `match` queries, `term` queries, etc.
    """
    list_body = {
        "size": page_size,
        "source_excludes": ["model", "semantics"],
        "query": payload,
    }
    if page != 0:
        list_body["from_"] = page
    try:
        res = es.search(index=es_index, **list_body)
    except es_exceptions.RequestError as es_exception:
        return JSONResponse(
            headers={
                "content-type": "application/json",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
            content=str(es_exception.error()),
        )

    list_response = (
        model_list_response(res["hits"]["hits"]) if res["hits"]["hits"] else []
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=list_response,
    )


@model_router.post("", **create.fastapi_endpoint_config)
def model_post(payload: Model) -> JSONResponse:
    """
    Create model and return its ID
    """

    res = payload.create()
    logger.info("new model created: %s", res["_id"])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content={"id": res["_id"]},
    )


@model_router.get("/{model_id}/descriptions", **retrieve.fastapi_endpoint_config)
def model_descriptions_get(model_id: str) -> JSONResponse | Response:
    """
    Retrieve a model 'description' from ElasticSearch
    """
    try:
        res = es.get(index=es_index, id=model_id)
        logger.info("model retrieved for description: %s", model_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=model_response(res, delete_fields=["model", "model_version"]),
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@model_router.get(
    "/{model_id}/model_configurations",
    response_model=list[ModelConfigurationResponse],
    **retrieve.fastapi_endpoint_config,
)
def model_configurations_get(
    model_id: str,
    page_size: int = 10,
    page: int = 0,
) -> JSONResponse | Response:
    """
    Retrieve a model 'description' from ElasticSearch
    """
    try:
        query = {
            "term": {"model_id": {"value": model_id}},
        }
        res = es.search(
            index=ModelConfiguration.index,
            query=query,
            from_=page,
            size=page_size,
            sort="timestamp:desc",
        )
        logger.info("model retrieved for description: %s", model_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=jsonable_encoder(configuration_response(res["hits"]["hits"])),
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@model_router.get(
    "/{model_id}/parameters", deprecated=True, **retrieve.fastapi_endpoint_config
)
def model_parameters_get(model_id: str) -> JSONResponse | Response:
    """
    Function retrieves a Model's parameters.
    """
    try:
        res = es.get(index=es_index, id=model_id, source_includes=["model.parameters"])
        logger.info("model retrieved for params: %s", model_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=res["_source"]["model"]["parameters"],
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@model_router.get("/{model_id}", **retrieve.fastapi_endpoint_config)
def model_get(model_id: str) -> JSONResponse | Response:
    """
    Retrieve a model from ElasticSearch
    """
    try:
        res = es.get(index=es_index, id=model_id)
        logger.info("model retrieved: %s", model_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
            content=model_response(res),
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


@model_router.put("/{model_id}", **update.fastapi_endpoint_config)
def model_put(model_id: str, payload: Model) -> JSONResponse:
    """
    Update a model in ElasticSearch
    """
    if payload.id != model_id:
        raise HTTPException(
            status_code=422, detail="ID in request URL and in payload must match."
        )
    res = payload.save()
    logger.info("model updated: %s", model_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content={"id": res["_id"]},
    )


@model_router.delete("/{model_id}", **delete.fastapi_endpoint_config)
def model_delete(model_id: str) -> Response:
    """
    Function deletes a TDS Model from ElasticSearch.
    """
    try:
        res = es.delete(index=es_index, id=model_id)

        if res["result"] != "deleted":
            logger.error("Failed to delete model: %s", model_id)
            raise Exception(
                f"Failed to delete model. ElasticSearch Response: {res['result']}"
            )

        logger.info("Model successfully deleted: %s", model_id)
        return Response(
            status_code=status.HTTP_200_OK,
            headers={
                "content-type": "application/json",
            },
        )
    except NotFoundError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={
                "content-type": "application/json",
            },
        )


# @TODO: Refactor this code to work with new AMR model representation in ES.
# @router.post("/opts/{model_operation}", **create.fastapi_endpoint_config)
# def model_opt(
#     payload: ModelOptPayload,
#     model_operation: enums.ModelOperations,
#     rdb: Engine = Depends(request_rdb),
#     graph_db=Depends(request_graph_db),
# ) -> Response:
#     """
#     Make modeling operations.
#     """
#     with Session(rdb) as session:
#         payload = payload.dict()
#         l_model = session.query(orm.ModelDescription).get(payload.get("left"))
#         if payload.get("right", False):
#             r_model = session.query(orm.ModelDescription).get(payload.get("right"))
#
#         if model_operation == "copy":
#             state = orm.ModelState(
#                 content=session.query(orm.ModelState)
#                 .get(payload.get("left"))
#                 .__dict__.get("content")
#             )
#
#         elif model_operation in ("decompose", "glue"):
#             state = orm.ModelState(content=payload.get("content"))
#         else:
#             raise HTTPException(status_code=400, detail="Operation not supported")
#
#         session.add(state)
#         session.commit()
#
#         # add new model
#         new_model = orm.ModelDescription(
#             name=payload.get("name"),
#             description=payload.get("description"),
#             framework=payload.get("framework"),
#             state_id=state.id,
#         )
#         session.add(new_model)
#         session.commit()
#
#         # add parameters to new model. Default to left model id parameters.
#         if payload.get("parameters") is None:
#             parameters: List[dict] = (
#                 session.query(orm.ModelParameter)
#                 .filter(orm.ModelParameter.model_id == payload.get("left"))
#                 .all()
#             )
#             payload["parameters"] = []
#             for parameter in parameters:
#                 payload["parameters"].append(parameter.__dict__)
#
#         for param in payload.get("parameters"):
#             session.add(
#                 orm.ModelParameter(
#                     model_id=new_model.id,
#                     name=param.get("name"),
#                     default_value=param.get("default_value"),
#                     type=param.get("type"),
#                     state_variable=param.get("state_variable"),
#                 )
#             )
#         session.commit()
#
#         if settings.NEO4J_ENABLED:
#             provenance_handler = ProvenanceHandler(rdb=rdb, graph_db=graph_db)
#             prov_payload = Provenance(
#                 left=state.id,
#                 left_type="ModelRevision",
#                 right=l_model.state_id,
#                 right_type="ModelRevision",
#                 relation_type=model_opt_relationship_mapping[model_operation],
#                 user_id=payload.get("user_id", None),
#                 concept=".",
#             )
#             provenance_handler.create_entry(prov_payload)
#
#             if model_operation == "glue" and payload.get("right", False):
#                 prov_payload = Provenance(
#                     left=state.id,
#                     left_type="ModelRevision",
#                     right=r_model.state_id,
#                     right_type="ModelRevision",
#                     relation_type=model_opt_relationship_mapping[model_operation],
#                     user_id=payload.get("user_id", None),
#                     concept=".",
#                 )
#                 provenance_handler.create_entry(prov_payload)
#
#             # add begins at relationship
#             prov_payload = Provenance(
#                 left=new_model.id,
#                 left_type="Model",
#                 right=state.id,
#                 right_type="ModelRevision",
#                 relation_type="BEGINS_AT",
#                 user_id=payload.get("user_id", None),
#                 concept=".",
#             )
#             provenance_handler.create_entry(prov_payload)
#
#             # get recently added parameters for the new model
#             parameters: Query[orm.ModelParameter] = session.query(
#                 orm.ModelParameter
#             ).filter(orm.ModelParameter.model_id == new_model.id)
#
#             created_parameters = orm_to_params(list(parameters))
#             # add ModelParameter nodes
#             for parameter in created_parameters:
#                 payload = Provenance(
#                     left=parameter.get("id"),
#                     left_type="ModelParameter",
#                     right=new_model.state_id,
#                     right_type="ModelRevision",
#                     relation_type="PARAMETER_OF",
#                     user_id=None,
#                     concept=".",
#                 )
#                 provenance_handler.create_entry(payload)
#
#     logger.info("new model created: %i", id)
#     return Response(
#         status_code=status.HTTP_201_CREATED,
#         headers={
#             "content-type": "application/json",
#         },
#         content=json.dumps({"id": new_model.id}),
#     )
