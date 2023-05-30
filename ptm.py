############################
# ProtoCSS Package Manager #
############################
import json

import requests
import os
import shutil
import argparse
from colorama import Back, Fore, Style
import firebase_admin
from firebase_admin import credentials, storage

with open(".env") as file:
    for line in file:
        if line.startswith("CERT_PATH"):
            __cert_path__ = line.split("=")[1].replace("\n", "").strip('"').strip("'")
        elif line.startswith("STORAGE_BUCKET"):
            __storage_bucket__ = line.split("=")[1].strip('"').replace("\n", "").strip('"').strip("'")

cred = credentials.Certificate(__cert_path__)
options = {
    'storageBucket': __storage_bucket__
}
firebase_admin.initialize_app(cred, options)


class ProtoCSSPackageManager:
    def __init__(self, server_url):
        self.server_url = server_url
        self.package_dir = "ptm_package"

    def initialize(self):
        if not os.path.exists(self.package_dir):
            os.makedirs(self.package_dir)

    def install_package(self, *packages, **kwargs):
        try:
            for package in packages:
                package_name = package
                package_version = kwargs.get("version", "latest")
                package_file_name = f"{package_name}-{package_version}.ptm"
                package_file_path = os.path.join(self.package_dir, package_file_name)
                if not os.path.exists(package_file_path):
                    print(f"Downloading {package_name}...")
                    r = requests.get(f"{self.server_url}/package/{package_name}/{package_version}")
                    with open(package_file_path, "wb") as file:
                        file.write(r.content)
                    print(f"Installing {package_name}...")
                    shutil.unpack_archive(package_file_path, package_name)
                    os.remove(package_file_path)
                    print(f"{package_name} installed successfully.")
                else:
                    print(f"{package_name} is already installed.")
        except Exception as e:
            print(f"{Fore.RED}Error: Package '{package_name}' not found.{Style.RESET_ALL}")

    def upload_package(self):
        try:
            if not os.path.exists(os.path.join(self.package_dir, "package.json")):
                print(
                    f"\n      {Back.LIGHTYELLOW_EX}{Fore.LIGHTWHITE_EX}      package.json not found      {Style.RESET_ALL}\n")

                package_name = input("Package name: ")
                package_description = input("Package description: ")
                package_author = input("Package author: ")
                package_version = input("Package version: ")
                package_file_name = f"{package_name}-{package_version}.ptm"
                package_file_path = os.path.join(self.package_dir, package_file_name)

                with open(os.path.join(os.path.abspath(self.package_dir), "package.json"), "w") as file:
                    file.write(f"""{{
        "name": "{package_name}",
        "description": "{package_description}",
        "author": "{package_author}",
        "version": "{package_version}"
    }}""")
                with open(os.path.join(self.package_dir, "package.json")) as file:
                    package_info = file.read()

                package_name = package_info.split('"name": "')[1].split('"')[0]
                package_version = package_info.split('"version": "')[1].split('"')[0].replace(".", "_")
                package_author = package_info.split('"author": "')[1].split('"')[0]
                package_file_name = f"{package_name}-{package_version}.ptm"
                package_file_path = os.path.join(self.package_dir, package_file_name)
                print("Uploading package...")
                print(f"\n{Fore.LIGHTWHITE_EX}Name:{Style.RESET_ALL} {package_name}")
                print(f"{Fore.LIGHTWHITE_EX}Version:{Style.RESET_ALL} {package_version.replace('_', '.')}")
                print(f"{Fore.LIGHTWHITE_EX}Author:{Style.RESET_ALL} {package_author}\n")
                # print(f"{Fore.LIGHTWHITE_EX}package_file_name:{Style.RESET_ALL} {package_file_name}\n")

                if os.path.exists(package_file_path):
                    os.remove(package_file_path)
                    print(f"{Fore.LIGHTYELLOW_EX}Last version removed.{Style.RESET_ALL}\n")

                print(f"{Fore.LIGHTYELLOW_EX}Creating new version of '{package_name}'...{Style.RESET_ALL}")
                output_path = os.path.abspath("ptm_package")
                # print(f"{Fore.LIGHTYELLOW_EX}output_path: {output_path}{Style.RESET_ALL}")
                shutil.make_archive(f"{package_name}-{package_version}", "zip", output_path)
                print(f"{Fore.YELLOW}New version created.{Style.RESET_ALL}")
                # print(os.path.join(self.package_dir, f"{package_name}-{package_version}.zip"))
                shutil.move(os.path.abspath(f"./{package_name}-{package_version}.zip"), package_file_path)
                print(f"{Fore.YELLOW}New version moved.{Style.RESET_ALL}")
                blob = storage.bucket().blob(f"packages/{package_file_name}")
                print(f"{Fore.LIGHTYELLOW_EX}Uploading new version...{Style.RESET_ALL}")
                blob.upload_from_filename(package_file_path)
                print(
                    f"\n      {Back.LIGHTGREEN_EX}{Fore.LIGHTWHITE_EX}      Package '{package_name}' uploaded successfully!      {Style.RESET_ALL}\n")

            else:
                print(
                    f"\n      {Back.LIGHTBLUE_EX}{Fore.LIGHTWHITE_EX}      package.json found      {Style.RESET_ALL}\n")

                with open(os.path.join(self.package_dir, "package.json")) as file:
                    package_info = file.read()

                package_name = package_info.split('"name": "')[1].split('"')[0]
                package_version = package_info.split('"version": "')[1].split('"')[0].replace(".", "_")
                package_author = package_info.split('"author": "')[1].split('"')[0]
                package_file_name = f"{package_name}-{package_version}.ptm"
                package_file_path = os.path.join(self.package_dir, package_file_name)
                print("Uploading package...")
                print(f"\n{Fore.LIGHTWHITE_EX}Name:{Style.RESET_ALL} {package_name}")
                print(f"{Fore.LIGHTWHITE_EX}Version:{Style.RESET_ALL} {package_version.replace('_', '.')}")
                print(f"{Fore.LIGHTWHITE_EX}Author:{Style.RESET_ALL} {package_author}\n")
                # print(f"{Fore.LIGHTWHITE_EX}package_file_name:{Style.RESET_ALL} {package_file_name}\n")

                if os.path.exists(package_file_path):
                    os.remove(package_file_path)
                    print(f"{Fore.LIGHTYELLOW_EX}Last version removed.{Style.RESET_ALL}\n")

                print(f"{Fore.LIGHTYELLOW_EX}Creating new version of '{package_name}'...{Style.RESET_ALL}")
                output_path = os.path.abspath("ptm_package")
                # print(f"{Fore.LIGHTYELLOW_EX}output_path: {output_path}{Style.RESET_ALL}")
                shutil.make_archive(f"{package_name}-{package_version}", "zip", output_path)
                print(f"{Fore.YELLOW}New version created.{Style.RESET_ALL}")
                # print(os.path.join(self.package_dir, f"{package_name}-{package_version}.zip"))
                shutil.move(os.path.abspath(f"./{package_name}-{package_version}.zip"), package_file_path)
                print(f"{Fore.YELLOW}New version moved.{Style.RESET_ALL}")
                # blob = storage.bucket().blob(f"packages/{package_name}/{package_version}/{package_file_name}")
                # blob = storage.bucket().blob(f"packages/{package_name}/{package_version}/package.json")
                print(f"{Fore.LIGHTYELLOW_EX}Uploading new version...{Style.RESET_ALL}")
                for upload in [package_file_path, os.path.join(self.package_dir, "package.json")]:
                    storage.bucket().blob(
                        f"packages/{package_name}/{package_version}/{upload.split('/')[-1]}").upload_from_filename(
                        upload)
                print(
                    f"\n      {Back.LIGHTGREEN_EX}{Fore.LIGHTWHITE_EX}      Package '{package_name}' uploaded successfully!      {Style.RESET_ALL}\n")

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def upgrade_package(self, *packages, **kwargs):
        self.install_package(*packages, **kwargs)

    def get_package_info(self, package_name):
        return self._fetch_package_info(package_name)

    def _fetch_package_info(self, package_name):
        print(f"Fetching package '{package_name}'...")
        try:
            # Authenticate the user with appropriate credentials
            # cred = credentials.Certificate(__cert_path__)
            # firebase_admin.initialize_app(cred, {'storageBucket': __storage_bucket__})

            # Access the package.json file from Firebase Storage
            bucket = storage.bucket()
            blob = bucket.blob(f"packages/{package_name}/1_0_0_/package.json")
            package_info = blob.download_as_text()
            package_info = json.loads(package_info)

            return package_info
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _download_file(self, url, file_path):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(prog="ptm", description="ProtoCSS Package Manager")
    parser.add_argument("packages", nargs="*", help="Package names")
    parser.add_argument("-i", "--install", action="store_true", help="Install packages")
    parser.add_argument("-u", "--upgrade", action="store_true", help="Upgrade packages")
    parser.add_argument("-gi", "--get-info", action="store_true", help="Get package information")
    parser.add_argument("-up", "--upload", action="store_true", help="Upload a package")

    args = parser.parse_args()

    server_url = ""
    ptm = ProtoCSSPackageManager(server_url)
    ptm.initialize()

    if args.install:
        ptm.install_package(*args.packages)
    elif args.upgrade:
        ptm.upgrade_package(*args.packages)
    elif args.get_info:
        for package_name in args.packages:
            package_info = ptm.get_package_info(package_name)
            if package_info is not None:
                print(f"{Fore.LIGHTWHITE_EX}Package name:{Style.RESET_ALL} {package_name}")
                print(f"{Fore.LIGHTWHITE_EX}Version:{Style.RESET_ALL} {package_info['version'].replace('_', '.')}")
                print(f"{Fore.LIGHTWHITE_EX}Author:{Style.RESET_ALL} {package_info['author']}")
                print(f"{Fore.LIGHTWHITE_EX}Description:{Style.RESET_ALL} {package_info['description']}")
                print()
            else:
                print(f"Package '{package_name}' not found.")
    elif args.upload:
        for package_name in args.packages:
            if package_name in os.listdir(ptm.package_dir):
                ptm.upload_package()
            else:
                print(f"Package '{package_name}' not found.")


if __name__ == "__main__":
    main()

# TODO:
#  - Add support for installing packages
#  - Add support for upgrading packages
#  - Add support for getting package information - CHECKED
#  - Add support for uploading packages: - CHECKED
#       - Upload with existing package.json - CHECKED
#       - Upload without existing package.json - CHECKED
#  - Add login mechanism:
#       - Ability to get the user's packages within the website.
#       - Ability to upload packages to the user's account (the only way to upload packages).
#       - Ability to install packages from the user's account, and track history of installed packages.
#  - Add support for private packages.
