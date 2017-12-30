#!/bin/sh
exec docker run -it --rm -p 127.0.0.1:1337:80 --name quaker eboda/quaker
