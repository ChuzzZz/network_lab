#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""module description"""

__author__ = 'CHUZ'

if __name__ == '__main__':
    from datetime import datetime
    from socket import *

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)

    for sequence in range(1, 11):
        message = 'Ping '
        try:
            start = datetime.now()
            clientSocket.sendto(message.encode(), ('127.0.0.1', 12000))
            modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
            end = datetime.now()
            rtt = end - start
            print('Ping %d %dms' % (sequence, rtt.microseconds))
        except timeout:
            print('Request timed out')

    clientSocket.close()
