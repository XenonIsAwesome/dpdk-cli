import logging
from typing import List

from dpdk_cli.utils import run_cmd
from dpdk_cli.utils.installers import Installer


class MacosInstaller(Installer):
    @staticmethod
    def install(packages: List[str], no_confirm: bool = False, dry_run: bool = False):
        logging.info("Using Homebrew to install DPDK packages")

        pm_cmd = ["brew", "install"]
        mapping = {
            "dpdk": "dpdk",
            "dpdk-dev": "dpdk",
        }

        translated = set()
        for p in packages:
            mapped = mapping.get(p)
            if mapped:
                translated.add(mapped)

        if not translated:
            logging.info("All requested packages already covered")
            return

        cmd = pm_cmd + list(translated)
        logging.info(f"Running: {' '.join(cmd)}")
        run_cmd(cmd, capture_output=False, check=True, dry_run=dry_run)
