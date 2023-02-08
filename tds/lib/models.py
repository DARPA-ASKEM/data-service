"""
Model-specific logic
"""

from logging import Logger

from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.schema.model import ModelParameters

logger = Logger(__file__)

model_opt_relationship_mapping = {
    orm.ModelOperations.copy: "COPIED_FROM",
    orm.ModelOperations.decompose: "DECOMPOSED_FROM",
    orm.ModelOperations.stratify: "STRATIFIED_FROM",
    orm.ModelOperations.glue: "GLUED_FROM",
}


def adjust_model_params(model_id: int, parameters: ModelParameters, session: Session):
    """
    Add new entries and remove unused entries
    """

    existing = []
    for param in session.query(orm.ModelParameter).filter(
        orm.ModelParameter.model_id == model_id
    ):
        existing.append(param.get("name"))

    for parameter in parameters:
        if parameter.get("name") not in existing:
            session.add(
                orm.ModelParameter(
                    model_id=model_id,
                    name=parameter.get("name"),
                    type=parameter.get("type"),
                    default_value=parameter.get("default_value"),
                    state_variable=parameter.get("state_variable", False),
                )
            )
        else:
            session.query(orm.ModelParameter).filter(
                orm.ModelParameter.model_id == model_id,
                orm.ModelParameter.id == parameter.get("id"),
            ).update(
                {
                    "type": parameter.get("type"),
                    "default_value": parameter.get("default_value"),
                    "state_variable": parameter.get("state_variable", False),
                }
            )

            existing.remove(parameter.name)

    for name in existing:
        for param in session.query(orm.ModelParameter).filter(
            orm.ModelParameter.model_id == model_id,
            orm.ModelParameter.name == name,
        ):
            session.delete(param)
