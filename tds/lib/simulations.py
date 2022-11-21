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

    for parameter in parameters:
        if parameter.name not in existing:
            session.add(
                orm.ProjectAsset(
                    run_id=run_id,
                    name=parameter.name,
                    type=parameter.type,
                    value=parameter.value,
                )
            )
        else:
            session.query(orm.SimulationParameter).filter(
                orm.SimulationParameter.run_id == run_id,
                orm.SimulationParameter.id == parameter.id,
            ).update({"type": parameter.type, "value": parameter.value})

            existing.remove(parameter.name)

    for name in existing:
        for param in session.query(orm.SimulationParameter).filter(
            orm.SimulationParameter.run_id == run_id,
            orm.SimulationParameter.name == name,
        ):
            session.delete(param)
