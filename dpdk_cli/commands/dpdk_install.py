import logging

from argparse import ArgumentParser

from dpdk_cli.consts import REQUIRED_PACKAGES
from dpdk_cli.utils.base_command import BaseCommand
from dpdk_cli.utils.installers import get_installer


class DpdkInstallCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser: ArgumentParser = subparsers.add_parser(
            "install", help="Installs all required dependencies for the package to work"
        )
        parser.add_argument(
            "-y",
            "--yes",
            dest="yes",
            action="store_true",
            help="Don't ask for confirmation",
        )
        parser.set_defaults(handler=DpdkInstallCommand.handle)

    @staticmethod
    def handle(args):
        installer_cls = get_installer()
        logging.info(f"Platform: {__import__('platform').platform()}")
        logging.info(f"Packages to install: {', '.join(REQUIRED_PACKAGES)}")

        if not args.yes:
            try:
                input(
                    f"This will install the following packages using your system package manager: "
                    f"{', '.join(REQUIRED_PACKAGES)}. Press Enter to continue or Ctrl-C to abort..."
                )
            except KeyboardInterrupt:
                logging.info("Aborted by user")
                return

        installer_cls.install(REQUIRED_PACKAGES)
        logging.info("Installation complete")
