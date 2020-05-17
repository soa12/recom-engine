from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.models.query import Query

router = APIRouter()

@router.post("/", name="put", status_code=200)
def post_queries():
    return {"result": "success"}
