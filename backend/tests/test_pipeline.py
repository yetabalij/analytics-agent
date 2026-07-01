from app.core.db import get_connection
from app.services.schema_extractor import SchemaExtractor
from app.services.schema_mapper import SchemaMapper
from app.services.schema_graph_builder import SchemaGraphBuilder
from app.services.semantic.semantic_schema_enricher import SemanticSchemaEnricher

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

#### SchemaGraphBuilder test #########
def test_schema_graph_builder():

    extractor = SchemaExtractor()
    raw_schema = extractor.get_schema()

    mapper = SchemaMapper()
    tables = mapper.map(raw_schema)

    builder = SchemaGraphBuilder()
    relationships = builder.build(tables)

    print("Relationships found:", len(relationships))

    if relationships:
        r = relationships[0]
        print("Sample relationship:")
        print(r.source_table, "→", r.target_table)

def test_semantic_enricher():

    extractor = SchemaExtractor()
    raw = extractor.get_schema()

    mapper = SchemaMapper()
    tables = mapper.map(raw)

    enricher = SemanticSchemaEnricher()
    enriched = enricher.enrich(tables)

    first = enriched[0]

    print("\nTable:", first.name)
    print("Domain:", first.business_domain)
    print("Tags:", first.tags)

    print("\nSample column:")
    print(first.columns[0].name)
    print(first.columns[0].description)

if __name__ == "__main__":
    # test_database_connection()
    # test_schema_extractor()
    #test_schema_mapper()
    #test_schema_graph_builder()
    test_semantic_enricher()