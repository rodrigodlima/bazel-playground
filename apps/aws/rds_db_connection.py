import os
import pymysql
from pymysql.cursors import DictCursor


def get_connection():
    """Create a connection to RDS MySQL using environment variables."""
    return pymysql.connect(
        host=os.environ.get('RDS_HOST'),
        port=int(os.environ.get('RDS_PORT', 3306)),
        user=os.environ.get('RDS_USER'),
        password=os.environ.get('RDS_PASSWORD'),
        database=os.environ.get('RDS_DATABASE'),
        cursorclass=DictCursor
    )


def execute_query(query: str, params: tuple = None) -> list:
    """Execute a SELECT query and return results.

    Args:
        query: SQL query to execute
        params: Optional tuple of parameters for the query

    Returns:
        List of dictionaries containing the results
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    finally:
        connection.close()


def execute_insert(query: str, params: tuple = None) -> int:
    """Execute an INSERT/UPDATE/DELETE query.

    Args:
        query: SQL query to execute
        params: Optional tuple of parameters for the query

    Returns:
        Number of affected rows
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
            return cursor.rowcount
    finally:
        connection.close()


def main():
    required_vars = ['RDS_HOST', 'RDS_USER', 'RDS_PASSWORD', 'RDS_DATABASE']
    missing = [var for var in required_vars if not os.environ.get(var)]

    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        return

    try:
        connection = get_connection()
        print("Connection to RDS MySQL successful!")

        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"MySQL version: {version['VERSION()']}")

        connection.close()

    except pymysql.Error as e:
        print(f"Error connecting to database: {e}")


if __name__ == '__main__':
    main()
