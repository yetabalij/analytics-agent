import json

class MetadataRepository:

    def __init__(self, path="app/knowledge/metadata/merged_catalog.json"):
        with open(path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

    def get_all_tables(self):
        return self.catalog
    
    