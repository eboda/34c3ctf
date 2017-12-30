#!/bin/sh
exec docker run -it --rm -p 127.0.0.1:1337:1337 --name babybash eboda/babybash
