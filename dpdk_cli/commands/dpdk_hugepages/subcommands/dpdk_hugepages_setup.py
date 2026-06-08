import logging

from dpdk_cli.utils.base_command import BaseCommand

DEFAULT_PAGE_SIZE_KB = 2048
DEFAULT_MOUNT_POINT = "/mnt/huge"


class DpdkHugePagesSetupCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser(
            "setup", help="Clear, unmount, reserve, and mount hugepages"
        )
        parser.add_argument("size", help="Total hugepage memory (e.g., 16G, 4096M)")
        parser.set_defaults(handler=DpdkHugePagesSetupCommand.handle)

    @staticmethod
    def handle(args):
        logging.debug("TODO: Implement dpdk hugepages setup")
        raise NotImplementedError()
