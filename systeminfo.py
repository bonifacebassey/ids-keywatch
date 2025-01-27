import os
import socket
import platform
from cfg import cfg_output_folder, cfg_add2files
from datetime import datetime
from requests import Session, exceptions as req_exceptions


class SystemInformation:

    @staticmethod
    def _get_public_ip():
        """Fetch the public IP address."""
        try:
            with Session() as session:
                return session.get("https://api.ipify.org", timeout=5).text
        except (req_exceptions.RequestException, req_exceptions.Timeout):
            return "Couldn't get Public IP Address (network issue or max query limit)"

    @staticmethod
    def _get_local_ip():
        try:
            # Connect to an external address to get the local network IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))  # Connect to Google DNS
                return s.getsockname()[0]
        except Exception as e:
            print(f"Error: {e}")
            return None

    def _system_info(self):
        """Collect system information and return it as a formatted string."""
        info = (
            f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - System Information]\n"
            f"******************************************\n"
            f"  Public IP Address: {self._get_public_ip()}\n"
            f"  Local IP Address: {self._get_local_ip()}\n"
            f"  Architecture: {platform.architecture()[0]}\n"
            f"  System: {platform.system()} {platform.release()} {platform.version()}\n"
            f"  Machine: {platform.machine()}\n"
            f"  Hostname (Node): {platform.node()}\n"
            f"  Python Version: {platform.python_version()}\n"
            f"******************************************\n\n"
        )
        return info

    def log_systeminfo(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(cfg_output_folder(), f"sysinfo_{timestamp}.log")
        cfg_add2files(output_file)

        sysinfo = self._system_info()
        try:
            with open(output_file, "w") as f:
                f.write(sysinfo + "\n")  # Ensure a new line after system info
        except OSError as e:
            print(f"Failed to write system information to file: {e}")