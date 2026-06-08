import argparse
import logging
import sys

from dpdk_cli.commands.dpdk_bind import DpdkBindCommand
from dpdk_cli.commands.dpdk_capture import DpdkCaptureCommand
from dpdk_cli.commands.dpdk_hugepages import DpdkHugePagesCommand
from dpdk_cli.commands.dpdk_install import DpdkInstallCommand
from dpdk_cli.commands.dpdk_status import DpdkStatusCommand
from dpdk_cli.commands.dpdk_top import DpdkTopCommand


def main():
    parser = argparse.ArgumentParser(
        prog="dpdk",
        description="DPDK CLI - Manage DPDK resources",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    DpdkStatusCommand.add_subparser(subparsers)
    DpdkBindCommand.add_subparser(subparsers)
    DpdkTopCommand.add_subparser(subparsers)
    DpdkCaptureCommand.add_subparser(subparsers)
    DpdkHugePagesCommand.add_subparser(subparsers)
    DpdkInstallCommand.add_subparser(subparsers)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

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
