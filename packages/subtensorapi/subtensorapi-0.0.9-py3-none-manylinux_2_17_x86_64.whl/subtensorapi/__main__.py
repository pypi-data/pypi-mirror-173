import argparse

from . import __version__, cli

from typing import List, Optional
import sys


def main(args: Optional[List[str]] = sys.argv[1:]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=__version__)

    cmd_parsers = parser.add_subparsers(dest="command")

    sync_and_save = cmd_parsers.add_parser("sync_and_save")
    cli.add_args_sync_and_save(sync_and_save)

    blockAtRegistration_for_all_and_save = cmd_parsers.add_parser(
        "blockAtRegistration_for_all_and_save"
    )
    cli.add_args_blockAtRegistration_for_all_and_save(
        blockAtRegistration_for_all_and_save
    )

    parsed_args = parser.parse_args(args)

    if parsed_args.command == "sync_and_save":
        cli.sync_and_save(parsed_args)
    elif parsed_args.command == "blockAtRegistration_for_all_and_save":
        cli.blockAtRegistration_for_all_and_save(parsed_args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main(sys.argv[1:])
