import fnmatch
import logging
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict

from dpdk_cli.consts import DPDK_SECTION_TO_IS_DPDK, DPDK_PCI_RE, DPDK_IF_RE, DPDK_DRV_RE, DPDK_UNUSED_RE, \
    DPDK_DEVBIND_EXEC_NAME


def run_cmd(cmd, sudo=False, capture_output=True, check=False):
    if sudo:
        require_sudo()
        if isinstance(cmd, list):
            cmd = ["sudo"] + cmd
        else:
            cmd = f"sudo {cmd}"
    if isinstance(cmd, str):
        result = subprocess.run(
            cmd, capture_output=capture_output, shell=True, text=True, check=check
        )
    else:
        result = subprocess.run(
            cmd, capture_output=capture_output, text=True, check=check
        )
    return result


def check_sudo():
    result = run_cmd(["sudo", "-n", "true"], capture_output=False)
    return result.returncode == 0


def require_sudo():
    if not check_sudo():
        logging.error("This command requires sudo privileges")
        raise exit(1)


def parse_size_to_kb(size_str):
    size_str = size_str.strip().lower()
    if size_str.endswith("g"):
        return int(float(size_str[:-1]) * 1024 * 1024)
    elif size_str.endswith("m"):
        return int(float(size_str[:-1]) * 1024)
    elif size_str.endswith("k"):
        return int(float(size_str[:-1]))
    else:
        return int(size_str)


def format_size_kb(kb):
    if kb >= 1024 * 1024:
        return f"{kb / (1024 * 1024):.0f}G"
    elif kb >= 1024:
        return f"{kb / 1024:.0f}M"
    else:
        return f"{kb}K"


def find_exec(exec_name: str) -> Optional[Path]:
    exec_path = shutil.which(exec_name)
    if exec_path:
        return Path(exec_path)

    raise FileNotFoundError(
        f"Couldn't locate {exec_name} in PATH, please add its location to PATH or install the dependencies with `dpdk install`")


@dataclass
class NetworkInterfaceData:
    pci_address: str  # PCI BDF (Bus:Device.Function)
    description: str  # NIC description
    bound_driver: Optional[str]  # Currently bound driver
    unused_driver: Optional[str]  # Driver available but not currently used
    is_dpdk: bool


def parse_dpdk_devbind() -> Dict[str, NetworkInterfaceData]:
    devbind = find_exec(DPDK_DEVBIND_EXEC_NAME)

    output = subprocess.run([str(devbind), "-s"], capture_output=True, text=True)
    if output.returncode != 0:
        raise RuntimeError(
            f"{devbind} -s failed (rc={output.returncode}): {output.stderr.strip()}"
        )

    result: Dict[str, NetworkInterfaceData] = {}
    current_section: Optional[bool] = None
    current = None  # holds partially parsed entry

    def flush():
        nonlocal current
        if not current:
            return

        if current.get("ifname") is None:
            # skip interfaces without Linux name
            current = None
            return

        result[current["ifname"]] = NetworkInterfaceData(
            pci_address=current["pci"],
            description=current["desc"],
            bound_driver=current.get("drv", ""),
            unused_driver=current.get("unused", ""),
            is_dpdk=current_section if current_section is not None else False,
        )
        current = None

    for line in output.stdout.splitlines():
        line = line.strip()

        if not line:
            continue

        # detect section header
        if line in DPDK_SECTION_TO_IS_DPDK:
            flush()
            current_section = DPDK_SECTION_TO_IS_DPDK[line]
            continue

        # New device line: PCI + description
        m = DPDK_PCI_RE.match(line)
        if m:
            flush()
            current = {
                "pci": m.group(1),
                "desc": m.group(2),
                "ifname": None,
                "drv": "",
                "unused": ""
            }
            continue

        if current is None:
            continue

        # parse fields
        m = DPDK_IF_RE.search(line)
        if m:
            current["ifname"] = m.group(1)

        m = DPDK_DRV_RE.search(line)
        if m:
            current["drv"] = m.group(1)

        m = DPDK_UNUSED_RE.search(line)
        if m:
            current["unused"] = m.group(1)

    flush()
    return result


def resolve_interfaces(iface_to_data: Dict[str, NetworkInterfaceData], patterns) -> Dict[str, NetworkInterfaceData]:
    """
    Resolve interface name(s) and/or glob patterns to PCI addresses
    by parsing the output of dpdk-devbind.py -s.

    Accepts a list of strings, each either an exact interface name
    (e.g. "eno1") or a glob pattern (e.g. "eno*").  Returns a
    deduplicated list of PCI BDF addresses.

    Raises FileNotFoundError if dpdk-devbind.py cannot be located,
    or RuntimeError if it exits with a non-zero status.
    """
    # Flatten space-separated tokens inside any pattern, then match
    tokens = []
    for p in patterns:
        tokens.extend(p.split())

    matched = {}
    for token in tokens:
        if token in iface_to_data:
            matched[token] = iface_to_data[token]
        else:
            for iface, data in iface_to_data.items():
                if fnmatch.fnmatch(iface, token):
                    matched[iface] = data

    return matched
