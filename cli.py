import sys

from commands.help import help_cmd
from commands.ls import ls_cmd
from commands.rem import rem_cmd
from commands.mkdir import mkdir_cmd
from commands.pwd import pwd_cmd
from commands.version import version_cmd
from commands.cat import cat_cmd
from commands.echo import echo_cmd

COMMANDS = {
    "help": help_cmd,
    "ls": ls_cmd,
    "rem": rem_cmd,
    "mkdir": mkdir_cmd,
    "pwd": pwd_cmd,
    "version": version_cmd
}

if len(sys.argv) < 2:
    print("CLI v1.0")
    print("Type: cli help")
    exit()

cmd = sys.argv[1]
args = sys.argv[2:]

if cmd in COMMANDS:
    COMMANDS[cmd](args)
else:
    print(f"Unknown command: {cmd}")
