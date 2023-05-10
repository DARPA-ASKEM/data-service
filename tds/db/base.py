from typing import Optional

from pydantic import BaseModel

from tds.db import es


class TdsModel(BaseModel):
    id: Optional[int | str]
    _index: str

    def save(self, id: Optional[None | str | int] = None):
        if self.id or id:
            res = es.index(
                index=self._index, body=self.dict(), id=(id if id else self.id)
            )
        else:
            res = es.index(index=self._index, body=self.dict())
        return res

    def delete(self):
        res = es.delete(index=self._index, id=self.id)
        return res
