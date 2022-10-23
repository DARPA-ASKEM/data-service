"""
router.models - crud operations for models
"""

from logging import Logger
from fastapi import APIRouter
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from generated import orm
from config.schema import Model, ModelBody

logger = Logger(__file__)


def gen_router(engine: Engine) -> APIRouter:
    """
    Generate model router with given DB engine
    """
    router = APIRouter()

    @router.get("/models/{id}")
    def get_model(id: int) -> Model:
        """
        Retrieve model
        """
        with Session(engine) as session:
            model = session.query(orm.Model).get(id)
            operation = session.query(orm.Operation).get(model.head_id)
            return Model.from_orm(model, operation)


    @router.post("/models")
    def create_model(payload: Model) -> str:
        """
        Create model
        """
        with Session(engine) as session:
            model_payload = payload.dict()
            operation_payload = model_payload.pop('body')
            operation = orm.Operation(**operation_payload)
            # pylint: disable-next=unused-variable
            concept_payload = model_payload.pop('concept') #TODO: Save ontology term
            session.add(operation)
            session.commit()
            model_payload['head_id'] = operation.id
            model = orm.Model(**model_payload)
            session.add(model)
            session.commit()
        return "Created model"


    @router.post("/models/{id}")
    def update_model(payload : ModelBody, id: int) -> Model:
        """
        Update model content
        """
        with Session(engine) as session:
            model = session.query(orm.Model).get(id)
            operation_payload = payload.dict()
            operation_payload['prev'] = model.head_id
            operation = orm.Operation(**operation_payload)
            session.add(operation)
            session.commit()
            model.head_id=operation.id
            session.commit()
        return get_model(id)


    @router.delete("/models/{id}")
    def delete_model(id: int) -> str:
        """
        Delete model head

        WARNING: The operation history is left dangling.
        """
        with Session(engine) as session:
            session.query(orm.Model).get(id).delete()
            session.commit()
        return "Deleted model"


    return router
