from dpdk_cli.utils.base_command import BaseCommand


class DpdkHugePagesMountCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("mount", help="Mount the huge page filesystem")
        parser.set_defaults(handler=DpdkHugePagesMountCommand.handle)

    @staticmethod
    def handle(args):
        raise NotImplementedError()
