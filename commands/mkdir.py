import os

def mkdir_cmd(args):
    if not args:
        print("Usage: cli mkdir <name>")
        return

    os.mkdir(args[0])
    print("Created:", args[0])
