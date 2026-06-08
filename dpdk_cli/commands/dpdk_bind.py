import logging

from dpdk_cli.consts import DPDK_DEVBIND_EXEC_NAME
from dpdk_cli.utils import resolve_interfaces, run_cmd, parse_dpdk_devbind, find_exec, require_sudo

from dpdk_cli.utils.base_command import BaseCommand


class DpdkBindCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("bind", help="Bind interface to a DPDK driver")
        parser.add_argument(
            "interfaces",
            nargs="+",
            help="Network interface name(s) or glob pattern(s) (e.g. eno1 eno2, eno*)",
        )
        parser.add_argument(
            "--driver",
            "-d",
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
        require_sudo()
        devbind = find_exec(DPDK_DEVBIND_EXEC_NAME)

        iface_to_data = resolve_interfaces(parse_dpdk_devbind(), args.interfaces)
        if not iface_to_data:
            logging.error("No matching interfaces found")
            exit(1)

        driver = args.driver
        for iface, data in iface_to_data.items():
            iface_driver = driver
            if iface_driver is None and data.unused_driver is not None:
                iface_driver = data.unused_driver

            result = run_cmd([str(devbind), "-b", iface_driver, data.pci_address], sudo=True, capture_output=False)
            if result.returncode != 0:
                raise exit(result.returncode)
