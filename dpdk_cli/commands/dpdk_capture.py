from argparse import ArgumentParser
from pathlib import Path

from dpdk_cli.utils.base_command import BaseCommand


class DpdkCaptureCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("capture", help="Capture packets on an interface")
        parser.add_argument("interfaces", help="Interface to capture packets from")

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
            help="Auto-stop condition",
        )

        parser.set_defaults(handler=DpdkCaptureCommand.handle)

    @staticmethod
    def handle(args):
        raise NotImplementedError()