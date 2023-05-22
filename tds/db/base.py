from datetime import datetime
from typing import Optional
import uuid

from elasticsearch import ConflictError
from pydantic import BaseModel, Field

from tds.db import es_client

es = es_client()

new_uuid = lambda: str(uuid.uuid4())

class TdsModel(BaseModel):
    id: str = Field(
        default_factory=new_uuid,
        description="Universally unique identifier for the item",
    )
    _index: str
    timestamp: Optional[datetime]

    def create(self):
        self.timestamp = datetime.now()
        try:
            res = es.create(
                index=self._index,
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
            index=self._index,
            body=self.dict(),
            id=self.id,
        )
        return res

    def delete(self):
        res = es.delete(index=self._index, id=self.id)
        return res
