from app.services.column_search_service import (
    ColumnSearchService
)

service = ColumnSearchService()

question = "Select first name, last name, and gender of every customers in the bank with low risk level"

results = service.search(
    question,
    table_name="customers"
)

print()
print("QUESTION")
print(question)
print()

for i, item in enumerate(results[:10], start=1):

    print("-" * 60)

    print("Rank:", i)
    print("Column:", item["column"])
    print("Score :", item["score"])
    print("Distance:", item["distance"])



"""from app.services.column_vectore_store_service import (
    ColumnVectorStoreService
)

service = ColumnVectorStoreService()

results = service.search(
    "account opening",
    k=1
)

doc, distance = results[0]

print(doc.metadata)"""