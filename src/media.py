import logging
from argparser import parse_args


def main() -> None:
    args = parse_args()

    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=log_level,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    if args.verbose:
        logging.info("Verbose mode enabled")

    # Call the function attached to the subcommand
    args.func(args)


if __name__ == "__main__":
    main()
