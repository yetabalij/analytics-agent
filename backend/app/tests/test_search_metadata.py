from app.services.vector_store_service import (
    VectorStoreService
)

vector_store = VectorStoreService()

results = vector_store.search(
    "how many accounts opend last month?"
)

for i, result in enumerate(results, start=1):
    print("=" * 80)
    print(f"Result {i}:")
    print("Metadata:", result.metadata)
    print()
    print(result.page_content[:600])
    print