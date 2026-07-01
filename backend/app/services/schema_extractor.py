from typing import List

from app.core.db import get_connection


class SchemaExtractor:
    """
    Extracts database schema into domain models.

    Version 1:
        - Load table names only.
    """

    def __init__(self):
        self.connection = get_connection()

    def _load_tables(self) -> List[str]:
        """
        Returns all user tables in the database.
        """

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
        """
        Returns column metadata for a given table.
        """

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
    
    def extract_schema(self):
        """
        Returns full schema: tables + columns (raw dict structure).
        """

        schema = {}

        for table in self._load_tables():
            columns_raw = self._load_columns(table)

            schema[table] = {
                "columns": [
                    {
                        "name": col[0],
                        "data_type": col[1],
                        "nullable": col[2],
                        "key": col[3],
                        "default": col[4],
                        "extra": col[5],
                    }
                    for col in columns_raw
                ]
            }

        return schema
    
    def get_schema(self):
        """
        Public API for schema extraction.
        """
        return self.extract_schema()