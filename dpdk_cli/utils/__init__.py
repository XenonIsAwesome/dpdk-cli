import fnmatch
import logging
import os
import shlex
import shutil
import subprocess
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict

from dpdk_cli.consts import DPDK_SECTION_TO_IS_DPDK, DPDK_PCI_RE, DPDK_IF_RE, DPDK_DRV_RE, DPDK_UNUSED_RE, \
    DPDK_DEVBIND_EXEC_NAME, DPDK_HUGEPAGES_EXEC_NAME, HUGEPAGES_PAGESIZE_RE


def run_cmd(cmd, sudo=False, capture_output=True, check=False, dry_run=False):
    if sudo:
        if not dry_run:
            require_sudo()

        if isinstance(cmd, list):
            cmd = ["sudo"] + cmd
        else:
            cmd = f"sudo {cmd}"

    if dry_run:
        if isinstance(cmd, list):
            cmd = shlex.join(cmd)

        logging.debug(f"+ {cmd}")
        return None

    if isinstance(cmd, str):
        result = subprocess.run(
            cmd, capture_output=capture_output, shell=True, text=True, check=check
        )
    else:
        result = subprocess.run(
            cmd, capture_output=capture_output, text=True, check=check
        )
    return result


def require_sudo():
    if os.geteuid() != 0:
        logging.error("This command must be run with privileges")
        exit(1)


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


def parse_dpdk_devbind_status() -> Dict[str, NetworkInterfaceData]:
    devbind = find_exec(DPDK_DEVBIND_EXEC_NAME)

    output = run_cmd([str(devbind), "--status-dev", "net"], capture_output=True)
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

        nic_id = current.get("ifname", current.get("pci", None))
        if nic_id is None:
            # skip interfaces without Linux name
            current = None
            return

        result[nic_id] = NetworkInterfaceData(
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
                "drv": "",
                "unused": ""
            }

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


@dataclass
class NumaHugePageSizes:
    node: int
    pages: int
    size: int
    size_str: str
    total: int
    total_str: str


@dataclass
class HugePageStatus:
    numa_page_sizes: Dict[int, NumaHugePageSizes]
    hugepages_mount: Optional[Path]


def filesize_to_bytes_amount(pagesize: str):
    size_to_bytes = {
        "G": 1024 ** 3,
        "M": 1024 ** 2,
        "K": 1024 ** 1,
        "b": 1,
    }

    match = HUGEPAGES_PAGESIZE_RE.match(pagesize)
    if match:
        groups = match.groups()
        size_str = groups[0]
        size_name = "b"
        if len(groups) == 2:
            size_name = groups[1]

        if size_name not in size_to_bytes:
            raise RuntimeError(f"Invalid size name '{size_name}' parsed from {DPDK_HUGEPAGES_EXEC_NAME}")

        return int(size_str) * size_to_bytes[size_name]

    raise RuntimeError(f"Invalid size {pagesize} parsed from {DPDK_HUGEPAGES_EXEC_NAME}")


def parse_dpdk_hugepages_status():
    hugepages = find_exec(DPDK_HUGEPAGES_EXEC_NAME)

    result = run_cmd([str(hugepages), "-s"], capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"{hugepages} -s failed (rc={result.returncode}): {result.stderr.strip()}"
        )

    hugepages_mnt = None
    numa_node_to_hugepages_status = {}

    for line in result.stdout.splitlines():
        components = list(filter(lambda x: x != '', line.split(' ')))
        if len(components) < 4:
            continue
        node, pages, size, total = components
        node, pages, size, total = node.strip().lower(), pages.strip().lower(), size.strip(), total.strip()

        if f"{node} {pages} {size.lower()} {total.lower()}" == "node pages size total":
            continue

        if f"{node} {pages} {size.lower()}" == "hugepages mounted on":
            hugepages_mnt = Path(total.strip())
            continue

        numa_node_to_hugepages_status[int(node)] = NumaHugePageSizes(int(node), int(pages),
                                                                     filesize_to_bytes_amount(size),
                                                                     size,
                                                                     filesize_to_bytes_amount(total),
                                                                     total)

    return HugePageStatus(numa_node_to_hugepages_status, hugepages_mnt)


def add_node_param(parser: ArgumentParser):
    parser.add_argument(
        "-n", "--node", type=int, required=False, help="NUMA node number"
    )


def add_page_param(parser: ArgumentParser):
    parser.add_argument(
        "-p", "--page", metavar="SIZE", required=False, help="Hugepage size (e.g., 2M, 1G)"
    )
