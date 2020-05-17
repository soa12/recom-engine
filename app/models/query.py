from typing import List
from pydantic import BaseModel


class Query(BaseModel):
    items: List[int]
    number: int
