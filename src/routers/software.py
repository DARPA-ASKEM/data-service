"""
router.software - very basic crud operations for software
"""

from logging import Logger

from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from src.autogen import orm, schema
from src.operation import create, delete, retrieve


def gen_router(engine: Engine, router_name) -> APIRouter:
    """
    Generate software router with given DB engine
    """
    logger = Logger(router_name)
    router = APIRouter(prefix=router_name)

    @router.get("/{id}", **retrieve.fastapi_endpoint_config)
    def get_software(id: int) -> schema.Software:
        """
        Retrieve software metadata
        """
        with Session(engine) as session:
            if session.query(orm.Software).filter(orm.Software.id == id).count() == 1:
                return session.query(orm.Software).get(id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    @router.post("", **create.fastapi_endpoint_config)
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
        logger.info("new software with %i", id)
        return id

    @router.delete("/{id}", **delete.fastapi_endpoint_config)
    def delete_software(id: int) -> Response:
        """
        Delete software metadata
        """
        with Session(engine) as session:
            if session.query(orm.Software).filter(orm.Software.id == id).count() == 1:
                software = session.query(orm.Software).get(id)
                session.delete(software)
                session.commit()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
        )

    return router
