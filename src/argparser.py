import argparse
from argparse import Namespace

from analyze import analyze_command


def build_parser() -> argparse.ArgumentParser:
    """Builds and returns the argument parser."""
    parser = argparse.ArgumentParser(description="Media management CLI")

    # Global options
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Analyze subcommand
    analyze_parser = subparsers.add_parser("analyze", help="Analyze media files")
    analyze_parser.add_argument(
        "database_path", type=str, help="Path to the database file"
    )
    analyze_parser.add_argument(
        "--media_folders", type=str, nargs="+", help="Paths to media folders"
    )
    analyze_parser.add_argument(
        "--media_type",
        type=str,
        choices=["image", "video"],
        help="Type of media to process",
    )
    analyze_parser.set_defaults(func=analyze_command)

    return parser


def parse_args() -> Namespace:
    """Parse command line arguments and return them."""
    parser = build_parser()
    return parser.parse_args()
