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