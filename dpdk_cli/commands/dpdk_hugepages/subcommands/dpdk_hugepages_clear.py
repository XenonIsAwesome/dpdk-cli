from dpdk_cli.utils.base_command import BaseCommand


class DpdkHugePagesClearCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser(
            "clear", help="Clear existing huge page reservations"
        )
        parser.add_argument(
            "driver", nargs="?", help="Driver to clear reservations for"
        )
        parser.set_defaults(handler=DpdkHugePagesClearCommand.handle)

    @staticmethod
    def handle(args):
        logging.debug("TODO: Implement dpdk hugepages clear")
        raise NotImplementedError()
