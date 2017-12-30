#!/bin/bash
set -x
killall -9 socat
socat tcp4-l:1337,bind=0.0.0.0,reuseaddr,fork exec:./spawn_instance.sh,stderr
