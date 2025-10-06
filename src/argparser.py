import argparse
from argparse import Namespace

from import_media import import_command


def build_parser() -> argparse.ArgumentParser:
    """Builds and returns the argument parser."""
    parser = argparse.ArgumentParser(description="Media management CLI")

    # Global options
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Import subcommand
    import_parser = subparsers.add_parser(
        "import", help="Import media files to database"
    )
    import_parser.add_argument(
        "database_path", type=str, help="Path to the database file"
    )
    import_parser.add_argument(
        "--media_folders", type=str, nargs="+", help="Paths to media folders"
    )
    import_parser.set_defaults(func=import_command)

    return parser


def parse_args() -> Namespace:
    """Parse command line arguments and return them."""
    parser = build_parser()
    return parser.parse_args()
