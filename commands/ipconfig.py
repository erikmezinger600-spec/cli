import socket
import platform

def ipconfig_cmd(args):
    print("System:", platform.system())
    print("Node Name:", platform.node())

    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        print("\nNetwork Info")
        print("-------------")
        print("Hostname:", hostname)
        print("Local IP:", local_ip)

    except Exception as e:
        print("Error:", e)
