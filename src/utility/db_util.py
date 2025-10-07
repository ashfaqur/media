from pathlib import Path
import logging


def validate_database_path(db_path: str) -> bool:
    """
    Validate a database path.

    Args:
        db_path (str): The path to the database file.

    Returns:
        bool: True if the database file exists, False otherwise.

    Raises:
        ValueError: If the database path is invalid or the
        database folder directory does not exist.
    """
    path = Path(db_path)

    if path.suffix.lower() != ".db":
        raise ValueError(
            f"Invalid database path: {db_path}. "
            "The database must have a filename with the .db extension."
        )
    if not path.parent.exists():
        raise ValueError(f"Database folder directory does not exist: {path.parent}")
    exists = path.is_file()
    logging.info(
        f"{'Using existing' if exists else 'Database file does not exist yet'}: {path}"
    )
    return exists
