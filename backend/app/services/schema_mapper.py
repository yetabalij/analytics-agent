from typing import List, Dict, Any

from app.domain.models.table import Table
from app.domain.models.column import Column


class SchemaMapper:
    """
    Converts raw schema dictionary into domain models.
    """

    def map(self, raw_schema: Dict[str, Any]) -> List[Table]:
        tables: List[Table] = []

        for table_name, table_data in raw_schema.items():

            columns = [
                Column(
                    name=col["name"],
                    data_type=col.get("data_type"),
                    description=None,   # enrichment later
                    nullable=col.get("nullable", True),
                    primary_key=(col.get("key") == "PRI"),
                    foreign_key=(col.get("key") == "MUL"),
                    references_table=None,
                    references_column=None,
                    aliases=[],
                    sample_values=[]
                )
                for col in table_data.get("columns", [])
            ]

            table_meta = Table(
                name=table_name,
                synonym=None,
                description=None,
                columns=columns,
                primary_keys=[
                    c.name for c in columns if c.primary_key
                ],
                foreign_keys=[
                    c.name for c in columns if c.foreign_key
                ],
                aliases=[],
                business_domain=None,
                tags=[]
            )

            tables.append(table_meta)

        return tables