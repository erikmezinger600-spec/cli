import os
import shutil

def rem_cmd(args):
    if len(args) < 2:
        print("Usage:")
        print("cli rem -d folder")
        print("cli rem -r folder")
        print("cli rem -rf folder")
        return

    flag = args[0]
    target = args[1]

    try:
        if flag == "-d":
            os.rmdir(target)

        elif flag == "-r":
            shutil.rmtree(target)

        elif flag == "-rf":
            shutil.rmtree(target, ignore_errors=True)

        else:
            print("Invalid flag")
            return

        print("Deleted:", target)

    except Exception as e:
        print("Error:", e)
