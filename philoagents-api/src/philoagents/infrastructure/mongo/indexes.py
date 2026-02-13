from langchain_mongodb.index import create_fulltext_search_index

from .client import MongoClientWrapper

class MongoIndex:
    def __init__(self, mongodb_client: MongoClientWrapper, retriever):
        self.mongodb_client = mongodb_client
        self.retriever = retriever

    def create_index(self, embedding_dim: int, is_hybrid: bool = False):
        vector_store = self.retriever.vectorstore

        vector_store.create_vector_search_index(dimensions=embedding_dim)

        if is_hybrid:
            create_fulltext_search_index(
                collection=self.mongodb_client.collection,
                field=vector_store._text_key,
                index_name=self.retriever.search_index_name
            )