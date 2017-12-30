FROM ubuntu:17.10
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python xinetd
RUN apt-get -y install python-crypto

RUN useradd cyber


COPY chal /chal
COPY xinetd.conf /etc/xinetd.d/chall

RUN chmod +x /chal/server.py
ENV PYTHONUNBUFFERED 1

CMD xinetd -d -dontfork
