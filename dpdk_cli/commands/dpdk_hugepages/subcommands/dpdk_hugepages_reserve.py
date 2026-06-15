import logging

from dpdk_cli.utils import add_page_param, add_node_param
from dpdk_cli.consts import DPDK_HUGEPAGES_EXEC_NAME
from dpdk_cli.utils import find_exec, run_cmd
from dpdk_cli.utils.base_command import BaseCommand


class DpdkHugePagesReserveCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("reserve", help="Reserve huge pages")
        parser.add_argument(
            "total_size", help="Number of hugepages or total memory (e.g., 1024, 4G)"
        )

        add_node_param(parser)
        add_page_param(parser)

        parser.set_defaults(handler=DpdkHugePagesReserveCommand.handle)

    @staticmethod
    def handle(args):
        hugepages = find_exec(DPDK_HUGEPAGES_EXEC_NAME)

        cmd = [str(hugepages)]
        if args.page:
            cmd += ["--page", args.page]
        if args.node:
            cmd += ["--node", str(args.node)]
        cmd += ["--reserve", str(args.total_size)]

        logging.info("Reserving %s huge pages (total size: %s), on NUMA node: %d", (args.page or "2Kb"),
                     args.total_size, (args.node or 0))
        run_cmd(cmd, capture_output=False, dry_run=args.dry_run)
