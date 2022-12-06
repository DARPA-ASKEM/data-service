"""
CRUD operations for datasets and related tables in the DB
"""

import json
import os
from logging import DEBUG, Logger
from typing import List, Optional

import pandas
import requests
from fastapi import APIRouter, Depends, File, Response, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm, schema
from tds.db import list_by_id, request_rdb
from tds.lib.datasets import create_qualifier_xref
from tds.lib.storage import get_rawfile, put_rawfile, stream_csv_from_data_paths

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


@router.get("/features/{id}")
def get_feature(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific feature by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.Feature).get(id)
        return result


@router.post("/features")
def create_feature(payload: schema.Feature, rdb: Engine = Depends(request_rdb)):
    """
    Create a feature
    """
    with Session(rdb) as session:
        featurep = payload.dict()
        del featurep["id"]
        feature = orm.Feature(**featurep)
        exists = session.query(orm.Feature).filter_by(**featurep).first() is not None
        if exists:
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


@router.patch("/features/{id}")
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


@router.delete("/features/{id}")
def delete_feature(id: int, rdb: Engine = Depends(request_rdb)) -> str:
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


@router.get("/qualifiers/{id}")
def get_qualifier(id: int, rdb: Engine = Depends(request_rdb)) -> str:
    """
    Get a specific qualifier by ID
    """
    with Session(rdb) as session:
        result = session.query(orm.Qualifier).get(id)
        return result


@router.post("/qualifiers")
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
        exists = (
            session.query(orm.Qualifier).filter_by(**qualifierp).first() is not None
        )
        if exists:
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


@router.patch("/qualifiers/{id}")
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


@router.delete("/qualifiers/{id}")
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
    is_simulation: bool = False,
    rdb: Engine = Depends(request_rdb),
):
    """
    Get a specific number of datasets
    """
    with Session(rdb) as session:
        return (
            session.query(orm.Dataset)
            .filter(orm.Dataset.simulation_run == is_simulation)
            .order_by(orm.Dataset.id.asc())
            .limit(page_size)
            .offset(page)
            .all()
        )


@router.get("/{id}")
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


@router.post("")
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


@router.patch("/{id}")
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
@router.delete("/{id}")
def delete_dataset(id: int, rdb: Engine = Depends(request_rdb)):
    """
    Delete a dataset by ID
    """
    with Session(rdb) as session:
        session.query(orm.Dataset).filter(orm.Dataset.id == id).delete()
        session.commit()


@router.get("/{id}/download/rawfile")
def get_csv_from_dataset(
    id: int,
    wide_format: bool = False,
    data_annotation_flag: bool = False,
    rdb: Engine = Depends(request_rdb),
):
    """
    Gets the csv of an annotated dataset that is registered
    via the data-annotation tool.
    """
    dataset = get_dataset(id=id, rdb=rdb)
    data_paths = dataset.annotations["data_paths"]

    if data_annotation_flag:
        response = requests.post(
            "http://data-annotation-api:80/datasets/download/csv",
            params={"data_path_list": data_paths},
            stream=True,
            timeout=15,
        )
        return StreamingResponse(response.raw, headers=response.headers)
    path = data_paths[0]
    if path.endswith(".parquet.gzip"):
        # Build single dataframe
        dataframe = pandas.concat(pandas.read_parquet(file) for file in data_paths)
        print(dataframe)
        output = stream_csv_from_data_paths(dataframe, wide_format)
        response = StreamingResponse(
            iter([output]),
            media_type="application/json",
        )
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response
    file = get_rawfile(path)
    if wide_format:
        dataframe = pandas.read_csv(file)
        output = stream_csv_from_data_paths(dataframe, wide_format)
        return StreamingResponse(iter([output]), media_type="text/csv")
    return StreamingResponse(file, media_type="text/csv")


@router.post("/{id}/upload/file")
def upload_file(
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
