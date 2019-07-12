FROM ubuntu:18.04

$SSH_STEPS

RUN useradd -m admin
RUN echo "guest ALL=(admin) NOPASSWD: /usr/bin/openssl" >> /etc/sudoers && \
    echo "FLAG{sF4mtJYqoqhbGPOsBmY06Nk2xDc03nENn0XbSRsS}" >> /home/admin/flag.txt && \
    chmod 640 /home/admin/flag.txt && \
    chown root:admin /home/admin/flag.txt