from pydantic import BaseModel
from typing import List

from app.models.item_score import ItemScore


class Recommendation(BaseModel):
    item_scores: List[ItemScore]


class Query(BaseModel):
    item_id: int
    number: int
