#!/bin/bash
set -x
socat tcp4-l:1337,bind=127.0.0.1,reuseaddr,fork exec:./run.sh,stderr
