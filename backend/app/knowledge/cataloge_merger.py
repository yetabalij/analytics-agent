import json


def merge_catalogs(db_catalog, dictionary_catalog):

    # safety: allow file path OR already-loaded list
    if isinstance(db_catalog, str):
        with open(db_catalog, "r", encoding="utf-8") as f:
            db_catalog = json.load(f)

    if isinstance(dictionary_catalog, str):
        with open(dictionary_catalog, "r", encoding="utf-8") as f:
            dictionary_catalog = json.load(f)

    dictionary_tables = {
        table["table"]: table
        for table in dictionary_catalog
        if isinstance(table, dict)
    }

    merged_catalog = []

    for db_table in db_catalog:

        table_name = db_table["table"]
        pdf_table = dictionary_tables.get(table_name, {})

        pdf_columns = {
            col["name"]: col
            for col in pdf_table.get("columns", [])
            if isinstance(col, dict)
        }

        merged_columns = []

        for db_column in db_table.get("columns", []):

            column_name = db_column["name"]
            pdf_column = pdf_columns.get(column_name, {})

            merged_columns.append({
                "name": column_name,
                "data_type": db_column.get("type"),
                "description": pdf_column.get("description")
            })

        merged_catalog.append({
            "table": table_name,
            "synonym": pdf_table.get("synonym"),
            "description": pdf_table.get("description"),
            "columns": merged_columns
        })

    return merged_catalog