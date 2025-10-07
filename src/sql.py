import sqlite3
import logging
from sqlite3 import Connection

from data_types import MediaData


def connect_to_db(file_path: str) -> Connection:
    conn = sqlite3.connect(file_path)
    logging.debug(f"Connected to database {file_path}")
    return conn


def close_connection(conn: Connection) -> None:
    if conn:
        conn.close()
        logging.debug("Database connection closed.")


def create_table(conn: Connection) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS media (
        date TEXT,
        file_path TEXT PRIMARY KEY,
        type TEXT,
        sequence TEXT,
        origin TEXT,
        size INTEGER,
        UNIQUE(date, file_path)
    )
    """
    )

    conn.commit()
    cursor.close()


def insert_media_data(database_path: str, data: list[MediaData]) -> None:
    """
    Inserts media data into the database.
    Args:
        database_path (str): The path to the SQLite database file.
        data (db_media_type): A list of tuples containing the media data.
    """
    try:
        logging.debug(f"Initializing database at: {database_path}")
        conn = connect_to_db(database_path)
        create_table(conn)
        cursor = conn.cursor()
        cursor.executemany(
            """
            INSERT OR REPLACE INTO media (date, file_path, type, sequence, origin, size)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            data,
        )
        conn.commit()
        cursor.close()
        close_connection(conn)
    except Exception as e:
        print(f"Failed to initialize database table: {e}")
