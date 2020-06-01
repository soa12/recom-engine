from fastapi import APIRouter, Depends
from app.models.recommendation import Recommendation
from app.service.recommender import UserToUserCollabRecommender

router = APIRouter()


@router.post("/", name="query")
def post_query(recommender: UserToUserCollabRecommender = Depends()) -> Recommendation:
    result = recommender.get_recommendation()
    return result
