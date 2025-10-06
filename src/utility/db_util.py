import os
import logging
from sql import is_database_empty


def check_database(db_path: str) -> None:
    #  Check if the given database path location is a valid path
    if not db_path.endswith(".db"):
        raise ValueError(
            f"Invalid database path: {db_path}. "
            "The database must have a filename with the .db extension."
        )
    # Check if the database folder exists
    db_folder = os.path.dirname(db_path)
    if not os.path.exists(db_folder):
        raise ValueError(f"Database folder directory does not exist: {db_folder}")

    # Check if the database file exists
    if os.path.isfile(db_path):
        logging.info(f"Using database file : {db_path}")
        if is_database_empty(db_path):
            logging.debug("Database is empty")
        else:
            logging.debug("Database is not empty")
    else:
        logging.info(f"New database file to be created: {db_path}")
