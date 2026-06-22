from app.database.mysql_connector import get_connection

def get_tables():
    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE()""")
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    return tables

def get_columns(table_name):
    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute(f"""SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = %s""", (table_name,))
    columns = cursor.fetchall()
    cursor.close()
    conn.close()
    return columns
