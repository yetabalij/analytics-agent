from app.core.db import get_connection


def test_database_connection():
    conn = get_connection()

    assert conn.is_connected()

    print("✓ Database connection successful")

    conn.close()


if __name__ == "__main__":
    test_database_connection()