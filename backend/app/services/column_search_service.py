from app.services.column_vectore_store_service import ColumnVectorStoreService


class ColumnSearchService:

    def __init__(self):
        self.vector_store = ColumnVectorStoreService()

    # -----------------------------
    # SEMANTIC SCORE
    # -----------------------------
    def semantic_score(self, distance):
        return 1 / (1 + distance)

    # -----------------------------
    # SCHEMA SIGNAL (GENERAL DB RULES)
    # -----------------------------
    def schema_score(self, column_name):

        name = column_name.lower()
        score = 0.0

        # time-related columns
        if any(x in name for x in ["date", "time", "created", "updated"]):
            score += 0.6

        # identifiers
        if "id" in name:
            score += 0.2

        # financial metrics
        if any(x in name for x in ["amount", "balance", "rate", "fee"]):
            score += 0.3

        # status/state columns
        if any(x in name for x in ["status", "state", "type"]):
            score += 0.2

        return score

    # -----------------------------
    # INTENT SIGNAL (GENERALIZED)
    # -----------------------------
    def intent_score(self, question, column_name):

        q = question.lower()
        c = column_name.lower()

        score = 0.0

        # overlap of meaningful tokens (NOT hardcoded rules)
        q_tokens = set(q.replace("_", " ").split())
        c_tokens = set(c.replace("_", " ").split())

        overlap = len(q_tokens.intersection(c_tokens))

        score += overlap * 0.3

        # weak semantic hints
        if "date" in q and "date" in c:
            score += 0.4

        return score

    # -----------------------------
    # SEARCH
    # -----------------------------
    def search(self, question, table_name=None, k=15):

        results = self.vector_store.search(question, k=k)

        ranked = []

        for doc, distance in results:

            meta = doc.metadata

            if table_name and meta["table"] != table_name:
                continue

            semantic = self.semantic_score(distance)
            schema = self.schema_score(meta["column"])
            intent = self.intent_score(question, meta["column"])

            # FINAL UNIVERSAL SCORING MODEL
            final_score = (
                0.65 * semantic +
                0.20 * schema +
                0.15 * intent
            )

            ranked.append({
                "table": meta["table"],
                "column": meta["column"],
                "score": round(final_score, 4),
                "semantic": round(semantic, 4),
                "schema": round(schema, 4),
                "intent": round(intent, 4),
                "distance": round(distance, 4)
            })

        ranked.sort(key=lambda x: x["score"], reverse=True)

        return ranked