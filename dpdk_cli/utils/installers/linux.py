import logging
from pathlib import Path
from typing import List, Dict

from dpdk_cli.utils import run_cmd
from dpdk_cli.utils.installers import Installer


class LinuxInstaller(Installer):
    _detected = None

    @classmethod
    def detect(cls) -> str:
        if cls._detected:
            return cls._detected

        data = Path("/etc/os-release").read_text().strip()

        installer_to_keywords = {
            "apt": ["ubuntu", "debian"],
            "dnf": ["fedora", "rhel", "centos", "almalinux", "rocky"],
            "pacman": ["arch", "manjaro"],
            "zypper": ["suse"]
        }

        for installer, keywords in installer_to_keywords.items():
            for keyword in keywords:
                if keyword.lower() in data.lower():
                    cls._detected = installer
                    return cls._detected

        cls._detected = "unknown"
        return cls._detected

    # noinspection PyTypeChecker
    @staticmethod
    def install(packages: List[str], no_confirm: bool = False, dry_run: bool = False):
        pm = LinuxInstaller.detect()
        logging.info(f"Detected package manager: {pm}")

        mapping = {
            "apt": {
                "cmd": ["apt", "install"],
                "no_confirm": "-y",
                "pkg_map": {
                    "dpdk": "dpdk",
                    "dpdk-dev": "dpdk-dev",
                    "driverctl": "driverctl",
                },
            },
            "dnf": {
                "cmd": ["dnf", "install"],
                "no_confirm": "-y",
                "pkg_map": {
                    "dpdk": "dpdk",
                    "dpdk-dev": "dpdk-devel",
                    "driverctl": "driverctl",
                },
            },
            "pacman": {
                "cmd": ["pacman", "-S"],
                "no_confirm": "--noconfirm",
                "pkg_map": {
                    "dpdk": "dpdk",
                    "dpdk-dev": "dpdk",
                    "driverctl": "driverctl",
                },
            },
            "zypper": {
                "cmd": ["zypper", "install"],
                "no_confirm": "-y",
                "pkg_map": {
                    "dpdk": "dpdk",
                    "dpdk-dev": "dpdk-devel",
                    "driverctl": "driverctl",
                },
            },
        }

        if pm not in mapping:
            logging.error(
                f"Unsupported package manager '{pm}'. "
                f"Please install DPDK manually: https://core.dpdk.org/download/"
            )
            exit(1)

        m = mapping[pm]

        # noinspection PyTypeChecker
        pkg_map: Dict[str, str] = m["pkg_map"]

        # noinspection PyTypeChecker
        cmd_list: List[str] = m["cmd"]

        no_confirm_arg: str = m["no_confirm"]

        translated = set()
        for p in packages:
            mapped = pkg_map.get(p)
            if mapped:
                translated.add(mapped)

        cmd = cmd_list
        if no_confirm:
            cmd += [no_confirm_arg]
        cmd += translated

        logging.info(f"Running: {' '.join(cmd)}")

        run_cmd(cmd, capture_output=False, check=True, dry_run=dry_run)
