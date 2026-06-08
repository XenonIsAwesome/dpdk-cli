import logging
import subprocess


def run_cmd(cmd, sudo=False, capture_output=True, check=False):
    if sudo:
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
        raise SystemExit(1)


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
