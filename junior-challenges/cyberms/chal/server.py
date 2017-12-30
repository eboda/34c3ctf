#!/usr/bin/env python

import binascii
import base64
import random
import signal

from Crypto import Random
from Crypto.Cipher import AES

from secrets import key

signal.alarm(600)

bs = AES.block_size
mail = open('/dev/null', 'wb')

def pad(m):
    return m + (bs - len(m) % bs) * chr(bs - len(m) % bs)

def unpad(m):
    assert len(m) % 16 == 0
    assert all(map(lambda x: x == m[-1], m[-ord(m[-1]):]))
    return m[:-ord(m[-1])]
        

def enc(m):
    iv = Random.new().read(bs)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + aes.encrypt(pad(m)))


def dec(c):
    c = base64.b64decode(c)
    aes = AES.new(key, AES.MODE_CBC, c[:16])
    return unpad(aes.decrypt(c[16:]))


def prepare_cyber_msg():
    rec = raw_input('Please input the recipient: ')
    msg = raw_input('Please input the message: ')
    c = enc('''{}
    To: {}
    {}'''.format('SMS-v0.1.337', rec, msg))
    print('Here is your cyberized message: {}'.format(c))


def send_cyber_msg():
    c = raw_input('Please input your ciphertext (base64): ')
    if not dec(c).startswith('SMS-v0.1.337'):
        print('That message doesn\'t look like it has the correct format.')
    else:
        print('Thank you. Your message is being transferred shortly.')
        mail.write(c)


if __name__ == '__main__':
    while True:
        print('Cyber messaging service')
        print('[1] Cyberize message')
        print('[2] Send cyberized message')
        choice = raw_input('> ')
        try:
            if choice == '1':
                prepare_cyber_msg()
            elif choice == '2':
                send_cyber_msg()
        except:
            print('There was an error while processing your request.')
