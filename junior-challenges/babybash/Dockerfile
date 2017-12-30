FROM ubuntu:17.10

RUN apt-get -y update && apt-get -y upgrade 
RUN apt-get -y install python3 xinetd

RUN groupadd -g 1000 baby && useradd -g baby -u 1000 baby 

COPY flag /flag
COPY chal/get_flag /get_flag

RUN chown root:root /flag \
    && chown root:root /get_flag \
    && chmod 4555 /get_flag \
    && chmod 400 /flag 

COPY xinetd.conf /etc/xinetd.d/chall
COPY chal/shell.py /bin/shell.py
COPY chal/run.sh /chal/run.sh
RUN chmod +x /bin/shell.py /chal/run.sh
RUN  chmod 733 /tmp


ENV PYTHONUNBUFFERED 1
CMD xinetd -d -dontfork
