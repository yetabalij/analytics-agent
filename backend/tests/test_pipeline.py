from app.core.db import get_connection
from app.services.schema_extractor import SchemaExtractor
from app.services.schema_mapper import SchemaMapper

####### connection test #######
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


######## SchemaMapper test #########
def test_schema_mapper():

    extractor = SchemaExtractor()
    raw_schema = extractor.get_schema()

    mapper = SchemaMapper()
    domain_tables = mapper.map(raw_schema)

    print("Mapped tables:", len(domain_tables))

    first = domain_tables[0]

    print("\nFirst table:")
    print("Name:", first.name)
    print("Columns:", len(first.columns))
    print("PKs:", first.primary_keys)
    print("FKs:", first.foreign_keys)


if __name__ == "__main__":
    # test_database_connection()
    # test_schema_extractor()
    test_schema_mapper()
   