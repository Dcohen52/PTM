############################
# ProtoCSS Package Manager #
############################

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
            __storage_bucket__ = line.split("=")[1].strip('"')

cred = credentials.Certificate(__cert_path__)
options = {
    'storageBucket': f'{__storage_bucket__}'
}
firebase_admin.initialize_app(cred, options)


class ProtoCSSPackageManager:
    def __init__(self, server_url):
        self.server_url = server_url
        self.package_dir = "ptm_packages"

    def initialize(self):
        if not os.path.exists(self.package_dir):
            os.makedirs(self.package_dir)

    def install_package(self, *packages, **kwargs):
        for package_name in packages:
            package_info = self._fetch_package_info(package_name)
            if package_info is not None:
                package_files = package_info.get("files", [])
                for file_info in package_files:
                    file_url = file_info.get("url")
                    file_path = os.path.join(self.package_dir, file_info.get("name"))
                    self._download_file(file_url, file_path)
                print(f"{Fore.GREEN}Package '{package_name}' installed successfully!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Package '{package_name}' not found.{Style.RESET_ALL}")

    def upload_package(self):
        try:
            bucket = storage.bucket()
            for file_name in os.listdir(self.package_dir):
                file_path = os.path.join(self.package_dir, file_name)
                blob = bucket.blob(f"packages/{file_name}")
                blob.upload_from_filename(file_path)
                print(f"{Fore.GREEN}Package '{file_name}' uploaded successfully!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def upgrade_package(self, *packages, **kwargs):
        self.install_package(*packages, **kwargs)

    def get_package_info(self, package_name):
        return self._fetch_package_info(package_name)

    def _fetch_package_info(self, package_name):
        url = f"{self.server_url}/packages/{package_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def _download_file(self, url, file_path):
        response = requests.get(url, stream=True)
        with open(file_path, "wb") as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)


def main():
    parser = argparse.ArgumentParser(prog="ptm", description="ProtoCSS Package Manager")
    parser.add_argument("packages", nargs="*", help="Package names")
    parser.add_argument("-i", "--install", action="store_true", help="Install packages")
    parser.add_argument("-u", "--upgrade", action="store_true", help="Upgrade packages")
    parser.add_argument("-gi", "--get-info", action="store_true", help="Get package information")
    parser.add_argument("-up", "--upload", action="store_true", help="Upload package to firebase")

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
                print(f"Package: {package_name}")
                print(f"Description: {package_info.get('description')}")
                print(f"Author: {package_info.get('author')}")
                print(f"Version: {package_info.get('version')}")
                print(f"Files: {package_info.get('files')}")
                print()
            else:
                print(f"Package '{package_name}' not found.")
    elif args.upload:
        ptm.upload_package()


if __name__ == "__main__":
    main()
