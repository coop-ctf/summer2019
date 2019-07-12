FROM ubuntu:18.04

$SSH_STEPS

RUN echo "This is not the file you are looking for." >> /home/guest/flag.txt && \
  mkdir .flag

COPY linux/linux-cat-hidden/flag.txt /home/guest/.flag/flag.txt
