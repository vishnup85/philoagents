from langchain_huggingface import HuggingFaceEmbeddings
EmbeddingsModel = HuggingFaceEmbeddings

def get_embeddings(model_name: str, 
                   device: str = "cpu") -> EmbeddingsModel:
    return get_huggingface_embeddings(model_name=model_name, device=device)


def get_huggingface_embeddings(model_name: str,
                               device: str) -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device, "trust_remote_code": True},
        encode_kwargs={"normalize_embeddings": False},
    )