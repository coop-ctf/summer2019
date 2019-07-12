FROM ubuntu:bionic

$SSH_STEPS

RUN apt-get install -y python3 python3-pip tcpdump libcap2-bin tcpflow && \
    useradd -m admin

COPY reverse/tcp-madness/src/madness/server.py .
COPY reverse/tcp-madness/src/madness/client.py .
COPY reverse/tcp-madness/src/requirements.txt .
COPY reverse/tcp-madness/Dockerfile .
COPY reverse/tcp-madness/flag.txt .
COPY reverse/tcp-madness/startup.sh .

RUN pip3 install -r requirements.txt && \
    rm requirements.txt

RUN chmod 704 Dockerfile && \
    chmod -R 700 startup.sh flag.txt server.py client.py && \
    chown admin /home/guest/server.py && \
    echo "guest ALL=(admin) NOPASSWD: /bin/kill" >> /etc/sudoers && \
    groupadd pcap && \
    usermod -a -G pcap guest && \
    chgrp pcap /usr/sbin/tcpdump && \
    ln -s /usr/sbin/tcpdump /usr/bin/tcpdump && \
    setcap cap_net_raw+ep /usr/sbin/tcpdump

CMD /bin/bash /home/guest/startup.sh && /usr/sbin/sshd -D
