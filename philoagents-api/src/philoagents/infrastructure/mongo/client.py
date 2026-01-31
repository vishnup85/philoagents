from typing import Generic, TypeVar, Type
from pydantic import BaseModel
from pymongo import MongoClient, errors
from loguru import logger
from typing import List
from langchain_core.documents import Document

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


    def ingest_documents(self, documents: List[T]):

        try:
            if not documents or not all(isinstance(doc, BaseModel) for doc in documents):
                raise ValueError("Documents must be a list of BaseModel objects")

            documents_dict = [doc.model_dump() for doc in documents]
            for doc in documents_dict:
                doc.pop("_id", None)
            self.collection.insert_many(documents_dict)
            logger.info(f"Ingested {len(documents)} documents into MongoDB")
        except errors.PyMongoError as e:
            logger.error(f"An error occurred: {e}")
            raise e

    def clear_collection(self):
        try:
            self.collection.delete_many({})
            logger.info(f"Cleared collection: {self.collection_name}")
        except errors.PyMongoError as e:
            logger.error(f"An error occurred: {e}")
            raise e


    def close(self):
        self.client.close()
        logger.info(f"Closed connection to MongoDB: {self.mongodb_uri}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False