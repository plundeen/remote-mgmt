import subprocess
from typing import List

# Constants
NIPKG_EXE = "C:\\Program Files\\National Instruments\\NI Package Manager\\nipkg.exe"


def update_cache() -> None:
    """Update the local nipkg cache"""
    subprocess.run([NIPKG_EXE, "update"], shell=True)


def build_package_list() -> None:
    """Generates a file containing the list of available package names"""
    # Dumping to file for now, in case we decide to just
    # do this periodically in the background
    update_cache()
    with subprocess.Popen(
        [NIPKG_EXE, "list"],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
    ) as p:
        with open("cache/packages.txt", "w") as f:
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
        [NIPKG_EXE, "list", package],
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


def get_available_feeds():
    """Query the systemlink server's package repository for available feeds"""
    # This will need to query the 'nirepo/v1/store/items' endpoint on the
    # Systemlink Package Repository  to retrieve list of feeds to populate
    # dropdown in feed registration page.
    # TODO: implement
    pass


def register_feed(name: str) -> None:
    """Registers a new feed so that contained packages can be installed"""
    subprocess.run([NIPKG_EXE, "update", f"--name={name}"], shell=True)


def install(package: str, version: str) -> None:
    """Function to trigger a package install and stream the stdout/stderr output"""
    # This will probably need to 'yield' the lines from stdout/stderr as it goes,
    # since it is a time-consuming process, and we want to keep users apprised of
    # the progress.
    # Alternatively, we *might* want to push the updates via websocket...
    # TODO: implement
    pass
