#!/bin/bash
prlimit --rss=128000 --cpu=20 --fsize=100000 --nproc=3000 python3 /bin/shell.py
