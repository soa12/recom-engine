from pydantic import BaseModel


class ItemScore(BaseModel):
    id: int
    score: float

