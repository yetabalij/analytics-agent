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

    def index_metadata(self, tables):

        documents = []
        metadatas = []

        for table in tables:

            document = build_document(table)

            documents.append(document)

            metadatas.append(
                {
                    "table_name": table["table"]
                }
            )

        self.vector_store.add_texts(
            texts=documents,
            metadatas=metadatas
        )

    def search(self, question, k=5):

        return self.vector_store.similarity_search(
            question,
            k=k
        )