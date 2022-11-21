"""
Sim-specific logic
"""

from logging import Logger

from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.schema.simulation import SimulationParameters

logger = Logger(__file__)


def adjust_run_params(run_id: int, parameters: SimulationParameters, session: Session):
    """
    Add new entries and remove unused entries
    """

    existing = []
    for param in session.query(orm.SimulationParameter).filter(
        orm.SimulationParameter.run_id == run_id
    ):
        existing.append(param.name)

    for name, (value, type) in parameters.items():
        if name not in existing:
            session.add(
                orm.ProjectAsset(run_id=run_id, name=name, type=type, value=value)
            )
        else:
            session.query(orm.SimulationParameter).filter(
                orm.SimulationParameter.run_id == run_id,
                orm.SimulationParameter.name == name,
            ).update({"type": type, "value": value})
        existing.remove(name)

    for name in existing:
        for param in session.query(orm.SimulationParameter).filter(
            orm.SimulationParameter.run_id == run_id,
            orm.SimulationParameter.name == name,
        ):
            session.delete(param)
