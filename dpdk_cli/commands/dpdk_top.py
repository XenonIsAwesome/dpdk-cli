import logging
import shutil
import sys

from dpdk_cli.consts import DPDK_TOP_URL
from dpdk_cli.utils import run_cmd
from dpdk_cli.utils.base_command import BaseCommand


class DpdkTopCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser(
            "top", help=f"Installs all required dependencies for the package to work"
        )
        parser.set_defaults(handler=DpdkTopCommand.handle)

    @staticmethod
    def handle(args):
        candidates = ["dpdk-top", "dpdk_top"]
        dpdk_top_bin = None
        for c in candidates:
            path = shutil.which(str(c))
            if path:
                dpdk_top_bin = path
                break

        if not dpdk_top_bin:
            logging.error(f"dpdk-top not found. Install from {DPDK_TOP_URL}")
            raise SystemExit(1)

        result = run_cmd([dpdk_top_bin], capture_output=False)
        sys.exit(result.returncode if result else 1)
