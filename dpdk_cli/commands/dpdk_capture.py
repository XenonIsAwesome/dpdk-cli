import logging
from pathlib import Path

from dpdk_cli.consts import DPDK_DUMPCAP_EXEC_NAME
from dpdk_cli.utils import find_exec, parse_dpdk_devbind_status, resolve_interfaces, run_cmd
from dpdk_cli.utils.base_command import BaseCommand


class DpdkCaptureCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser(
            "capture", help="Capture packets on an interface"
        )

        parser.add_argument(
            "interfaces",
            nargs="+",
            help="Interface name(s) or glob pattern(s) to capture from (e.g. eno1 eno2, eno*)",
        )

        parser.add_argument(
            "-o",
            "--output",
            type=str,
            default=Path.cwd() / "capture.pcap",
            help="Output file path (default: capture.pcap)",
        )

        stop_cond_group = parser.add_mutually_exclusive_group(required=True)
        stop_cond_group.add_argument(
            "-c",
            "--count",
            type=int,
            default=None,
            help="Number of packets to capture",
        )
        stop_cond_group.add_argument(
            "-a",
            "--autostop",
            type=str,
            default=None,
            help="""duration:NUM - stop after NUM seconds;
filesize:NUM - stop this file after NUM kB;
packets:NUM - stop after NUM packets""",
        )

        parser.set_defaults(handler=DpdkCaptureCommand.handle)

    @staticmethod
    def handle(args):
        dumpcap = find_exec(DPDK_DUMPCAP_EXEC_NAME)
        iface_to_data = resolve_interfaces(parse_dpdk_devbind_status(), args.interfaces)
        if len(iface_to_data) == 0:
            logging.error("No matching interfaces found")
            exit(1)

        cmd = [str(dumpcap)]

        # resolved interfaces
        for iface, data in iface_to_data.items():
            if not data.is_dpdk:
                logging.error(f"Port {iface} is not a DPDK interface, please bind it.")
                exit(1)
            cmd.extend(["-i", data.pci_address])

        # packet count stop condition
        if args.count is not None:
            cmd.extend(["-c", str(args.count)])

        # autostop stop condition
        if args.autostop is not None:
            cmd.extend(["-a", str(args.autostop)])

        # Writing to output file
        cmd.extend(["-w", str(args.output)])

        run_cmd(cmd, capture_output=False, dry_run=args.dry_run)
