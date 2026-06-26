from app.services.metadata_context_builder import MetadataContextBuilder

builder = MetadataContextBuilder()

result = builder.build("How many accounts opened last month?")

print("\nFINAL OUTPUT")
print(result)