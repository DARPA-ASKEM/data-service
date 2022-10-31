"""
router.software - very basic crud operations for software
"""
from fastapi import APIRouter
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from src.autogen import orm, schema


def gen_router(engine: Engine) -> APIRouter:
    """
    Generate software router with given DB engine
    """
    router = APIRouter()

    @router.get("/software/{id}")
    def get_software(id: int) -> schema.Software:
        """
        Retrieve software metadata
        """
        with Session(engine) as session:
            return session.query(orm.Software).get(id)

    @router.post("/software")
    def create_software(payload: schema.Software) -> int:
        """
        Create software metadata
        """
        with Session(engine) as session:
            model_payload = payload.dict()
            model = orm.Software(**model_payload)
            session.add(model)
            session.commit()
            id: int = model.id
        return id

    @router.delete("/software/{id}")
    def delete_software(id: int) -> str:
        """
        Delete software metadata
        """
        with Session(engine) as session:
            software = session.query(orm.Model).filter(orm.Software.id == id).first()
            if software is not None:
                software.delete()
                session.commit()
        return "Deleted original software for model"

    return router
