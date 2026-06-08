from dpdk_cli.commands.dpdk_hugepages.subcommands.dpdk_hugepages_clear import DpdkHugePagesClearCommand
from dpdk_cli.commands.dpdk_hugepages.subcommands.dpdk_hugepages_mount import DpdkHugePagesMountCommand
from dpdk_cli.commands.dpdk_hugepages.subcommands.dpdk_hugepages_page import DpdkHugePagesPageCommand
from dpdk_cli.commands.dpdk_hugepages.subcommands.dpdk_hugepages_node import DpdkHugePagesNodeCommand
from dpdk_cli.commands.dpdk_hugepages.subcommands.dpdk_hugepages_reserve import DpdkHugePagesReserveCommand
from dpdk_cli.commands.dpdk_hugepages.subcommands.dpdk_hugepages_setup import DpdkHugePagesSetupCommand
from dpdk_cli.commands.dpdk_hugepages.subcommands.dpdk_hugepages_unmount import DpdkHugePagesUnmountCommand
from dpdk_cli.utils.base_command import BaseCommand


class DpdkHugePagesCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("hugepages", help="Manage huge pages")
        sub = parser.add_subparsers(dest="hugepages_command")

        DpdkHugePagesUnmountCommand.add_subparser(sub)
        DpdkHugePagesMountCommand.add_subparser(sub)
        DpdkHugePagesNodeCommand.add_subparser(sub)
        DpdkHugePagesPageCommand.add_subparser(sub)
        DpdkHugePagesClearCommand.add_subparser(sub)
        DpdkHugePagesReserveCommand.add_subparser(sub)
        DpdkHugePagesSetupCommand.add_subparser(sub)

        parser.set_defaults(handler=DpdkHugePagesCommand.handle)

    @staticmethod
    def handle(args):
        raise NotImplementedError()
