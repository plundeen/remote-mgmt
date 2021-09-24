import subprocess

NIPKG = 'C:\\Program Files\\National Instruments\\NI Package Manager\\nipkg.exe'

print(f"{NIPKG} help")

p1 = subprocess.run([NIPKG, 'help'], shell=True)

p2 = subprocess.run([NIPKG, 'feed-info', 'canary'], shell=True)