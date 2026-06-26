from app.services.metadata_search_service import (
    MetadataSearchService
)

service = MetadataSearchService()

question = "How many accounts opened last month?"

results = service.search(question)

print("=" * 80)
print("Question:", question)
print()

for i, result in enumerate(results, start=1):

    print("-" * 80)
    print(f"Rank {i}")
    print("Table      :", result["table"])
    print("Score      :", round(result["score"], 4))
    print("Distance   :", round(result["distance"], 4))

    print()