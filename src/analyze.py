from argparse import Namespace

from util import check_database


def analyze_command(args: Namespace) -> None:
    print("Running analyze command")
    print(args)
    analyze(args.database_path)


def analyze(db_path: str) -> None:
    check_database(db_path)
