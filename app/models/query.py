from typing import List
from pydantic import BaseModel


class Query(BaseModel):
    item: int
    number: int
