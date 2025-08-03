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



To compile the .cpp exploit from https://www.exploit-db.com/exploits/47176, I used the following command on Developer Command Prompt for Visual Studio 2017:  `cl /EHsc privesc.cpp /link /subsystem:console user32.lib kernel32.lib`

Breakdown:

    cl

        This is the command to invoke the Microsoft Visual C++ compiler. It's the primary tool used to turn C and C++ source code files into object files and, ultimately, executable programs within the Visual Studio environment.

    /EHsc

        This is a compiler flag that specifies how the compiler should handle C++ exceptions.

        /EH stands for "Exception Handling."

        s specifies that the compiler should assume that external C-style functions (those not compiled with this flag) do not throw exceptions.

        c ensures that the compiler generates code to handle C++ exceptions in functions declared with extern "C".

        This flag is considered standard practice for compiling modern C++ code and ensures the program behaves correctly with regard to exceptions.

    /link

        tells the cl.exe command to stop processing compiler options and to pass all subsequent arguments to the linker.

        The linker's job is to take the compiled code (.obj files) and combine it with the necessary library files (.lib files) and other resources to create the final executable file (.exe).

    /subsystem:console

        /subsystem:console creates a console application. 

    user32.lib

        This is the library file that contains the code for the Windows User Interface API.

        for functions such as CreateMenu, SendMessageW, SetWindowsHookExW, and TrackPopupMenuEx. 

    kernel32.lib

        This is the library file that contains the code for the core Windows Kernel API.

        The exploit code needs this for fundamental operating system services like process and thread management (GetCurrentProcessId, GetCurrentThreadId), and dynamic linking functions (GetProcAddress, LoadLibraryA). The linker uses this file to resolve these crucial system function calls.