#!/bin/bash
gcc chal/shell.c -o chal/shell
gcc chal/get_flag.c -o chal/get_flag
exec docker build -t eboda/minbashmaxfun .
