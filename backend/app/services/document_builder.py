def build_document(table):

    text = f"""
    Table Name:
    {table['table']}

    Description:
    {table.get('description', '')}

    Synonym:
    {table.get('synonym', '')}
    """

    for column in table["columns"]:

        text += f"""

        Column Name:
        {column['name']}

        Data Type:
        {column['data_type']}

        Description:
        {column.get('description', '')}
        """

    return text

table = {
    "table": "accounts",
    "description": "Manages all bank accounts",
    "columns": [
        {
            "name": "opened_date",
            "data_type": "date",
            "description": "Account opening date"
        }
    ]
}