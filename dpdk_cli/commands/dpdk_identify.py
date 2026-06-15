import logging

from dpdk_cli.utils import run_cmd, resolve_interfaces, parse_dpdk_devbind_status, find_exec
from dpdk_cli.utils.base_command import BaseCommand


class DpdkIdentifyCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser(
            "identify", help="Show visible port identification (e.g. blinking)"
        )
        parser.add_argument(
            "interfaces",
            nargs="+",
            help="Network interface name(s) or glob pattern(s) (e.g. eno1 eno2, eno*)",
        )
        parser.set_defaults(handler=DpdkIdentifyCommand.handle)

    @staticmethod
    def handle(args):
        # Resolving interfaces
        iface_to_data = resolve_interfaces(parse_dpdk_devbind_status(), args.interfaces)
        if not iface_to_data:
            logging.error("No matching interfaces found")
            exit(1)

        # Only one interface can be used in this command
        if len(iface_to_data) > 1:
            logging.warning("This command can only be used with one interface, only the first one will be used")

        # Cannot be taken by DPDK
        nic_id, iface_data = list(iface_to_data.items())[0]
        if iface_data.is_dpdk:
            logging.error("The NIC cannot be taken by DPDK")
            exit(1)

        # Finding ethtool
        ethtool = find_exec('ethtool')
        if not ethtool:
            logging.error("Ethtool not found")
            exit(1)

        # Running ethtool -p {nic_id}
        returncode = 0
        try:
            logging.info("Press Ctrl+C to exit")
            result = run_cmd([str(ethtool), "-p", nic_id], capture_output=False, dry_run=args.dry_run)
            if result is not None:
                returncode = result.returncode
        except KeyboardInterrupt:
            logging.info("Detected Ctrl+C, Stopping...")

        exit(returncode)
