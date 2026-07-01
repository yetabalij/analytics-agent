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