import mysql.connector

from app.config.settings import settings


def get_connection():
    """
    Create and return a MySQL database connection.
    """

    return mysql.connector.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
    )