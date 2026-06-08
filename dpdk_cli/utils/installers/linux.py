import logging
import subprocess
from pathlib import Path
from typing import List, Dict

from dpdk_cli.utils.installers import Installer


class LinuxInstaller(Installer):
    _detected = None

    @classmethod
    def detect(cls) -> str:
        if cls._detected:
            return cls._detected

        data = Path("/etc/os-release").read_text().strip().lower()

        if "ubuntu" in data or "debian" in data:
            cls._detected = "apt"
        elif "fedora" in data:
            cls._detected = "dnf"
        elif (
                "rhel" in data or "centos" in data or "almalinux" in data or "rocky" in data
        ):
            cls._detected = "dnf"
        elif "arch" in data or "Manjaro" in data:
            cls._detected = "pacman"
        elif "opensuse" in data or "suse" in data:
            cls._detected = "zypper"
        else:
            cls._detected = "unknown"

        return cls._detected

    # noinspection PyTypeChecker
    @staticmethod
    def install(packages: List[str], no_confirm: bool = False):
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
            raise RuntimeError(
                f"Unsupported package manager '{pm}'. "
                f"Please install DPDK manually: https://core.dpdk.org/download/"
            )

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
        subprocess.run(cmd, check=True)
