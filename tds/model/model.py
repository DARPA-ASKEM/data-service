from typing import List, Optional

from pydantic import BaseModel


class Model(BaseModel):
    id: Optional[int]
    name: str
    description: str
    parameters: Optional[List]
