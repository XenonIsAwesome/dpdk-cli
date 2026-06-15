import logging

from dpdk_cli.commands.dpdk_hugepages.subcommands import register_subcommands
from dpdk_cli.utils import parse_dpdk_hugepages_status
from dpdk_cli.utils.base_command import BaseCommand


class DpdkHugePagesCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("hugepages", help="Show hugepages status")
        sub = parser.add_subparsers(dest="hugepages_command")

        register_subcommands(sub)

        parser.set_defaults(handler=DpdkHugePagesCommand.handle)

    @staticmethod
    def handle(args):
        status = parse_dpdk_hugepages_status()
        logging.info("Node\tPages\tSize\tTotal")
        for numa, info in status.numa_page_sizes.items():
            logging.info(f"{numa}\t{info.pages}\t{info.size_str}\t{info.total_str}")
        logging.info("")
        logging.info(f"HugePages mount: {status.hugepages_mount}")
