import os
import shutil
import subprocess

PROJECT = r"C:\Users\catvi\cli"
DIST_EXE = os.path.join(PROJECT, "dist", "cli.exe")
TARGET = r"C:\cli\cli.exe"

print("Building CLI...")

# build exe
subprocess.run(["pyinstaller", "--onefile", "cli.py"], cwd=PROJECT)

print("Installing CLI...")

# create folder if needed
os.makedirs(r"C:\cli", exist_ok=True)

# copy automatically
shutil.copyfile(DIST_EXE, TARGET)

print("Done! CLI installed to C:\\cli\\cli.exe")
