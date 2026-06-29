import json
from app.config.paths import MERGED_CATALOG_FILE

class MetadataRepository:

    def __init__(self, path=MERGED_CATALOG_FILE):
        with open(path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

    def get_all_tables(self):
        return self.catalog
    
    