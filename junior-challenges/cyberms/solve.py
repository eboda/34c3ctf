#!/usr/bin/env python2

import socket
import telnetlib
import base64

LOCAL_HOST = 'cyberms'
LOCAL_PORT = 1338

def cipher():
    return base64.b64decode(open('intercepted_msg', 'rb').read())

s = socket.create_connection((LOCAL_HOST, LOCAL_PORT))
def oracle(c):
    assert len(c) % 16 == 0, 'invalid length: {}'.format(len(c))
    rt(s, b'> ')
    se(s, b'2\n')
    se(s,base64.b64encode(c) +  b'\n')
    m = rt(s, b'.\n')
    return b'Thank you' in m


def pwn():
    c = cipher()
    blocks = len(c) // 16

    plain = ''
    for b in range(blocks-1):
        print("b = {}".format(b))
        c1 = c[-32-b*16:-16-b*16]
        c2 = c[-16-b*16:len(c)-b*16]
        cur_pad = ''
        for p in range(len(cur_pad)+1, 17):
            for i in range(256):
                c1p = 'A'*(16-p) + chr(i)  + ''.join(map(lambda x: chr(ord(x)^p), cur_pad))
                if oracle(c[:-32-b*16] + c1p + c2):
                    plain = chr(ord(c1[-p]) ^ i ^ p) + plain
                    print('Decrypted: {}'.format(repr(plain)))
                    cur_pad = chr(i ^ p) + cur_pad
                    break
    print('Recovered message:\n{}'.format(plain))



    

########### standard functions and stuff ##############
def interact(s):
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()

def rt(s, delim):
    buf = b''
    while delim not in buf:
        buf += s.recv(1)
    return buf

def se(s, data):
    s.sendall(data)

pwn()
