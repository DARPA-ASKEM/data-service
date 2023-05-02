"""
CRUD operations for datasets and related tables in the DB
"""

import json
import os
from collections import defaultdict
from logging import DEBUG, Logger
from typing import List, Optional

import pandas
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import StreamingResponse
from sqlalchemy import or_
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm, schema
from tds.db import entry_exists, list_by_id, request_rdb
from tds.lib.datasets import create_qualifier_xref
from tds.lib.storage import get_rawfile, prepare_csv, put_rawfile
from tds.operation import create, delete, retrieve, update

logger = Logger(__file__)
logger.setLevel(DEBUG)
router = APIRouter()


@router.get("/features")
def get_features(
    page_size: int = 100, page: int = 0, rdb: Engine = Depends(request_rdb)
):
    """
    Get a specified number of features
    """
    return list_by_id(rdb.connect(), orm.Feature, page_size, page)


@router.get("/features/{id}", **retrieve.fastapi_endpoint_config)
def get_feature(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific feature by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.Feature).get(id)
        return result


@router.post("/features", **create.fastapi_endpoint_config)
def create_feature(payload: schema.Feature, rdb: Engine = Depends(request_rdb)):
    """
    Create a feature
    """
    with Session(rdb) as session:
        featurep = payload.dict()
        del featurep["id"]
        feature = orm.Feature(**featurep)
        feature_result = session.query(orm.Feature).filter_by(**featurep).first()
        if feature_result is not None:
            featurep["id"] = feature_result.id
            return Response(
                status_code=status.HTTP_200_OK,
                headers={
                    "content-type": "application/json",
                },
                content=json.dumps(featurep),
            )
        session.add(feature)
        session.commit()
        data_id = feature.id
        featurep["id"] = data_id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "content-type": "application/json",
            },
            content=json.dumps(featurep),
        )


@router.patch("/features/{id}", **update.fastapi_endpoint_config)
def update_feature(
    payload: schema.Feature, id: int, rdb: Engine = Depends(request_rdb)
) -> str:
    """
    Update a feature by ID
    """
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Feature).filter(orm.Feature.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Feature"


@router.delete("/features/{id}", **delete.fastapi_endpoint_config)
def delete_feature(id: int, rdb: Engine = Depends(request_rdb)):
    """
    Delete a feature by ID
    """
    with Session(rdb) as session:
        session.query(orm.Feature).filter(orm.Feature.id == id).delete()
        session.commit()


@router.get("/qualifiers")
def get_qualifiers(
    page_size: int = 100, page: int = 0, rdb: Engine = Depends(request_rdb)
):
    """
    Get a specific number of qualifiers
    """
    return list_by_id(rdb.connect(), orm.Qualifier, page_size, page)


@router.get("/qualifiers/{id}", **retrieve.fastapi_endpoint_config)
def get_qualifier(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific qualifier by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.Qualifier).get(id)
        return result


@router.post("/qualifiers", **create.fastapi_endpoint_config)
def create_qualifier(
    payload: schema.Qualifier,
    qualifies_array: List[str],
    rdb: Engine = Depends(request_rdb),
):
    """
    Create a qualifier
    """
    with Session(rdb) as session:
        qualifierp = payload.dict()
        del qualifierp["id"]
        qualifier = orm.Qualifier(**qualifierp)
        qualifier_result = session.query(orm.Qualifier).filter_by(**qualifierp).first()
        if qualifier_result is not None:
            qualifierp["id"] = qualifier_result.id
            return Response(
                status_code=status.HTTP_200_OK,
                headers={
                    "content-type": "application/json",
                },
                content=json.dumps(qualifierp),
            )

        session.add(qualifier)
        session.commit()
        data_id = qualifier.id
        for qual in qualifies_array:
            feature = (
                session.query(orm.Feature)
                .filter_by(name=qual, dataset_id=qualifierp["dataset_id"])
                .first()
            )
            try:
                qualifier_xrefp = {
                    "id": 0,
                    "qualifier_id": data_id,
                    "feature_id": feature.id,
                }
                create_qualifier_xref(qualifier_xrefp, rdb)
            except AttributeError as error:
                logger.warning("Skipped xref because of %s", error)

        qualifierp["id"] = data_id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "content-type": "application/json",
            },
            content=json.dumps(qualifierp),
        )


@router.patch("/qualifiers/{id}", **update.fastapi_endpoint_config)
def update_qualifier(
    payload: schema.Qualifier, id: int, rdb: Engine = Depends(request_rdb)
) -> str:
    """
    Update a qualifier by ID
    """
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Qualifier).filter(orm.Qualifier.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Qualifier"


@router.delete("/qualifiers/{id}", **delete.fastapi_endpoint_config)
def delete_qualifier(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Delete a qualifier by ID
    """
    with Session(rdb) as session:
        session.query(orm.Qualifier).filter(orm.Qualifier.id == id).delete()
        session.commit()


@router.get("")
def get_datasets(
    page_size: int = 100,
    page: int = 0,
    is_sim_run: Optional[bool] = None,
    rdb: Engine = Depends(request_rdb),
):
    """
    Get a specific number of datasets
    """
    with Session(rdb) as session:
        datasets = (
            session.query(orm.Dataset)
            .filter(or_(is_sim_run is None, orm.Dataset.simulation_run == is_sim_run))
            .order_by(orm.Dataset.id.asc())
            .limit(page_size)
            .offset(page)
            .all()
        )
        dataset_ids = [dataset.id for dataset in datasets]

        features = (
            session.query(orm.Feature)
            .filter(orm.Feature.dataset_id.in_(dataset_ids))
            .all()
        )

        feature_ids = [feature.id for feature in features]
        concepts = (
            session.query(orm.OntologyConcept)
            .filter(
                orm.OntologyConcept.type == "features",
                orm.OntologyConcept.object_id.in_(feature_ids),
            )
            .all()
        )

        concept_index = defaultdict(list)
        for concept in concepts:
            concept_index[concept.object_id].append(concept)

        feature_index = defaultdict(list)
        for feature in features:
            feature.concepts = concept_index[feature.id]
            feature_index[feature.dataset_id].append(feature)

        for dataset in datasets:
            dataset.annotations["annotations"]["feature"] = feature_index.get(
                dataset.id, None
            )
        return datasets


@router.get("/{id}", **retrieve.fastapi_endpoint_config)
def get_dataset(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific dataset by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.Dataset).get(id)
        return result


@router.get("/{id}/features")
def search_feature(
    id: int,
    rdb: Engine = Depends(request_rdb),
):
    """
    Search features by dataset id and/or name
    """
    with Session(rdb) as session:
        dataset = session.query(orm.Dataset).get(id)
        query = session.query(orm.Feature).filter(orm.Feature.dataset_id == int(id))
        result = query.all()

        for feature in result:
            feature_id = feature.id
            result_list = (
                session.query(orm.OntologyConcept)
                .filter(
                    orm.OntologyConcept.type == "features",
                    orm.OntologyConcept.object_id == feature_id,
                )
                .all()
            )
            feature.concepts = result_list
        dataset.features = result

        return dataset


@router.post("", **create.fastapi_endpoint_config)
def create_dataset(payload: schema.Dataset, rdb: Engine = Depends(request_rdb)):
    """
    Create a dataset
    """

    with Session(rdb) as session:
        datasetp = payload.dict()
        del datasetp["id"]
        dataset = orm.Dataset(**datasetp)
        session.add(dataset)
        session.commit()
        logger.debug(dataset)
        data_id = dataset.id
        datasetp["id"] = data_id
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "content-type": "application/json",
            },
            content=json.dumps(datasetp, default=str),
        )


@router.patch("/{id}", **update.fastapi_endpoint_config)
def update_dataset(
    payload: schema.Dataset, id: int, rdb: Engine = Depends(request_rdb)
) -> Response:
    """
    Update a dataset by ID
    """
    with Session(rdb) as session:
        data_payload = payload.dict(
            exclude_unset=True
        )  # Exclude unset not working, throws 422 if schema.Datasets is malformed.
        data_payload["id"] = id
        logger.info(data_payload)

        data_to_update = session.query(orm.Dataset).filter(orm.Dataset.id == id)
        data_to_update.update(data_payload)
        session.commit()
    return Response(
        status_code=status.HTTP_200_OK,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps(data_payload, default=str),
    )


@router.post("/deprecate/{id}")
def deprecate_dataset(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Toggle a dataset's deprecated status by ID
    """
    with Session(rdb) as session:
        to_toggle_deprecated = session.query(orm.Dataset).filter(orm.Dataset.id == id)
        deprecated_value = not to_toggle_deprecated.first().deprecated
        to_toggle_deprecated.update({"deprecated": deprecated_value})
        session.commit()
        return f"Set dataset with id {id} to deprecated state {deprecated_value}"


# Not working because of lack of cascade settings in ORM?
# Features foreign key blocks the delete.
@router.delete("/{id}", **delete.fastapi_endpoint_config)
def delete_dataset(id: int, rdb: Engine = Depends(request_rdb)):
    """
    Delete a dataset by ID
    """
    with Session(rdb) as session:
        session.query(orm.Dataset).filter(orm.Dataset.id == id).delete()
        session.commit()


# TODO: DELETE THIS DEPRECATED ENDPOINT
@router.get("/{id}/download/rawfile", deprecated=True)
def get_csv_from_dataset_depr(
    id: int,
    wide_format: bool = False,
    row_limit: Optional[int] = None,
    rdb: Engine = Depends(request_rdb),
):
    """
    Gets the csv of an annotated dataset that is registered
    via the data-annotation tool.
    """
    dataset = get_dataset(id=id, rdb=rdb)
    data_paths = dataset.annotations["data_paths"]
    storage_options = {"client_kwargs": {"endpoint_url": os.getenv("STORAGE_HOST")}}
    path = data_paths[0]
    if path.endswith(".parquet.gzip"):
        # Build single dataframe
        dataframe = pandas.concat(
            pandas.read_parquet(file, storage_options=storage_options)
            for file in data_paths
        )
        output = prepare_csv(dataframe, wide_format, row_limit)
        response = StreamingResponse(
            iter([output]),
            media_type="text/csv",
        )
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response

    file = get_rawfile(path)
    dataframe = pandas.read_csv(file)
    output = prepare_csv(dataframe, wide_format, row_limit)
    return StreamingResponse(iter([output]), media_type="text/csv")


# TODO: DELETE THIS DEPRECATED ENDPOINT
@router.post("/{id}/upload/file", deprecated=True)
def upload_file_depr(
    id: int,
    file: UploadFile = File(...),
    filename: Optional[str] = None,
):
    """Upload a file to the DATASET_BASE_STORAGE_URL

    Args:
        id (int): Dataset ID.
        file (UploadFile, optional): Upload of file-like object.
        filename (Optional[str], optional): Allows the specification of
        a particular filename at upload. Defaults to None.

    Returns:
        Reponse: FastAPI Response object containing
        information about the uploaded file.
    """
    base_uri = os.getenv("DATASET_STORAGE_BASE_URL")

    if filename is None:
        filename = file.filename

    # Upload file
    dest_path = os.path.join(base_uri, str(id), filename)
    put_rawfile(path=dest_path, fileobj=file.file)

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id, "filename": filename}),
    )


@router.get("/{id}/file")
def get_csv_from_dataset(
    id: int,
    wide_format: bool = False,
    row_limit: Optional[int] = None,
    rdb: Engine = Depends(request_rdb),
):
    """
    Gets the csv of an annotated dataset that is registered
    via the data-annotation tool.
    """
    dataset = get_dataset(id=id, rdb=rdb)
    uses_annotations = dataset.annotations is not None
    path = dataset.annotations["data_paths"][0] if uses_annotations else dataset.url
    storage_options = {"client_kwargs": {"endpoint_url": os.getenv("STORAGE_HOST")}}
    if uses_annotations and path.endswith(".parquet.gzip"):
        # Build single dataframe
        dataframe = pandas.concat(
            pandas.read_parquet(file, storage_options=storage_options)
            for file in dataset.annotations["data_paths"]
        )
        output = prepare_csv(dataframe, wide_format, row_limit)
        response = StreamingResponse(
            iter([output]),
            media_type="text/csv",
        )
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response

    file = get_rawfile(path)
    dataframe = pandas.read_csv(file)
    output = prepare_csv(dataframe, wide_format, row_limit)
    return StreamingResponse(iter([output]), media_type="text/csv")


@router.post("/{id}/file")
def upload_file(
    id: int,
    file: UploadFile = File(...),
    filename: Optional[str] = None,
    rdb: Engine = Depends(request_rdb),
):
    """Upload a file to the DATASET_BASE_STORAGE_URL

    Args:
        id (int): Dataset ID.
        file (UploadFile, optional): Upload of file-like object.
        filename (Optional[str], optional): Allows the specification of
        a particular filename at upload. Defaults to None.

    Returns:
        Reponse: FastAPI Response object containing
        information about the uploaded file.
    """

    if not entry_exists(rdb.connect(), orm.Dataset, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    base_uri = os.getenv("DATASET_STORAGE_BASE_URL")

    if filename is None:
        filename = file.filename

    # Upload file
    dest_path = os.path.join(base_uri, str(id), filename)
    put_rawfile(path=dest_path, fileobj=file.file)

    with Session(rdb) as session:
        dataset = session.query(orm.Dataset).get(id)
        if dataset.annotations is None:
            dataset.url = dest_path
            session.commit()

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "content-type": "application/json",
        },
        content=json.dumps({"id": id, "filename": filename}),
    )
