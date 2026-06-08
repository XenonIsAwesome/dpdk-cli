import logging

from dpdk_cli.commands.dpdk_hugepages.subcommands import register_subcommands
from dpdk_cli.utils.base_command import BaseCommand


class DpdkHugePagesCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("hugepages", help="Manage huge pages")
        sub = parser.add_subparsers(dest="hugepages_command")

        register_subcommands(sub)

        parser.set_defaults(handler=DpdkHugePagesCommand.handle)

    @staticmethod
    def handle(args):
        logging.debug("TODO: Implement dpdk hugepages")
        raise NotImplementedError()
