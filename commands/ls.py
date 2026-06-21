import os

def ls_cmd(args):
    for item in os.listdir():
        print(item)
