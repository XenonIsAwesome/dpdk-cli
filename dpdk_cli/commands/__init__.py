from dpdk_cli.commands.dpdk_bind import DpdkBindCommand
from dpdk_cli.commands.dpdk_capture import DpdkCaptureCommand
from dpdk_cli.commands.dpdk_hugepages import DpdkHugePagesCommand
from dpdk_cli.commands.dpdk_install import DpdkInstallCommand
from dpdk_cli.commands.dpdk_status import DpdkStatusCommand
from dpdk_cli.commands.dpdk_top import DpdkTopCommand


def register_subparsers(subparsers):
    DPDK_COMMAND_CLASSES = [
        DpdkBindCommand,
        DpdkCaptureCommand,
        DpdkHugePagesCommand,
        DpdkInstallCommand,
        DpdkStatusCommand,
        DpdkTopCommand
    ]

    for command_cls in DPDK_COMMAND_CLASSES:
        command_cls.add_subparser(subparsers)
