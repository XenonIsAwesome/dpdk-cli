from dpdk_cli.utils.base_command import BaseCommand

PAGE_SIZES = {
    "4k": 4,
    "64k": 64,
    "2m": 2048,
    "1g": 1048576,
}


class DpdkHugePagesPageCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("page", help="Select hugepage size to use")
        parser.add_argument(
            "size", nargs="?", default=None, help="Hugepage size (e.g., 2M, 1G)"
        )
        parser.set_defaults(handler=DpdkHugePagesPageCommand.handle)

    @staticmethod
    def handle(args):
        raise NotImplementedError()
