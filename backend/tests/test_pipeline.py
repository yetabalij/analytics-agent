from app.core.db import get_connection
from app.services.schema_extractor import SchemaExtractor

#######     connection test     #######
def test_database_connection():
    conn = get_connection()

    assert conn.is_connected()

    print("✓ Database connection successful")

    conn.close()


######### SchemaExtractor test #########
def test_schema_extractor():
    extractor = SchemaExtractor()

    schema = extractor.get_schema()

    print("Tables found:", len(schema))

    first_table = list(schema.keys())[0]

    print("Sample table:", first_table)
    print(schema[first_table])


if __name__ == "__main__":
    #test_database_connection()
    test_schema_extractor()
    