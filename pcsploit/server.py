"""
PCSploit C2 Server
Runs on your machine. Listens for target connections.
"""

import socket
import threading
import sys


def handle_client(client_socket, address):
    """
    Runs in its own thread for EACH connected client.
    Receives data from that one client and prints it.
    """
    print(f"[+] Connection received from {address[0]}:{address[1]}")
    
    try:
        while True:
            # Try to receive up to 4096 bytes of data
            data = client_socket.recv(4096)
            
            # If recv() returns empty bytes, the client disconnected
            if not data:
                break
            
            # Decode bytes into a string and print it
            message = data.decode("utf-8", errors="ignore")
            print(f"[{address[0]}] {message}")
            
    except ConnectionResetError:
        # Client closed the connection abruptly
        pass
    except Exception as e:
        print(f"[!] Error with {address[0]}: {e}")
    finally:
        print(f"[-] {address[0]} disconnected")
        client_socket.close()


def start_server(host="0.0.0.0", port=4443):
    """
    Starts the listener.
    
    host="0.0.0.0" means "listen on ALL network interfaces"
    — so your machine accepts connections from the internet AND local network.
    
    port=4443 is the door number clients connect to.
    """
    # Create a TCP socket
    # AF_INET = IPv4, SOCK_STREAM = TCP (reliable, ordered)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # SO_REUSEADDR = lets you restart the server immediately without waiting
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind = claim this port. Like registering your phone number.
        server.bind((host, port))
    except OSError:
        # Port is already in use by another program
        print(f"[!] Port {port} is already in use. Try a different port.")
        sys.exit(1)
    
    # Start listening. 10 = max queued connections before we start rejecting.
    server.listen(10)
    
    print(f"[*] PCSploit C2 Server listening on {host}:{port}")
    print("[*] Waiting for target connections...")
    print("[*] Press Ctrl+C to stop")
    
    try:
        while True:
            # accept() BLOCKS until a client connects
            # Returns: (client_socket, (ip, port))
            client, addr = server.accept()
            
            # Create a NEW THREAD for this client so we can handle multiple
            # targets at the same time without blocking
            # daemon=True = thread auto-dies when main program exits
            t = threading.Thread(
                target=handle_client,
                args=(client, addr),
                daemon=True
            )
            t.start()
            
    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print("\n[*] Shutting down server...")
    finally:
        server.close()
        print("[*] Server stopped.")


def main():
    """
    This is what runs when you type 'pcsploit' in the terminal.
    The entry_points in setup.py maps: pcsploit = pcsploit.server:main
    """
    # Allow the user to specify a port: pcsploit 5555
    port = 4443
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"[!] Invalid port number: {sys.argv[1]}")
            sys.exit(1)
    
    start_server(port=port)


# This line only runs when you execute THIS file directly
# (not when it's imported as a module)
if __name__ == "__main__":
    main()
