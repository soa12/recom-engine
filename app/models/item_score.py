from pydantic import BaseModel, ValidationError, validator


class ItemScore(BaseModel):
    id: int
    # score: float