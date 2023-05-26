import datetime
import os
import platform
import re
from colorama import Fore, Back, Style

system_type = platform.architecture()[0]

if os.name == 'nt':
    os_type = 'win32'
else:
    os_type = 'darwin'

if os.path.exists(".env"):
    state = "dev"
    with open(".env", "r") as file:
        contents = file.read()
        date_time_match = re.search(r"DATE_TIME=(.+)", contents)
        current_date_time = date_time_match.group(1)
        version_match = re.search(r"VERSION=(\d+)\.(\d+)\.(\d+)-(.+)", contents)
        current_major_version = int(version_match.group(1))
        current_minor_version = int(version_match.group(2))
        current_patch_version = int(version_match.group(3))
        current_state = version_match.group(4)
        current_version = print(
            f"{Fore.LIGHTBLUE_EX}Current version:{Style.RESET_ALL} {current_major_version}.{current_minor_version}.{current_patch_version}-{current_state}")

    if current_state == "major":
        new_major_version = current_major_version + 1
        new_minor_version = 0
        new_patch_version = 0
        new_state = state
    elif current_state == "minor":
        new_major_version = current_major_version
        new_minor_version = current_minor_version + 1
        new_patch_version = 0
        new_state = state
    else:
        new_major_version = current_major_version
        new_minor_version = current_minor_version
        new_patch_version = current_patch_version + 1
        new_state = state

    now = datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")

    with open(".env", "w") as file:
        file.write(f'DATE_TIME="{now}"\n')
        file.write(f"SYSTEM={os_type}\n")
        file.write(f"SYSTEM_TYPE={system_type}\n")
        file.write(f"VERSION={new_major_version}.{new_minor_version}.{new_patch_version}-{new_state}\n")

    print(
        f"{Fore.LIGHTGREEN_EX}New version:{Style.RESET_ALL} {new_major_version}.{new_minor_version}.{new_patch_version}-{new_state}")
else:
    with open(".env", "a") as file:
        version = "0.0.1-dev"
        now = datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")
        file.write(f'DATE_TIME="{now}"\n')
        file.write(f"SYSTEM={os_type}\n")
        file.write(f"SYSTEM_TYPE={system_type}\n")
        file.write(f"VERSION={version}\n")
    print(f"Initial version: {version}")

with open(".env", "r") as file:
    contents = file.read()
    version_match = re.search(r"VERSION=(\d+)\.(\d+)\.(\d+)-(.+)", contents)
    current_major_version = int(version_match.group(1))
    current_minor_version = int(version_match.group(2))
    current_patch_version = int(version_match.group(3))
    current_state = version_match.group(4)
    system_match = re.search(r"SYSTEM=(\S+)", contents)
    current_os_type = system_match.group(1) if system_match is not None else "unknown"
    system_type_match = re.search(r"SYSTEM_TYPE=(\S+)", contents)
    current_system_type = system_type_match.group(1) if system_type_match is not None else "unknown"

print(f"\nSystem: {current_os_type}\nArchitecture: {current_system_type}")
