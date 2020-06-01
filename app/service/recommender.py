from pydantic import BaseModel
from app.data.connect import Connection
from app.core.config import CF_NEAREST_NEIGHBORS
from fastapi import Depends
from loguru import logger

from app.models.recommendation import Recommendation, Query
from app.models.item_score import ItemScore


class UserToUserCollabRecommender:
    def __init__(self, query: Query, db_connect=Depends(Connection)):
        self.db_connect = db_connect
        self.user_id: int = query.item_id
        self.number: int = query.number
        self.nearest_neighbors: int = CF_NEAREST_NEIGHBORS

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
            RETURN u1.userId as user, COLLECT(p.productName)[0..{number}] as recos       // return top n products
    """

    def get_recommendation(self):
        result = self.db_connect.run_get_query(
            self._query_tpl.format(user_id=self.user_id, number=self.number, nearest_neighbors=self.nearest_neighbors)
        )
        rows = result.single()
        # logger.debug(result._records)
        # for row in result._records:
        #     for record in row:
        #         logger.debug(record)
        # return Recommendation(item_scores=[ItemScore(id=3066)])

        # if result.single() is None:
        #     logger.debug('None')
        #     return '{self.user_id}'
        # else:
        #     logger.debug('Not None')
        #     return result.single()[1]
        return rows if rows is not None else [self.user_id, []]
