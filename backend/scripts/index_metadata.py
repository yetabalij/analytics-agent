from app.repositories.metadata_repository import (
    MetadataRepository
)

from app.services.vector_store_service import (
    VectorStoreService
)

repository = MetadataRepository()

tables = repository.get_all_tables()

vector_service = VectorStoreService()

vector_service.index_metadata(tables)

print(
    f"Indexed {len(tables)} tables into the vector store."
)