import logging

from dpdk_cli.utils.base_command import BaseCommand


class DpdkStatusCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("status", help="Show status on everything")
        parser.set_defaults(handler=DpdkStatusCommand.handle)

    @staticmethod
    def handle(args):
        logging.debug("TODO: Implement dpdk status")
        raise NotImplementedError()
