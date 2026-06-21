import subprocess

def ipconfig_cmd(args):
    # default = /all
    mode = "/all"

    if args:
        if args[0] == "/all":
            mode = "/all"
        elif args[0] == "/release":
            mode = "/release"
        elif args[0] == "/renew":
            mode = "/renew"
        else:
            mode = args[0]

    try:
        result = subprocess.run(
            ["ipconfig", mode],
            capture_output=True,
            text=True,
            shell=True
        )

        print(result.stdout)

    except Exception as e:
        print("Error:", e)
