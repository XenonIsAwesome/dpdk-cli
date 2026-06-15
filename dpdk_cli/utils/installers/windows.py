import logging
import shutil
from typing import List

from dpdk_cli.utils import run_cmd
from dpdk_cli.utils.installers import Installer


class WindowsInstaller(Installer):
    @staticmethod
    def install(packages: List[str], no_confirm: bool = False, dry_run: bool = False):
        winget = shutil.which("winget")
        choco = shutil.which("choco") if not winget else None

        if winget:
            logging.info("Using winget to install DPDK packages")
            mapping = {
                "dpdk": "dpdk",
                "dpdk-dev": "dpdk",
                "driverctl": None,
            }
            translated = []
            for p in packages:
                mapped = mapping.get(p)
                if mapped:
                    translated.append(mapped)

            if not translated:
                return

            cmd = [
                "winget",
                "install",
            ]
            if no_confirm:
                cmd += [
                    "--accept-package-agreements",
                    "--accept-source-agreements"
                ]
            cmd += translated
        elif choco:
            logging.info("Using Chocolatey to install DPDK packages")
            mapping = {
                "dpdk": "dpdk",
                "dpdk-dev": "dpdk",
                "driverctl": None,
            }
            translated = set()
            for p in packages:
                mapped = mapping.get(p)
                if mapped:
                    translated.add(mapped)

            if not translated:
                return

            cmd = ["choco", "install"]
            if no_confirm:
                cmd += ["-y"]
            cmd += list(translated)
        else:
            logging.error(
                "No supported package manager found. "
                "Please install DPDK manually: https://core.dpdk.org/download/"
            )
            exit(1)

        logging.info(f"Running: {' '.join(cmd)}")
        run_cmd(cmd, capture_output=False, check=True, dry_run=dry_run)