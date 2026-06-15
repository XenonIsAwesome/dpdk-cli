import logging

from dpdk_cli.consts import DPDK_HUGEPAGES_EXEC_NAME
from dpdk_cli.utils import find_exec, run_cmd
from dpdk_cli.utils.base_command import BaseCommand


class DpdkHugePagesMountCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("mount", help="Mount the huge page filesystem")
        parser.set_defaults(handler=DpdkHugePagesMountCommand.handle)

    @staticmethod
    def handle(args):
        hugepages = find_exec(DPDK_HUGEPAGES_EXEC_NAME)

        logging.info("Mounting huge page filesystem")
        run_cmd([str(hugepages), "-m"], capture_output=False, dry_run=args.dry_run)
