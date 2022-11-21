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
        existing.append(param.get("name"))

    for parameter in parameters:
        if parameter.get("name") not in existing:
            session.add(
                orm.SimulationParameter(
                    run_id=run_id,
                    name=parameter.get("name"),
                    type=parameter.get("type"),
                    value=parameter.get("value"),
                )
            )
        else:
            session.query(orm.SimulationParameter).filter(
                orm.SimulationParameter.run_id == run_id,
                orm.SimulationParameter.id == parameter.get("id"),
            ).update({"type": parameter.get("type"), "value": parameter.get("value")})

            existing.remove(parameter.name)

    for name in existing:
        for param in session.query(orm.SimulationParameter).filter(
            orm.SimulationParameter.run_id == run_id,
            orm.SimulationParameter.name == name,
        ):
            session.delete(param)
