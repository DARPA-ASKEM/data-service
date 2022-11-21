"""
Model-specific logic
"""

from logging import Logger

from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.schema.model import ModelParameters

logger = Logger(__file__)


def adjust_model_params(model_id: int, parameters: ModelParameters, session: Session):
    """
    Add new entries and remove unused entries
    """

    existing = []
    for param in session.query(orm.SimulationParameter).filter(
        orm.ModelParameter.model_id == model_id
    ):
        existing.append(param.name)

    for name, type in parameters.items():
        if name not in existing:
            session.add(orm.ModelParameter(run_id=model_id, name=name, type=type))
        else:
            session.query(orm.ModelParameter).filter(
                orm.ModelParameter.model_id == model_id,
                orm.ModelParameter.name == name,
            ).update(
                {
                    "type": type,
                }
            )
        existing.remove(name)

    for name in existing:
        for param in session.query(orm.ModelParameter).filter(
            orm.ModelParameter.run_id == model_id,
            orm.ModelParameter.name == name,
        ):
            session.delete(param)
