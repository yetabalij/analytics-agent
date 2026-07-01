from typing import List
from app.domain.models.table import Table
from app.domain.models.relationship import Relationship


class SchemaGraphBuilder:
    """
    Builds a graph (edges) from mapped schema tables.
    """

    def build(self, tables: List[Table]) -> List[Relationship]:

        relationships: List[Relationship] = []

        table_map = {t.name: t for t in tables}

        for table in tables:
            for col in table.columns:

                # only process real FK columns
                if col.foreign_key and col.references_table:

                    # validate target exists in schema
                    if col.references_table in table_map:

                        relationships.append(
                            Relationship(
                                source_table=table.name,
                                source_column=col.name,
                                target_table=col.references_table,
                                target_column=col.references_column or "id"
                            )
                        )

        return relationships