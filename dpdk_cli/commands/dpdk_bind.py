import logging

from dpdk_cli.consts import DPDK_DEVBIND_EXEC_NAME, DRIVERCTL_EXEC_NAME
from dpdk_cli.utils import resolve_interfaces, run_cmd, parse_dpdk_devbind_status, find_exec, require_sudo, \
    NetworkInterfaceData

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
        iface_to_data = resolve_interfaces(parse_dpdk_devbind_status(), args.interfaces)
        if not iface_to_data:
            logging.error("No matching interfaces found")
            exit(1)

        driver = args.driver

        def handle_devbind_single(iface_data: NetworkInterfaceData, chosen_driver: str):
            devbind = find_exec(DPDK_DEVBIND_EXEC_NAME)
            run_cmd([str(devbind), "-b", chosen_driver, iface_data.pci_address], capture_output=False, dry_run=args.dry_run)

        def handle_driverctl_single(iface_data: NetworkInterfaceData, chosen_driver: str):
            driverctl = find_exec(DRIVERCTL_EXEC_NAME)

            cmd = [str(driverctl)]
            if iface_data.is_dpdk:
                cmd += ["unset-override", iface_data.pci_address]
            else:
                cmd += ["set-override", iface_data.pci_address, chosen_driver]

            run_cmd(cmd, capture_output=False, dry_run=args.dry_run)

        for iface, data in iface_to_data.items():
            iface_driver = driver
            if iface_driver is None and data.unused_driver is not None:
                iface_driver = data.unused_driver

            if args.permanent:
                handle_driverctl_single(data, iface_driver)
            else:
                handle_devbind_single(data, iface_driver)
