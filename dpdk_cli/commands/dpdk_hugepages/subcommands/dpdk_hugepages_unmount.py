import logging

from dpdk_cli.consts import DPDK_HUGEPAGES_EXEC_NAME
from dpdk_cli.utils import find_exec, run_cmd
from dpdk_cli.utils.base_command import BaseCommand


class DpdkHugePagesUnmountCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("unmount", help="Unmount the huge page filesystem")
        parser.set_defaults(handler=DpdkHugePagesUnmountCommand.handle)

    @staticmethod
    def handle(args):
        hugepages = find_exec(DPDK_HUGEPAGES_EXEC_NAME)

        logging.info("Unmounting huge page filesystem")
        run_cmd([str(hugepages), "-u"], capture_output=False, dry_run=args.dry_run)
