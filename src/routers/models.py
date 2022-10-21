"""
router.models - crud operations for models
"""

from db import ENGINE
from fastapi import APIRouter
from generated import schema, orm
from api_schema import Model, ModelBody
from logging import Logger
from sqlalchemy.orm import Session

logger = Logger(__file__)
router = APIRouter()


@router.get("/models/{id}")
def get_model(id: int) -> Model:
    with Session(ENGINE) as session:
        model = session.query(orm.Model).get(id)
        operation = session.query(orm.Operation).get(model.head_id)
        return Model.from_orm(model, operation)


@router.post("/models")
def create_model(payload: Model) -> str:
    with Session(ENGINE) as session:
        model_payload = payload.dict()
        operation_payload = model_payload.pop('body')
        operation = orm.Operation(**operation_payload)
        concept_payload = model_payload.pop('concept') #TODO: Save ontology term
        session.add(operation)
        session.commit()
        model_payload['head_id'] = operation.id
        model = orm.Model(**model_payload)
        session.add(model)
        session.commit()
    return "Created model"


@router.patch("/models/{id}")
def update_model(payload : ModelBody, id: int) -> Model:
    with Session(ENGINE) as session:
        model = session.query(orm.Model).get(id)
        operation_payload = payload.dict()
        operation = orm.Operation(**operation_payload, prev=model.head_id)
        session.add(operation)
        session.commit()
        model.update(head_id=operation.id)
        session.commit()
    return get_model(id)


@router.post("/models/{id}")
def undo_model(id: int) -> Model:
    with Session(ENGINE) as session:
        model = session.query(orm.Model).get(id)
        operation = session.query(orm.Operation).get(model.head_id)
        model.update({'head_id':operation.prev})
        session.commit()
    return get_model(id)


@router.delete("/models/{id}")
def delete_model(id: int) -> str:
    with Session(ENGINE) as session:
        session.query(orm.Model).get(id).delete()
        session.commit()
    return "Deleted model"


@router.get("/models/raw/{id}")
def get_raw_model(id: int) -> schema.Software:
    with Session(ENGINE) as session:
        result = session.query(orm.Software).get(id)
        return result


@router.post("/models/raw")
def create_raw_model(payload: schema.Software) -> str:
    with Session(ENGINE) as session:
        model_payload = payload.dict()
        model = orm.Software(**model_payload)
        session.add(model)
        session.commit()
    return "Stored original software for model"


@router.patch("/models/raw/{id}")
def update_raw_model(payload, id: int) -> str:
    with Session(ENGINE) as session:
        model_payload = payload.dict()
        model = session.query(orm.Software).filter(orm.Software.id == id)
        model.update(model_payload)
        session.commit()
    return "Updated original software for model"


@router.delete("/models/raw/{id}")
def delete_raw_model(id: int) -> str:
    with Session(ENGINE) as session:
        session.query(orm.Model).filter(orm.Software.id == id).delete()
        session.commit()
    return "Deleted original software for model"

