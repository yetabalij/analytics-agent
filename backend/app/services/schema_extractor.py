from typing import List, Dict
from app.core.db import get_connection


class SchemaExtractor:
    """
    Extracts database schema into raw structured dict.
    """

    def __init__(self):
        self.connection = get_connection()

    def _load_tables(self) -> List[str]:
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = DATABASE()
            ORDER BY table_name;
        """

        cursor = self.connection.cursor()
        cursor.execute(query)
        tables = cursor.fetchall()
        cursor.close()

        return [table[0] for table in tables]

    def _load_columns(self, table_name: str):
        query = """
            SELECT
                column_name,
                data_type,
                is_nullable,
                column_key,
                column_default,
                extra
            FROM information_schema.columns
            WHERE table_schema = DATABASE()
                AND table_name = %s
            ORDER BY ordinal_position;
        """

        cursor = self.connection.cursor()
        cursor.execute(query, (table_name,))
        columns = cursor.fetchall()
        cursor.close()

        return columns

    def _load_foreign_keys(self):
        """
        Proper FK extraction from MySQL metadata
        """
        query = """
            SELECT
                table_name,
                column_name,
                referenced_table_name,
                referenced_column_name
            FROM information_schema.key_column_usage
            WHERE table_schema = DATABASE()
              AND referenced_table_name IS NOT NULL;
        """

        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        fk_map = {}

        for row in rows:
            table = row[0]
            column = row[1]

            fk_map[(table, column)] = {
                "ref_table": row[2],
                "ref_column": row[3]
            }

        return fk_map

    def extract_schema(self):
        schema = {}

        tables = self._load_tables()
        fk_map = self._load_foreign_keys()

        for table in tables:
            columns_raw = self._load_columns(table)

            columns = []

            for col in columns_raw:
                col_name = col[0]

                fk_info = fk_map.get((table, col_name))

                columns.append({
                    "name": col_name,
                    "data_type": col[1],
                    "nullable": col[2],
                    "key": col[3],
                    "default": col[4],
                    "extra": col[5],

                    # ⭐ IMPORTANT FIX
                    "references_table": fk_info["ref_table"] if fk_info else None,
                    "references_column": fk_info["ref_column"] if fk_info else None
                })

            schema[table] = {
                "columns": columns
            }

        return schema

    def get_schema(self):
        return self.extract_schema()