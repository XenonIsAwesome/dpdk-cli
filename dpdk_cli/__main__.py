import argparse
import logging
import sys

from dpdk_cli.commands import register_subparsers


def main():
    parser = argparse.ArgumentParser(
        prog="dpdk",
        description="DPDK CLI - Manage DPDK resources",
    )

    parser.add_argument("--dry-run", action='store_true', help="Prints dangerous commands instead of executing them")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    register_subparsers(subparsers)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        exit(1)

    try:
        args.handler(args)
    except NotImplementedError:
        logging.critical(
            f"The command `dpdk {' '.join(sys.argv[1:])}` is not implemented yet..."
        )
        exit(1)
    except Exception as e:
        logging.critical(f"Exception occurred during execution of the command: {e}")
        exit(1)


if __name__ == "__main__":
    main()
