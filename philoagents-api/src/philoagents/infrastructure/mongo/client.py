from typing import Generic, TypeVar, Type
from pydantic import BaseModel
from pymongo import MongoClient, errors
from loguru import logger

T = TypeVar('T', bound=BaseModel)

class MongoClientWrapper(Generic[T]):
    def __init__(self, 
                model: Type[T],
                collection_name: str, 
                database_name: str, 
                mongodb_uri: str):


        self.model = model
        self.collection_name = collection_name
        self.database_name = database_name
        self.mongodb_uri = mongodb_uri

        try:
            self.client = MongoClient(self.mongodb_uri, appname="philoagents")

        except Exception as e:
            raise Exception(f"An error occurred: {e}")
     

        self.database = self.client[self.database_name]
        self.collection = self.database[self.collection_name]

        logger.info(f"Connected to MongoDB: {self.mongodb_uri} with database: {self.database_name} and collection: {self.collection_name}")


    def close(self):
        self.client.close()
        logger.info(f"Closed connection to MongoDB: {self.mongodb_uri}")