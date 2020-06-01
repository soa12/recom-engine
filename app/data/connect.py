import string
from fastapi import Depends
from loguru import logger
from neo4j import GraphDatabase
from pydantic import BaseModel

from app.core.config import DB_URL, DB_USERNAME, DB_PASSWORD


def get_driver():
    return GraphDatabase.driver(DB_URL, auth=(DB_USERNAME, DB_PASSWORD), encrypted=False)


class Connection:
    def __init__(self, driver=Depends(get_driver)):
        self.driver = driver

    def run_get_query(self, query: string):
        logger.info("READ query to {0}", repr(DB_URL))

        def fetch(tx, query):
            return tx.run(query)

        session = self.driver.session()
        result = session.read_transaction(fetch, query)
        session.close()
        logger.info("READ query done")
        return result

    def close_db_connection(self, query: string, data):
        logger.info("WRITE query to database")

        def put(tx, query, data):
            return tx.run(query, **data).single().value()

        session = self.driver.session()
        result = session.write_transaction(put, query, data)
        session.close()
        logger.info("WRITE query done")
        return result
