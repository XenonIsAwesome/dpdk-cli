import logging

from dpdk_cli.utils.colored_formatter import ColoredFormatter

handler = logging.StreamHandler()
handler.setFormatter(
    ColoredFormatter(
        "[%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )
)

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)
