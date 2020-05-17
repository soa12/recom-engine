from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.models.recommendation import Recommendation
from app.models.query import Query


router = APIRouter()


@router.post("/queries", response_model=Recommendation, name="queries")
def post_queries(
    request: Request,
    block_data: Query
) -> Recommendation:
    recommendation: Recommendation
    return recommendation