from app.repositories.metadata_repository import MetadataRepository
from app.services.column_vectore_store_service import ColumnVectorStoreService

repo = MetadataRepository()
service = ColumnVectorStoreService()

service.reset()
service.index_metadata(repo.get_all_tables())

print("Column index rebuilt.")