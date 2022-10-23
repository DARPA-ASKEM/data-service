"""
router.software - very basic crud operations for software
"""
from fastapi import APIRouter
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from generated import schema, orm


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
    def create_software(payload: schema.Software) -> str:
        """
        Create software metadata
        """
        with Session(engine) as session:
            model_payload = payload.dict()
            model = orm.Software(**model_payload)
            session.add(model)
            session.commit()
        return "Stored original software for model"


    @router.patch("/software/{id}")
    def update_software(payload, id: int) -> str:
        """
        Update software metadata
        """

        with Session(engine) as session:
            model_payload = payload.dict()
            session.query(orm.Software).filter(orm.Software.id == id).update(model_payload)
            session.commit()
        return "Updated original software for model"


    @router.delete("/software/{id}")
    def delete_software(id: int) -> str:
        """
        Delete software metadata
        """
        with Session(engine) as session:
            session.query(orm.Model).filter(orm.Software.id == id).delete()
            session.commit()
        return "Deleted original software for model"


    return router
