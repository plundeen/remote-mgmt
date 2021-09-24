from subprocess import Popen, PIPE, STDOUT
import datetime

# This demo shows how we might call nipkg install operations and print live results
# (we should probably also capture them to file)

with Popen(
    "timeout 2 && echo hello && timeout 2 && echo goodbye && dir nonexistent_dir",
    shell=True,
    stdout=PIPE,
    stderr=STDOUT,
    bufsize=1,
    universal_newlines=True,
) as p:
    for line in p.stdout:
        print(f"{datetime.datetime.now().time()} {line}", end="")
    