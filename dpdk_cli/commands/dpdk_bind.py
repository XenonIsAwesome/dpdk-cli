from dataclasses import dataclass

from dpdk_cli.utils.base_command import BaseCommand


@dataclass
class InterfaceData:
    original_driver: str  # i40e
    dpdk_driver: str  # vfio-pci


class DpdkBindCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("bind", help="Bind interface to a DPDK driver")
        parser.add_argument("interfaces", help="Network interface to bind")
        parser.add_argument(
            "driver",
            nargs="?",
            default=None,
            help="Driver to bind to (default: auto-detect DPDK driver)",
        )
        parser.add_argument(
            "--permanent",
            action="store_true",
            help="Make the binding permanent (uses driverctl)",
        )
        parser.set_defaults(handler=DpdkBindCommand.handle)

    @staticmethod
    def handle(args):
        # For iface in interface-glob:
        #   Do we have driver?
        #       N:
        #           1. Parse dpdk-devbind.py -s
        #           2. Filter only for relevant interface
        #           3. Parse line into InterfaceData object
        #           4. `dpdk-devbind.py <iface> -b <driver that is not enabled>`
        #       Y: `dpdk-devbind.py <iface> -b <driver>`
        raise NotImplementedError()
