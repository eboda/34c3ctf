#!/usr/bin/env python2

import socket
import telnetlib

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 1337


def pwn():
    role = '#overlord'
    role = int(role.encode('hex'), 16)

    # get encryption of '#overlord'//2
    s = socket.create_connection((LOCAL_HOST, LOCAL_PORT))
    role = '{:x}'.format(role // 2).decode('hex')
    se(s, '2\nfoobar\n{}\n'.format(role))
    rt(s, 'token:\n')
    token = rt(s, '\n')

    # send back enc('#overlord'//2) * 2
    c1, c2 = token.split('_')
    c2 = '{:x}'.format(int(c2, 16) * 2)
    s = socket.create_connection((LOCAL_HOST, LOCAL_PORT))
    se(s, '1\n{}_{}\n'.format(c1, c2))
    interact(s)

########### standard functions and stuff ##############
def interact(s):
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()

def rt(s, delim):
    buf = ''
    while delim not in buf:
        buf += s.recv(1)
    return buf

def se(s, data):
    s.sendall(data)

pwn()
