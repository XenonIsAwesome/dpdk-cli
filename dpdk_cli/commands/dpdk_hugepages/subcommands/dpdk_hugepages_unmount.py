from dpdk_cli.utils.base_command import BaseCommand


class DpdkHugePagesUnmountCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("unmount", help="Unmount the huge page filesystem")
        parser.set_defaults(handler=DpdkHugePagesUnmountCommand.handle)

    @staticmethod
    def handle(args):
        raise NotImplementedError()
