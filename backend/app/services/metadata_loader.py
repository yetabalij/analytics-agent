from typing import List
import json

from app.domain.models.table_metadata import TableMetadata
from app.domain.models.column_metadata import ColumnMetadata

from app.database.metadata_extractor import get_tables, get_columns
from app.config.paths import MERGED_CATALOG_FILE


class MetadataLoader:
    """
    Single source of truth for all metadata.
    Combines DB + dictionary enrichment.
    """

    def load_from_database(self) -> List[TableMetadata]:

        tables = get_tables()
        result = []

        for table in tables:
            table_name = table[0]
            columns = get_columns(table_name)

            table_meta = TableMetadata(
                name=table_name,
                columns=[
                    ColumnMetadata(
                        name=col[0],
                        data_type=col[1]
                    )
                    for col in columns
                ]
            )

            result.append(table_meta)

        return result

    def load_enriched_metadata(self) -> List[TableMetadata]:
        """
        Load merged catalog JSON (PDF + DB enriched version)
        and convert into domain objects.
        """

        with open(MERGED_CATALOG_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        result = []

        for table in raw_data:

            columns = [
                ColumnMetadata(
                    name=col["name"],
                    data_type=col.get("data_type"),
                    description=col.get("description"),
                    primary_key=False,
                    foreign_key=False
                )
                for col in table.get("columns", [])
            ]

            table_meta = TableMetadata(
                name=table["table"],
                synonym=table.get("synonym"),
                description=table.get("description"),
                columns=columns
            )

            result.append(table_meta)

        return result

    def load_full_metadata(self) -> List[TableMetadata]:
        """
        MAIN ENTRY POINT
        """

        return self.load_enriched_metadata()