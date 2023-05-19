from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from tds.db import es


class TdsModel(BaseModel):
    id: Optional[int | str]
    index: str
    timestamp: Optional[datetime]

    def save(self, entity_id: Optional[None | str | int] = None):
        self.timestamp = datetime.now()
        if self.id or entity_id:
            res = es.index(
                index=self.index,
                body=self.dict(),
                id=(entity_id if entity_id else self.id),
            )
        else:
            res = es.index(index=self.index, body=self.dict())
            self.id = res["_id"]
        return res

    def delete(self):
        res = es.delete(index=self.index, id=self.id)
        return res
