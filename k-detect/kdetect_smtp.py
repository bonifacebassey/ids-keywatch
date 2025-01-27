#!/usr/bin/env python
import shlex
import subprocess
import psutil
import os

# Initialize variables
time = 1
black_list = []
white_list = []

# Autostart directory
autostart_path = os.path.expanduser('~/.config/autostart/')

# Main scanning loop
while True:
    if time == 1:
        print("\033[93m\nScanning in progress...\033[0m")

    command = shlex.split('lsof -nP -iTCP:587 -iTCP:465 -iTCP:2525')
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    output = out.decode()
    time += 1

    if "ESTABLISHED" in output:
        my_list = list(filter(None, output.split(" ")))
        port_num = my_list[-2]
        port = port_num.split(":")[-1]
        process_name = my_list[8].split("\n")[-1]
        pid = my_list[9]
        p = psutil.Process(int(pid))

        if process_name not in white_list:
            print("\033[91mKEYLOGGER DETECTED!\033[0m")

            if process_name in black_list:
                p.kill()
                print("\033[91mBlacklist application found running.\nProcess automatically terminated.\033[0m")
                time = 1
            else:
                print("\033[93mPausing application...\033[0m")
                p.suspend()
                print("\033[93mInformation on application identified as a potential threat:\033[0m")
                print(f'\033[96mApplication name:\033[0m {process_name}\n'
                      f'\033[96mProcess ID (PID):\033[0m {pid}\n'
                      f'\033[96mTrying to communicate on port:\033[0m {port}\n')

                while True:
                    is_safe = input("\033[96mWould you like to whitelist this application? (Y/N): \033[0m").lower()
                    if is_safe == 'y':
                        print("\033[92mResuming process...\033[0m")
                        p.resume()
                        print("\033[92mAdding to whitelist...\033[0m")
                        white_list.append(process_name)
                        time = 1
                        break
                    elif is_safe == 'n':
                        print("\033[91mTerminating process...\033[0m")
                        p.kill()
                        print("\033[91mAdding to blacklist...\033[0m")
                        black_list.append(process_name)
                        time = 1
                        break

                print(f"\033[92mWhitelist: {white_list}\033[0m")
                print(f"\033[91mBlacklist: {black_list}\033[0m")
