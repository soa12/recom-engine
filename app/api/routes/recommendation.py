from fastapi import APIRouter, Depends
from starlette.requests import Request
from loguru import logger

from app.models.recommendation import Recommendation
from app.models.query import Query
from app.data.connect import Connection
from app.service.recommender import UserToUserCollabRecommender

from neo4j import GraphDatabase
from pydantic import BaseModel

from app.core.config import DB_URL, DB_USERNAME, DB_PASSWORD

router = APIRouter()


@router.post("/",  name="query")
def post_query(recommender: UserToUserCollabRecommender = Depends()) -> Recommendation:
    result = recommender.get_recommendation()
    return result


@router.post("/test")
def get_rec():
    _query_tpl = """
            MATCH (u1:User)-[:ORDERED]->(:Order)-[:CONTAINS]->(p:Product)<-[:CONTAINS]-(:Order)<-[:ORDERED]-(u2:User)
                WHERE u1 <> u2
                AND u1.userId = {user_id}
                WITH u1, u2, COUNT(DISTINCT p) as intersection_count

                // Get count of all the distinct products that they have purchased between them
                MATCH (u:User)-[:ORDERED]->(:Order)-[:CONTAINS]->(p:Product)
                WHERE u in [u1, u2]
                WITH u1, u2, intersection_count, COUNT(DISTINCT p) as union_count

                // Compute Jaccard index
                WITH u1, u2, intersection_count, union_count, (intersection_count*1.0/union_count) as jaccard_index

                // Get top k neighbours based on Jaccard index
                ORDER BY jaccard_index DESC, u2.userId
                WITH u1, COLLECT(u2)[0..{nearest_neighbors}] as neighbours
                WHERE SIZE(neighbours) = {nearest_neighbors}                                        // only want users with enough neighbours
                UNWIND neighbours as neighbour
                WITH u1, neighbour

                // Get top n recommendations from the selected neighbours
                MATCH (neighbour)-[:ORDERED]->(:Order)-[:CONTAINS]->(p:Product)                         // get all products bought by neighbour
                WHERE not (u1)-[:ORDERED]->(:Order)-[:CONTAINS]->(p)                                    // which target user has not already bought
                WITH u1, p, COUNT(DISTINCT neighbour) as cnt                                            // count neighbours who purchased product
                ORDER BY u1.userId, cnt DESC                                                            // sort by count desc
                RETURN u1.userId as user, COLLECT(p.productName)[0..{nearest_neighbors}] as recos       // return top n products
        """

    driver = GraphDatabase.driver(DB_URL, auth=(DB_USERNAME, DB_PASSWORD), encrypted=False)

    db_connect = Connection(driver)
    result = db_connect.run_get_query(_query_tpl.format(user_id=3860, number=5, nearest_neighbors=10))
    return result._records
