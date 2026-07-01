from app.core.db import get_connection

"""
#######     connection test     #######
def test_database_connection():
    conn = get_connection()

    assert conn.is_connected()

    print("✓ Database connection successful")

    conn.close()


if __name__ == "__main__":
    test_database_connection()
"""

######### SchemaExtractor test #########
from app.services.schema_extractor import SchemaExtractor


extractor = SchemaExtractor()

tables = extractor._load_tables()

print("\nTables found:")

for table in tables:
    print(f" - {table}")

print(f"\nTotal tables: {len(tables)}")