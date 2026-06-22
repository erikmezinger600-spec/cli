import os

from commands.cat import cat_cmd
from commands.echo import echo_cmd
from commands.open import open_cmd
from commands.rg import rg_cmd
from commands.ipconfig import ipconfig_cmd
from commands.netstat import netstat_cmd
from commands.host import host_cmd

# add your shell commands here
def ls_cmd(args):
    path = args[0] if args else "."
    for item in os.listdir(path):
        print(item)

def pwd_cmd(args):
    print(os.getcwd())

def mkdir_cmd(args):
    if not args:
        print("Usage: mkdir <name>")
        return
    os.makedirs(args[0], exist_ok=True)

def rem_cmd(args):
    import shutil
    if not args:
        print("Usage: rem <file/folder>")
        return
    target = args[0]
    if os.path.isdir(target):
        shutil.rmtree(target)
    else:
        os.remove(target)

def version_cmd(args):
    print("CLI Shell v1.0")

COMMANDS = {
    "ls": ls_cmd,
    "pwd": pwd_cmd,
    "mkdir": mkdir_cmd,
    "rem": rem_cmd,
    "version": version_cmd,
    "cat": cat_cmd,
    "echo": echo_cmd,
    "open": open_cmd,
    "rg": rg_cmd,
    "ipconfig": ipconfig_cmd,
    "netstat": netstat_cmd,
    "host": host_cmd,
}

def main():
    print("CLI Shell v1.0")
    print("Type 'help' for commands. Type 'exit' to quit.\n")

    while True:
        try:
            raw = input("cli> ").strip()

            if not raw:
                continue

            if raw == "exit":
                break

            if raw == "help":
                print("Available commands:")
                for k in COMMANDS:
                    print(" ", k)
                continue

            parts = raw.split()
            cmd = parts[0]
            args = parts[1:]

            if cmd in COMMANDS:
                COMMANDS[cmd](args)
            else:
                print("Unknown command:", cmd)

        except KeyboardInterrupt:
            print("\nexit")
            break

if __name__ == "__main__":
    main()
