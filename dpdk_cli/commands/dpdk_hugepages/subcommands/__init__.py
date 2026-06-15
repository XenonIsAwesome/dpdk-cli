from argparse import ArgumentParser

from dpdk_cli.commands.dpdk_hugepages.subcommands.dpdk_hugepages_clear import DpdkHugePagesClearCommand
from dpdk_cli.commands.dpdk_hugepages.subcommands.dpdk_hugepages_mount import DpdkHugePagesMountCommand
from dpdk_cli.commands.dpdk_hugepages.subcommands.dpdk_hugepages_reserve import DpdkHugePagesReserveCommand
from dpdk_cli.commands.dpdk_hugepages.subcommands.dpdk_hugepages_setup import DpdkHugePagesSetupCommand
from dpdk_cli.commands.dpdk_hugepages.subcommands.dpdk_hugepages_unmount import DpdkHugePagesUnmountCommand


def register_subcommands(subparsers):
    DPDK_HUGEPAGES_SUBCOMMAND_CLASSES = [
        DpdkHugePagesClearCommand,
        DpdkHugePagesMountCommand,
        DpdkHugePagesReserveCommand,
        DpdkHugePagesSetupCommand,
        DpdkHugePagesUnmountCommand
    ]

    for subcommand_cls in DPDK_HUGEPAGES_SUBCOMMAND_CLASSES:
        subcommand_cls.add_subparser(subparsers)
