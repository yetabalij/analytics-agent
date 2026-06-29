# convert database metadata into structured catalog objects
import json
from pathlib import Path
from app.config.paths import (
    METADATA_DIR,
    CATALOG_FILE
)

from app.database.metadata_extractor import (
    get_tables,
    get_columns
)


def build_catalog():

    catalog = []

    tables = get_tables()

    for table in tables:

        table_name = table[0]

        columns = get_columns(table_name)

        catalog.append({
            "table": table_name,
            "columns": [
                {
                    "name": column[0],
                    "type": column[1]
                }
                for column in columns
            ]
        })

    return catalog


def save_catalog():

    catalog = build_catalog()

    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(
            catalog,
            f,
            indent=4
        )

    print(f"Catalog saved to {CATALOG_FILE}")