FROM ubuntu:17.10
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python xinetd

RUN useradd megalal


COPY megalal /megalal
COPY xinetd.conf /etc/xinetd.d/chall

RUN chmod +x /megalal/megalal.py
ENV PYTHONUNBUFFERED 1

CMD xinetd -d -dontfork
