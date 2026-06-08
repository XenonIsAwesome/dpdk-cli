import logging

from dpdk_cli.utils.base_command import BaseCommand

DEFAULT_PAGE_SIZE_KB = 2048


class DpdkHugePagesReserveCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("reserve", help="Reserve huge pages")
        parser.add_argument(
            "size", help="Number of hugepages or total memory (e.g., 1024, 4G)"
        )
        parser.set_defaults(handler=DpdkHugePagesReserveCommand.handle)

    @staticmethod
    def handle(args):
        logging.debug("TODO: Implement dpdk hugepages reserve")
        raise NotImplementedError()
