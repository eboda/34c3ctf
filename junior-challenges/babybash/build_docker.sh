#!/bin/bash
gcc chal/get_flag.c -o chal/get_flag
exec docker build -t eboda/babybash .
