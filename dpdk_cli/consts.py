import re

# dpdk-top
DPDK_TOP_URL = "https://github.com/njenia/dpdk-top"

# Sections in dpdk-devbind.py -s
DPDK_SECTION_TO_IS_DPDK = {
    "Network devices using DPDK-compatible driver": True,
    "Crypto devices using DPDK-compatible driver": True,
    "Eventdev devices using DPDK-compatible driver": True,
    "Baseband devices using DPDK-compatible driver": True,

    "Network devices using kernel driver": False,
    "Crypto devices using kernel driver": False,
    "Eventdev devices using kernel driver": False,
    "Baseband devices using kernel driver": False,
}

# Regex Patterns
DPDK_PCI_RE = re.compile(r"^([0-9a-fA-F:.]+)\s+'(.+)'")
DPDK_IF_RE = re.compile(r"if=(\S+)")
DPDK_DRV_RE = re.compile(r"drv=(\S+)")
DPDK_UNUSED_RE = re.compile(r"unused=([^\s]+)")
HUGEPAGES_PAGESIZE_RE = re.compile("^(\d+)([GMK])?b?$")

# Execs
DPDK_DEVBIND_EXEC_NAME = "dpdk-devbind.py"
DPDK_DUMPCAP_EXEC_NAME = "dpdk-dumpcap"
DPDK_HUGEPAGES_EXEC_NAME = "dpdk-hugepages.py"
DRIVERCTL_EXEC_NAME = "driverctl"

# Installtion packages
REQUIRED_PACKAGES = ["dpdk", "dpdk-dev", "driverctl"]
