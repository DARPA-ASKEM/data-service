"""
Qualifier specific logic
"""

import json
from logging import Logger

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.db import rdb as rdb_engine
from tds.lib.s3 import copy_object, get_file_path, parse_filename
from tds.modules.dataset.model import (
    Dataset,
    QualifierPayload,
    QualifierXref,
    QualifierXrefPayload,
)
from tds.modules.person.model import Person
from tds.modules.simulation.model import Simulation
from tds.settings import settings

logger = Logger(__file__)


def get_qualifier_xrefs(count: int, rdb: Engine):
    """
    Get a specified number of qualifier xrefs
    """
    with Session(rdb) as session:
        result = (
            session.query(QualifierXref).order_by(QualifierXref.id.asc()).limit(count)
        )
        result = result[::]
        return result


def get_qualifier_xref(xref_id: int, rdb: Engine) -> str:
    """
    Get a specific qualifier xref by ID
    """
    with Session(rdb) as session:
        result = session.query(QualifierXref).get(xref_id)
        return result


def create_qualifier_xref(payload: QualifierXrefPayload, rdb: Engine):
    """
    Create a qualifier xref
    """
    with Session(rdb) as session:
        qualifier_xrefp = {}
        try:
            qualifier_xrefp = payload.dict()
        except AttributeError as error:
            logger.error(error)
            qualifier_xrefp = payload
            logger.info("Set qualifier_xref to raw payload.")
        del qualifier_xrefp["id"]
        qualifier_xref = QualifierXref(**qualifier_xrefp)
        exists = (
            session.query(QualifierXref).filter_by(**qualifier_xrefp).first()
            is not None
        )
        if exists:
            return "Qualifier Xref already exists."
        session.add(qualifier_xref)
        session.commit()
        data_id = qualifier_xref.id
        qualifier_xrefp["id"] = data_id
        return json.dumps(qualifier_xrefp)


def update_qualifier_xref(payload: QualifierPayload, xref_id: int, rdb: Engine) -> str:
    """
    Update a qualifier xref by ID
    """
    with Session(rdb) as session:
        data_payload = payload.dict(exclude_unset=True)
        data_payload["id"] = xref_id
        logger.info(data_payload)

        data_to_update = session.query(QualifierXref).filter(
            QualifierXref.id == xref_id
        )
        data_to_update.update(data_payload)
        session.commit()
    return "Updated Qualifier xref"


def delete_qualifier_xref(xref_id: int, rdb: Engine) -> None:
    """
    Delete a qualifier xref by ID
    """
    with Session(rdb) as session:
        session.query(QualifierXref).filter(QualifierXref.id == xref_id).delete()
        session.commit()


def copy_simulation_result_to_dataset(simulation: Simulation):
    """
    Function copies a simulation object to a dataset.
    """
    sim_id = simulation["id"]
    sim_name = simulation["name"]
    dataset_obj = {
        "name": f"{sim_name} Result Dataset",
        "description": simulation["description"],
        "metadata": {"simulation_id": sim_id},
        "file_names": simulation["result_files"],
        "data_source_date": simulation["timestamp"],
        "columns": [],
    }

    # Get the user name and attach it to dataset.
    if simulation["user_id"]:
        with Session(rdb_engine) as session:
            user = session.query(Person).get(simulation["user_id"])
            dataset_obj["username"] = user.name

    dataset = Dataset(**dataset_obj)
    dataset.save()
    if simulation["result_files"]:
        for result_file in simulation["result_files"]:
            filename = parse_filename(result_file)
            origin_path = get_file_path(
                entity_id=sim_id, file_name=filename, path=settings.S3_RESULTS_PATH
            )
            dest_path = get_file_path(
                entity_id=dataset.id, file_name=filename, path=settings.S3_DATASET_PATH
            )
            copy_object(origin_path=origin_path, destination_path=dest_path)

    return {"id": dataset.id}
