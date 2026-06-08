from dpdk_cli.utils.base_command import BaseCommand


class DpdkHugePagesNodeCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser(
            "node", help="Set NUMA node for hugepage operations"
        )
        parser.add_argument(
            "node", type=int, help="NUMA node number"
        )
        parser.set_defaults(handler=DpdkHugePagesNodeCommand.handle)

    @staticmethod
    def handle(args):
        raise NotImplementedError()
