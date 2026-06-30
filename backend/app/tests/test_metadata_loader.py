from app.services.metadata_loader import MetadataLoader

loader = MetadataLoader()

metadata = loader.load_full_metadata()

print(f"Loaded tables: {len(metadata)}")

print(metadata[0].model_dump())