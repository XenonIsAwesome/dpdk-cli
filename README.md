# DPDK CLI
## Notable commands

```bash
dpdk status  # Show status on everything (port, hugepages, etc...)

# Uses dpdk-hugepages
dpdk hugepages                 # Get status on huge pages
               clear <driver>  # Clear existing huge page reservation
               mount           # Mount the huge page filesystem
               unmount         # Unmount the huge page filesystem
               node <node>     # Set NUMA node to reserve pages on
               page <size>     # Select hugepage size to use
               reserve <size>  # Reserve huge pages
               setup <size>    # Clears, unmounts, reserves and mounts a 
                               # hugepage based on the given size

# Uses dpdk-devbind.py and driverctl
dpdk bind <interfaces> [driver] [--permanent]  # Binds <interfaces> to driver
                                               # If driver is not supplied:
                                               #   If the NIC is not taken by DPDK:
                                               #   It will choose the correct DPDK
                                               #   driver based on the available ones.
                                               #   Otherwise, It will revert the 
                                               #   NIC to its original driver.

dpdk top  # Opens dpdk-top (https://github.com/njenia/dpdk-top)

# Uses dpdk-dumpcap
dpdk capture <interfaces> [-c <count>/-a <autostop cond>] [-o <output filepath>]  # Captures packets

dpdk install  # Installs all required dependencies for the package to work (dpdk, dpdk-top)
```

## Development status

- [ ] `dpdk status`
- [ ] `dpdk hugepages`
- [ ] `dpdk hugepages clear`
- [ ] `dpdk hugepages mount`
- [ ] `dpdk hugepages unmount`
- [ ] `dpdk hugepages node`
- [ ] `dpdk hugepages page`
- [ ] `dpdk hugepages reserve`
- [ ] `dpdk hugepages setup`
- [ ] `dpdk bind`
- [x] `dpdk top`
- [ ] `dpdk capture`
- [ ] `dpdk install`
