from argparse import ArgumentParser

from dpdk_cli.utils.base_command import BaseCommand


class DpdkInstallCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser: ArgumentParser = subparsers.add_parser(
            "install", help="Installs all required dependencies for the package to work"
        )
        parser.add_argument("-y", "--yes", dest="yes", action="store_true", help="Don't ask for confirmation")
        parser.set_defaults(handler=DpdkInstallCommand.handle)

    @staticmethod
    def handle(args):
        raise NotImplementedError()
