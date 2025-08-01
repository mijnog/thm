#!/usr/bin/env python3

import socket, time, sys

ip = "172.20.192.1"
port = 31337
timeout = 5

string = "A" * 10

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            
            try:
                banner = s.recv(1024).decode("latin-1")
            except socket.timeout:
                pass

            payload = string + "\n"
            
            print(f"Fuzzing with {len(string)} bytes")
            s.send(bytes(payload, "latin-1"))
            
            response = s.recv(1024).decode("latin-1")
            
    except ConnectionRefusedError:
        print("Connection refused. Is the server running?")
        sys.exit(0)
    except ConnectionResetError:
        print(f"Fuzzing crashed at {len(string)} bytes")
        sys.exit(0)
    except socket.timeout:
        print(f"Fuzzing crashed at {len(string)} bytes (connection timed out)")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(f"Fuzzing likely crashed at {len(string)} bytes")
        sys.exit(0)

    string += "A" * 10
    time.sleep(1)
