from .embeddings import get_embeddings
from philoagents.config import settings
from loguru import logger
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_mongodb.retrievers import MongoDBAtlasHybridSearchRetriever
Retriever = MongoDBAtlasHybridSearchRetriever

def get_retriever(embedding_model_name: str,
                  k: int = 3,
                  device: str = "cpu") -> Retriever:

    logger.info(f"Getting retriever for embedding model: {embedding_model_name} with device: {device}")
    embeddings = get_embeddings(model_name=embedding_model_name, device=device)

    return get_hybrid_search_retriever(
        embedding=embeddings,
        k=k,
    )



def get_hybrid_search_retriever(embedding: HuggingFaceEmbeddings,
                                k: int = 3) -> MongoDBAtlasHybridSearchRetriever:
    vector_store = MongoDBAtlasVectorSearch.from_connection_string(
        connection_string=settings.MONGODB_URI,
        embedding=embedding,
        namespace=f"{settings.MONGO_DB_NAME}.{settings.MONGO_LONG_TERM_MEMORY_COLLECTION}",
        text_key="chunk",
        embedding_key="embedding",
        relevance_score_fn="dotProduct",
    )
    
    retriever = MongoDBAtlasHybridSearchRetriever(
        vectorstore=vector_store,
        search_index_name=settings.MONGO_RAG_INDEX_NAME,
        k=k,
        vector_penalty=50,
        fulltext_penalty=50
    )
    
    return retriever