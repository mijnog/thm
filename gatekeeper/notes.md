1. We do a standard nmap scan:
`nmap -sC -sV $VICTIM_IP -oA nmap -Pn'

2. We find there's an interesting port open, 31337 and some smb shares.

3. ncat $VICTIM_IP 31337 gives a simple tcp server that echoes back "Hello <input>!!!". Entering a long string AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA crashes the server. This must be a BOF vuln

4. SMB enumeration (following the techniques on my github notes) shows a share we can access where with a tiny bit of digging we find a .exe

5. If we run that .exe in windows we find it is precisely the BOF vulnerable server.

6. I tried using the template found in the bufferoverflowprep room and it didn't work. Turns out you need to make sure to send a '\n' character at the end of the string. Also very useful is to have logic similar to the following, as there is no banner.

```python
try:
    banner = s.recv(1024).decode("latin-1")
except socket.timeout:
    pass # No initial banner, which is fine.
```

7. Fuzzing crashes at 150 bytes. Now we need to generate a cyclical pattern to find the EIP.

8. I made a tiny bash script that just calls the command so I don't have to google the directory for create_pattern.rb
