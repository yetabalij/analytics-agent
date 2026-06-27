def build_column_document(table, column):
    """
    Builds one searchable document for a single column.
    """

    return f"""
    Table: {table['table']}

    Table Description: {table.get('description', '')}

    Column: {column['name']}

    Data Type: {column.get('data_type', '')}

    Column Description: {column.get('description', '')}
    """