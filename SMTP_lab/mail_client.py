#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""module description"""

__author__ = 'CHUZ'

if __name__ == '__main__':
    from socket import *

    msg = "\r\n I love computer networks!"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) and call it mailserver
    mailserver = 'smtp.163.com'

    # Create socket called clientSocket and establish a TCP connection with mailserver
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, 25))

    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send AUTH LOGIN command and print server response
    loginCommand = 'AUTH LOGIN\r\n'
    clientSocket.send(loginCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '334':
        print('334 reply not received from server.')

    # Send username(base64) command and print server response
    username = 'amlzb29fa2ltQDE2My5jb20=\r\n'
    clientSocket.send(username.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '334':
        print('334 reply not received from server.')

    # Send password(base64) command and print server response
    password = 'bWFyeTk4NzEy\r\n'
    clientSocket.send(password.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '235':
        print('235 reply not received from server.')

    # Send MAIL FROM command and print server response.
    clientSocket.send('MAIL FROM: <jisoo_kim@163.com>\r\n'.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send RCPT TO command and print server response.
    clientSocket.send('RCPT TO: <jisoo_kim@163.com>\r\n'.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send DATA command and print server response.
    clientSocket.send('DATA\r\n'.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '354':
        print('354 reply not received from server.')

    # Send message data.
    clientSocket.send(msg.encode())

    # Message ends with a single period.
    clientSocket.send(endmsg.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send QUIT command and get server response.
    clientSocket.send('QUIT\r\n'.encode())
    clientSocket.close()
