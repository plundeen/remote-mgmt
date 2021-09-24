import subprocess
from typing import List

# Constants
NIPKG = "C:\\Program Files\\National Instruments\\NI Package Manager\\nipkg.exe"


def query(arg: str) -> str:
    """Function to perform an nipkg.exe query and return the results"""
    return ""


def update_cache() -> None:
    """Update the local nipkg cache"""
    subprocess.run([NIPKG, "update"], shell=True)


def build_package_list() -> None:
    """Generates a file containing the list of available package names"""
    # Dumping to file for now, in case we decide to just
    # do this periodically in the background
    update_cache()
    with subprocess.Popen(
        [NIPKG, "list"],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
    ) as p:
        with open("options/packages.txt", "w") as f:
            packages = set()
            for line in p.stdout:
                if line.split():
                    packages.add(line.split()[0])
            f.write("\n".join(packages))


def get_package_versions(package: str) -> List[str]:
    """Returns a list of available versions for the specified package"""
    # Update the cache to check for newly-available versions
    update_cache()
    versions = []
    with subprocess.Popen(
        [NIPKG, "list", package],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
    ) as p:
        for line in p.stdout:
            if line.split():
                version = line.split()[1]
                print(version)
                versions.append(version)
    return versions


def register_feed(name: str) -> None:
    """Registers a new feed so that contained packages can be installed"""
    subprocess.run([NIPKG, "update", f"--name={name}"], shell=True)


def install(package: str, version: str) -> None:
    """Function to trigger a package install and stream the stdout/stderr output"""
    # Question: can we provide a pipe as an input that this function can stream to?
    # Probably should be a websocket, right? Can we pass the socket in?
    # Or should this function just handle the full websocket stuff?
    pass
