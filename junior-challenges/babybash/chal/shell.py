#!/bin/usr/env python3

import subprocess
import re
import random
import os
import signal
import atexit
import shutil

signal.alarm(600)

BANNED = re.compile("[a-z.?*]")

def setup_env():
    directory = '/tmp/{:x}/'.format(random.SystemRandom().getrandbits(160))
    os.mkdir(directory)
    atexit.register(lambda: shutil.rmtree(directory))
    
    return directory

def print_help():
    print("""
    Welcome to \033[1;96mbabaybash\033[0m!

    This is a challenge where you find yourself in a bash-jail.

    You want to execute \033[1m/get_flag\033[0m to get the flag!

    But the following characters are \033[1;91mbanned\033[0m:
        - a-z
        - *
        - ?
        - .
    """)

def main_loop(directory):
    while True:
        inp = input("\033[1mbaby\033[0m> ")
        if inp == 'help':
            print_help()
        elif BANNED.search(inp):
            print('Invalid character. Try \'\033[1mhelp\033[0m\'.')
        else:
            try: 
                subprocess.run(['/bin/bash', '-c', inp],
                        stdin=subprocess.PIPE,
                        timeout=5,
                        cwd=directory)
            except subprocess.TimeoutExpired as te:
                print("Your command timed out.")


if __name__ == '__main__':
    main_loop(setup_env())
