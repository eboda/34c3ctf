FROM ubuntu:17.10

RUN groupadd -g 1000 bashor && useradd -g bashor -u 1000 bashor -s /bin/shell

ADD flag /flag
ADD chal/get_flag /get_flag

RUN chown root:root /flag \
    && chown root:root /get_flag \
    && chmod 4555 /get_flag \
    && chmod 400 /flag 
ADD chal/shell /bin/shell


ADD scripts/clean.sh /tmp/clean.sh
RUN bash /tmp/clean.sh && rm /tmp/clean.sh


CMD runuser -u bashor -g bashor /bin/shell
