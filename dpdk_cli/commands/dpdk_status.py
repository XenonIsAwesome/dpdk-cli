import logging

from dpdk_cli.utils import parse_dpdk_hugepages_status, parse_dpdk_devbind_status
from dpdk_cli.utils.base_command import BaseCommand


class DpdkStatusCommand(BaseCommand):
    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("status", help="Show status on everything")
        parser.set_defaults(handler=DpdkStatusCommand.handle)

    @staticmethod
    def handle(args):
        logging.info("Network interfaces:")
        logging.info("=" * 130)

        nic_status = parse_dpdk_devbind_status()
        logging.info(
            f"{'NIC':<10}\t{'PCI Address':<10}\t{'Description':<50}\t{'Bound Driver':<15}\t{'Unused Driver':<15}\t{'DPDK?':<10}")
        for nic_id, iface_data in nic_status.items():
            is_dpdk_str = 'Yes' if iface_data.is_dpdk else 'No'
            logging.info(
                f"{nic_id:<10}\t{iface_data.pci_address:<10}\t{iface_data.description:<50}\t{iface_data.bound_driver:<15}\t{iface_data.unused_driver:<15}\t{is_dpdk_str:<10}")
        logging.info("=" * 130)
        logging.info("")

        logging.info("HugePages:")
        logging.info("=" * 35)
        huge_pages_status = parse_dpdk_hugepages_status()
        logging.info("Node\tPages\tSize\tTotal")
        for numa, info in huge_pages_status.numa_page_sizes.items():
            logging.info(f"{numa}\t{info.pages}\t{info.size_str}\t{info.total_str}")
        logging.info("")
        logging.info(f"HugePages mount: {huge_pages_status.hugepages_mount}")
        logging.info("=" * 35)
