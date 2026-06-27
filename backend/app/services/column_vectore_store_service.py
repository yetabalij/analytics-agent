from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.services.column_document_builder import (
    build_column_document
)


class ColumnVectorStoreService:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        self.vector_store = Chroma(
            collection_name="metadata_columns",
            embedding_function=self.embedding_model,
            persist_directory="chroma_db"
        )

    def index_metadata(self, tables):

        documents = []
        metadatas = []

        for table in tables:

            for column in table["columns"]:

                documents.append(
                    build_column_document(
                        table,
                        column
                    )
                )

                metadatas.append(
                    {
                        "table": table["table"],
                        "column": column["name"]
                    }
                )

        self.vector_store.add_texts(
            texts=documents,
            metadatas=metadatas
        )

        print(
            f"Indexed {len(documents)} columns into the vector store."
        )

    def search(self, question, k=10):

        return self.vector_store.similarity_search_with_score(
            question,
            k=k
        )