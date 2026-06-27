import json

from app.services.column_vectore_store_service import (
    ColumnVectorStoreService
)

# Load merged metadata
with open(
    "app/knowledge/metadata/merged_catalog.json",
    "r",
    encoding="utf-8"
) as f:

    tables = json.load(f)

# Create service
vector_store = ColumnVectorStoreService()

# Index all columns
vector_store.index_metadata(tables)