"""
TDS Base Model for ElasticSearch
"""
import uuid
from datetime import datetime
from typing import Optional

from elasticsearch import ConflictError
from pydantic import BaseModel, Field

from tds.db import es_client
from tds.settings import settings

es = es_client()

new_uuid = lambda: str(uuid.uuid4())


class TdsModel(BaseModel):
    id: str = Field(
        default_factory=new_uuid,
        description="Universally unique identifier for the item",
    )
    _index: str
    timestamp: Optional[datetime]

    @classmethod
    @property
    def index(self):
        return f"{settings.ES_INDEX_PREFIX}{self._index}"

    def create(self):
        self.timestamp = datetime.now()
        try:
            res = es.create(
                index=self.index,
                body=self.dict(),
                id=self.id,
            )
        except ConflictError:
            # ID is already in use, create a new id and resave
            self.id = new_uuid()
            return self.save()
        return res

    def save(self):
        self.timestamp = datetime.now()
        res = es.index(
            index=self.index,
            body=self.dict(),
            id=self.id,
        )
        return res

    def delete(self):
        res = es.delete(index=self.index, id=self.id)
        return res
