from typing import Optional

from pydantic import BaseModel


class Model(BaseModel):
    id: Optional[int]
    name: str
    description: str
