#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""module description"""

__author__ = 'CHUZ'

if __name__ == '__main__':
    from socket import *
    import sys

    # if len(sys.argv) <= 1:
    #     print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    #     sys.exit(2)

    # Create a server socket, bind it to a port and start listening
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(('127.0.0.1', 8888))
    tcpSerSock.listen(5)

    while 1:
        # Start receiving data from the client
        print('Ready to serve...')
        tcpCliSock, addr = tcpSerSock.accept()
        print('Received a connection from:', addr)
        message = tcpCliSock.recv(1024).decode()
        print('message: ' + message)
        # Extract the filename from the given message
        print(message.split()[1])
        filename = message.split()[1].partition("/")[2]
        print('filename: ' + filename)
        fileExist = "false"
        filetouse = "/" + filename
        print('filetouse: ' + filetouse)
        try:
            # Check whether the file exist in the cache
            f = open(filetouse[1:], "r")
            outputdata = f.readlines()
            fileExist = "true"

            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
            tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())

            # Send the content of the requested file to the client
            for data in outputdata:
                tcpCliSock.send(data.encode())
            tcpCliSock.send("\r\n".encode())
            print('Read from cache')

            # Error handling for file not found in cache
        except IOError:
            if fileExist == "false":
                # Create a socket on the proxyserver
                s = socket(AF_INET, SOCK_STREAM)

                hostn = filename.replace("www.", "", 1)
                print('hostn: ' + hostn)
                try:
                    # Connect to the socket to port 80
                    s.connect((hostn, 80))
                    print('Socket connected to port 80 of the host')

                    # Create a temporary file on this socket and ask port 80 for the file requested by the client
                    fileobj = s.makefile('rwb', 0)
                    fileobj.write(("GET " + "http://" + filename + " HTTP/1.0\n\n").encode())
                    # Read the response into buffer
                    buff = fileobj.readlines()

                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket and the corresponding file in the cache
                    tmpFile = open("./" + filename, "wb")
                    for i in range(0, len(buff)):
                        tmpFile.write(buff[i])
                        tcpCliSock.send(buff[i])
                except:
                    print("Illegal request")
            else:
                # HTTP response message for file not found
                tcpCliSock.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                tcpCliSock.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

            # Close the client and the server sockets
            tcpCliSock.close()
    tcpSerSock.close()
