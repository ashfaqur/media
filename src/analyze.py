from argparse import Namespace


from utility.db_util import validate_database_path


def analyze_command(args: Namespace) -> None:
    print("Running analyze command")
    print(args)
    analyze(args.database_path)


def analyze(db_path: str) -> None:
    validate_database_path(db_path)
