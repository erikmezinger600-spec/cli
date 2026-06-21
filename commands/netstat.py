import subprocess

def netstat_cmd(args):
    # default mode
    flags = ["-ano"]

    if args:
        # allow custom flags like -an, -a, -o, -b
        flags = args

    try:
        result = subprocess.run(
            ["netstat"] + flags,
            capture_output=True,
            text=True,
            shell=True
        )

        print(result.stdout)

    except Exception as e:
        print("Error:", e)
