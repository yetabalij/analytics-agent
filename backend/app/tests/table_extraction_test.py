import json

from app.knowledge.dictionary_parser import (
    extract_pdf_text,
    extract_table_section,
    parse_table,
)

from app.knowledge.cataloge_merger import merge_catalogs

from app.config.paths import (
    DICTIONARY_PDF,
    DICTIONARY_CATALOG_FILE,
    CATALOG_FILE,
    MERGED_CATALOG_FILE
)

# ========================
# STEP 1: PARSE PDF
# ========================
text = extract_pdf_text(DICTIONARY_PDF)

tables = extract_table_section(text)

print(f"Found {len(tables)} tables")

catalog = [parse_table(t) for t in tables]


# ========================
# STEP 2: SAVE DICTIONARY CATALOG
# ========================
with open(
    DICTIONARY_CATALOG_FILE,
    "w",
    encoding="utf-8"
) as f:
    json.dump(catalog, f, indent=4)

print(f"Wrote {len(catalog)} tables to dictionary catalog")


# ========================
# STEP 3: LOAD DB + MERGE
# ========================
with open(CATALOG_FILE, "r", encoding="utf-8") as f:
    db_catalog = json.load(f)

with open(DICTIONARY_CATALOG_FILE, "r", encoding="utf-8") as f:
    dictionary_catalog = json.load(f)

merged = merge_catalogs(db_catalog, dictionary_catalog)

# ========================
# STEP 4: OUTPUT save merged catalog
# ========================
with open(
    MERGED_CATALOG_FILE,
    "w",
    encoding="utf-8"
) as f:
    json.dump(merged, f, indent=4)

print(f"Wrote {len(merged)} tables to merged catalog")

# ========================
# STEP 5: OUTPUT CHECK
# ========================
print("\n=== SAMPLE MERGED TABLE ===\n")
print(json.dumps(merged[0], indent=4))