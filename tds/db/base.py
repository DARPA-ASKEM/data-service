"""
TDS Base Model for ElasticSearch
"""
import uuid
from datetime import datetime
from typing import Optional

from elasticsearch import ConflictError
from pydantic import BaseModel, Field
from sqlalchemy.ext.declarative import declarative_base

from tds.db import es_client
from tds.settings import settings

es = es_client()
RelationalDatabaseBase = declarative_base()


def new_uuid() -> str:
    """Generates a uuid string"""
    return str(uuid.uuid4())


class BaseElasticSearchModel(BaseModel):
    """
    TDS Base Model class.
    """

    id: str = Field(
        default_factory=new_uuid,
        description="Universally unique identifier for the item",
    )
    _index: str
    timestamp: Optional[datetime]
    _date_format = "%Y-%m-%d %H:%M:%S"

    @classmethod
    @property
    def index(cls):
        """
        Method returns the prefaced index.
        """
        return f"{settings.ES_INDEX_PREFIX}{cls._index}"

    def create(self):
        """
        Method creates the entity in ES.
        """
        self.timestamp = datetime.now().strftime(self._date_format)
        try:
            res = es.create(
                index=self.index,
                document=self.dict(),
                id=self.id,
                refresh="wait_for",
            )
        except ConflictError:
            # ID is already in use, create a new id and resave
            self.id = new_uuid()
            return self.save()
        return res

    def save(self):
        """
        Method saves the entity in ES.
        """
        self.timestamp = datetime.now().strftime(self._date_format)
        res = es.index(
            index=self.index,
            document=self.dict(),
            id=self.id,
        )
        return res

    def delete(self):
        """
        Method deletes an entity in ES.
        """
        res = es.delete(index=self.index, id=self.id)
        return res
