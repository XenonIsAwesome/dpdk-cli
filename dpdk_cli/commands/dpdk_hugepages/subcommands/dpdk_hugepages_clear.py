import logging

from dpdk_cli.utils import add_node_param
from dpdk_cli.consts import DPDK_HUGEPAGES_EXEC_NAME
from dpdk_cli.utils import run_cmd, find_exec
from dpdk_cli.utils.base_command import BaseCommand


class DpdkHugePagesClearCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser(
            "clear", help="Clear existing huge page reservations"
        )

        add_node_param(parser)

        parser.set_defaults(handler=DpdkHugePagesClearCommand.handle)

    @staticmethod
    def handle(args):
        hugepages = find_exec(DPDK_HUGEPAGES_EXEC_NAME)

        logging.info("Clearing huge page reservations")
        run_cmd([str(hugepages), "-c"], capture_output=False, dry_run=args.dry_run)
