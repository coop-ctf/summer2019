FROM ubuntu:bionic

$SSH_STEPS

RUN apt-get install -y python3 python3-pip tcpdump libcap2-bin

COPY reverse/py-jack-of-all-trades/src/ .
COPY reverse/py-jack-of-all-trades/Dockerfile .
COPY reverse/py-jack-of-all-trades/flag.txt .

RUN pip3 install uncompyle6 requests schedule && \
    pip3 install -r ./server/requirements.txt

RUN python3 -m compileall ./scripts && \
    apt-get remove -y python3-pip

RUN rm ./scripts/script.py && \
    mv ./scripts/__pycache__/script.cpython-36.pyc ./script.pyc && \
    rm -rf ./scripts/ && \
    chmod 704 Dockerfile key.txt script.pyc && \
    chmod -R 700 startup.sh flag.txt ./server/* ./server && \
    groupadd pcap && \
    usermod -a -G pcap guest && \
    chgrp pcap /usr/sbin/tcpdump && \
    ln -s /usr/sbin/tcpdump /usr/bin/tcpdump && \
    setcap cap_net_raw+ep /usr/sbin/tcpdump

CMD /bin/bash /home/guest/startup.sh && /usr/sbin/sshd -D
