from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

class VectorStoreService:

    def __init__(self):

        self.embedding_model = (
            HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2"
            )
        )

        self.vector_store = Chroma(
            collection_name="metadata",
            embedding_function=self.embedding_model,
            persist_directory="chroma_db"
        )