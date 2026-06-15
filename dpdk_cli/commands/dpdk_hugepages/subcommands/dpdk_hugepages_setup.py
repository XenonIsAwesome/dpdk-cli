import logging

from dpdk_cli.utils import add_page_param, add_node_param
from dpdk_cli.consts import DPDK_HUGEPAGES_EXEC_NAME
from dpdk_cli.utils import run_cmd, find_exec
from dpdk_cli.utils.base_command import BaseCommand

DEFAULT_PAGE_SIZE_KB = 2048
DEFAULT_MOUNT_POINT = "/mnt/huge"


class DpdkHugePagesSetupCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser(
            "setup", help="Clear, unmount, reserve, and mount hugepages"
        )
        parser.add_argument("total_size", help="Total hugepage memory (e.g., 16G, 4096M)")

        add_node_param(parser)
        add_page_param(parser)

        parser.set_defaults(handler=DpdkHugePagesSetupCommand.handle)

    @staticmethod
    def handle(args):
        hugepages = find_exec(DPDK_HUGEPAGES_EXEC_NAME)

        cmd = [str(hugepages)]
        if args.page:
            cmd += ["--page", args.page]
        if args.node:
            cmd += ["--node", str(args.node)]
        cmd += ["--setup", str(args.total_size)]

        logging.info("Setting up %s huge pages (total size: %s), on NUMA node: %d", (args.page or "2Kb"),
                     args.total_size, (args.node or 0))
        run_cmd(cmd, capture_output=False, dry_run=args.dry_run)
