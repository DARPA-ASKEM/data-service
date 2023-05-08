from pydantic import BaseModel


class Model(BaseModel):
    id: int

    def __init__(self):
        pass
