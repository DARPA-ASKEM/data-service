"""
Concept-specific logic
"""

import json
from logging import Logger
from urllib.parse import quote_plus

import requests
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.lib.errors import DKGError
from tds.settings import settings

logger = Logger(__file__)

RETRIES = 5


def fetch_from_dkg(request_url: str):
    """
    Interface with the DKG
    """
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    base_url = settings.DKG_URL + ":" + str(settings.DKG_API_PORT) + "/api"
    url = base_url + request_url
    logger.info("Sending data to %s", url)

    response = requests.get(url, headers=headers, timeout=5)
    logger.debug("response: %s", response)
    logger.debug("response reason: %s", response.raw.reason)

    if response.status_code == 200:
        return json.loads(response.content.decode("utf8"))
    logger.debug("Failed to fetch ontologies: %s", response)
    raise DKGError(f"DKG server returned the status {response.status_code}")


def mark_concept_active(session: Session, curie):
    """
    Page through table using given ORM
    """
    if (
        session.query(orm.ActiveConcept)
        .filter(orm.ActiveConcept.curie == curie)
        .count()
        == 0
    ):
        for _ in range(RETRIES):
            try:
                params = f"/entity/{quote_plus(curie)}"
                name = fetch_from_dkg(params)["name"]
            except DKGError:
                continue
            else:
                active = orm.ActiveConcept(curie=curie, name=name)
                session.add(active)
                session.commit()
                logger.info("added active %s", curie)
                return

        active = orm.ActiveConcept(curie=curie, name=None)
        session.add(active)
        session.commit()
        logger.info("added active %s", curie)
    else:
        logger.info("%s already active", curie)
