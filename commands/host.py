import http.server
import socketserver
import threading
import os

def host_cmd(args):
    if not args or args[0] != "-n":
        print("Usage: host -n <network_name> [port]")
        return

    network_name = args[1] if len(args) > 1 else "default"
    port = int(args[2]) if len(args) > 2 else 8000

    folder = os.getcwd()

    handler = http.server.SimpleHTTPRequestHandler

    def start_server():
        with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
            print(f"[HOST] Network '{network_name}' running on port {port}")
            print(f"[HOST] Serving folder: {folder}")
            print(f"[HOST] Open: http://localhost:{port}")
            httpd.serve_forever()

    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()
