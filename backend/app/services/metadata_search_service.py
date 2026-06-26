from app.services.vector_store_service import VectorStoreService


class MetadataSearchService:

    def __init__(self):
        self.vector_store = VectorStoreService()

    def semantic_score(self, distance):
        return 1 / (1 + distance)

    def table_name_score(self, question, table_name):
        return 1.0 if table_name.lower() in question.lower() else 0.0

    def combine_scores(self, semantic, name_score):
        return (0.7 * semantic) + (0.3 * name_score)

    def search(self, question, k=10):

        raw_results = self.vector_store.search(question, k=k)

        ranked = []

        for doc, distance in raw_results:

            table_name = doc.metadata["table_name"]

            semantic = self.semantic_score(distance)
            name_score = self.table_name_score(question, table_name)
            final_score = self.combine_scores(semantic, name_score)

            ranked.append({
                "table": table_name,
                "score": round(final_score, 4),
                "distance": round(distance, 4)
            })

        ranked.sort(key=lambda x: x["score"], reverse=True)

        return ranked