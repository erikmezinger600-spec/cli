import os
import sys

def open_cmd(args):
    if not args:
        print("Usage: open <file_or_program>")
        return

    target = args[0]

    try:
        if sys.platform.startswith("win"):
            os.startfile(target)
        else:
            os.system(f'xdg-open "{target}"')

    except Exception as e:
        print("Error:", e)
