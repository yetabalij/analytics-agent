def build_document(table):

    text_parts = []

    # Table header (VERY IMPORTANT FOR RETRIEVAL)
    text_parts.append(f"TABLE: {table['table']}")

    if table.get("description"):
        text_parts.append(f"DESCRIPTION: {table['description']}")

    if table.get("synonym"):
        text_parts.append(f"SYNONYM: {table['synonym']}")

    text_parts.append("COLUMNS:")

    # Columns section
    for column in table.get("columns", []):

        col_text = (
            f"{column['name']} "
            f"{column.get('data_type', '')} "
            f"{column.get('description', '')}"
        )

        text_parts.append(col_text)

    return "\n".join(text_parts)