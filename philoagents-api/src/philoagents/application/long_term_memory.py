from philoagents.config import settings
from loguru import logger
from philoagents.application.rag.retrievers import Retriever, get_retriever
from philoagents.application.rag.splitters import Splitter, get_splitter

from langchain_core.documents import Document
from philoagents.domain.philosopher import PhilosopherExtract

from typing import List

from philoagents.infrastructure.mongo import MongoClientWrapper, MongoIndex
from philoagents.application.data.deduplicate_documents import deduplicate_documents
from philoagents.application.data.extract import get_extraction_generator

class LongTermMemoryCreator:
    
    def __init__(self,retriever: Retriever, splitter: Splitter):
        self.retriever = retriever
        self.splitter = splitter

    @classmethod
    def build_from_settings(cls):
        retriever = get_retriever(embedding_model_name=settings.RAG_TEXT_EMBEDDING_MODEL,
                                  k=settings.RAG_TOP_K,
                                  device=settings.RAG_DEVICE)
        splitter = get_splitter(chunk_size=settings.RAG_CHUNK_SIZE)
        return cls(retriever, splitter)


    def __call__(self, philosphers=List[PhilosopherExtract]) -> None:

        if len(philosphers) == 0:
            logger.warning("No philosophers provided")
            return

        with MongoClientWrapper(
            model=Document,
            collection_name=settings.MONGO_LONG_TERM_MEMORY_COLLECTION,
            database_name=settings.MONGO_DB_NAME,
            mongodb_uri=settings.MONGODB_URI
        ) as client:
            client.clear_collection()
        
        extraction_generator = get_extraction_generator(philosphers)
        for _, docs in extraction_generator:
            chunked_docs = self.splitter.split_documents(docs)
            chunked_docs = deduplicate_documents(chunked_docs, threshold=0.7)

            self.retriever.vectorstore.add_documents(chunked_docs)

        self.__create_index()

    def __create_index(self) -> None:
        with MongoClientWrapper(
            model=Document,
            collection_name=settings.MONGO_LONG_TERM_MEMORY_COLLECTION,
            database_name=settings.MONGO_DB_NAME,
            mongodb_uri=settings.MONGODB_URI
        ) as client:
            
            self.index = MongoIndex(mongodb_client=client,
                                    retriever=self.retriever
                                   )
            self.index.create_index(is_hybrid=True, embedding_dim=settings.RAG_TEXT_EMBEDDING_DIMENSIONS)


class LongTermMemoryRetriever:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    @classmethod
    def build_from_settings(cls):
        retriever = get_retriever(embedding_model_name=settings.RAG_TEXT_EMBEDDING_MODEL,
                                  k=settings.RAG_TOP_K,
                                  device=settings.RAG_DEVICE)
        return cls(retriever)

    def __call__(self, query: str) -> List[Document]:
        return self.retriever.invoke(query)
    