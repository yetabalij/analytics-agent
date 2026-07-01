from typing import List, Dict, Any

from app.domain.models.table import Table
from app.domain.models.column import Column


class SchemaMapper:

    def map(self, raw_schema: Dict[str, Any]) -> List[Table]:

        tables: List[Table] = []

        for table_name, table_data in raw_schema.items():

            columns = [
                Column(
                    name=col["name"],
                    data_type=col.get("data_type"),
                    description=None,
                    nullable=(col.get("nullable") == "YES"),

                    # PK detection
                    primary_key=(col.get("key") == "PRI"),

                    # ⭐ REAL FK DETECTION
                    foreign_key=bool(col.get("references_table")),

                    references_table=col.get("references_table"),
                    references_column=col.get("references_column"),

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