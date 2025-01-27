#!/usr/bin/env python
import psutil
import time


def detect_keylogger():
    suspicious_keywords = ["keylogger", "hook", "intercept", "spy", "record", "pynput", "keyboard", "listener", "input"]

    while True:
        print("\033[93m\nScanning for potential keylogger processes...\033[0m")
        detected = False
        for process in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                process_name = process.info['name'].lower()
                process_cmdline = " ".join(process.info['cmdline']).lower()

                # Log every process for visibility
                print(f'\033[94mChecking Process: {process_name}, PID: {process.info["pid"]}\033[0m')

                # Check if suspicious keywords are in the process name or command line
                for keyword in suspicious_keywords:
                    if keyword in process_name or keyword in process_cmdline:
                        print("\033[91mPotential keylogger detected!\033[0m")
                        print(f'\033[96mProcess Name:\033[0m {process.info["name"]}\n'
                              f'\033[96mProcess ID (PID):\033[0m {process.info["pid"]}\n'
                              f'\033[96mCommand Line:\033[0m {process_cmdline}\n')
                        detected = True
                        break
                if detected:
                    return
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        time.sleep(5)  # Wait for 5 seconds before scanning again


if __name__ == "__main__":
    detect_keylogger()
