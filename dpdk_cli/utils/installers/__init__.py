import platform
from abc import ABC, abstractmethod
from typing import List, Type


class Installer(ABC):
    @staticmethod
    @abstractmethod
    def install(packages: List[str], no_confirm: bool = False):
        raise NotImplementedError()


def get_installer() -> Type[Installer]:
    system = platform.system().lower()

    if system == "linux":
        from dpdk_cli.utils.installers.linux import LinuxInstaller

        return LinuxInstaller
    elif system == "darwin":
        from dpdk_cli.utils.installers.macos import MacosInstaller

        return MacosInstaller
    elif system == "windows":
        from dpdk_cli.utils.installers.windows import WindowsInstaller

        return WindowsInstaller
    else:
        raise RuntimeError(
            f"Unsupported platform: {system}. "
            f"Please install DPDK manually: https://core.dpdk.org/download/"
        )
