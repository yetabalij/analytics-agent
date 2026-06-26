from app.services.metadata_search_service import MetadataSearchService
from app.services.column_selection_service import ColumnSelector
from app.repositories.metadata_repository import MetadataRepository


class MetadataContextBuilder:

    def __init__(self):
        self.search = MetadataSearchService()
        self.columns = ColumnSelector()
        self.repo = MetadataRepository()

    def build(self, question):

        ranked_tables = self.search.search(question)

        table_map = {
            t["table"]: t for t in self.repo.get_all_tables()
        }

        result_tables = []
        result_columns = {}

        for item in ranked_tables[:3]:

            table_name = item["table"]
            table_data = table_map.get(table_name)

            if not table_data:
                continue

            cols = self.columns.select_columns(question, table_data)

            result_tables.append({
                "name": table_name,
                "score": item["score"]
            })

            result_columns[table_name] = cols

        return {
            "tables": result_tables,
            "columns": result_columns
        }