# DPDK CLI

## Notable commands

```bash
dpdk status  # Show status on everything (port, hugepages, etc...)

# Uses dpdk-hugepages
dpdk hugepages                                                             # Get status on huge pages
               clear [-n/--node <node>]                                    # Clear existing huge page reservation
               mount                                                       # Mount the huge page filesystem
               unmount                                                     # Unmount the huge page filesystem
               reserve [-p/--page <page>] [-n/--node <node>] <total-size>  # Reserve huge pages
               setup [-p/--page <page>] [-n/--node <node>] <total-size>    # Clears, unmounts, reserves and mounts a 
                                                                           # huge page based on the given size

# Uses dpdk-devbind.py and driverctl
dpdk bind [--permanent] [-d/--driver <driver>] <interfaces>  # Binds <interfaces> to driver
                                               # If driver is not supplied:
                                               #   If the NIC is not taken by DPDK:
                                               #   It will choose the correct DPDK
                                               #   driver based on the available ones.
                                               #   Otherwise, It will revert the 
                                               #   NIC to its original driver.

dpdk top  # Opens dpdk-top (https://github.com/njenia/dpdk-top)

# Uses dpdk-dumpcap
dpdk capture [-c <count>/-a <autostop cond>] [-o <output filepath>] <interfaces>  # Captures packets

dpdk install  # Installs all required dependencies for the package to work (dpdk, dpdk-dev, driverctl)
```

## Development status

- [x] `dpdk status`
- [x] `dpdk hugepages`
- [x] `dpdk hugepages clear` - not tested
- [x] `dpdk hugepages mount` - not tested
- [x] `dpdk hugepages unmount` - not tested
- [x] `dpdk hugepages reserve` - not tested
- [x] `dpdk hugepages setup` - not tested
- [x] `dpdk bind`
- [x] `dpdk top`
- [x] `dpdk capture`

- ### `dpdk install`

| Platform | Distribution                               | Installer | Working?   |
|----------|--------------------------------------------|-----------|------------|
| Linux    | Linux mint                                 | apt       | Yes        |
| Linux    | Ubuntu / Debian                            | apt       | Not tested |
| Linux    | Arch / Manjaro                             | pacman    | Not tested |
| Linux    | Fedora / RHEL / CentOS / Rocky / Almalinux | dnf       | Not tested |
| Linux    | OpenSUSE / SUSE                            | zypper    | Not tested |
| Windows  | -                                          | winget    | Not tested |
| Windows  | -                                          | choco     | Not tested |
| MacOS    | -                                          | brew      | Not tested |
